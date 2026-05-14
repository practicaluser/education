from itertools import combinations_with_replacement

def generate_arrow_distributions(n):
    # 11개의 점수 구간 (10점 ~ 0점)
    scores = list(range(11))  
    
    # n발을 11개의 구간에 배분하는 모든 경우의 수 생성
    # combinations_with_replacement는 "n개의 화살을 11개의 바구니에 넣는 경우"를 표현
    distributions = []
    for comb in combinations_with_replacement(scores, n):
        # comb는 예: (0,0,1,2,10) 이런 식으로 화살이 들어간 구간을 나타냄
        arr = [0] * 11
        for c in comb:
            arr[c] += 1
        distributions.append(arr)
    
    return distributions

def calculate_score(distribution, info):
    """
    라이언의 배치(distribution)와 어피치의 배치(info)를 비교해 점수 차이를 계산
    """
    ryan_score, apeach_score = 0, 0
    
    for i in range(11):
        if distribution[i] == 0 and info[i] == 0:
            continue  # 둘 다 못 맞히면 점수 없음
        if distribution[i] > info[i]:
            ryan_score += (10 - i)
        else:
            apeach_score += (10 - i)
    
    return ryan_score - apeach_score
    
def get_best_distributions(distributions, info):
    """
    최대 점수 차이를 기록하는 경우만 리스트로 추적하여 반환
    """
    max_score_diff = 0
    best_candidates = []
    
    for dist in distributions:
        score_diff = calculate_score(dist, info)
        
        if score_diff > 0:
            # 새로운 최대 점수 차이가 발견되면 후보 리스트를 새로 덮어씀
            if score_diff > max_score_diff:
                max_score_diff = score_diff
                best_candidates = [dist]
            # 최대 점수 차이와 동일한 경우 후보 리스트에 추가
            elif score_diff == max_score_diff:
                best_candidates.append(dist)
    
    # 라이언이 이길 수 있는 경우가 없으면
    if max_score_diff == 0:  
        return {-1: []}
    
    return {max_score_diff: best_candidates}

def tie_breaker(best_dict):
    """
    get_best_distributions에서 반환된 {max_score: [배치들]} 딕셔너리를 받아서
    가장 낮은 점수를 더 많이 맞힌 경우를 선택해 하나만 남긴 딕셔너리로 반환
    """
    max_score = next(iter(best_dict)) # 딕셔너리 첫 번째 키 가져오기
    candidates = best_dict[max_score]

    # 여러 후보 중에서 tie-breaker 규칙 적용
    # 낮은 점수(0점부터 시작)에서 더 많은 화살을 쏜 경우를 우선
    candidates.sort(key=lambda dist: dist[::-1], reverse=True)

    # 가장 우선순위 높은 배치 하나만 남김
    best_distribution = candidates[0]
    return {max_score: best_distribution}

def solution(n, info):
    # 1. n발의 화살로 쏠 수 있는 모든 과녁 점수 조합을 생성합니다.
    distributions = generate_arrow_distributions(n)
    
    # 2. 어피치의 기록(info)과 비교하여 라이언이 승리할 수 있는 최대 점수차 조합들을 가져옵니다.
    best_dict = get_best_distributions(distributions, info)
    
    # 3. 라이언이 우승할 방법이 없는 경우 (최대 점수차 키가 -1인 경우)
    if -1 in best_dict:
        return [-1]
        
    max_score = next(iter(best_dict))
    candidates = best_dict[max_score]
    
    # ⭐ 최대 점수 차이 조합이 단 하나뿐이라면 바로 반환
    if len(candidates) == 1:
        return candidates[0]
    
    # 4. 최대 점수차로 이기는 방법이 여러 가지일 경우 우선순위(가장 낮은 점수를 많이 맞힌 경우)를 적용합니다.
    final_result = tie_breaker(best_dict)
    
    # 5. 최종 결정된 화살 배치 배열을 추출하여 반환합니다.
    max_score = next(iter(final_result))
    answer = final_result[max_score]
    
    return answer
