from datetime import date, datetime

def get_input_record():
    """
    사용자로부터 가계부 내역을 입력받습니다.
    한 줄 입력(빠른 입력)과 여러 줄 입력(단계별 입력) 중 선택할 수 있습니다.
    """
    print("\n[새로운 내역 입력]")
    print("1. ⚡ 한 줄로 빠르게 입력 (예: 오늘 식비 15000 점심식사)")
    print("2. 📝 항목별로 차근차근 입력")
    
    # 입력 방식 선택 무한루프
    while True:
        choice = input("▶ 입력 방식을 선택하세요 (1 또는 2): ").strip()
        
        if choice == '1':
            return _get_single_line_input()
        elif choice == '2':
            return _get_step_by_step_input()
        else:
            print("⚠️ 잘못된 입력입니다. '1' 또는 '2'를 입력해주세요.")


def _get_single_line_input():
    """1번 모드: 띄어쓰기를 기준으로 한 줄로 입력받고 검증합니다."""
    print("\n[한 줄 입력 모드]")
    print("형식: 날짜(YYYY-MM-DD 또는 '오늘') 분류 금액 메모(선택)")
    
    while True:
        line_input = input("입력: ").strip()
        
        # 입력 취소 기능 (엔터만 쳤을 때)
        if not line_input:
            print("⚠️ 입력이 취소되었습니다. 다시 선택해주세요.")
            return get_input_record()

        # 1. split()을 사용하여 띄어쓰기 기준으로 문자열 분리
        # maxsplit=3: 날짜, 분류, 금액을 쪼개고, 나머지 띄어쓰기가 포함된 긴 메모는 하나로 뭉침
        parts = line_input.split(maxsplit=3)
        
        # 최소한 날짜, 분류, 금액 3가지는 입력해야 함
        if len(parts) < 3:
            print("⚠️ 형식이 맞지 않습니다. 띄어쓰기로 구분하여 3개 이상 입력해주세요.")
            continue
            
        date_str = parts[0]
        category = parts[1]
        amount_str = parts[2]
        # 메모는 생략 가능하므로, 입력 길이가 4개일 때만 가져오고 아니면 빈 문자열 처리
        memo = parts[3] if len(parts) == 4 else ""

        # 2. 날짜 검증
        if date_str == "오늘":
            record_date = str(date.today())
        else:
            try:
                record_date = str(datetime.strptime(date_str, "%Y-%m-%d").date())
            except ValueError:
                print(f"⚠️ 날짜 형식 오류: '{date_str}' (YYYY-MM-DD 형식 또는 '오늘'로 입력)")
                continue

        # 3. 금액 검증
        if not amount_str.isdigit():
            print(f"⚠️ 금액 형식 오류: '{amount_str}' (숫자만 입력)")
            continue
        amount = int(amount_str)

        print("✅ 한 줄 입력이 성공적으로 완료되었습니다.")
        return {
            "date": record_date,
            "category": category,
            "amount": amount,
            "memo": memo
        }


def _get_step_by_step_input():
    """2번 모드: 기존과 동일한 단계별 입력 및 검증 로직입니다."""
    print("\n[항목별 입력 모드]")
    
    # 1. 날짜 입력
    while True:
        date_input = input("날짜 (YYYY-MM-DD) [엔터: 오늘]: ").strip()
        if date_input == "":
            record_date = str(date.today())
            break
        else:
            try:
                record_date = str(datetime.strptime(date_input, "%Y-%m-%d").date())
                break
            except ValueError:
                print("⚠️ 잘못된 형식입니다. '2026-04-24' 형태로 입력해주세요.")

    # 2. 분류 입력
    while True:
        category = input("분류 (예: 식비, 교통비): ").strip()
        if category == "":
            print("⚠️ 분류는 필수입니다.")
        else:
            break

    # 3. 금액 입력
    while True:
        amount_input = input("금액 (숫자만): ").strip()
        if amount_input.isdigit():
            amount = int(amount_input)
            break
        else:
            print("⚠️ 금액은 숫자만 입력해야 합니다.")

    # 4. 메모 입력
    memo = input("메모 (선택사항): ").strip()

    print("✅ 내역이 성공적으로 입력되었습니다.")
    return {
        "date": record_date,
        "category": category,
        "amount": amount,
        "memo": memo
    }

# 테스트 실행 블록
if __name__ == "__main__":
    new_record = get_input_record()
    print("\n--- [최종 반환된 데이터] ---")
    print(new_record)