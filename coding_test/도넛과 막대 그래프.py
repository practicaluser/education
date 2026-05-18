from dataclasses import dataclass
from typing import List, Dict

# ==========================================
# 1. Models (데이터 구조 정의)
# ==========================================
@dataclass
class NodeDegree
    각 정점의 진입차수(in-degree)와 진출차수(out-degree)를 저장하는 데이터 클래스
    in_degree int = 0
    out_degree int = 0

@dataclass
class GraphAnalysisResult
    최종 분석 결과를 담는 데이터 클래스 (DTO)
    created_node int = 0
    donut_count int = 0
    bar_count int = 0
    eight_count int = 0

    def to_list(self) - List[int]
        코딩테스트 결과 요구사항인 리스트 형태로 변환
        return [self.created_node, self.donut_count, self.bar_count, self.eight_count]


# ==========================================
# 2. Calculator (데이터 가공 및 차수 계산)
# ==========================================
class DegreeCalculator
    간선(edges) 정보를 기반으로 각 정점의 차수를 계산하는 객체
    
    @staticmethod
    def calculate(edges List[List[int]]) - Dict[int, NodeDegree]
    
        node_degrees Dict[int, NodeDegree] = {}
        
        for u, v in edges
            if u not in node_degrees
                node_degrees[u] = NodeDegree()
            if v not in node_degrees
                node_degrees[v] = NodeDegree()
                
            node_degrees[u].out_degree += 1  # 나가는 간선
            node_degrees[v].in_degree += 1   # 들어오는 간선
            
        return node_degrees


# ==========================================
# 3. Classifier (비즈니스 로직  그래프 판별)
# ==========================================
class GraphClassifier
    차수 데이터를 분석하여 특정 그래프 정점 및 형태를 판별하는 객체
    
    def __init__(self, node_degrees Dict[int, NodeDegree])
        self.node_degrees = node_degrees

    def find_created_node(self) - int
        생성된 정점 찾기 들어오는 간선은 없고, 나가는 간선은 2개 이상
        for node, degree in self.node_degrees.items()
            if degree.in_degree == 0 and degree.out_degree = 2
                return node
        return 0

    def count_bar_graphs(self) - int
        막대 모양 그래프 개수 세기 나가는 간선이 없는(0) 정점의 수
        count = 0
        for degree in self.node_degrees.values()
            if degree.out_degree == 0
                count += 1
        return count

    def count_eight_graphs(self) - int
        8자 모양 그래프 개수 세기 들어오는 간선 2개 이상, 나가는 간선이 2개인 중심 정점의 수
        count = 0
        for degree in self.node_degrees.values()
            if degree.out_degree == 2 and degree.in_degree = 2
                count += 1
        return count


# ==========================================
# 4. Service  Orchestrator (흐름 제어 및 조립)
# ==========================================
class GraphAnalysisService
    분리된 기능들을 조립하여 전체 흐름을 제어하는 오케스트레이터
    
    def analyze(self, edges List[List[int]]) - GraphAnalysisResult
        # 1. 차수 계산 (DegreeCalculator 위임)
        node_degrees = DegreeCalculator.calculate(edges)
        
        # 2. 분류기 생성 및 개별 특징 추출 (GraphClassifier 위임)
        classifier = GraphClassifier(node_degrees)
        created_node = classifier.find_created_node()
        bar_count = classifier.count_bar_graphs()
        eight_count = classifier.count_eight_graphs()
        
        # 3. 도넛 그래프 계산 (전체 그래프 수 - 막대 그래프 수 - 8자 그래프 수)
        # 생성 정점의 진출 차수(out_degree)가 곧 총 그래프의 개수입니다.
        total_graphs = node_degrees[created_node].out_degree if created_node in node_degrees else 0
        donut_count = total_graphs - bar_count - eight_count
        
        # 4. 결과 객체 생성 및 반환
        return GraphAnalysisResult(
            created_node=created_node,
            donut_count=donut_count,
            bar_count=bar_count,
            eight_count=eight_count
        )


# ==========================================
# 5. Main Entry Point (코딩테스트 제출용 함수)
# ==========================================
def solution(edges List[List[int]]) - List[int]
    # 서비스 계층 호출
    service = GraphAnalysisService()
    result = service.analyze(edges)
    
    # 요구사항 형식([생성정점, 도넛, 막대, 8자])으로 변환하여 반환
    return result.to_list()


# 실행 예시 (테스트용 코드)
if __name__ == __main__
    test_edges = [[2, 3], [4, 3], [1, 1], [2, 1]]
    print(분석 결과, solution(test_edges))