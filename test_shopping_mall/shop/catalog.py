import random
import itertools
from typing import List, Generator, Tuple, Iterator
from .models import Product

class ProductIterator:
    """
    상품 목록을 하나씩 순회하기 위한 커스텀 이터레이터입니다.
    __iter__와 __next__ 매직 메서드를 구현하여 동작합니다.
    """
    def __init__(self, products: List[Product]) -> None:
        self._products: List[Product] = products
        self._index: int = 0

    def __iter__(self) -> 'ProductIterator':
        return self

    def __next__(self) -> Product:
        # 인덱스가 리스트 길이를 넘어가면 순회가 끝난 것으로 간주하고 예외 발생
        if self._index >= len(self._products):
            raise StopIteration
        
        item: Product = self._products[self._index]
        self._index += 1
        return item


class ProductCatalog:
    """쇼핑몰의 전체 상품을 관리하고 조회 기능을 제공하는 클래스입니다."""
    
    def __init__(self) -> None:
        self._products: List[Product] = []
        self._load_dummy_data()

    def _load_dummy_data(self) -> None:
        """테스트를 위한 대량의 더미 상품 데이터를 적재합니다."""
        for i in range(1, 26):  # 25개의 상품 생성
            self._products.append(
                Product(f"P{i:03d}", f"테스트 상품 {i}", 10000 + (i * 1000), 50)
            )

    def __iter__(self) -> ProductIterator:
        """
        객체 자체를 for문에서 돌릴 수 있도록 커스텀 이터레이터를 반환합니다.
        예: for item in catalog: print(item)
        """
        return ProductIterator(self._products)

    def get_paginated_products(self, page_size: int = 10) -> Generator[List[Product], None, None]:
        """
        상품 목록을 지정된 크기(page_size)만큼 잘라서 스트리밍하는 제너레이터입니다.
        대용량 데이터를 한 번에 메모리에 올리지 않고 필요할 때마다 방출(yield)합니다.
        """
        for i in range(0, len(self._products), page_size):
            # i부터 i+page_size 전까지 슬라이싱하여 반환하고 실행을 일시 정지(yield)
            yield self._products[i : i + page_size]

    def get_random_recommendations(self, count: int = 3) -> List[Product]:
        """random 모듈을 사용하여 지정된 개수만큼 무작위 추천 상품을 반환합니다."""
        if count > len(self._products):
            count = len(self._products)
        # random.sample은 중복 없이 무작위로 요소를 추출합니다.
        return random.sample(self._products, count)

    def get_discount_sets(self, bundle_size: int = 2, limit: int = 3) -> List[Tuple[Product, ...]]:
        """
        itertools.combinations를 사용하여 상품들을 묶은 세트 조합을 생성합니다.
        모든 조합을 만들면 너무 많으므로, 상위 limit 개수만 반환합니다.
        """
        # 앞의 5개 상품만 대상으로 세트 조합 생성 (성능 및 가독성 목적)
        target_products = self._products[:5]
        
        # bundle_size(예: 2)개씩 묶은 모든 수학적 조합 생성
        all_combinations = itertools.combinations(target_products, bundle_size)
        
        # 생성된 이터레이터에서 limit(예: 3)개만 뽑아서 리스트로 반환
        return list(itertools.islice(all_combinations, limit))

# 시스템 전반에서 사용할 싱글톤 카탈로그 인스턴스
catalog_service: ProductCatalog = ProductCatalog()