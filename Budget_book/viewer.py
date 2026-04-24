def display_records(records):
    """
    가계부 데이터 리스트를 전달받아 금액순으로 정렬한 뒤,
    보기 좋은 형태로 화면에 출력합니다.
    """
    print("\n📊 [가계부 내역 조회 - 금액 높은 순]")
    
    if not records:
        print("등록된 내역이 없습니다.")
        return

    # 1. 내장함수 sorted + lambda 함수
    # key=lambda x: x['amount'] -> 딕셔너리의 'amount' 값을 기준으로 정렬하겠다는 의미
    # reverse=True -> 내림차순 (금액이 높은 것부터 아래로) 정렬
    sorted_records = sorted(records, key=lambda x: x['amount'], reverse=True)

    

    # 표의 헤더 출력 (문자열 포맷팅으로 간격 맞춤)
    print("-" * 60)
    print(f"{'날짜':<12} | {'분류':<10} | {'금액':<12} | {'메모'}")
    print("-" * 60)

    # 2. 제어문: for + continue
    for record in sorted_records:
        # 특정 조건 검사: 만약 금액이 0원이라면 무의미한 내역으로 간주하고 출력을 건너뜀
        if record['amount'] == 0:
            continue 
            
        # 천 단위 콤마(,)를 포함하여 보기 좋게 포맷팅
        date_str = record['date']
        category_str = record['category']
        amount_str = f"{record['amount']:,}원" # 천 단위 쉼표 추가
        memo_str = record['memo']

        # <, > 기호를 사용하여 좌우 정렬 및 칸 간격 조정
        print(f"{date_str:<14} | {category_str:<10} | {amount_str:<13} | {memo_str}")
        
    print("-" * 60)
    print("조회가 완료되었습니다.\n")

# 테스트 실행 블록
# if __name__ == "__main__":
#     # 임시 테스트 데이터 (순서가 뒤죽박죽이고, 0원인 데이터도 포함)
#     sample_records = [
#         {"date": "2026-04-24", "category": "식비", "amount": 15000, "memo": "점심 식사"},
#         {"date": "2026-04-25", "category": "교통비", "amount": 0, "memo": "환승 무료 (출력에서 제외됨)"},
#         {"date": "2026-04-23", "category": "월급", "amount": 3500000, "memo": "4월 급여"},
#         {"date": "2026-04-26", "category": "쇼핑", "amount": 45000, "memo": "운동화 구매"}
#     ]

#     # 조회 함수 실행
#     display_records(sample_records)