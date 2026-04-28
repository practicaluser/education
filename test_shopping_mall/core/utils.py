import time
import functools
from typing import Callable, Any

def time_logger(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    함수의 실행 시간을 측정하여 터미널에 출력하는 데코레이터입니다.
    """
    # functools.wraps는 원본 함수(func)의 메타데이터(이름, docstring 등)를 
    # 래퍼 함수에 복사하여 내부 구조와 속성을 유지하게 해줍니다.
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time: float = time.time()  # 실행 시작 시간 기록
        
        # *args, **kwargs를 사용해 원본 함수가 어떤 인자를 받든 그대로 전달합니다.
        result: Any = func(*args, **kwargs) 
        
        end_time: float = time.time()    # 실행 종료 시간 기록
        execution_time: float = end_time - start_time
        
        print(f"[LOG] '{func.__name__}' 함수 실행 완료 (소요 시간: {execution_time:.4f}초)")
        
        return result  # 원본 함수의 반환값을 그대로 반환
    
    return wrapper