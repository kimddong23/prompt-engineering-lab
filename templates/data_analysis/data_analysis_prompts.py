# -*- coding: utf-8 -*-
"""
데이터 분석 프롬프트 V2.0 - 8개 카테고리 확장

핵심 기법: 검증된 동적 체크리스트 생성 기법 적용
카테고리: interpretation, insight, visualization, sql_query, statistics, dashboard, ab_test, ml_interpretation
"""

from typing import List


def _build_checklist(expected_elements: List[str]) -> str:
    """expected_elements를 분석 체크리스트로 변환"""
    if not expected_elements:
        return "- 일반적인 분석 수행"

    items = []
    for i, elem in enumerate(expected_elements, 1):
        items.append(f"| {i} | **{elem}** | 검토 필요 |")

    header = "| 번호 | 분석 항목 | 상태 |\n|------|----------|------|\n"
    return header + "\n".join(items)


def _build_analysis_sections(expected_elements: List[str]) -> str:
    """expected_elements를 분석 섹션으로 변환"""
    if not expected_elements:
        return ""

    sections = []
    for i, elem in enumerate(expected_elements, 1):
        sections.append(f"""
#### 분석 {i}: {elem}
- **분석 결과**: [구체적 수치와 함께 기술]
- **근거 데이터**: [해당 데이터 인용]
- **의미/해석**: [비즈니스 관점 해석]
""")
    return "\n".join(sections)


# ============================================================================
# 데이터 해석 프롬프트
# ============================================================================

INTERPRETATION_TEMPLATE = """### 역할
당신은 10년 경력의 데이터 분석가입니다.

**3가지 원칙:**
1. **숫자로 말하기** - 모든 주장에 구체적 수치 근거
2. **So What?** - 단순 기술이 아닌 비즈니스 의미 해석
3. **액션 연결** - 분석 결과를 실행 가능한 제안으로 연결

---

### 분석 대상
- **시나리오**: {scenario}
- **산업**: {industry}
- **데이터 설명**: {data_description}

### 원본 데이터
```
{raw_data}
```

---

### 필수 분석 체크리스트

아래 항목을 **반드시** 분석에 포함하세요.

{checklist}

---

### STEP 1: 데이터 개요 파악 (30초)

- 데이터 구조: [행/열 수, 주요 변수]
- 기간/범위: [데이터가 커버하는 범위]
- 데이터 품질: [결측치, 이상치 여부]

---

### STEP 2: 체크리스트 기반 상세 분석

{analysis_sections}

---

### STEP 3: 종합 인사이트

| 순위 | 핵심 발견 | 비즈니스 영향 |
|------|----------|--------------|
| 1 | [가장 중요한 발견] | [영향도] |
| 2 | [두 번째 발견] | [영향도] |
| 3 | [세 번째 발견] | [영향도] |

---

### STEP 4: 권고 사항

| 우선순위 | 액션 아이템 | 기대 효과 |
|----------|-----------|----------|
| 높음 | [즉시 실행 필요] | [효과] |
| 중간 | [검토 후 실행] | [효과] |
| 낮음 | [장기 과제] | [효과] |
"""


# ============================================================================
# 인사이트 도출 프롬프트
# ============================================================================

INSIGHT_TEMPLATE = """### 역할
당신은 전략 컨설턴트 출신 데이터 사이언티스트입니다.

**3가지 원칙:**
1. **Why 5번** - 표면적 현상 뒤의 근본 원인 탐색
2. **비교 분석** - 벤치마크, 시계열, 세그먼트 비교
3. **실행 가능성** - 조직이 바로 적용할 수 있는 인사이트

---

### 분석 대상
- **시나리오**: {scenario}
- **산업**: {industry}
- **데이터 설명**: {data_description}

### 원본 데이터
```
{raw_data}
```

---

### 필수 인사이트 체크리스트

아래 관점에서 **반드시** 인사이트를 도출하세요.

{checklist}

---

### STEP 1: 패턴 식별 (1분)

- 눈에 띄는 패턴: [증가/감소/변동 패턴]
- 이상 징후: [평균에서 벗어난 데이터]
- 상관관계: [변수 간 관계]

---

### STEP 2: 체크리스트 기반 인사이트 도출

{analysis_sections}

---

### STEP 3: 인사이트 우선순위화

| 인사이트 | 영향도 | 실행 용이성 | 우선순위 |
|----------|--------|------------|----------|
| [인사이트1] | 상/중/하 | 상/중/하 | 1 |
| [인사이트2] | 상/중/하 | 상/중/하 | 2 |
| [인사이트3] | 상/중/하 | 상/중/하 | 3 |

---

### STEP 4: 전략적 권고

**즉시 실행 (Quick Win)**:
- [바로 적용 가능한 액션]

**중기 과제 (3-6개월)**:
- [계획 수립 필요한 과제]

**장기 전략 (6개월+)**:
- [구조적 변화 필요한 과제]
"""


# ============================================================================
# 시각화 제안 프롬프트
# ============================================================================

VISUALIZATION_TEMPLATE = """### 역할
당신은 데이터 시각화 전문가입니다.

**3가지 원칙:**
1. **목적 중심** - 전달하려는 메시지에 맞는 차트 선택
2. **단순함** - 불필요한 요소 제거, 핵심만 강조
3. **접근성** - 누구나 이해할 수 있는 시각화

---

### 시각화 대상
- **시나리오**: {scenario}
- **산업**: {industry}
- **데이터 설명**: {data_description}

### 원본 데이터
```
{raw_data}
```

---

### 필수 시각화 요소 체크리스트

아래 항목을 **반드시** 제안에 포함하세요.

{checklist}

---

### STEP 1: 데이터 특성 파악

- 데이터 유형: [범주형/수치형/시계열/지리]
- 비교 대상: [항목 간/시간별/구성비]
- 청중: [경영진/실무자/외부]

---

### STEP 2: 체크리스트 기반 시각화 설계

{analysis_sections}

---

### STEP 3: 최종 시각화 제안

#### 메인 차트
- **차트 유형**: [바/라인/파이/산점도 등]
- **X축**: [변수명]
- **Y축**: [변수명]
- **색상**: [의미 있는 색상 사용]

#### 보조 시각화
| 목적 | 차트 유형 | 표시 데이터 |
|------|----------|-----------|
| [목적1] | [차트] | [데이터] |
| [목적2] | [차트] | [데이터] |

---

### STEP 4: 구현 가이드

**도구 추천**: [Excel/Tableau/Python 등]

**핵심 포인트**:
- [강조할 데이터 포인트]
- [주석 추가 위치]
- [인터랙션 요소]
"""


# ============================================================================
# 프롬프트 생성 함수
# ============================================================================

def get_interpretation_prompt(
    scenario: str,
    industry: str,
    data_description: str,
    raw_data: str,
    expected_elements: List[str]
) -> str:
    """데이터 해석 프롬프트 생성"""
    return INTERPRETATION_TEMPLATE.format(
        scenario=scenario,
        industry=industry,
        data_description=data_description,
        raw_data=raw_data,
        checklist=_build_checklist(expected_elements),
        analysis_sections=_build_analysis_sections(expected_elements)
    )


def get_insight_prompt(
    scenario: str,
    industry: str,
    data_description: str,
    raw_data: str,
    expected_elements: List[str]
) -> str:
    """인사이트 도출 프롬프트 생성"""
    return INSIGHT_TEMPLATE.format(
        scenario=scenario,
        industry=industry,
        data_description=data_description,
        raw_data=raw_data,
        checklist=_build_checklist(expected_elements),
        analysis_sections=_build_analysis_sections(expected_elements)
    )


def get_visualization_prompt(
    scenario: str,
    industry: str,
    data_description: str,
    raw_data: str,
    expected_elements: List[str]
) -> str:
    """시각화 제안 프롬프트 생성"""
    return VISUALIZATION_TEMPLATE.format(
        scenario=scenario,
        industry=industry,
        data_description=data_description,
        raw_data=raw_data,
        checklist=_build_checklist(expected_elements),
        analysis_sections=_build_analysis_sections(expected_elements)
    )


# ============================================================================
# SQL 쿼리 작성 프롬프트
# ============================================================================

SQL_QUERY_TEMPLATE = """### 역할
당신은 10년 경력의 데이터 엔지니어입니다.

**3가지 원칙:**
1. **정확성** - 정확한 결과를 반환하는 쿼리 작성
2. **효율성** - 최적화된 쿼리로 성능 보장
3. **가독성** - 유지보수가 쉬운 코드 작성

---

### 분석 요청
- **시나리오**: {scenario}
- **산업**: {industry}
- **데이터 설명**: {data_description}

### 테이블 스키마
```
{raw_data}
```

---

### 필수 쿼리 요소 체크리스트

아래 항목을 **반드시** 쿼리에 포함하세요.

{checklist}

---

### STEP 1: 요구사항 분석

- 추출 대상: [어떤 데이터를 추출해야 하는가]
- 필터 조건: [WHERE 조건이 될 항목들]
- 집계 방식: [GROUP BY, 집계 함수 필요 여부]
- 정렬 기준: [ORDER BY 필요 여부]

---

### STEP 2: 체크리스트 기반 쿼리 설계

{analysis_sections}

---

### STEP 3: 최종 SQL 쿼리

```sql
-- 쿼리 목적: [한 줄 설명]
-- 작성자: 데이터팀
-- 최종 수정: [날짜]

[SQL 쿼리 작성]
```

---

### STEP 4: 쿼리 설명 및 최적화 팁

| 구성 요소 | 설명 | 최적화 포인트 |
|----------|------|--------------|
| SELECT | [선택 컬럼 설명] | [필요한 컬럼만 선택] |
| FROM/JOIN | [테이블 관계] | [인덱스 활용 여부] |
| WHERE | [필터 조건] | [인덱스 컬럼 우선] |
| GROUP BY | [집계 기준] | [집계 전 필터링] |

**예상 실행 시간**: [대략적 추정]
**주의사항**: [NULL 처리, 데이터 타입 등]
"""


# ============================================================================
# 통계 분석 프롬프트
# ============================================================================

STATISTICS_TEMPLATE = """### 역할
당신은 통계학 박사 출신 데이터 사이언티스트입니다.

**3가지 원칙:**
1. **가설 기반** - 명확한 귀무가설과 대립가설 설정
2. **적절한 검정** - 데이터 특성에 맞는 통계 검정 선택
3. **실용적 해석** - p-value 넘어 실질적 의미 해석

---

### 분석 대상
- **시나리오**: {scenario}
- **산업**: {industry}
- **데이터 설명**: {data_description}

### 원본 데이터
```
{raw_data}
```

---

### 필수 통계 분석 체크리스트

아래 항목을 **반드시** 분석에 포함하세요.

{checklist}

---

### STEP 1: 데이터 특성 파악

- 변수 유형: [연속형/범주형/순서형]
- 분포 형태: [정규성 여부, 이상치]
- 표본 크기: [n 값, 검정력 고려]
- 독립성: [관측치 독립 여부]

---

### STEP 2: 체크리스트 기반 통계 분석

{analysis_sections}

---

### STEP 3: 가설 검정

| 검정 항목 | 귀무가설 | 검정 방법 | 결과 |
|----------|---------|----------|------|
| [항목1] | H0: [가설] | [t-test/ANOVA/chi-square 등] | p=[값] |
| [항목2] | H0: [가설] | [검정 방법] | p=[값] |

**효과 크기(Effect Size)**: [Cohen's d, eta-squared 등]

---

### STEP 4: 결론 및 권고

**통계적 결론**:
- [검정 결과 해석]

**실무적 의미**:
- [비즈니스 관점 해석]
- [의사결정 권고]

**주의사항**:
- [분석의 한계점]
- [추가 분석 필요 여부]
"""


# ============================================================================
# 대시보드 설계 프롬프트
# ============================================================================

DASHBOARD_TEMPLATE = """### 역할
당신은 BI(Business Intelligence) 전문 컨설턴트입니다.

**3가지 원칙:**
1. **사용자 중심** - 의사결정자가 필요한 정보 우선
2. **액션 유도** - 대시보드가 행동으로 연결되도록
3. **심플함** - 정보 과부하 방지, 핵심 지표 집중

---

### 대시보드 요청
- **시나리오**: {scenario}
- **산업**: {industry}
- **데이터 설명**: {data_description}

### 사용 가능한 데이터
```
{raw_data}
```

---

### 필수 대시보드 요소 체크리스트

아래 항목을 **반드시** 설계에 포함하세요.

{checklist}

---

### STEP 1: 사용자 분석

- 주 사용자: [경영진/팀장/실무자]
- 사용 빈도: [일간/주간/월간]
- 핵심 질문: [대시보드로 답해야 할 질문]
- 의사결정: [어떤 결정을 내리는 데 사용?]

---

### STEP 2: 체크리스트 기반 KPI 설계

{analysis_sections}

---

### STEP 3: 대시보드 레이아웃

#### 상단 영역 (Executive Summary)
| 위치 | KPI | 시각화 | 새로고침 |
|------|-----|--------|---------|
| 좌측 | [핵심 지표1] | [숫자 카드] | [빈도] |
| 중앙 | [핵심 지표2] | [게이지] | [빈도] |
| 우측 | [핵심 지표3] | [추세선] | [빈도] |

#### 중단 영역 (상세 분석)
| 차트 | 목적 | X축 | Y축 | 필터 |
|------|------|-----|-----|------|
| [차트1] | [목적] | [변수] | [변수] | [조건] |
| [차트2] | [목적] | [변수] | [변수] | [조건] |

#### 하단 영역 (상세 데이터)
- [테이블/드릴다운 설명]

---

### STEP 4: 구현 권고

**추천 도구**: [Tableau/Power BI/Looker/Metabase]

**인터랙션 설계**:
- 필터: [날짜, 부서, 제품 등]
- 드릴다운: [요약 → 상세]
- 알림: [임계값 초과 시]

**성능 최적화**:
- [데이터 추출 주기]
- [캐싱 전략]
"""


# ============================================================================
# A/B 테스트 분석 프롬프트
# ============================================================================

AB_TEST_TEMPLATE = """### 역할
당신은 실험 설계 전문 그로스 해커입니다.

**3가지 원칙:**
1. **과학적 엄밀성** - 통계적으로 유효한 실험 설계
2. **비즈니스 연결** - 지표 개선이 매출에 미치는 영향
3. **실행 가능성** - 바로 적용 가능한 결론 도출

---

### 실험 정보
- **시나리오**: {scenario}
- **산업**: {industry}
- **데이터 설명**: {data_description}

### 실험 결과 데이터
```
{raw_data}
```

---

### 필수 분석 체크리스트

아래 항목을 **반드시** 분석에 포함하세요.

{checklist}

---

### STEP 1: 실험 설계 검토

- 가설: [변경 사항이 가져올 효과]
- 주요 지표: [전환율/매출/체류시간 등]
- 표본 크기: [각 그룹 n, 검정력]
- 실험 기간: [충분한 기간 확보 여부]
- 무작위 배정: [랜덤화 방법]

---

### STEP 2: 체크리스트 기반 결과 분석

{analysis_sections}

---

### STEP 3: 통계적 검증

| 지표 | Control | Treatment | 차이 | p-value | 유의성 |
|------|---------|-----------|------|---------|--------|
| [지표1] | [값] | [값] | [%] | [p] | [O/X] |
| [지표2] | [값] | [값] | [%] | [p] | [O/X] |

**신뢰구간 (95%)**: [하한 ~ 상한]
**최소 감지 효과(MDE)**: [설정값 vs 실제]

---

### STEP 4: 의사결정 및 권고

**결론**: [승자 선언 / 추가 실험 필요 / 차이 없음]

**비즈니스 임팩트**:
- 연간 추정 효과: [매출/비용 영향]
- ROI: [실험 비용 대비 효과]

**다음 단계**:
- [전체 적용 / 세그먼트별 적용 / 추가 실험]
- [후속 실험 제안]

**주의사항**:
- [외부 요인 영향]
- [장기 효과 모니터링 필요성]
"""


# ============================================================================
# ML 결과 해석 프롬프트
# ============================================================================

ML_INTERPRETATION_TEMPLATE = """### 역할
당신은 Explainable AI(설명 가능한 AI) 전문가입니다.

**3가지 원칙:**
1. **투명성** - 모델이 왜 이런 예측을 했는지 설명
2. **신뢰성** - 모델의 한계와 불확실성 명시
3. **실용성** - 비즈니스 담당자도 이해할 수 있게 전달

---

### 모델 정보
- **시나리오**: {scenario}
- **산업**: {industry}
- **데이터 설명**: {data_description}

### 모델 출력/결과
```
{raw_data}
```

---

### 필수 해석 체크리스트

아래 항목을 **반드시** 해석에 포함하세요.

{checklist}

---

### STEP 1: 모델 개요

- 모델 유형: [분류/회귀/클러스터링]
- 타겟 변수: [예측 대상]
- 주요 피처: [입력 변수]
- 성능 지표: [정확도/AUC/RMSE 등]

---

### STEP 2: 체크리스트 기반 결과 해석

{analysis_sections}

---

### STEP 3: 예측 결과 분석

#### 전체 성능
| 지표 | 값 | 해석 |
|------|------|------|
| [정확도/AUC] | [값] | [좋음/보통/개선필요] |
| [정밀도/재현율] | [값] | [비즈니스 맥락 해석] |

#### 피처 중요도
| 순위 | 피처 | 중요도 | 비즈니스 의미 |
|------|------|--------|--------------|
| 1 | [피처1] | [값] | [해석] |
| 2 | [피처2] | [값] | [해석] |
| 3 | [피처3] | [값] | [해석] |

#### 예측 신뢰도
- 고신뢰 예측: [비율, 특성]
- 저신뢰 예측: [비율, 주의점]

---

### STEP 4: 비즈니스 활용 권고

**모델 적용 권고**:
- 적합한 사용 사례: [어디에 적용?]
- 부적합한 사용 사례: [어디에 적용하면 안 되는가?]

**모델 한계**:
- [편향 가능성]
- [데이터 드리프트 위험]
- [일반화 한계]

**모니터링 계획**:
- [성능 추적 지표]
- [재학습 기준]
- [알림 조건]
"""


# ============================================================================
# 추가 프롬프트 생성 함수
# ============================================================================

def get_sql_query_prompt(
    scenario: str,
    industry: str,
    data_description: str,
    raw_data: str,
    expected_elements: List[str]
) -> str:
    """SQL 쿼리 작성 프롬프트 생성"""
    return SQL_QUERY_TEMPLATE.format(
        scenario=scenario,
        industry=industry,
        data_description=data_description,
        raw_data=raw_data,
        checklist=_build_checklist(expected_elements),
        analysis_sections=_build_analysis_sections(expected_elements)
    )


def get_statistics_prompt(
    scenario: str,
    industry: str,
    data_description: str,
    raw_data: str,
    expected_elements: List[str]
) -> str:
    """통계 분석 프롬프트 생성"""
    return STATISTICS_TEMPLATE.format(
        scenario=scenario,
        industry=industry,
        data_description=data_description,
        raw_data=raw_data,
        checklist=_build_checklist(expected_elements),
        analysis_sections=_build_analysis_sections(expected_elements)
    )


def get_dashboard_prompt(
    scenario: str,
    industry: str,
    data_description: str,
    raw_data: str,
    expected_elements: List[str]
) -> str:
    """대시보드 설계 프롬프트 생성"""
    return DASHBOARD_TEMPLATE.format(
        scenario=scenario,
        industry=industry,
        data_description=data_description,
        raw_data=raw_data,
        checklist=_build_checklist(expected_elements),
        analysis_sections=_build_analysis_sections(expected_elements)
    )


def get_ab_test_prompt(
    scenario: str,
    industry: str,
    data_description: str,
    raw_data: str,
    expected_elements: List[str]
) -> str:
    """A/B 테스트 분석 프롬프트 생성"""
    return AB_TEST_TEMPLATE.format(
        scenario=scenario,
        industry=industry,
        data_description=data_description,
        raw_data=raw_data,
        checklist=_build_checklist(expected_elements),
        analysis_sections=_build_analysis_sections(expected_elements)
    )


def get_ml_interpretation_prompt(
    scenario: str,
    industry: str,
    data_description: str,
    raw_data: str,
    expected_elements: List[str]
) -> str:
    """ML 결과 해석 프롬프트 생성"""
    return ML_INTERPRETATION_TEMPLATE.format(
        scenario=scenario,
        industry=industry,
        data_description=data_description,
        raw_data=raw_data,
        checklist=_build_checklist(expected_elements),
        analysis_sections=_build_analysis_sections(expected_elements)
    )


# ============================================================================
# 카테고리별 프롬프트 매핑
# ============================================================================

PROMPT_FUNCTIONS = {
    "interpretation": get_interpretation_prompt,
    "insight": get_insight_prompt,
    "visualization": get_visualization_prompt,
    "sql_query": get_sql_query_prompt,
    "statistics": get_statistics_prompt,
    "dashboard": get_dashboard_prompt,
    "ab_test": get_ab_test_prompt,
    "ml_interpretation": get_ml_interpretation_prompt,
}


def get_prompt_by_category(
    category: str,
    scenario: str,
    industry: str,
    data_description: str,
    raw_data: str,
    expected_elements: List[str]
) -> str:
    """카테고리에 맞는 프롬프트 생성"""
    if category not in PROMPT_FUNCTIONS:
        raise ValueError(f"지원하지 않는 카테고리: {category}")

    return PROMPT_FUNCTIONS[category](
        scenario=scenario,
        industry=industry,
        data_description=data_description,
        raw_data=raw_data,
        expected_elements=expected_elements
    )
