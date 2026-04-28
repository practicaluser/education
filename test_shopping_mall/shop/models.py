class Product:
    """상품 정보를 담는 데이터 모델 클래스입니다."""
    
    def __init__(self, product_id: str, name: str, price: int, stock: int) -> None:
        self.product_id: str = product_id
        self.name: str = name
        self.price: int = price
        self.stock: int = stock

    def __str__(self) -> str:
        return f"[{self.product_id}] {self.name} - {self.price:,}원 (재고: {self.stock}개)"
    
    def has_stock(self, required_qty: int) -> bool:
        """요청한 수량만큼 재고가 충분한지 확인합니다."""
        return self.stock >= required_qty