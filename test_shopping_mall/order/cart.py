from typing import Dict, List, Any
from shop.models import Product

class Cart:
    """사용자의 장바구니 상태를 관리하는 클래스입니다."""
    
    def __init__(self) -> None:
        # product_id를 키(key)로, 상품 객체와 수량을 딕셔너리로 저장합니다.
        # 예: {'P001': {'product': Product(...), 'quantity': 2}}
        self._items: Dict[str, Dict[str, Any]] = {}

    def add_item(self, product: Product, quantity: int) -> None:
        """장바구니에 상품을 추가합니다. 이미 있으면 수량만 증가시킵니다."""
        if product.product_id in self._items:
            self._items[product.product_id]['quantity'] += quantity
        else:
            self._items[product.product_id] = {
                'product': product, 
                'quantity': quantity
            }
        print(f"[장바구니] '{product.name}' {quantity}개가 담겼습니다.")

    def get_total_price(self) -> int:
        """장바구니에 담긴 모든 상품의 총 결제 금액을 계산합니다."""
        total: int = sum(
            item['product'].price * item['quantity'] 
            for item in self._items.values()
        )
        return total

    def get_items(self) -> List[Dict[str, Any]]:
        """장바구니에 담긴 상품 목록을 리스트로 반환합니다."""
        return list(self._items.values())

    def clear(self) -> None:
        """결제 완료 후 장바구니를 비웁니다."""
        self._items.clear()