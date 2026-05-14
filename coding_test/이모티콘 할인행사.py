from itertools import product

# 1. 단일 유저의 구매 합계를 계산하는 함수
def get_user_purchase_amount(user_rate, emoticons, discounts):
    """
    특정 유저가 주어진 할인율(discounts)에서 구매할 이모티콘의 총 금액을 반환합니다.
    """
    purchase_amount = 0
    
    for i in range(len(emoticons)):
        # 이모티콘 할인율이 유저의 기준 비율 이상이면 구매
        if discounts[i] >= user_rate:
            # 할인된 가격을 계산하여 합계에 추가
            purchase_amount += emoticons[i] * (100 - discounts[i]) // 100
            
    return purchase_amount


# 2. 특정 할인율 조합에 대한 모든 유저의 결과를 계산하는 함수
def calculate_subscribers_and_revenue(users, emoticons, discounts):
    """
    주어진 할인율 조합에서 이모티콘 플러스 가입자 수와 총 매출액을 반환합니다.
    """
    subscribers = 0
    total_revenue = 0
    
    for user_rate, user_limit in users:
        # 1번 함수를 호출하여 해당 유저의 구매 합계 계산
        purchase_amount = get_user_purchase_amount(user_rate, emoticons, discounts)
        
        # 구매 합계가 기준 가격 이상이면 플러스 서비스 가입
        if purchase_amount >= user_limit:
            subscribers += 1
        # 기준 가격 미만이면 이모티콘 구매 (매출에 합산)
        else:
            total_revenue += purchase_amount
            
    return subscribers, total_revenue


# 3. 메인 함수: 모든 경우의 수를 탐색하고 최적의 결과를 반환
def solution(users, emoticons):
    discount_rates = [10, 20, 30, 40]
    results = [] # 결과를 담을 리스트
    
    # 모든 할인율 조합(중복 순열) 생성
    for discounts in product(discount_rates, repeat=len(emoticons)):
        # 2번 함수를 호출하여 현재 할인율 조합의 결과(가입자 수, 매출액) 계산
        subscribers, revenue = calculate_subscribers_and_revenue(users, emoticons, discounts)
        
        # 리스트에 [가입자 수, 매출액] 형태로 추가
        results.append([subscribers, revenue])
        
    # 가입자 수를 기준으로 1차 내림차순, 매출액을 기준으로 2차 내림차순 정렬
    results.sort(key=lambda x: (x[0], x[1]), reverse=True)
    
    # 가장 위에 있는(조건에 가장 잘 맞는) 값을 반환
    return results[0]