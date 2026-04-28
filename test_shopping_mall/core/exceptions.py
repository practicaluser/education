class ShoppingMallError(Exception):
    """쇼핑몰 시스템에서 발생하는 모든 커스텀 예외의 최상위 부모 클래스입니다."""
    pass

class OutOfStockError(ShoppingMallError):
    """재고 부족 시 발생하는 예외입니다."""
    
    def __init__(self, product_name: str, requested_qty: int, available_qty: int) -> None:
        self.product_name: str = product_name
        self.requested_qty: int = requested_qty
        self.available_qty: int = available_qty
        
        # 에러 발생 시 출력될 상세 메시지를 구성하여 부모 클래스에 전달합니다.
        message: str = (
            f"재고 부족: '{self.product_name}'의 재고가 부족합니다. "
            f"(요청 수량: {self.requested_qty}, 남은 수량: {self.available_qty})"
        )
        super().__init__(message)

class PaymentError(ShoppingMallError):
    """결제 과정에서 문제가 발생했을 때 던져지는 예외입니다."""
    
    def __init__(self, reason: str) -> None:
        self.reason: str = reason
        message: str = f"결제 실패: {self.reason}"
        super().__init__(message)