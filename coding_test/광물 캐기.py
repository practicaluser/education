from enum import Enum
from typing import List, Dict

# ==========================================
# 1. Constants & Enums (상수 및 데이터 타입 정의)
# ==========================================
class MineralType(str, Enum):
    DIAMOND = "diamond"
    IRON = "iron"
    STONE = "stone"

class PickaxeType(int, Enum):
    DIAMOND = 0
    IRON = 1
    STONE = 2

# 피로도 테이블 (곡괭이 종류에 따른 광물별 피로도)
FATIGUE_TABLE: Dict[PickaxeType, Dict[MineralType, int]] = {
    PickaxeType.DIAMOND: {MineralType.DIAMOND: 1, MineralType.IRON: 1, MineralType.STONE: 1},
    PickaxeType.IRON:    {MineralType.DIAMOND: 5, MineralType.IRON: 1, MineralType.STONE: 1},
    PickaxeType.STONE:   {MineralType.DIAMOND: 25, MineralType.IRON: 5, MineralType.STONE: 1},
}


# ==========================================
# 2. Models (데이터 구조 및 상태 관리)
# ==========================================
class MineralChunk:
    """광물 5개를 하나의 묶음으로 관리하고 책임을 지는 클래스"""
    
    CHUNK_SIZE = 5

    def __init__(self, minerals: List[str]):
        self.minerals = minerals
        self._dia_count = minerals.count(MineralType.DIAMOND.value)
        self._iron_count = minerals.count(MineralType.IRON.value)
        self._stone_count = minerals.count(MineralType.STONE.value)

    @property
    def sort_priority(self) -> tuple:
        """정렬 우선순위를 반환 (다이아몬드 > 철 > 돌 순)"""
        return (self._dia_count, self._iron_count, self._stone_count)

    def calculate_fatigue(self, pickaxe: PickaxeType) -> int:
        """특정 곡괭이로 이 묶음을 캤을 때의 피로도를 계산"""
        fatigue = 0
        for mineral_str in self.minerals:
            mineral_type = MineralType(mineral_str)
            fatigue += FATIGUE_TABLE[pickaxe][mineral_type]
        return fatigue


# ==========================================
# 3. Services (핵심 비즈니스 로직)
# ==========================================
class MiningService:
    """광물 캐기 작업을 총괄하는 서비스 클래스"""
    
    @staticmethod
    def prepare_mineable_minerals(picks: List[int], minerals: List[str]) -> List[str]:
        """곡괭이 개수에 맞춰 캘 수 있는 최대 광물 리스트를 반환"""
        total_picks = sum(picks)
        max_mineable = total_picks * MineralChunk.CHUNK_SIZE
        return minerals[:max_mineable]

    @staticmethod
    def create_sorted_chunks(minerals: List[str]) -> List[MineralChunk]:
        """광물을 청크 단위로 나누고, 캐기 힘든 순서대로 정렬하여 반환"""
        chunks = []
        for i in range(0, len(minerals), MineralChunk.CHUNK_SIZE):
            chunk_data = minerals[i : i + MineralChunk.CHUNK_SIZE]
            chunks.append(MineralChunk(chunk_data))
            
        # Chunk 객체의 sort_priority(다이아, 철, 돌 개수) 기준으로 내림차순 정렬
        chunks.sort(key=lambda chunk: chunk.sort_priority, reverse=True)
        return chunks

    @staticmethod
    def calculate_minimum_fatigue(picks: List[int], sorted_chunks: List[MineralChunk]) -> int:
        """가장 좋은 곡괭이부터 순서대로 배정하여 최소 피로도를 계산"""
        total_fatigue = 0
        
        # 곡괭이 재고를 복사하여 사용 (원본 훼손 방지)
        available_picks = {
            PickaxeType.DIAMOND: picks[0],
            PickaxeType.IRON: picks[1],
            PickaxeType.STONE: picks[2]
        }

        for chunk in sorted_chunks:
            # 다이아 -> 철 -> 돌 순서로 곡괭이 선택
            selected_pickaxe = None
            for pickaxe_type in PickaxeType:
                if available_picks[pickaxe_type] > 0:
                    selected_pickaxe = pickaxe_type
                    available_picks[pickaxe_type] -= 1
                    break
            
            # 더 이상 사용할 곡괭이가 없으면 종료
            if selected_pickaxe is None:
                break
                
            total_fatigue += chunk.calculate_fatigue(selected_pickaxe)

        return total_fatigue


# ==========================================
# 4. Controller / Main (조립 및 실행)
# ==========================================
def solution(picks: List[int], minerals: List[str]) -> int:
    """
    클라이언트(프로그래머스 플랫폼 등)와 맞닿아 있는 진입점(Entry Point).
    세부 로직은 모르게 하고, 서비스들을 호출하여 조립만 담당합니다.
    """
    # 1. 캘 수 있는 한계 설정
    mineable_minerals = MiningService.prepare_mineable_minerals(picks, minerals)
    
    # 2. 광물 묶음 생성 및 중요도(피로도) 순 정렬
    sorted_chunks = MiningService.create_sorted_chunks(mineable_minerals)
    
    # 3. 곡괭이 배정 및 최소 피로도 계산
    answer = MiningService.calculate_minimum_fatigue(picks, sorted_chunks)
    
    return answer