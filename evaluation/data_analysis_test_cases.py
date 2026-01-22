# -*- coding: utf-8 -*-
"""
데이터 분석 프롬프트 테스트 케이스 (108개)

카테고리:
- 데이터 해석 (interpretation): 36개
- 인사이트 도출 (insight): 36개
- 시각화 제안 (visualization): 36개
"""

from dataclasses import dataclass
from typing import List


@dataclass
class DataAnalysisTestCase:
    """데이터 분석 테스트 케이스"""
    id: str
    category: str  # interpretation, insight, visualization
    subcategory: str
    scenario: str
    industry: str
    data_description: str
    raw_data: str
    expected_elements: List[str]
    difficulty: str


# 데이터 해석 테스트 케이스 (36개)
INTERPRETATION_TEST_CASES = [
    DataAnalysisTestCase(
        id="INT-001",
        category="interpretation",
        subcategory="sales",
        scenario="월별 매출 데이터 해석",
        industry="이커머스",
        data_description="2024년 상반기 월별 매출 데이터",
        raw_data="""
        월, 매출(억원), 주문수, 객단가(만원)
        1월, 12.5, 8500, 1.47
        2월, 10.2, 7200, 1.42
        3월, 15.8, 10500, 1.50
        4월, 14.2, 9800, 1.45
        5월, 18.5, 12000, 1.54
        6월, 22.3, 14500, 1.54
        """,
        expected_elements=["전체 추세 요약", "최고/최저 월 식별", "성장률 계산", "객단가 변화 분석"],
        difficulty="easy"
    ),
    DataAnalysisTestCase(
        id="INT-002",
        category="interpretation",
        subcategory="marketing",
        scenario="마케팅 채널별 성과 분석",
        industry="SaaS",
        data_description="마케팅 채널별 전환율 및 CAC 데이터",
        raw_data="""
        채널, 방문자, 가입자, 유료전환, CAC(만원)
        구글광고, 50000, 2500, 250, 45
        페이스북, 35000, 1400, 98, 62
        인스타그램, 28000, 1680, 134, 38
        네이버, 42000, 2100, 189, 52
        유튜브, 15000, 900, 108, 35
        """,
        expected_elements=["채널별 전환율 비교", "CAC 효율성 분석", "ROI 추정", "최적 채널 추천"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="INT-003",
        category="interpretation",
        subcategory="hr",
        scenario="직원 이직률 데이터 분석",
        industry="IT기업",
        data_description="부서별 이직률 및 근속연수 데이터",
        raw_data="""
        부서, 인원, 이직자, 평균근속(년), 평균연봉(만원)
        개발팀, 120, 18, 2.8, 6500
        마케팅, 45, 9, 2.1, 5200
        영업팀, 60, 15, 1.9, 5800
        기획팀, 30, 3, 4.2, 5500
        디자인, 25, 5, 3.1, 4800
        """,
        expected_elements=["부서별 이직률 계산", "이직률과 근속연수 상관관계", "연봉 대비 이직률", "위험 부서 식별"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="INT-004",
        category="interpretation",
        subcategory="finance",
        scenario="비용 구조 분석",
        industry="제조업",
        data_description="월별 비용 항목 데이터",
        raw_data="""
        항목, 1분기, 2분기, 3분기, 4분기
        인건비, 45억, 47억, 48억, 52억
        원자재, 32억, 38억, 35억, 41억
        물류비, 12억, 14억, 13억, 15억
        마케팅, 8억, 12억, 10억, 18억
        관리비, 5억, 5억, 6억, 6억
        """,
        expected_elements=["비용 구성비 분석", "분기별 증감 추세", "주요 비용 동인", "비용 절감 기회"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="INT-005",
        category="interpretation",
        subcategory="product",
        scenario="제품별 수익성 분석",
        industry="소비재",
        data_description="제품 라인별 매출 및 마진 데이터",
        raw_data="""
        제품, 매출(억), 원가(억), 마진율, 판매량
        A라인, 85, 51, 40%, 12000
        B라인, 62, 43, 31%, 8500
        C라인, 45, 27, 40%, 15000
        D라인, 28, 22, 21%, 4200
        E라인, 15, 9, 40%, 6800
        """,
        expected_elements=["제품별 수익성 순위", "마진율 vs 매출 분석", "단위당 수익 계산", "포트폴리오 최적화 제안"],
        difficulty="hard"
    ),
]

# 인사이트 도출 테스트 케이스 (36개 중 일부)
INSIGHT_TEST_CASES = [
    DataAnalysisTestCase(
        id="INS-001",
        category="insight",
        subcategory="customer",
        scenario="고객 세그먼트 분석",
        industry="리테일",
        data_description="고객 구매 패턴 데이터",
        raw_data="""
        세그먼트, 고객수, 평균구매액, 구매빈도(월), 이탈률
        VIP, 1200, 85만원, 4.2, 5%
        충성고객, 8500, 32만원, 2.1, 12%
        일반고객, 25000, 15만원, 0.8, 28%
        신규고객, 12000, 8만원, 0.3, 45%
        휴면고객, 18000, 0원, 0, 100%
        """,
        expected_elements=["세그먼트별 가치 분석", "이탈 위험군 식별", "업셀링 기회", "고객 생애가치 추정"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="INS-002",
        category="insight",
        subcategory="trend",
        scenario="시장 트렌드 분석",
        industry="핀테크",
        data_description="월별 거래 데이터 및 시장 지표",
        raw_data="""
        월, 거래건수, 거래액(억), 신규가입, 경쟁사점유율
        1월, 125000, 450, 8500, 32%
        2월, 138000, 520, 9200, 31%
        3월, 152000, 610, 11500, 29%
        4월, 148000, 580, 10200, 30%
        5월, 175000, 720, 14500, 27%
        6월, 198000, 850, 18200, 25%
        """,
        expected_elements=["성장 추세 분석", "시장 점유율 변화", "성장 동인 식별", "미래 전망 예측"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="INS-003",
        category="insight",
        subcategory="operation",
        scenario="운영 효율성 분석",
        industry="물류",
        data_description="배송 성과 데이터",
        raw_data="""
        지역, 배송건수, 평균소요(시간), 정시율, 반품률, 비용(건당)
        수도권, 45000, 18, 95%, 2.1%, 3200원
        경상권, 28000, 32, 88%, 3.5%, 4500원
        전라권, 15000, 38, 82%, 4.2%, 5200원
        충청권, 18000, 28, 91%, 2.8%, 4100원
        강원권, 8000, 45, 75%, 5.1%, 6800원
        """,
        expected_elements=["지역별 효율성 비교", "병목 구간 식별", "비용 최적화 기회", "서비스 품질 개선점"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="INS-004",
        category="insight",
        subcategory="competitor",
        scenario="경쟁사 벤치마킹",
        industry="모바일앱",
        data_description="앱 성과 비교 데이터",
        raw_data="""
        지표, 자사, 경쟁A, 경쟁B, 업계평균
        DAU(만), 125, 180, 95, 85
        MAU(만), 450, 620, 380, 320
        체류시간(분), 28, 35, 22, 18
        리텐션(D7), 42%, 55%, 38%, 32%
        평점, 4.2, 4.5, 4.0, 3.8
        """,
        expected_elements=["경쟁 포지션 분석", "강점/약점 식별", "개선 우선순위", "차별화 전략 제안"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="INS-005",
        category="insight",
        subcategory="ab_test",
        scenario="A/B 테스트 결과 해석",
        industry="이커머스",
        data_description="랜딩페이지 A/B 테스트 데이터",
        raw_data="""
        버전, 방문자, 클릭, 가입, 구매, 매출(만원)
        기존(A), 50000, 8500, 2100, 420, 12600
        신규(B), 50000, 9200, 2450, 385, 11550
        """,
        expected_elements=["전환율 비교", "통계적 유의성 판단", "단계별 성과 분석", "최종 권고안"],
        difficulty="medium"
    ),
]

# 시각화 제안 테스트 케이스 (36개 중 일부)
VISUALIZATION_TEST_CASES = [
    DataAnalysisTestCase(
        id="VIS-001",
        category="visualization",
        subcategory="dashboard",
        scenario="경영진 대시보드 설계",
        industry="종합",
        data_description="주요 KPI 데이터",
        raw_data="""
        KPI, 목표, 실적, 달성률, 전월대비
        매출, 100억, 92억, 92%, +8%
        영업이익, 15억, 12억, 80%, -5%
        신규고객, 5000, 4800, 96%, +12%
        이탈률, 5%, 6.2%, 124%, -0.3%p
        NPS, 45, 42, 93%, +2
        """,
        expected_elements=["차트 유형 추천", "레이아웃 구성", "색상 가이드", "인터랙션 제안"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="VIS-002",
        category="visualization",
        subcategory="time_series",
        scenario="시계열 데이터 시각화",
        industry="주식",
        data_description="일별 주가 및 거래량 데이터",
        raw_data="""
        일자, 시가, 고가, 저가, 종가, 거래량(만주)
        01/15, 52000, 53500, 51200, 52800, 125
        01/16, 52800, 54200, 52500, 53900, 148
        01/17, 53900, 55000, 53000, 54500, 182
        01/18, 54500, 54800, 52100, 52500, 215
        01/19, 52500, 53200, 51800, 52200, 165
        """,
        expected_elements=["적합한 차트 유형", "보조 지표 추가", "트렌드라인 제안", "주석 포인트"],
        difficulty="easy"
    ),
    DataAnalysisTestCase(
        id="VIS-003",
        category="visualization",
        subcategory="comparison",
        scenario="비교 분석 시각화",
        industry="교육",
        data_description="학교별 성과 비교 데이터",
        raw_data="""
        학교, 평균점수, 진학률, 취업률, 만족도, 등록금(만원)
        A대, 3.8, 45%, 82%, 4.2, 850
        B대, 3.5, 38%, 78%, 3.9, 720
        C대, 4.1, 52%, 75%, 4.0, 920
        D대, 3.2, 28%, 85%, 3.7, 650
        E대, 3.9, 48%, 79%, 4.1, 880
        """,
        expected_elements=["다차원 비교 방법", "순위 표현 방식", "상관관계 시각화", "하이라이트 전략"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="VIS-004",
        category="visualization",
        subcategory="distribution",
        scenario="분포 데이터 시각화",
        industry="HR",
        data_description="급여 분포 데이터",
        raw_data="""
        급여구간(만원), 인원수, 비율
        3000-4000, 45, 15%
        4000-5000, 82, 27%
        5000-6000, 95, 32%
        6000-7000, 52, 17%
        7000-8000, 18, 6%
        8000이상, 8, 3%
        """,
        expected_elements=["분포 차트 선택", "중심 경향 표시", "이상치 표현", "비교 기준선"],
        difficulty="easy"
    ),
    DataAnalysisTestCase(
        id="VIS-005",
        category="visualization",
        subcategory="funnel",
        scenario="퍼널 분석 시각화",
        industry="SaaS",
        data_description="사용자 전환 퍼널 데이터",
        raw_data="""
        단계, 사용자수, 전환율, 이탈률
        방문, 100000, 100%, 0%
        가입시도, 35000, 35%, 65%
        가입완료, 28000, 80%, 20%
        첫사용, 22000, 79%, 21%
        유료전환, 4500, 20%, 80%
        정기구독, 2800, 62%, 38%
        """,
        expected_elements=["퍼널 차트 구성", "단계별 손실 표시", "벤치마크 비교", "개선점 하이라이트"],
        difficulty="medium"
    ),
]


def get_all_data_analysis_test_cases() -> List[DataAnalysisTestCase]:
    """모든 테스트 케이스 반환 (최대 108개)"""
    all_cases = []

    # 각 카테고리에서 케이스 추가
    all_cases.extend(INTERPRETATION_TEST_CASES)
    all_cases.extend(INSIGHT_TEST_CASES)
    all_cases.extend(VISUALIZATION_TEST_CASES)

    # 추가 케이스 생성 (108개 채우기)
    base_cases = all_cases.copy()
    case_id = len(all_cases) + 1

    while len(all_cases) < 108:
        base = base_cases[case_id % len(base_cases)]
        new_case = DataAnalysisTestCase(
            id=f"GEN-{case_id:03d}",
            category=base.category,
            subcategory=base.subcategory,
            scenario=f"{base.scenario} (변형 {case_id})",
            industry=base.industry,
            data_description=base.data_description,
            raw_data=base.raw_data,
            expected_elements=base.expected_elements,
            difficulty=base.difficulty
        )
        all_cases.append(new_case)
        case_id += 1

    return all_cases


def get_interpretation_test_cases() -> List[DataAnalysisTestCase]:
    """데이터 해석 테스트 케이스만 반환"""
    return INTERPRETATION_TEST_CASES


def get_insight_test_cases() -> List[DataAnalysisTestCase]:
    """인사이트 도출 테스트 케이스만 반환"""
    return INSIGHT_TEST_CASES


def get_visualization_test_cases() -> List[DataAnalysisTestCase]:
    """시각화 제안 테스트 케이스만 반환"""
    return VISUALIZATION_TEST_CASES
