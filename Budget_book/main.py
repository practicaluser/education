# 앞서 만든 1~4단계 기능들을 불러옵니다.
from data_io import load_data, save_data
from input_handler import get_input_record
from viewer import display_records
from analyzer import calculate_statistics

def main():
    print("=" * 40)
    print(" 🗂️ 개인 가계부 CLI 앱에 오신 것을 환영합니다! ")
    print("=" * 40)

    # 1. 프로그램 시작 시 파일에서 기존 데이터 불러오기
    # data_io 모듈의 기능 활용 (없으면 빈 리스트 반환)
    account_book = load_data() 

    # 2. while 무한루프: 사용자가 '4(종료)'를 누를 때까지 앱을 계속 실행
    while True:
        print("\n[ 메인 메뉴 ]")
        print("1. 📝 새로운 내역 입력")
        print("2. 🔍 전체 내역 조회")
        print("3. 📊 통계 및 분석")
        print("4. 🚪 프로그램 종료")
        
        # 사용자 메뉴 선택
        choice = input("▶ 원하시는 메뉴의 번호를 입력하세요: ").strip()

        # 3. if/elif 분기 처리: 선택된 번호에 따라 독립된 함수 호출
        if choice == '1':
            # --- 연속 입력을 위한 루프 시작 ---
            while True:
                # 1. 입력 모듈 호출 (한 줄 혹은 단계별 입력 중 선택하여 수행)
                new_record = get_input_record()
                
                # 2. 결과가 있으면(취소되지 않았으면) 리스트에 추가 및 저장
                if new_record:
                    account_book.append(new_record)
                    if save_data(account_book):
                        print("💾 현재까지의 모든 내역이 안전하게 저장되었습니다.")
                
                # 3. 사용자에게 계속 입력할지 물어보기
                # .lower()를 사용해 Y나 y 모두 처리 가능하게 합니다.
                cont = input("\n➕ 내역을 더 입력하시겠습니까? (계속하려면 'y' 입력, 메뉴로 가려면 '엔터'): ").lower().strip()
                
                if cont != 'y':
                    print("🏠 메인 메뉴로 돌아갑니다.")
                    break # 이 루프를 빠져나가면 다시 상위의 '메뉴 선택 루프'로 돌아갑니다.
            # --- 연속 입력 루프 끝 ---

        elif choice == '2':
            # 조회 모듈 호출
            display_records(account_book)

        elif choice == '3':
            # 통계 모듈을 위한 추가 입력 받기
            print("\n[통계 조건 입력]")
            target_month = input("조회할 연월 (예: 2026-04): ").strip()
            target_category = input("조회할 카테고리 (예: 식비): ").strip()
            
            # 분석 모듈 호출 (계산 결과만 딕셔너리로 받아옴)
            stats = calculate_statistics(account_book, target_month, target_category)
            
            # 메인 함수에서 결과를 포맷팅하여 출력
            if stats:
                print(f"\n--- 📈 [{target_month}] 통계 ---")
                print(f"총 지출액: {stats['monthly_total']:,}원")
                print(f"평균 지출액: {stats['category_avg']:,}원")
                
                if stats['max_expense_item']:
                    print(f"🔥 {target_category} 최고 지출: {stats['max_expense_item']['amount']:,}원 ({stats['max_expense_item']['memo']})")
                    print(f"🧊 {target_category} 최저 지출: {stats['min_expense_item']['amount']:,}원 ({stats['min_expense_item']['memo']})")
                print("-" * 40)
            else:
                print("⚠️ 조건에 맞는 데이터가 없습니다.")

        elif choice == '4':
            # 종료 조건
            print("\n가계부 앱을 종료합니다. 이용해 주셔서 감사합니다! 👋")
            break # while 무한루프 탈출

        else:
            # 예외 처리
            print("⚠️ 잘못된 입력입니다. 1번부터 4번 사이의 숫자를 입력해주세요.")

# 이 파일이 직접 실행될 때만 main() 함수를 구동하도록 하는 파이썬의 표준 관례
if __name__ == "__main__":
    main()