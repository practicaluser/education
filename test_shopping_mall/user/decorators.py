import functools
from typing import Callable, Any
from .auth import session_manager

def login_required(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    함수 실행 전 로그인 상태를 검증하는 데코레이터입니다.
    로그인되어 있지 않으면 경고 메시지를 출력하고 함수 실행을 차단합니다.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # auth.py에 정의된 세션 매니저를 통해 로그인 상태 확인
        if not session_manager.is_logged_in():
            print("\n[접근 거부] 로그인이 필요한 서비스입니다. 먼저 로그인을 진행해 주세요.")
            return None  # 함수 실행을 취소하고 None 반환
        
        # 로그인 상태라면 원래의 함수를 정상적으로 실행
        return func(*args, **kwargs)
    
    return wrapper