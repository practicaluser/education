import json

def load_data(filename="account_book.json"):
    """
    JSON 파일에서 데이터를 읽어와 파이썬 리스트로 반환하는 함수.
    파일이 없거나 읽을 수 없는 경우 빈 리스트를 반환합니다.
    """
    try:
        # 1. 파일 읽기 및 with 문 사용 (파일을 안전하게 열고 자동 종료)
        with open(filename, 'r', encoding='utf-8') as file:
            # 2. json.load: JSON 데이터(텍스트)를 파이썬 자료형(리스트/딕셔너리)으로 변환 (역직렬화)
            data = json.load(file)
            return data # 3. 리턴값: 변환된 리스트 반환
            
    except FileNotFoundError:
        # 프로그램 최초 실행 시 파일이 없을 때 에러를 방지하고 빈 리스트(초기 상태) 반환
        return []
    except json.JSONDecodeError:
        # 파일이 비어있거나 형식이 망가졌을 때 빈 리스트 반환
        return []


def save_data(data, filename="account_book.json"):
    """
    파이썬 리스트/딕셔너리 데이터를 JSON 파일로 저장하는 함수.
    """
    try:
        # 1. 파일 쓰기('w' 모드) 및 with 문 사용
        with open(filename, 'w', encoding='utf-8') as file:
            # 2. json.dump: 파이썬 자료형을 JSON 문자열로 변환하여 파일에 저장 (직렬화)
            # ensure_ascii=False: 한글 깨짐 방지 / indent=4: 사람이 읽기 좋게 줄바꿈 적용
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")
        return False


# 테스트 실행 블록 (실제 메인 로직에서는 지워도 됩니다)
# if __name__ == "__main__":
#     # 임시 테스트 데이터 (리스트 안에 딕셔너리가 있는 형태)
#     sample_data = [
#         {"date": "2023-10-25", "category": "식비", "amount": 8500, "memo": "점심 식사"},
#         {"date": "2023-10-26", "category": "교통비", "amount": 2500, "memo": "지하철"}
#     ]

#     # 1. 저장 테스트 (매개변수 초깃값 적용)
#     print("데이터를 저장합니다...")
#     save_data(sample_data)  # filename을 안 넣으면 "account_book.json"으로 자동 저장됨
#     print("저장 완료!\n")

#     # 2. 불러오기 테스트
#     print("데이터를 불러옵니다...")
#     loaded_data = load_data()
    
#     # 불러온 데이터 출력
#     for item in loaded_data:
#         print(f"날짜: {item['date']}, 분류: {item['category']}, 금액: {item['amount']}원, 메모: {item['memo']}")