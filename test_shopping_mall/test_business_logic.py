import unittest
import time
from core.exceptions import OutOfStockError, PaymentError
from user.models import User
from shop.models import Product
from order.cart import Cart
from order.checkout import OrderService

class TestOrderService(unittest.TestCase):
    def setUp(self):
        # 테스트용 가짜 데이터(Mock Data) 준비
        self.test_user = User("test_id", "pw", "테스트유저")
        self.test_product = Product("TEST-01", "맥북", 2000000, stock=5)
        self.cart = Cart()
        # 영수증이 본 서버에 섞이지 않도록 테스트 전용 폴더 지정
        self.order_service = OrderService(data_dir="./test_temp_data")

    def test_payment_insufficient_funds(self):
        """잔액 부족 시 PaymentError가 발생하는지 테스트"""
        self.cart.add_item(self.test_product, 1) # 200만 원짜리 1개
        
        # 100만 원만 냈을 때 PaymentError가 터지는지 확인
        with self.assertRaises(PaymentError):
            self.order_service.process_payment(self.test_user, self.cart, amount_paid=1000000)
            
        # 트랜잭션이 차단되었으므로 재고는 여전히 5개여야 함
        self.assertEqual(self.test_product.stock, 5)

    def test_payment_success_and_threading(self):
        """정상 결제 시 재고가 차감되는지 테스트 (스레드 동기화 고려)"""
        self.cart.add_item(self.test_product, 2)
        
        # 500만 원 지불 -> 결제 성공해야 함
        result = self.order_service.process_payment(self.test_user, self.cart, amount_paid=5000000)
        self.assertTrue(result)
        
        # [중요] 백그라운드 스레드가 재고를 깎는 시간(0.5초)을 벌어주기 위해 메인 테스트 흐름도 잠깐 대기
        time.sleep(1) 
        
        # 5개 중 2개를 샀으므로 3개가 남아있어야 함
        self.assertEqual(self.test_product.stock, 3)

if __name__ == '__main__':
    unittest.main()