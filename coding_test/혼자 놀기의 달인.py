from typing import List

# ==========================================
# Module 1: 알고리즘 영역 (cycle_finder.py)
# 역할: 그래프 탐색을 통해 독립적인 그룹(사이클)의 크기들을 찾아냄
# ==========================================
def find_all_group_sizes(cards: List[int]) -> List[int]:
    """주어진 카드 배열에서 독립적인 상자 그룹들의 크기를 찾아 반환합니다."""
    visited = [False] * len(cards)
    group_sizes = []

    for i in range(len(cards)):
        if visited[i]:
            continue
        
        current = i
        count = 0
        
        # 하나의 사이클(그룹) 탐색
        while not visited[current]:
            visited[current] = True
            current = cards[current] - 1
            count += 1
            
        group_sizes.append(count)

    return group_sizes


# ==========================================
# Module 2: 도메인 로직 영역 (score_calculator.py)
# 역할: 게임의 룰을 적용하여 최종 점수를 계산함
# ==========================================
def calculate_highest_score(group_sizes: List[int]) -> int:
    """그룹 크기 목록을 바탕으로 게임 규칙에 따른 최고 점수를 계산합니다."""
    # 예외 처리: 그룹이 1개 이하면 점수는 0점
    if len(group_sizes) < 2:
        return 0
    
    # 내림차순 정렬 후 가장 큰 두 그룹의 곱 반환
    sorted_sizes = sorted(group_sizes, reverse=True)
    return sorted_sizes[0] * sorted_sizes[1]


# ==========================================
# Module 3: 메인 실행 영역 (main.py)
# 역할: 각 모듈을 조립하여 전체 프로그램의 흐름을 제어하는 오케스트레이터
# ==========================================
def solution(cards: List[int]) -> int:
    """
    카드 게임의 최종 점수를 반환하는 메인 함수
    독립된 모듈들을 조립하여 하나의 프로세스를 완성합니다.
    """
    # 1. 알고리즘 모듈에게 상자 그룹화를 지시
    group_sizes = find_all_group_sizes(cards)
    
    # 2. 도메인 로직 모듈에게 점수 계산을 지시
    final_score = calculate_highest_score(group_sizes)
    
    # 3. 최종 결과 반환
    return final_score