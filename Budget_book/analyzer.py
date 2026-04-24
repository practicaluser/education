def calculate_statistics(records, target_month, target_category):
    """
    가계부 데이터 리스트를 받아 월별 합계, 특정 카테고리 평균, 
    최고/최저 지출 항목을 계산하여 반환합니다.
    """
    if not records:
        return None

    # 1. filter: 특정 월(YYYY-MM)의 데이터만 추려내기
    # x['date']가 target_month(예: '2026-04')로 시작하는 내역만 필터링
    month_records = list(filter(lambda x: x['date'].startswith(target_month), records))

    # 2. map & sum: 월별 지출 합계 계산
    # 필터링된 데이터에서 'amount' 값만 뽑아낸 리스트 생성 후, sum으로 모두 더함
    month_amounts = list(map(lambda x: x['amount'], month_records))
    monthly_total = sum(month_amounts) if month_amounts else 0

    # 3. filter & map: 특정 카테고리의 데이터만 추려내어 금액 뽑기
    category_records = list(filter(lambda x: x['category'] == target_category, month_records))
    category_amounts = list(map(lambda x: x['amount'], category_records))

    # 4. round & sum: 카테고리별 평균 계산
    if category_amounts:
        # 합계를 개수로 나누어 평균을 구하고, round를 사용
        category_avg = round(sum(category_amounts) / len(category_amounts))
    else:
        category_avg = 0.0

    # 5. max & min: 가장 지출이 큰 항목과 적은 항목 찾기
    # key=lambda 를 사용하여 딕셔너리 안의 'amount'를 기준으로 전체 내역 중 최대/최소를 찾음
    # (단, 금액이 0원인 무의미한 내역은 제외하기 위해 0보다 큰 데이터만 먼저 필터링)
    valid_expenses = list(filter(lambda x: x['amount'] > 0, category_records))
    
    if valid_expenses:
        max_expense_item = max(valid_expenses, key=lambda x: x['amount'])
        min_expense_item = min(valid_expenses, key=lambda x: x['amount'])
    else:
        max_expense_item = None
        min_expense_item = None

    # 계산된 통계 수치들을 딕셔너리로 묶어서 반환 (출력은 하지 않음)
    return {
        "target_month": target_month,
        "monthly_total": monthly_total,
        "target_category": target_category,
        "category_avg": category_avg,
        "max_expense_item": max_expense_item,
        "min_expense_item": min_expense_item
    }

# 테스트 실행 블록
# if __name__ == "__main__":
#     # 임시 테스트 데이터
#     sample_records = [
#         {"date": "2026-04-01", "category": "식비", "amount": 8000, "memo": "김밥"},
#         {"date": "2026-04-15", "category": "식비", "amount": 45000, "memo": "회식"},
#         {"date": "2026-04-24", "category": "교통비", "amount": 15000, "memo": "택시"},
#         {"date": "2026-05-02", "category": "식비", "amount": 12000, "memo": "점심"},
#     ]

#     # 함수 실행 (2026년 4월 데이터, '식비' 카테고리 분석)
#     stats = calculate_statistics(sample_records, target_month="2026-04", target_category="식비")

#     # 반환받은 딕셔너리 데이터 확인
#     print("--- 📊 통계 계산 결과 ---")
#     print(f"[{stats['target_month']}] 총 지출액: {stats['monthly_total']:,}원")
#     print(f"[{stats['target_category']}] 평균 지출액: {stats['category_avg']:,}원")
    
#     if stats['max_expense_item']:
#         print(f"\n최고 지출 항목: {stats['max_expense_item']['amount']:,}원 ({stats['max_expense_item']['memo']})")
#         print(f"최저 지출 항목: {stats['min_expense_item']['amount']:,}원 ({stats['min_expense_item']['memo']})")