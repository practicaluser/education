# 1. 유저 상태 관리 모듈
class Player:
    def __init__(self, k):
        self.k = k                  # 현재 피로도
        self.explore_count = 0      # 현재까지 탐험한 횟수

    def can_explore(self, min_required):
        """탐험 가능 여부 검증"""
        return self.k >= min_required

    def explore(self, cost):
        """던전 탐험 적용 (상태 변경)"""
        self.k -= cost
        self.explore_count += 1

    def rollback(self, cost):
        """탐험 취소 (백트래킹을 위한 상태 복구)"""
        self.k += cost
        self.explore_count -= 1


# 2. 던전 및 맵 관리 모듈
class DungeonSystem:
    def __init__(self, dungeons):
        self.dungeons = dungeons
        self.num_dungeons = len(dungeons) # len라고 하면 리스트의 최상위 요소 개수를 세어줌
        self.visited = [False] * self.num_dungeons

    def is_visited(self, index):
        return self.visited[index]

    def mark_visited(self, index):
        self.visited[index] = True

    def mark_unvisited(self, index):
        self.visited[index] = False

    def get_dungeon_info(self, index):
        """(최소 필요 피로도, 소모 피로도) 반환"""
        return self.dungeons[index]


# 3. 최고 기록 관리 모듈
class RecordManager:
    def __init__(self):
        self.max_explored = 0

    def update_record(self, current_count):
        """현재 횟수가 최고 기록을 넘으면 갱신"""
        if current_count > self.max_explored:
            self.max_explored = current_count


# 4. 탐색 엔진 (오케스트레이터)
class GameManager:
    def __init__(self, player, dungeon_system, record_manager):
        # 의존성 주입 (Dependency Injection): 외부에서 모듈(객체)을 받아와 조립
        self.player = player
        self.dungeon_system = dungeon_system
        self.record_manager = record_manager

    def start_exploration(self):
        """탐색을 시작하고 최종 최고 기록을 반환"""
        self._dfs()
        return self.record_manager.max_explored

    def _dfs(self):
        # 1. 현재 상태의 탐험 횟수를 기록 관리자에게 전달하여 갱신 시도
        self.record_manager.update_record(self.player.explore_count)

        # 2. 던전 시스템에 등록된 모든 던전을 순회
        for i in range(self.dungeon_system.num_dungeons):
            if not self.dungeon_system.is_visited(i):
                min_req, cost = self.dungeon_system.get_dungeon_info(i)
                
                # 3. 플레이어에게 해당 던전 입장 조건을 묻기
                if self.player.can_explore(min_req):
                    
                    # [진행] 던전 방문 처리 및 플레이어 피로도 소모
                    self.dungeon_system.mark_visited(i)
                    self.player.explore(cost)
                    
                    # 다음 깊이로 탐색 진행
                    self._dfs()
                    
                    # [복구] 탐색이 끝난 후, 다른 경로 탐색을 위해 상태 원상 복구
                    self.player.rollback(cost)
                    self.dungeon_system.mark_unvisited(i)


# 5. 최종 메인 실행 함수 (프로그래머스 제출용)
def solution(k, dungeons):
    # 각 모듈(객체) 생성
    player = Player(k)
    dungeon_system = DungeonSystem(dungeons)
    record_manager = RecordManager()
    
    # 게임 매니저에 모듈들을 조립하여 실행
    game = GameManager(player, dungeon_system, record_manager)
    
    return game.start_exploration()