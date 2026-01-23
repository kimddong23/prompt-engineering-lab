# -*- coding: utf-8 -*-
"""
데이터 분석 프롬프트 테스트 케이스 V2.0 (80개)

카테고리 (8개, 각 10개):
1. 데이터 해석 (interpretation): 10개
2. 인사이트 도출 (insight): 10개
3. 시각화 제안 (visualization): 10개
4. SQL 쿼리 (sql_query): 10개
5. 통계 분석 (statistics): 10개
6. 대시보드 설계 (dashboard): 10개
7. A/B 테스트 (ab_test): 10개
8. ML 결과 해석 (ml_interpretation): 10개
"""

from dataclasses import dataclass
from typing import List


@dataclass
class DataAnalysisTestCase:
    """데이터 분석 테스트 케이스"""
    id: str
    category: str
    subcategory: str
    scenario: str
    industry: str
    data_description: str
    raw_data: str
    expected_elements: List[str]
    difficulty: str


# =============================================================================
# 1. 데이터 해석 (interpretation) - 10개
# =============================================================================
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
        data_description="분기별 비용 항목 데이터",
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
    DataAnalysisTestCase(
        id="INT-006",
        category="interpretation",
        subcategory="inventory",
        scenario="재고 회전율 분석",
        industry="유통",
        data_description="카테고리별 재고 현황 데이터",
        raw_data="""
카테고리, 평균재고(억), 월매출(억), 회전율, 재고일수
가전, 45, 15, 4.0, 90
의류, 32, 24, 9.0, 40
식품, 18, 36, 24.0, 15
생활용품, 25, 12, 5.8, 63
화장품, 28, 21, 9.0, 40
        """,
        expected_elements=["회전율 해석", "적정 재고 수준 판단", "카테고리별 전략", "재고 비용 분석"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="INT-007",
        category="interpretation",
        subcategory="web_analytics",
        scenario="웹사이트 트래픽 분석",
        industry="미디어",
        data_description="일별 트래픽 및 사용자 행동 데이터",
        raw_data="""
요일, 방문자, 페이지뷰, 체류시간(분), 이탈률
월, 125000, 375000, 4.2, 45%
화, 132000, 410000, 4.5, 42%
수, 128000, 384000, 4.3, 44%
목, 135000, 425000, 4.8, 40%
금, 118000, 330000, 3.8, 52%
토, 95000, 245000, 3.2, 58%
일, 88000, 220000, 3.0, 62%
        """,
        expected_elements=["요일별 패턴 분석", "핵심 지표 해석", "문제 구간 식별", "개선 방향 제시"],
        difficulty="easy"
    ),
    DataAnalysisTestCase(
        id="INT-008",
        category="interpretation",
        subcategory="subscription",
        scenario="구독 서비스 지표 분석",
        industry="OTT",
        data_description="월별 구독 현황 데이터",
        raw_data="""
월, 신규가입, 해지, 순증, 누적구독자, MRR(억)
1월, 45000, 28000, 17000, 850000, 42.5
2월, 52000, 32000, 20000, 870000, 43.5
3월, 68000, 35000, 33000, 903000, 45.2
4월, 55000, 38000, 17000, 920000, 46.0
5월, 48000, 42000, 6000, 926000, 46.3
6월, 42000, 45000, -3000, 923000, 46.2
        """,
        expected_elements=["성장 추세 분석", "이탈률 계산", "MRR 변화 해석", "경고 신호 식별"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="INT-009",
        category="interpretation",
        subcategory="campaign",
        scenario="프로모션 효과 분석",
        industry="리테일",
        data_description="프로모션 전후 매출 데이터",
        raw_data="""
기간, 매출(억), 객수, 객단가, 할인율, 마진율
프로모션전(2주), 28.5, 42000, 6.8만, 0%, 35%
프로모션중(1주), 52.3, 85000, 6.2만, 20%, 22%
프로모션후(2주), 24.2, 38000, 6.4만, 0%, 35%
        """,
        expected_elements=["매출 증가 효과", "수익성 영향 분석", "고객 유입 효과", "ROI 계산"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="INT-010",
        category="interpretation",
        subcategory="cohort",
        scenario="코호트별 사용자 분석",
        industry="앱서비스",
        data_description="가입월별 코호트 리텐션 데이터",
        raw_data="""
가입월, M0, M1, M2, M3, M6, M12
2024-01, 10000, 4200, 3100, 2800, 2200, 1800
2024-02, 12000, 4800, 3500, 3000, 2400, -
2024-03, 15000, 5700, 4200, 3600, 2850, -
2024-04, 11000, 4100, 2900, 2400, -, -
2024-05, 13000, 4550, 3200, -, -, -
        """,
        expected_elements=["리텐션 곡선 분석", "코호트 간 비교", "임계 시점 식별", "개선 포인트 도출"],
        difficulty="hard"
    ),
]


# =============================================================================
# 2. 인사이트 도출 (insight) - 10개
# =============================================================================
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
        subcategory="churn",
        scenario="이탈 고객 패턴 분석",
        industry="구독서비스",
        data_description="이탈 고객 특성 데이터",
        raw_data="""
이탈시점, 고객수, 평균사용일, 평균결제액, 주요이탈사유
1개월내, 2500, 12일, 9900원, 기능부족(45%)
3개월내, 1800, 45일, 29700원, 가격(38%)
6개월내, 1200, 120일, 59400원, 경쟁사(52%)
1년내, 800, 280일, 118800원, 필요감소(61%)
        """,
        expected_elements=["이탈 시점별 특성", "이탈 사유 분석", "고위험군 프로파일", "리텐션 전략 제안"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="INS-006",
        category="insight",
        subcategory="pricing",
        scenario="가격 탄력성 분석",
        industry="이커머스",
        data_description="가격 변동에 따른 판매량 데이터",
        raw_data="""
제품, 원가격, 할인가, 할인율, 원판매량, 할인판매량, 매출변화
A, 50000, 45000, 10%, 1000, 1350, +21.5%
B, 80000, 64000, 20%, 500, 850, +36%
C, 30000, 27000, 10%, 2000, 2200, -1%
D, 120000, 96000, 20%, 200, 380, +52%
E, 25000, 20000, 20%, 3000, 3300, -12%
        """,
        expected_elements=["탄력성 계산", "제품별 민감도 분류", "최적 가격 전략", "수익 극대화 방안"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="INS-007",
        category="insight",
        subcategory="user_journey",
        scenario="사용자 여정 분석",
        industry="SaaS",
        data_description="사용자 행동 퍼널 데이터",
        raw_data="""
단계, 진입수, 완료수, 전환율, 평균소요시간, 이탈사유
회원가입, 10000, 6500, 65%, 3분, 복잡한양식(42%)
프로필설정, 6500, 5200, 80%, 5분, 스킵가능(35%)
튜토리얼, 5200, 3640, 70%, 8분, 지루함(55%)
첫기능사용, 3640, 2912, 80%, 12분, 어려움(48%)
반복사용(3회), 2912, 1747, 60%, -, 가치미인식(62%)
        """,
        expected_elements=["병목 구간 식별", "이탈 원인 분석", "단계별 개선안", "우선순위 결정"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="INS-008",
        category="insight",
        subcategory="seasonal",
        scenario="계절성 패턴 분석",
        industry="패션",
        data_description="월별 카테고리 매출 데이터 (2년치)",
        raw_data="""
월, 아우터, 상의, 하의, 신발, 액세서리
1월, 45억, 12억, 8억, 5억, 3억
2월, 38억, 15억, 10억, 6억, 4억
3월, 25억, 22억, 15억, 12억, 5억
4월, 12억, 28억, 20억, 15억, 6억
...
11월, 42억, 15억, 12억, 8억, 8억
12월, 52억, 18억, 14억, 10억, 15억
        """,
        expected_elements=["계절성 패턴 식별", "카테고리별 피크 시즌", "재고 전략 제안", "프로모션 타이밍"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="INS-009",
        category="insight",
        subcategory="cross_sell",
        scenario="교차 판매 기회 분석",
        industry="은행",
        data_description="상품 보유 현황 및 교차 판매 데이터",
        raw_data="""
보유상품, 고객수, 평균예금, 추가상품률, 주요추가상품
예금만, 250000, 1200만, 15%, 적금(45%)
예금+적금, 85000, 2800만, 32%, 펀드(38%)
예금+카드, 120000, 1800만, 28%, 대출(42%)
예금+대출, 65000, 3500만, 45%, 보험(52%)
종합(3+), 45000, 5200만, 62%, 프리미엄(65%)
        """,
        expected_elements=["상품 연관성 분석", "고객가치별 전략", "교차판매 우선순위", "타겟팅 기준 제안"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="INS-010",
        category="insight",
        subcategory="nps",
        scenario="NPS 심층 분석",
        industry="통신",
        data_description="NPS 설문 결과 및 고객 특성 데이터",
        raw_data="""
구분, 응답수, 비율, 평균사용기간, 평균ARPU, 주요의견
추천(9-10), 1200, 24%, 5.2년, 78000원, 네트워크품질(65%)
중립(7-8), 2800, 56%, 3.1년, 62000원, 가격(45%)
비추천(0-6), 1000, 20%, 1.8년, 55000원, 고객서비스(58%)

전체 NPS: +4
업계평균 NPS: +12
        """,
        expected_elements=["NPS 분석 및 해석", "그룹별 특성 비교", "개선 우선순위", "업계 대비 포지션"],
        difficulty="medium"
    ),
]


# =============================================================================
# 3. 시각화 제안 (visualization) - 10개
# =============================================================================
VISUALIZATION_TEST_CASES = [
    DataAnalysisTestCase(
        id="VIS-001",
        category="visualization",
        subcategory="executive",
        scenario="경영진 보고용 차트 설계",
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
        expected_elements=["차트 유형 추천", "레이아웃 구성", "색상 가이드", "핵심 메시지 강조"],
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
        scenario="다차원 비교 시각화",
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
    DataAnalysisTestCase(
        id="VIS-006",
        category="visualization",
        subcategory="geo",
        scenario="지역별 데이터 시각화",
        industry="부동산",
        data_description="지역별 부동산 가격 데이터",
        raw_data="""
지역, 평균가(억), 전년대비, 거래량, 평당가(만원)
강남구, 18.5, +12%, 850, 8500
서초구, 16.2, +10%, 720, 7800
송파구, 14.8, +15%, 980, 6500
용산구, 15.5, +8%, 420, 7200
마포구, 12.3, +18%, 650, 5800
        """,
        expected_elements=["지도 시각화 방법", "색상 스케일 설계", "레이어 구성", "인터랙션 제안"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="VIS-007",
        category="visualization",
        subcategory="correlation",
        scenario="상관관계 시각화",
        industry="헬스케어",
        data_description="건강 지표 상관관계 데이터",
        raw_data="""
변수쌍, 상관계수, 샘플수, 유의수준
BMI-혈압, 0.65, 5000, p<0.001
운동-체중, -0.52, 5000, p<0.001
수면-스트레스, -0.48, 5000, p<0.001
나이-혈당, 0.42, 5000, p<0.001
음주-간수치, 0.58, 5000, p<0.001
        """,
        expected_elements=["상관관계 차트 유형", "강도 표현 방법", "유의성 표시", "해석 가이드"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="VIS-008",
        category="visualization",
        subcategory="part_to_whole",
        scenario="구성비 시각화",
        industry="미디어",
        data_description="콘텐츠 소비 패턴 데이터",
        raw_data="""
연령대, 드라마, 예능, 영화, 뉴스, 스포츠, 기타
10대, 35%, 40%, 15%, 2%, 5%, 3%
20대, 32%, 28%, 25%, 5%, 7%, 3%
30대, 28%, 22%, 20%, 15%, 12%, 3%
40대, 22%, 18%, 18%, 25%, 14%, 3%
50대+, 18%, 15%, 15%, 35%, 12%, 5%
        """,
        expected_elements=["파이/도넛 vs 바 차트", "다중 그룹 비교", "색상 일관성", "레이블 전략"],
        difficulty="easy"
    ),
    DataAnalysisTestCase(
        id="VIS-009",
        category="visualization",
        subcategory="flow",
        scenario="흐름 데이터 시각화",
        industry="이커머스",
        data_description="사용자 페이지 이동 데이터",
        raw_data="""
출발페이지, 도착페이지, 이동수, 비율
홈, 카테고리, 45000, 35%
홈, 검색, 32000, 25%
홈, 이벤트, 25000, 19%
카테고리, 상품상세, 38000, 84%
검색, 상품상세, 28000, 88%
상품상세, 장바구니, 22000, 33%
장바구니, 결제, 15000, 68%
        """,
        expected_elements=["Sankey/Flow 차트", "노드 배치 전략", "링크 두께 표현", "핵심 경로 강조"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="VIS-010",
        category="visualization",
        subcategory="anomaly",
        scenario="이상치 시각화",
        industry="제조",
        data_description="생산 품질 모니터링 데이터",
        raw_data="""
시간, 온도, 압력, 습도, 불량률, 상태
08:00, 72.5, 1.02, 45%, 0.8%, 정상
09:00, 73.2, 1.01, 44%, 0.9%, 정상
10:00, 78.5, 1.05, 52%, 2.5%, 경고
11:00, 82.1, 1.08, 58%, 4.2%, 이상
12:00, 74.0, 1.02, 46%, 1.0%, 정상
        """,
        expected_elements=["관리도 구성", "임계값 표시", "이상 패턴 강조", "실시간 알림 연동"],
        difficulty="hard"
    ),
]


# =============================================================================
# 4. SQL 쿼리 (sql_query) - 10개
# =============================================================================
SQL_QUERY_TEST_CASES = [
    DataAnalysisTestCase(
        id="SQL-001",
        category="sql_query",
        subcategory="aggregation",
        scenario="매출 집계 쿼리 작성",
        industry="이커머스",
        data_description="주문 테이블에서 월별 매출 집계",
        raw_data="""
테이블: orders
- order_id (PK)
- user_id (FK)
- order_date (DATE)
- amount (INT)
- status (VARCHAR): 'completed', 'cancelled', 'refunded'

요구사항: 2024년 월별 완료된 주문의 총 매출, 주문 건수, 평균 주문금액 조회
        """,
        expected_elements=["SELECT 문 구성", "WHERE 조건", "GROUP BY 사용", "집계 함수 활용"],
        difficulty="easy"
    ),
    DataAnalysisTestCase(
        id="SQL-002",
        category="sql_query",
        subcategory="join",
        scenario="고객별 구매 분석 쿼리",
        industry="리테일",
        data_description="다중 테이블 조인 쿼리",
        raw_data="""
테이블1: customers
- customer_id (PK), name, signup_date, tier

테이블2: orders
- order_id (PK), customer_id (FK), order_date, total_amount

테이블3: order_items
- item_id (PK), order_id (FK), product_id, quantity, price

요구사항: 고객 등급별 평균 구매금액, 구매 빈도, 최근 구매일 조회
        """,
        expected_elements=["JOIN 구문 작성", "다중 테이블 연결", "서브쿼리 활용", "성능 고려"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="SQL-003",
        category="sql_query",
        subcategory="window",
        scenario="순위 및 누적 계산 쿼리",
        industry="영업",
        data_description="윈도우 함수를 활용한 분석",
        raw_data="""
테이블: sales
- sale_id (PK)
- salesperson_id (FK)
- sale_date (DATE)
- amount (INT)
- region (VARCHAR)

요구사항:
1. 영업사원별 월 매출 순위
2. 지역별 누적 매출
3. 전월 대비 성장률
        """,
        expected_elements=["RANK/ROW_NUMBER 사용", "SUM OVER 활용", "LAG/LEAD 함수", "PARTITION BY 구성"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="SQL-004",
        category="sql_query",
        subcategory="subquery",
        scenario="복잡한 조건 필터링 쿼리",
        industry="구독서비스",
        data_description="서브쿼리를 활용한 고객 필터링",
        raw_data="""
테이블1: users
- user_id (PK), email, created_at, status

테이블2: subscriptions
- sub_id (PK), user_id (FK), plan_type, start_date, end_date, amount

테이블3: user_events
- event_id (PK), user_id (FK), event_type, event_date

요구사항: 최근 30일 내 로그인했지만, 유료 구독 이력이 없는 사용자 조회
        """,
        expected_elements=["서브쿼리 구성", "NOT EXISTS/NOT IN 활용", "날짜 조건 처리", "효율적인 필터링"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="SQL-005",
        category="sql_query",
        subcategory="cte",
        scenario="코호트 분석 쿼리",
        industry="앱서비스",
        data_description="CTE를 활용한 리텐션 분석",
        raw_data="""
테이블: user_activity
- activity_id (PK)
- user_id (FK)
- activity_date (DATE)
- activity_type (VARCHAR)

요구사항:
가입 월 기준 코호트별 M+1, M+2, M+3 리텐션율 계산
(각 월에 최소 1회 이상 활동한 사용자 비율)
        """,
        expected_elements=["CTE(WITH) 구문", "코호트 그룹화", "리텐션 계산 로직", "피벗 형태 출력"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="SQL-006",
        category="sql_query",
        subcategory="pivot",
        scenario="피벗 테이블 쿼리",
        industry="마케팅",
        data_description="채널별 월간 성과 피벗",
        raw_data="""
테이블: campaign_results
- campaign_id (PK)
- channel (VARCHAR): 'google', 'facebook', 'instagram', 'naver'
- month (DATE)
- impressions (INT)
- clicks (INT)
- conversions (INT)
- spend (INT)

요구사항: 채널을 행으로, 월을 열로 하는 피벗 테이블 (전환수 기준)
        """,
        expected_elements=["CASE WHEN 피벗", "PIVOT 함수 활용", "동적 열 처리", "합계 행 추가"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="SQL-007",
        category="sql_query",
        subcategory="recursive",
        scenario="계층 구조 쿼리",
        industry="조직",
        data_description="조직도 계층 쿼리",
        raw_data="""
테이블: employees
- emp_id (PK)
- name (VARCHAR)
- manager_id (FK, self-reference)
- department (VARCHAR)
- hire_date (DATE)

요구사항:
1. 특정 임원의 모든 하위 직원 조회
2. 각 직원의 조직 레벨 계산
3. 부서별 관리자 체인 표시
        """,
        expected_elements=["재귀 CTE 사용", "CONNECT BY 대안", "레벨 계산", "경로 표현"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="SQL-008",
        category="sql_query",
        subcategory="optimization",
        scenario="쿼리 성능 최적화",
        industry="로그분석",
        data_description="대용량 로그 테이블 쿼리 최적화",
        raw_data="""
테이블: user_logs (10억 건)
- log_id (PK)
- user_id (FK)
- action_type (VARCHAR)
- created_at (TIMESTAMP)
- metadata (JSON)

인덱스: (user_id), (created_at), (action_type, created_at)

현재 쿼리 (느림):
SELECT user_id, COUNT(*)
FROM user_logs
WHERE created_at >= '2024-01-01'
AND action_type = 'purchase'
GROUP BY user_id
HAVING COUNT(*) > 5

실행시간: 45초
        """,
        expected_elements=["인덱스 활용 전략", "쿼리 리팩토링", "파티셔닝 고려", "실행계획 분석"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="SQL-009",
        category="sql_query",
        subcategory="gap_analysis",
        scenario="연속성 분석 쿼리",
        industry="구독",
        data_description="구독 이력 갭 분석",
        raw_data="""
테이블: subscriptions
- sub_id (PK)
- user_id (FK)
- start_date (DATE)
- end_date (DATE)
- plan_type (VARCHAR)

요구사항:
1. 구독 갭(중단 기간)이 있는 사용자 식별
2. 갭 기간 계산
3. 재구독까지 평균 기간
        """,
        expected_elements=["LAG/LEAD로 갭 탐지", "날짜 연산", "갭 기간 계산", "통계 집계"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="SQL-010",
        category="sql_query",
        subcategory="funnel",
        scenario="퍼널 분석 쿼리",
        industry="이커머스",
        data_description="구매 퍼널 전환율 쿼리",
        raw_data="""
테이블: user_events
- event_id (PK)
- user_id (FK)
- event_type (VARCHAR): 'view', 'add_cart', 'checkout', 'purchase'
- product_id (FK)
- event_time (TIMESTAMP)
- session_id (VARCHAR)

요구사항:
세션 기준 단계별 전환율 계산
- 상품조회 → 장바구니 → 결제시도 → 구매완료
        """,
        expected_elements=["세션별 그룹화", "단계별 카운트", "전환율 계산", "시간 조건 처리"],
        difficulty="medium"
    ),
]


# =============================================================================
# 5. 통계 분석 (statistics) - 10개
# =============================================================================
STATISTICS_TEST_CASES = [
    DataAnalysisTestCase(
        id="STAT-001",
        category="statistics",
        subcategory="hypothesis",
        scenario="두 그룹 평균 비교 검정",
        industry="제약",
        data_description="신약 vs 위약 효과 비교 데이터",
        raw_data="""
그룹, 샘플수, 평균효과, 표준편차
신약군, 150, 23.5, 8.2
위약군, 148, 18.2, 7.8

유의수준: 0.05
        """,
        expected_elements=["적합한 검정 방법 선택", "귀무가설/대립가설 설정", "검정통계량 해석", "결론 도출"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="STAT-002",
        category="statistics",
        subcategory="correlation",
        scenario="변수 간 상관관계 분석",
        industry="부동산",
        data_description="아파트 가격 영향 요인 데이터",
        raw_data="""
변수, 가격과_상관계수, p-value
면적, 0.82, <0.001
역거리, -0.65, <0.001
층수, 0.23, 0.042
건축연도, -0.31, 0.008
학군등급, 0.58, <0.001
        """,
        expected_elements=["상관관계 강도 해석", "유의성 판단", "다중공선성 검토", "인과관계 주의사항"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="STAT-003",
        category="statistics",
        subcategory="regression",
        scenario="회귀분석 결과 해석",
        industry="마케팅",
        data_description="광고비와 매출 회귀분석 결과",
        raw_data="""
회귀분석 결과:
- 종속변수: 월매출(백만원)
- R-squared: 0.76
- Adjusted R-squared: 0.74

변수, 계수, 표준오차, t-value, p-value
상수, 120.5, 25.3, 4.76, <0.001
TV광고비, 2.35, 0.42, 5.60, <0.001
온라인광고비, 1.82, 0.38, 4.79, <0.001
프로모션비, 0.95, 0.51, 1.86, 0.068
        """,
        expected_elements=["모델 적합도 해석", "계수 의미 설명", "유의성 판단", "예측 활용 방안"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="STAT-004",
        category="statistics",
        subcategory="chi_square",
        scenario="범주형 변수 독립성 검정",
        industry="HR",
        data_description="성별과 승진 여부 교차표",
        raw_data="""
교차표:
        승진O  승진X  합계
남성     45     85    130
여성     28     72    100
합계     73    157    230

카이제곱 통계량: 1.24
자유도: 1
p-value: 0.265
        """,
        expected_elements=["검정 방법 설명", "기대빈도 계산", "결과 해석", "실무적 함의"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="STAT-005",
        category="statistics",
        subcategory="sample_size",
        scenario="표본 크기 산정",
        industry="리서치",
        data_description="설문조사 표본 크기 결정",
        raw_data="""
조건:
- 모집단: 50,000명
- 신뢰수준: 95%
- 허용오차: ±3%
- 예상 비율: 50% (최대 변동)

질문: 필요한 최소 표본 크기는?
        """,
        expected_elements=["표본크기 공식 적용", "계산 과정 설명", "실무적 조정 사항", "비용-정확도 트레이드오프"],
        difficulty="easy"
    ),
    DataAnalysisTestCase(
        id="STAT-006",
        category="statistics",
        subcategory="anova",
        scenario="다중 그룹 비교 분석",
        industry="교육",
        data_description="교수법별 학습 효과 비교",
        raw_data="""
교수법, 학생수, 평균점수, 표준편차
전통강의, 45, 72.3, 12.5
토론식, 42, 78.5, 10.8
프로젝트, 48, 81.2, 11.2
온라인, 40, 74.8, 14.2

ANOVA 결과:
F-statistic: 5.82
p-value: 0.001
        """,
        expected_elements=["ANOVA 해석", "사후검정 필요성", "그룹간 차이 분석", "실무 권고"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="STAT-007",
        category="statistics",
        subcategory="time_series",
        scenario="시계열 분해 분석",
        industry="리테일",
        data_description="월별 매출 시계열 분해 결과",
        raw_data="""
분해 결과 (3년치 월별 데이터):
- 추세(Trend): 연 8% 상승
- 계절성(Seasonal): 12월 +35%, 2월 -20%
- 잔차(Residual): 표준편차 5%

계절성 지수:
1월: 0.92, 2월: 0.80, 3월: 0.95, 4월: 1.02
5월: 1.05, 6월: 0.98, 7월: 1.08, 8월: 1.12
9월: 0.95, 10월: 1.00, 11월: 1.08, 12월: 1.35
        """,
        expected_elements=["분해 요소 해석", "계절성 패턴 설명", "예측 모델 제안", "비즈니스 활용"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="STAT-008",
        category="statistics",
        subcategory="power",
        scenario="검정력 분석",
        industry="임상",
        data_description="임상시험 검정력 계산",
        raw_data="""
계획된 임상시험:
- 예상 효과 크기 (Cohen's d): 0.5
- 유의수준 (alpha): 0.05
- 목표 검정력 (1-beta): 0.80
- 검정 유형: 양측 검정

현재 계획된 샘플:
- 실험군: 50명
- 대조군: 50명
        """,
        expected_elements=["검정력 계산", "필요 샘플 크기", "효과 크기 영향", "비용 고려"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="STAT-009",
        category="statistics",
        subcategory="survival",
        scenario="생존 분석 해석",
        industry="SaaS",
        data_description="고객 이탈 생존 분석 결과",
        raw_data="""
Kaplan-Meier 생존 분석 결과:

기간(월), 생존율(전체), 생존율(프리미엄), 생존율(기본)
1, 85%, 92%, 78%
3, 68%, 82%, 55%
6, 52%, 71%, 35%
12, 38%, 58%, 22%

Log-rank test p-value: 0.001
Hazard Ratio (프리미엄 vs 기본): 0.45
        """,
        expected_elements=["생존 곡선 해석", "그룹 간 비교", "Hazard Ratio 설명", "비즈니스 함의"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="STAT-010",
        category="statistics",
        subcategory="bayesian",
        scenario="베이지안 추론 해석",
        industry="마케팅",
        data_description="전환율 베이지안 분석 결과",
        raw_data="""
A/B 테스트 베이지안 분석:

사전 분포: Beta(1, 1) - 균등 분포
데이터:
- A안: 1000명 중 32명 전환 (3.2%)
- B안: 1000명 중 45명 전환 (4.5%)

사후 분포:
- A안: Beta(33, 969), 평균 3.3%, 95% CI [2.3%, 4.5%]
- B안: Beta(46, 956), 평균 4.6%, 95% CI [3.4%, 6.0%]

P(B > A) = 94.2%
        """,
        expected_elements=["사전/사후 분포 설명", "신용구간 해석", "빈도주의와 비교", "의사결정 기준"],
        difficulty="hard"
    ),
]


# =============================================================================
# 6. 대시보드 설계 (dashboard) - 10개
# =============================================================================
DASHBOARD_TEST_CASES = [
    DataAnalysisTestCase(
        id="DASH-001",
        category="dashboard",
        subcategory="executive",
        scenario="CEO 대시보드 설계",
        industry="스타트업",
        data_description="경영진용 핵심 KPI 대시보드",
        raw_data="""
필요 KPI:
- MRR (월간 반복 매출)
- ARR (연간 반복 매출)
- Churn Rate (이탈률)
- CAC (고객 획득 비용)
- LTV (고객 생애 가치)
- Runway (남은 자금 기간)
- NRR (순수익 유지율)

대시보드 요구사항:
- 한 눈에 회사 건강상태 파악
- 투자자 미팅에 활용 가능
- 월간/분기별 트렌드 확인
        """,
        expected_elements=["KPI 우선순위화", "레이아웃 설계", "차트 유형 선정", "알림/임계값 설정"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="DASH-002",
        category="dashboard",
        subcategory="operations",
        scenario="실시간 운영 대시보드",
        industry="이커머스",
        data_description="CS팀 실시간 모니터링 대시보드",
        raw_data="""
모니터링 지표:
- 실시간 주문 건수
- 결제 성공/실패율
- CS 문의 인입량
- 평균 응답 시간
- 배송 현황 (준비/배송중/완료)
- 재고 부족 상품 수

갱신 주기: 5분
사용자: CS팀 10명
        """,
        expected_elements=["실시간 갱신 설계", "이상 상황 알림", "드릴다운 구조", "모바일 대응"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="DASH-003",
        category="dashboard",
        subcategory="marketing",
        scenario="마케팅 성과 대시보드",
        industry="D2C브랜드",
        data_description="퍼포먼스 마케팅 성과 추적",
        raw_data="""
채널별 지표:
- 노출수, 클릭수, CTR
- CPC, CPM, CPA
- 전환수, 전환율
- ROAS, ROI
- 신규/재방문 비율

채널: 구글, 메타, 네이버, 카카오, 틱톡
기간: 일별/주별/월별 비교
        """,
        expected_elements=["채널 비교 뷰", "기간별 트렌드", "예산 대비 성과", "자동 리포트 기능"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="DASH-004",
        category="dashboard",
        subcategory="product",
        scenario="제품 분석 대시보드",
        industry="모바일앱",
        data_description="앱 사용성 분석 대시보드",
        raw_data="""
핵심 지표:
- DAU/WAU/MAU
- 세션당 체류시간
- 기능별 사용률
- 퍼널 전환율
- 크래시율
- 앱 평점 추이

세그먼트: OS, 버전, 가입경로, 사용자등급
        """,
        expected_elements=["핵심 지표 배치", "세그먼트 필터", "코호트 분석 뷰", "A/B 테스트 연동"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="DASH-005",
        category="dashboard",
        subcategory="finance",
        scenario="재무 대시보드 설계",
        industry="중소기업",
        data_description="월간 재무 현황 대시보드",
        raw_data="""
재무 지표:
- 매출액, 매출원가, 매출총이익
- 판관비, 영업이익
- 현금흐름 (영업/투자/재무)
- 미수금, 미지급금
- 부채비율, 유동비율

비교 기준: 전월, 전년동기, 예산
        """,
        expected_elements=["재무제표 요약 뷰", "현금흐름 시각화", "예산 대비 분석", "경고 지표 설정"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="DASH-006",
        category="dashboard",
        subcategory="sales",
        scenario="영업팀 대시보드",
        industry="B2B SaaS",
        data_description="영업 파이프라인 대시보드",
        raw_data="""
파이프라인 단계:
- 리드(Lead): 건수, 금액
- 기회(Opportunity): 건수, 금액, 전환율
- 제안(Proposal): 건수, 금액
- 협상(Negotiation): 건수, 금액
- 성사(Won): 건수, 금액, 승률

영업사원별, 업종별, 기간별 필터 필요
        """,
        expected_elements=["파이프라인 시각화", "예측 매출 표시", "목표 대비 현황", "개인별 성과"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="DASH-007",
        category="dashboard",
        subcategory="hr",
        scenario="HR 분석 대시보드",
        industry="대기업",
        data_description="인사 지표 종합 대시보드",
        raw_data="""
인사 지표:
- 총 인원, 부서별 분포
- 이직률 (자발적/비자발적)
- 평균 근속연수
- 채용 현황 (TO/지원/합격)
- 교육 이수율
- 직원 만족도 (eNPS)

세분화: 부서, 직급, 입사연차
        """,
        expected_elements=["인력 현황 요약", "이직 분석 뷰", "채용 퍼널", "트렌드 비교"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="DASH-008",
        category="dashboard",
        subcategory="customer_success",
        scenario="CS 대시보드",
        industry="SaaS",
        data_description="고객 성공 지표 대시보드",
        raw_data="""
핵심 지표:
- 고객 건강 점수 분포
- NRR (순수익유지율)
- 확장 MRR vs 이탈 MRR
- 온보딩 완료율
- 기능 채택률
- NPS/CSAT 추이

위험 신호:
- 사용량 급감 고객
- 티켓 급증 고객
- 계약 만료 임박 고객
        """,
        expected_elements=["건강 점수 시각화", "위험 고객 리스트", "확장 기회 식별", "CSM 할당 뷰"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="DASH-009",
        category="dashboard",
        subcategory="supply_chain",
        scenario="공급망 대시보드",
        industry="제조",
        data_description="공급망 모니터링 대시보드",
        raw_data="""
모니터링 지표:
- 재고 수준 (원자재/재공품/완제품)
- 공급업체별 리드타임
- 주문 이행률
- 물류비용
- 품질 불량률

위험 지표:
- 재고 부족 예상 품목
- 지연 배송 건
- 품질 이슈 발생 공급사
        """,
        expected_elements=["재고 현황 지도", "공급망 흐름도", "알림 우선순위", "예측 분석 연동"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="DASH-010",
        category="dashboard",
        subcategory="embedded",
        scenario="고객용 임베디드 대시보드",
        industry="B2B 플랫폼",
        data_description="고객사 제공용 분석 대시보드",
        raw_data="""
제공 지표:
- 사용량 통계
- 비용 분석
- 성과 벤치마크 (업계 평균 대비)
- ROI 계산

요구사항:
- 화이트 라벨링 (브랜드 커스텀)
- 권한별 뷰 제한
- 데이터 내보내기
- 모바일 최적화
        """,
        expected_elements=["멀티테넌트 구조", "권한 설계", "커스터마이징 옵션", "임베딩 방식"],
        difficulty="hard"
    ),
]


# =============================================================================
# 7. A/B 테스트 (ab_test) - 10개
# =============================================================================
AB_TEST_CASES = [
    DataAnalysisTestCase(
        id="AB-001",
        category="ab_test",
        subcategory="design",
        scenario="A/B 테스트 설계",
        industry="이커머스",
        data_description="결제 페이지 개선 테스트 설계",
        raw_data="""
현재 상황:
- 일 방문자: 50,000명
- 현재 결제 전환율: 3.2%
- 목표 개선율: 10% 상대적 향상 (3.2% → 3.52%)

테스트 기간: 최대 2주
비즈니스 제약: 매출 손실 최소화 필요
        """,
        expected_elements=["표본 크기 계산", "테스트 기간 산정", "트래픽 분배 전략", "중단 기준 설정"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="AB-002",
        category="ab_test",
        subcategory="analysis",
        scenario="A/B 테스트 결과 분석",
        industry="SaaS",
        data_description="온보딩 플로우 테스트 결과",
        raw_data="""
테스트 결과:
버전, 사용자수, 온보딩완료, 전환율, 유료전환
A(기존), 12500, 4875, 39.0%, 312 (6.4%)
B(신규), 12500, 5250, 42.0%, 357 (6.8%)

테스트 기간: 14일
신뢰수준: 95%
        """,
        expected_elements=["통계적 유의성 검정", "효과 크기 계산", "신뢰구간 산출", "의사결정 권고"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="AB-003",
        category="ab_test",
        subcategory="multivariate",
        scenario="다변량 테스트 분석",
        industry="미디어",
        data_description="뉴스레터 제목/이미지 조합 테스트",
        raw_data="""
테스트 조합 (2x2):
조합, 발송수, 오픈, 오픈율, 클릭, 클릭율
A1(기존제목+기존이미지), 25000, 5500, 22.0%, 825, 15.0%
A2(기존제목+신규이미지), 25000, 5750, 23.0%, 920, 16.0%
B1(신규제목+기존이미지), 25000, 6250, 25.0%, 875, 14.0%
B2(신규제목+신규이미지), 25000, 6500, 26.0%, 1040, 16.0%
        """,
        expected_elements=["주효과 분석", "교호작용 분석", "최적 조합 도출", "추가 테스트 제안"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="AB-004",
        category="ab_test",
        subcategory="segment",
        scenario="세그먼트별 테스트 분석",
        industry="핀테크",
        data_description="UI 변경 테스트 세그먼트 분석",
        raw_data="""
전체 결과: B안 +5% 전환율 향상 (유의함)

세그먼트별 결과:
세그먼트, A전환율, B전환율, 차이, 유의성
신규유저, 8.2%, 10.5%, +2.3%p, 유의함
기존유저, 15.1%, 14.8%, -0.3%p, 유의하지않음
모바일, 9.5%, 12.1%, +2.6%p, 유의함
PC, 12.8%, 11.9%, -0.9%p, 유의하지않음
        """,
        expected_elements=["심슨 패러독스 검토", "세그먼트별 영향 분석", "롤아웃 전략 제안", "추가 분석 권고"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="AB-005",
        category="ab_test",
        subcategory="bayesian",
        scenario="베이지안 A/B 테스트 해석",
        industry="게임",
        data_description="인앱 구매 테스트 베이지안 분석 결과",
        raw_data="""
테스트: 상점 UI 변경
기간: 7일

베이지안 분석 결과:
- B가 A보다 나을 확률: 94.2%
- 예상 개선율: +8.5% (95% CI: +2.1% ~ +15.2%)
- 예상 손실 (B 선택시): 0.3%
- 예상 손실 (A 유지시): 2.8%

현재 샘플: A=8,500, B=8,200
        """,
        expected_elements=["베이지안 결과 해석", "빈도주의와 차이 설명", "의사결정 기준", "조기 종료 판단"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="AB-006",
        category="ab_test",
        subcategory="guardrail",
        scenario="가드레일 메트릭 분석",
        industry="검색엔진",
        data_description="검색 알고리즘 테스트 가드레일 분석",
        raw_data="""
주요 메트릭 (개선 목표):
지표, A, B, 변화, 유의성
클릭률, 32.5%, 34.2%, +5.2%, 유의함
검색당매출, 0.85$, 0.92$, +8.2%, 유의함

가드레일 메트릭 (유지 목표):
지표, A, B, 변화, 유의성
페이지로딩, 1.2초, 1.8초, +50%, 유의함 (악화)
0결과율, 2.1%, 2.3%, +9.5%, 유의하지않음
사용자불만, 0.5%, 0.8%, +60%, 유의함 (악화)
        """,
        expected_elements=["가드레일 위반 판단", "트레이드오프 분석", "의사결정 프레임워크", "조건부 롤아웃"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="AB-007",
        category="ab_test",
        subcategory="sequential",
        scenario="순차 분석 테스트",
        industry="OTT",
        data_description="추천 알고리즘 순차 테스트",
        raw_data="""
순차 테스트 결과 (일별 누적):
일차, 누적샘플, A전환율, B전환율, 중단경계도달
1, 5000, 8.2%, 9.1%, 미도달
3, 15000, 8.0%, 9.3%, 미도달
5, 25000, 8.1%, 9.2%, 미도달
7, 35000, 8.0%, 9.4%, B우위 경계도달
10, 50000, 8.1%, 9.3%, B우위 확정

설계 파라미터:
- Alpha spending: O'Brien-Fleming
- 총 중간분석: 5회
- 최종 유의수준: 0.05
        """,
        expected_elements=["순차 분석 원리 설명", "중단 경계 해석", "Type I 에러 통제", "조기 종료 권고"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="AB-008",
        category="ab_test",
        subcategory="ratio_metric",
        scenario="비율 메트릭 분석",
        industry="광고",
        data_description="광고 CTR 테스트 분석",
        raw_data="""
테스트: 광고 크리에이티브 변경
- 메트릭: 클릭률 (CTR = 클릭수 / 노출수)

결과:
버전, 노출수, 클릭수, CTR
A, 1,000,000, 15,000, 1.50%
B, 1,200,000, 19,200, 1.60%

주의: 노출수가 다름 (트래픽 할당 불균형)
        """,
        expected_elements=["비율 메트릭 분석법", "분산 추정 방법", "Delta Method 적용", "불균형 처리"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="AB-009",
        category="ab_test",
        subcategory="novelty",
        scenario="신규성 효과 분석",
        industry="소셜미디어",
        data_description="UI 변경 신규성 효과 검증",
        raw_data="""
테스트: 피드 알고리즘 UI 변경

기간별 결과:
기간, A체류시간, B체류시간, 차이
1주차, 25분, 32분, +28%
2주차, 25분, 30분, +20%
3주차, 26분, 28분, +8%
4주차, 25분, 26분, +4%

질문: 실제 개선인가, 신규성 효과인가?
        """,
        expected_elements=["신규성 효과 식별", "시간별 추세 분석", "장기 영향 추정", "실험 설계 개선"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="AB-010",
        category="ab_test",
        subcategory="network",
        scenario="네트워크 효과 테스트",
        industry="메신저",
        data_description="기능 변경의 네트워크 효과 분석",
        raw_data="""
테스트: 그룹채팅 기능 개선

일반 분석 결과:
버전, 사용자, 그룹생성, 메시지수
A, 50000, 2500, 125000
B, 50000, 3200, 168000
개선: 그룹생성 +28%, 메시지 +34%

네트워크 효과 고려:
- B그룹 사용자가 A그룹 사용자와 상호작용
- A그룹 사용자의 메시지 수도 증가
- 실험군 오염 가능성
        """,
        expected_elements=["네트워크 효과 식별", "SUTVA 위반 분석", "클러스터 기반 실험", "효과 크기 보정"],
        difficulty="hard"
    ),
]


# =============================================================================
# 8. ML 결과 해석 (ml_interpretation) - 10개
# =============================================================================
ML_INTERPRETATION_TEST_CASES = [
    DataAnalysisTestCase(
        id="ML-001",
        category="ml_interpretation",
        subcategory="classification",
        scenario="분류 모델 성능 해석",
        industry="금융",
        data_description="대출 연체 예측 모델 평가",
        raw_data="""
모델: XGBoost 이진 분류
테스트셋: 10,000건 (연체 8%, 정상 92%)

혼동행렬:
              예측정상  예측연체
실제정상       8,850     350
실제연체         180     620

지표:
- Accuracy: 94.7%
- Precision: 63.9%
- Recall: 77.5%
- F1-Score: 70.1%
- AUC-ROC: 0.89
        """,
        expected_elements=["지표별 의미 해석", "불균형 데이터 고려", "임계값 조정 제안", "비즈니스 영향 분석"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="ML-002",
        category="ml_interpretation",
        subcategory="feature_importance",
        scenario="피처 중요도 분석",
        industry="이커머스",
        data_description="구매 예측 모델 피처 분석",
        raw_data="""
모델: Random Forest
타겟: 30일 내 구매 여부

피처 중요도 (Top 10):
피처, 중요도, 타입
최근방문일수, 0.185, 행동
총구매금액, 0.142, 거래
방문빈도, 0.128, 행동
장바구니상품수, 0.095, 행동
가입기간, 0.082, 기본
평균주문금액, 0.075, 거래
찜목록수, 0.068, 행동
쿠폰보유수, 0.055, 프로모션
리뷰작성수, 0.048, 참여
마지막구매일수, 0.045, 거래
        """,
        expected_elements=["중요도 해석", "피처 그룹별 분석", "액션 가능한 피처 식별", "추가 피처 제안"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="ML-003",
        category="ml_interpretation",
        subcategory="shap",
        scenario="SHAP 분석 결과 해석",
        industry="보험",
        data_description="보험료 예측 모델 SHAP 분석",
        raw_data="""
모델: Gradient Boosting Regressor
타겟: 연간 보험료

개별 예측 SHAP 값 (고객 A):
예측 보험료: 285만원 (기준값: 180만원)

피처, 값, SHAP기여도
나이, 58세, +45만원
BMI, 32.5, +28만원
흡연여부, Yes, +22만원
운동빈도, 1회/주, +8만원
가족력, No, -5만원
직업위험도, 낮음, -12만원
        """,
        expected_elements=["SHAP 값 의미 설명", "개별 예측 해석", "전체 패턴과 비교", "고객 설명 방안"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="ML-004",
        category="ml_interpretation",
        subcategory="model_comparison",
        scenario="모델 비교 분석",
        industry="리테일",
        data_description="수요 예측 모델 비교",
        raw_data="""
예측 대상: 주간 제품 판매량
테스트 기간: 12주

모델별 성능:
모델, MAE, RMSE, MAPE, 학습시간
Linear Regression, 245, 312, 18.5%, 2초
Random Forest, 198, 267, 14.2%, 45초
XGBoost, 185, 251, 13.1%, 38초
LSTM, 172, 238, 11.8%, 15분
Prophet, 210, 285, 15.8%, 30초

운영 환경:
- 예측 주기: 매일
- 제품 수: 5,000개
- 응답 시간 제약: 5분 이내
        """,
        expected_elements=["성능 지표 비교", "복잡도-성능 트레이드오프", "운영 환경 고려", "최종 모델 추천"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="ML-005",
        category="ml_interpretation",
        subcategory="error_analysis",
        scenario="모델 오류 분석",
        industry="물류",
        data_description="배송 시간 예측 오류 분석",
        raw_data="""
모델: 배송 소요시간 예측 (시간 단위)
전체 MAE: 2.8시간

오류 분석 (상위 오차 케이스):
조건, 케이스수, 평균오차, 과대/과소
우천시, 1,200, 5.2시간, 과소예측
주말배송, 2,500, 4.1시간, 과소예측
도서산간, 800, 6.8시간, 과소예측
새벽배송, 1,500, 3.5시간, 과대예측
당일배송, 3,200, 1.2시간, 정확

피처 현황: 날씨 정보 미포함
        """,
        expected_elements=["오류 패턴 분석", "개선 우선순위", "피처 엔지니어링 제안", "모델 개선 방향"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="ML-006",
        category="ml_interpretation",
        subcategory="calibration",
        scenario="확률 보정 분석",
        industry="마케팅",
        data_description="전환 예측 모델 확률 보정",
        raw_data="""
모델: 전환 확률 예측
예측 확률 vs 실제 전환율:

예측구간, 샘플수, 예측평균, 실제전환율
0-10%, 45000, 5.2%, 4.8%
10-20%, 28000, 14.8%, 12.5%
20-30%, 15000, 24.5%, 18.2%
30-40%, 8500, 34.2%, 25.8%
40-50%, 5200, 44.8%, 32.5%
50%+, 3800, 62.5%, 45.2%

Brier Score: 0.18
Expected Calibration Error: 0.12
        """,
        expected_elements=["보정 곡선 해석", "과신/과소신 진단", "보정 방법 제안", "비즈니스 영향"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="ML-007",
        category="ml_interpretation",
        subcategory="fairness",
        scenario="모델 공정성 분석",
        industry="HR",
        data_description="채용 추천 모델 공정성 검토",
        raw_data="""
모델: 서류 합격 예측

그룹별 성능:
그룹, 샘플수, 합격예측률, 실제합격률, TPR, FPR
남성, 5000, 35%, 32%, 0.78, 0.15
여성, 3500, 28%, 30%, 0.65, 0.12
수도권, 6000, 38%, 35%, 0.82, 0.18
비수도권, 2500, 22%, 25%, 0.58, 0.10

공정성 메트릭:
- Demographic Parity Diff: 0.07
- Equalized Odds Diff: 0.13
- Predictive Parity Diff: 0.05
        """,
        expected_elements=["공정성 지표 해석", "편향 원인 분석", "완화 전략 제안", "법적/윤리적 고려"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="ML-008",
        category="ml_interpretation",
        subcategory="drift",
        scenario="모델 드리프트 분석",
        industry="신용평가",
        data_description="신용 점수 모델 성능 저하 분석",
        raw_data="""
모델: 연체 예측 (12개월 전 배포)

월별 성능 추이:
월, AUC, Precision, Recall, PSI
배포시, 0.85, 0.72, 0.68, 0.00
+3개월, 0.84, 0.70, 0.67, 0.02
+6개월, 0.82, 0.65, 0.64, 0.08
+9개월, 0.78, 0.58, 0.60, 0.15
+12개월, 0.72, 0.48, 0.55, 0.25

피처 드리프트 (PSI):
소득, 0.32 (높음)
부채비율, 0.18 (중간)
고용기간, 0.08 (낮음)
        """,
        expected_elements=["드리프트 유형 진단", "원인 분석", "재학습 기준 설정", "모니터링 전략"],
        difficulty="hard"
    ),
    DataAnalysisTestCase(
        id="ML-009",
        category="ml_interpretation",
        subcategory="ensemble",
        scenario="앙상블 모델 분석",
        industry="주식",
        data_description="주가 방향 예측 앙상블 분석",
        raw_data="""
앙상블 구성:
모델, 개별정확도, 앙상블기여도
LSTM, 58.2%, 0.35
XGBoost, 56.8%, 0.30
Random Forest, 55.5%, 0.20
Logistic Reg, 54.2%, 0.15

앙상블 정확도: 61.5%
개별 최고 대비: +3.3%p

모델 간 상관관계:
LSTM-XGB: 0.72
LSTM-RF: 0.65
XGB-RF: 0.81
        """,
        expected_elements=["앙상블 효과 분석", "다양성 평가", "가중치 최적화", "모델 조합 제안"],
        difficulty="medium"
    ),
    DataAnalysisTestCase(
        id="ML-010",
        category="ml_interpretation",
        subcategory="clustering",
        scenario="클러스터링 결과 해석",
        industry="마케팅",
        data_description="고객 세그먼테이션 클러스터 분석",
        raw_data="""
알고리즘: K-Means (k=5)
평가지표: Silhouette Score = 0.42

클러스터 프로파일:
클러스터, 고객수, RFM평균, 특성
0, 12500, R:15,F:8,M:120k, 고가치-활성
1, 28000, R:45,F:2,M:35k, 중간-휴면위험
2, 8500, R:5,F:12,M:250k, VIP-충성
3, 35000, R:90,F:1,M:15k, 저가치-이탈
4, 16000, R:30,F:4,M:65k, 성장가능

클러스터 간 거리:
0-2: 가까움 (0.8)
3-4: 중간 (1.5)
1-3: 멂 (2.8)
        """,
        expected_elements=["클러스터 특성 해석", "비즈니스 네이밍", "타겟팅 전략 제안", "클러스터 품질 평가"],
        difficulty="medium"
    ),
]


# =============================================================================
# 통합 함수
# =============================================================================
def get_all_data_analysis_test_cases() -> List[DataAnalysisTestCase]:
    """모든 테스트 케이스 반환 (80개)"""
    all_cases = []
    all_cases.extend(INTERPRETATION_TEST_CASES)
    all_cases.extend(INSIGHT_TEST_CASES)
    all_cases.extend(VISUALIZATION_TEST_CASES)
    all_cases.extend(SQL_QUERY_TEST_CASES)
    all_cases.extend(STATISTICS_TEST_CASES)
    all_cases.extend(DASHBOARD_TEST_CASES)
    all_cases.extend(AB_TEST_CASES)
    all_cases.extend(ML_INTERPRETATION_TEST_CASES)
    return all_cases


def get_test_cases_by_category(category: str) -> List[DataAnalysisTestCase]:
    """카테고리별 테스트 케이스 반환"""
    category_map = {
        "interpretation": INTERPRETATION_TEST_CASES,
        "insight": INSIGHT_TEST_CASES,
        "visualization": VISUALIZATION_TEST_CASES,
        "sql_query": SQL_QUERY_TEST_CASES,
        "statistics": STATISTICS_TEST_CASES,
        "dashboard": DASHBOARD_TEST_CASES,
        "ab_test": AB_TEST_CASES,
        "ml_interpretation": ML_INTERPRETATION_TEST_CASES,
    }
    return category_map.get(category, [])


# 하위 호환성을 위한 개별 함수
def get_interpretation_test_cases() -> List[DataAnalysisTestCase]:
    return INTERPRETATION_TEST_CASES

def get_insight_test_cases() -> List[DataAnalysisTestCase]:
    return INSIGHT_TEST_CASES

def get_visualization_test_cases() -> List[DataAnalysisTestCase]:
    return VISUALIZATION_TEST_CASES

def get_sql_query_test_cases() -> List[DataAnalysisTestCase]:
    return SQL_QUERY_TEST_CASES

def get_statistics_test_cases() -> List[DataAnalysisTestCase]:
    return STATISTICS_TEST_CASES

def get_dashboard_test_cases() -> List[DataAnalysisTestCase]:
    return DASHBOARD_TEST_CASES

def get_ab_test_test_cases() -> List[DataAnalysisTestCase]:
    return AB_TEST_CASES

def get_ml_interpretation_test_cases() -> List[DataAnalysisTestCase]:
    return ML_INTERPRETATION_TEST_CASES
