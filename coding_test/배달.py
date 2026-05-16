import heapq
from collections import defaultdict
from typing import List, Dict, Tuple

class GraphBuilder:
    """도로 정보를 바탕으로 그래프를 생성하는 모듈"""
    
    @staticmethod
    def build(n: int, roads: List[List[int]]) -> Dict[int, List[Tuple[int, int]]]:
        """
        N개의 노드와 간선 정보를 받아 인접 리스트 형태의 그래프를 반환합니다.
        
        :param n: 마을의 개수
        :param roads: 도로 정보가 담긴 2차원 리스트 [출발, 도착, 시간]
        :return: 각 마을과 연결된 마을 및 걸리는 시간 정보를 담은 딕셔너리
        """
        graph = defaultdict(list)
        
        for u, v, w in roads:
            # 양방향 통행이므로 양쪽 노드에 모두 추가합니다.
            # 중복된 도로가 있을 수 있으나, 다익스트라 알고리즘 내에서 
            # 더 긴 거리는 무시되므로 그대로 모두 추가해도 무방합니다.
            graph[u].append((v, w))
            graph[v].append((u, w))
            
        return graph

class PathFinder:
    """최단 경로를 계산하는 모듈"""
    
    @staticmethod
    def get_shortest_paths(graph: Dict[int, List[Tuple[int, int]]], num_nodes: int, start: int) -> Dict[int, int]:
        """
        다익스트라 알고리즘을 사용하여 시작점에서 모든 노드까지의 최단 거리를 계산합니다.
        
        :param graph: 인접 리스트 형태의 그래프 데이터
        :param num_nodes: 전체 노드의 수
        :param start: 시작 노드 번호
        :return: 시작 노드로부터 각 노드까지의 최단 거리를 담은 딕셔너리
        """
        # 모든 마을까지의 거리를 무한대로 초기화
        distances = {i: float('inf') for i in range(1, num_nodes + 1)}
        distances[start] = 0
        
        # 우선순위 큐 (거리, 노드번호)
        queue = [(0, start)]
        
        while queue:
            # queue는 빈 리스트가 된다
            current_distance, current_node = heapq.heappop(queue)
            
            # 큐에서 뽑은 거리가 이미 기록된 최단 거리보다 크면 무시
            if distances[current_node] < current_distance:
                continue
                
            # 인접 노드 탐색
            for adjacent_node, weight in graph[current_node]:
                distance = current_distance + weight
                
                # 새로운 경로가 기존 경로보다 짧으면 업데이트
                if distance < distances[adjacent_node]:
                    distances[adjacent_node] = distance
                    heapq.heappush(queue, (distance, adjacent_node))
                    
        return distances

class DeliveryService:
    """배달 관련 비즈니스 로직을 처리하는 모듈"""
    
    @staticmethod
    def count_deliverable_villages(distances: Dict[int, int], max_time: int) -> int:
        """
        제한 시간 내에 배달 가능한 마을의 수를 셉니다.
        
        :param distances: 시작 노드로부터 각 노드까지의 거리 정보
        :param max_time: 배달 가능한 최대 시간 (K)
        :return: 배달 가능한 마을의 개수
        """
        return sum(1 for dist in distances.values() if dist <= max_time)

# ==========================================
# 메인 실행 함수 (Orchestrator)
# ==========================================
def solution(N: int, road: List[List[int]], K: int) -> int:
    """
    각 독립적인 모듈을 조립하여 최종 결과를 만들어냅니다.
    """
    # 1. 원시 데이터로부터 그래프 데이터 구조 생성
    graph = GraphBuilder.build(N, road)
    
    # 2. 1번 마을(음식점)을 시작점으로 모든 마을까지의 최단 거리 계산
    distances = PathFinder.get_shortest_paths(graph, N, start=1)
    
    # 3. K 시간 이하로 배달 가능한 마을의 개수 필터링 및 산출
    result = DeliveryService.count_deliverable_villages(distances, K)
    
    return result