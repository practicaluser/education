class User:
    """사용자 정보를 담는 데이터 모델 클래스입니다."""
    
    def __init__(self, user_id: str, password: str, name: str) -> None:
        self.user_id: str = user_id
        self.password: str = password  # 실제 상용 환경에서는 해시(Hash) 처리해야 합니다.
        self.name: str = name

    def __str__(self) -> str:
        return f"User({self.user_id}, {self.name})"