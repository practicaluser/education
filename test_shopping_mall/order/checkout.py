import os
import json
import threading
import time
from datetime import datetime
from typing import List, Dict, Any

from core.exceptions import OutOfStockError, PaymentError
from user.models import User
from .cart import Cart

class OrderService:
    """결제, 재고 차감, 주문 기록 저장을 처리하는 서비스 클래스입니다."""
    
    def __init__(self, data_dir: str = "./order_data") -> None:
        self.data_dir: str = data_dir
        # 주문 내역을 저장할 폴더가 없으면 os 모듈을 이용해 생성합니다.
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def process_payment(self, user: User, cart: Cart, amount_paid: int) -> bool:
        """장바구니의 상품들을 결제하고 주문을 확정합니다."""
        total_price: int = cart.get_total_price()
        items: List[Dict[str, Any]] = cart.get_items()

        if not items:
            print("[시스템] 장바구니가 비어 있어 결제할 수 없습니다.")
            return False

        # --- 1. 사전 검증 단계 (try-except로 래핑될 수 있도록 예외를 던짐) ---
        if amount_paid < total_price:
            # 1단계에서 만든 결제 실패 커스텀 예외 발생
            raise PaymentError(f"금액이 부족합니다. (필요: {total_price:,}원, 지불: {amount_paid:,}원)")

        for item in items:
            product = item['product']
            qty = item['quantity']
            if not product.has_stock(qty):
                # 1단계에서 만든 재고 부족 커스텀 예외 발생
                raise OutOfStockError(product.name, qty, product.stock)

        print(f"\n[시스템] 결제가 승인되었습니다! (결제 금액: {total_price:,}원)")
        print("[시스템] 주문 처리 및 재고 차감을 백그라운드에서 진행합니다...")

        # --- 2. 병렬 처리 단계 (재고 차감 & 파일 기록) ---
        order_data: Dict[str, Any] = self._create_order_data(user, cart, total_price)

        # threading.Thread를 사용하여 두 가지 작업을 별도의 실행 흐름으로 분리합니다.
        stock_thread = threading.Thread(target=self._deduct_stock, args=(items,))
        record_thread = threading.Thread(target=self._save_order_record, args=(order_data,))

        # 스레드 실행 시작 (동시에 출발)
        stock_thread.start()
        record_thread.start()

        # join()을 호출하여 두 스레드의 작업이 모두 안전하게 끝날 때까지 메인 흐름이 기다립니다.
        stock_thread.join()
        record_thread.join()

        print("[시스템] 모든 주문 처리가 안전하게 완료되었습니다.")
        cart.clear()  # 결제 완료 후 장바구니 비우기
        return True

    def _deduct_stock(self, items: List[Dict[str, Any]]) -> None:
        """[스레드 작업 1] 상품의 재고를 차감합니다."""
        time.sleep(0.5)  # DB 업데이트 등 무거운 네트워크 작업이라 가정하고 0.5초 대기
        for item in items:
            product = item['product']
            product.stock -= item['quantity']
            print(f"  -> [재고 스레드] '{product.name}' 재고 차감 완료 (남은 재고: {product.stock}개)")

    def _save_order_record(self, order_data: Dict[str, Any]) -> None:
        """[스레드 작업 2] 영수증(주문 내역)을 로컬 JSON 파일로 저장합니다."""
        time.sleep(0.5)  # 무거운 파일 I/O 작업이라 가정
        file_name: str = f"order_{order_data['order_id']}.json"
        file_path: str = os.path.join(self.data_dir, file_name)
        
        try:
            # json 모듈을 사용하여 파이썬 딕셔너리를 파일로 직렬화(저장)합니다.
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(order_data, f, ensure_ascii=False, indent=4)
            print(f"  -> [기록 스레드] 주문 내역 저장 완료 ({file_name})")
        except Exception as e:
            print(f"  -> [기록 스레드 에러] 내역 저장 실패: {e}")

    def _create_order_data(self, user: User, cart: Cart, total_price: int) -> Dict[str, Any]:
        """저장할 영수증 형태의 데이터를 조립합니다."""
        timestamp: str = datetime.now().strftime("%Y%m%d%H%M%S")
        return {
            "order_id": f"ORD-{timestamp}-{user.user_id}",
            "buyer": user.name,
            "total_price": total_price,
            "timestamp": datetime.now().isoformat(),
            "items": [
                {
                    "product_name": item['product'].name, 
                    "quantity": item['quantity'], 
                    "price": item['product'].price
                }
                for item in cart.get_items()
            ]
        }

# 싱글톤처럼 사용할 서비스 인스턴스
order_service: OrderService = OrderService()