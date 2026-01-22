# -*- coding: utf-8 -*-
"""
데이터 분석 프롬프트 V1.0 - 동적 체크리스트 적용

핵심 기법: 검증된 동적 체크리스트 생성 기법을 처음부터 적용
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
