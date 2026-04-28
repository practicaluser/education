import unittest
from unittest.mock import patch
from io import StringIO
import sys

# 우리가 만든 모듈 임포트
from user.auth import session_manager
from main import handle_auth

class TestUI(unittest.TestCase):
    def setUp(self):
        # 매 테스트 전에 세션 초기화
        session_manager.logout()

    # builtins.input을 가로채서 우리가 원하는 값을 순서대로 반환하게 만듭니다.
    @patch('builtins.input', side_effect=['admin', '1234'])
    # sys.stdout을 가로채서 print()로 출력되는 글자들을 캡처합니다.
    @patch('sys.stdout', new_callable=StringIO)
    def test_login_success(self, mock_stdout, mock_input):
        handle_auth() # 로그인 함수 실행
        
        # 출력된 결과물 캡처
        output = mock_stdout.getvalue()
        
        # 검증 (Assertion)
        self.assertTrue(session_manager.is_logged_in())
        self.assertIn("[시스템] 관리자님 환영합니다.", output)

if __name__ == '__main__':
    unittest.main()