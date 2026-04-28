import sys

# 우리가 만든 패키지들의 __init__.py 덕분에, 내부 모듈 이름을 몰라도 깔끔하게 임포트가 가능합니다.
from core import ShoppingMallError, time_logger
from user import session_manager, login_required
from shop import catalog_service
from order import Cart, order_service

# 현재 접속자의 세션 동안 유지될 장바구니 객체 생성
my_cart: Cart = Cart()

def handle_auth() -> None:
    """로그인 및 로그아웃을 처리하는 헬퍼 함수"""
    if session_manager.is_logged_in():
        session_manager.logout()
    else:
        print("\n--- 시스템 로그인 ---")
        user_id = input("아이디를 입력하세요 (admin 또는 guest): ").strip()
        password = input("비밀번호를 입력하세요 (1234 또는 1111): ").strip()
        session_manager.login(user_id, password)

@time_logger
def display_products() -> None:
    """상품을 페이지네이션하여 보여주고 장바구니에 담는 함수"""
    print("\n--- 전체 상품 목록 ---")
    
    # 3단계에서 만든 제너레이터를 호출하여 5개씩 데이터를 스트리밍합니다.
    product_generator = catalog_service.get_paginated_products(page_size=5)
    
    for page in product_generator:
        for product in page:
            print(product)
            
        cmd = input("\n장바구니에 담을 상품ID 입력 (다음 페이지는 엔터, 취소는 q): ").strip()
        
        if cmd.lower() == 'q':
            break
        elif cmd:
            # 입력한 ID로 카탈로그(커스텀 이터레이터)를 순회하며 상품을 찾습니다.
            target_product = next((p for p in catalog_service if p.product_id == cmd), None)
            
            if target_product:
                try:
                    qty = int(input(f"'{target_product.name}' 몇 개를 담으시겠습니까? "))
                    my_cart.add_item(target_product, qty)
                except ValueError:
                    print("[오류] 수량은 숫자로 입력해주세요.")
            else:
                print("[오류] 존재하지 않는 상품 ID입니다.")

# 2단계에서 만든 권한 검증 데코레이터를 부착! (비로그인 시 실행 차단)
@login_required  
def view_cart() -> None:
    """장바구니 내역을 확인하는 함수"""
    print("\n--- 내 장바구니 ---")
    items = my_cart.get_items()
    
    if not items:
        print("장바구니가 비어있습니다.")
        return
        
    for item in items:
        p = item['product']
        print(f" - {p.name}: {p.price:,}원 x {item['quantity']}개")
        
    print(f"\n총 결제 예정 금액: {my_cart.get_total_price():,}원")

# 데코레이터 2개 중첩 적용 (로그인 검증 통과 후 -> 실행 시간 측정)
@login_required
@time_logger
def checkout() -> None:
    """결제를 진행하는 함수"""
    print("\n--- 결제 데스크 ---")
    items = my_cart.get_items()
    if not items:
        print("장바구니가 비어 결제할 수 없습니다.")
        return

    total = my_cart.get_total_price()
    print(f"고객님의 총 결제 금액은 {total:,}원 입니다.")
    
    try:
        amount_paid = int(input("지불하실 금액을 입력하세요: "))
        user = session_manager.get_current_user()
        
        # 4단계에서 만든 비동기 결제 서비스 호출
        # 여기서 예외가 발생하면 즉시 아래의 except 블록으로 점프합니다.
        order_service.process_payment(user, my_cart, amount_paid)
        
    except ShoppingMallError as e:
        # 1단계에서 만든 최상위 커스텀 예외로 묶어서 처리
        # (잔액 부족, 재고 부족 에러가 모두 이곳에서 캐치됩니다)
        print(f"\n[결제 중단] {e}")
    except ValueError:
        print("\n[오류] 올바른 금액(숫자)을 입력해주세요.")

def main() -> None:
    """사용자와 상호작용하는 메인 루프"""
    while True:
        user = session_manager.get_current_user()
        user_name = user.name if user else "비회원"
        
        print(f"\n========== 파이썬 미니 쇼핑몰 (접속자: {user_name}) ==========")
        print("1. 로그인 / 로그아웃")
        print("2. 상품 둘러보기 및 장바구니 담기")
        print("3. 장바구니 확인 (로그인 필요)")
        print("4. 결제하기 (로그인 필요)")
        print("0. 쇼핑몰 종료")
        print("==========================================================")
        
        choice = input("원하시는 메뉴 번호를 선택하세요: ").strip()
        
        if choice == '1':
            handle_auth()
        elif choice == '2':
            display_products()
        elif choice == '3':
            view_cart()
        elif choice == '4':
            checkout()
        elif choice == '0':
            print("이용해 주셔서 감사합니다. 안녕히 가세요!")
            sys.exit(0)
        else:
            print("잘못된 입력입니다. 다시 선택해 주세요.")

# 직접 실행했을 때만 main() 함수를 호출하도록 하는 진입점 보호기
if __name__ == "__main__":
    main()