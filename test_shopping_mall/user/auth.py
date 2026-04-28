from typing import Dict, Optional
from .models import User

class AuthService:
    """사용자 인증 및 로그인 세션을 관리하는 클래스입니다."""
    
    def __init__(self) -> None:
        # 임시 데이터베이스 역할 (아이디를 키로, User 객체를 값으로 저장)
        self._users: Dict[str, User] = {
            "admin": User("admin", "1234", "관리자"),
            "guest": User("guest", "1111", "게스트")
        }
        # 현재 로그인한 사용자의 상태를 보관 (로그인하지 않은 상태면 None)
        self._current_user: Optional[User] = None

    def login(self, user_id: str, password: str) -> bool:
        """아이디와 비밀번호를 검증하여 세션을 생성합니다."""
        user: Optional[User] = self._users.get(user_id)
        
        if user is not None and user.password == password:
            self._current_user = user
            print(f"[시스템] {user.name}님 환영합니다.")
            return True
        
        print("[시스템] 아이디 또는 비밀번호가 일치하지 않습니다.")
        return False

    def logout(self) -> None:
        """현재 세션을 종료(로그아웃)합니다."""
        if self._current_user:
            print(f"[시스템] {self._current_user.name}님이 로그아웃 하셨습니다.")
            self._current_user = None
        else:
            print("[시스템] 로그인 상태가 아닙니다.")

    def get_current_user(self) -> Optional[User]:
        """현재 로그인된 사용자 객체를 반환합니다."""
        return self._current_user

    def is_logged_in(self) -> bool:
        """현재 로그인 여부를 boolean 값으로 반환합니다."""
        return self._current_user is not None

# 시스템 전반에서 단일 세션 상태를 공유하기 위해 전역 인스턴스 생성 (싱글톤 패턴 대체)
session_manager: AuthService = AuthService()