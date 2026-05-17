from collections import deque

# ---------------------------------------------------------
# 기능 1: 단일 석유 덩어리 탐색 (BFS)
# ---------------------------------------------------------
def explore_chunk(start_r, start_c, land, visited, chunk_id):
    """
    특정 위치에서 연결된 석유 덩어리를 탐색하고 크기를 반환합니다.
    """
    n, m = len(land), len(land[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # 상, 하, 좌, 우
    
    queue = deque([(start_r, start_c)])
    visited[start_r][start_c] = chunk_id
    chunk_size = 1
    
    while queue:
        r, c = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # 격자 범위 내에 있고, 석유가 있으며, 아직 방문하지 않은 땅이라면
            if 0 <= nr < n and 0 <= nc < m:
                if land[nr][nc] == 1 and visited[nr][nc] == 0:
                    visited[nr][nc] = chunk_id
                    chunk_size += 1
                    queue.append((nr, nc))
                    
    return chunk_size

# ---------------------------------------------------------
# 기능 2: 전체 지도 라벨링 및 덩어리 정보 저장
# ---------------------------------------------------------
def label_all_chunks(land):
    """
    전체 땅을 순회하며 석유 덩어리에 ID를 부여하고 크기를 딕셔너리에 저장합니다.
    """
    n, m = len(land), len(land[0])
    # visited 배열: 0은 빈 땅, 1 이상은 석유 덩어리의 ID를 의미
    visited = [[0] * m for _ in range(n)] 
    chunk_size_map = {}
    current_chunk_id = 1
    
    for r in range(n):
        for c in range(m):
            # 방문하지 않은 석유 덩어리를 발견한 경우
            if land[r][c] == 1 and visited[r][c] == 0:
                size = explore_chunk(r, c, land, visited, current_chunk_id)
                chunk_size_map[current_chunk_id] = size
                current_chunk_id += 1 # 다음 덩어리를 위해 ID 증가
                
    return visited, chunk_size_map

# ---------------------------------------------------------
# 기능 3: 각 열(Column)별 획득 가능 석유량 계산
# ---------------------------------------------------------
def calculate_oil_per_column(visited, chunk_size_map):
    """
    각 열에 시추관을 뚫었을 때 얻을 수 있는 총 석유량을 리스트로 반환합니다.
    """
    n, m = len(visited), len(visited[0])
    oil_per_column = [0] * m
    
    for c in range(m):
        chunk_ids_in_column = set() # 중복 ID 방지를 위한 Set
        
        # 해당 열을 위에서 아래로 훑기
        for r in range(n):
            chunk_id = visited[r][c]
            if chunk_id > 0: # 석유 덩어리가 존재한다면
                chunk_ids_in_column.add(chunk_id)
                
        # Set에 모인 고유 ID들의 크기를 딕셔너리에서 찾아 합산
        total_oil = sum(chunk_size_map[chunk_id] for chunk_id in chunk_ids_in_column)
        oil_per_column[c] = total_oil
        
    return oil_per_column

# ---------------------------------------------------------
# 기능 4: 메인 솔루션 (프로젝트 완성)
# ---------------------------------------------------------
def solution(land):
    """
    위 기능들을 조립하여 최대 획득 가능한 석유량을 반환합니다.
    """
    # 1. 지도 전체를 분석하여 덩어리별 고유 ID 지도와 크기 정보를 얻음
    visited_map, chunk_size_map = label_all_chunks(land)
    
    # 2. 각 열별로 시추관을 내렸을 때 얻을 수 있는 석유량을 계산
    oil_per_column = calculate_oil_per_column(visited_map, chunk_size_map)
    
    # 3. 계산된 열별 획득량 중 최댓값을 반환
    return max(oil_per_column)