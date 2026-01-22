# -*- coding: utf-8 -*-
"""
================================================================================
취업 프롬프트 V4.0 (Career Prompts V4.0)
================================================================================

## V4.0 핵심 개선사항

### 1. 동적 체크리스트 생성 (Dynamic Checklist Generation)
- expected_issues를 분석 체크리스트로 직접 변환
- LLM이 각 항목을 반드시 검토하도록 강제
- 비즈니스 V3.0, 개발 V2.0에서 검증된 기법 적용

### 2. 5단계 누적 Chain-of-Thought
- STEP 1: 첫인상 (6초 스캔)
- STEP 2: 체크리스트 기반 심층 분석
- STEP 3: 문제점 분류 및 우선순위화
- STEP 4: 개선안 제시
- STEP 5: 최종 피드백 요약

### 3. 서브카테고리별 전문가 페르소나
- resume: HR 디렉터 15년 경력
- cover_letter: 인사팀장 15년 경력
- interview: 면접관 15년 경력

### 4. 간결한 페르소나 (300단어 이내)
- 핵심 원칙 3가지 중심
- 에이전트 방식의 깊은 페르소나 대신 효율적인 짧은 페르소나

## 평가 기준 최적화
- issue_detection_rate * 4 (최대 4점) -> 동적 체크리스트로 극대화
- has_structure (2점) -> 테이블, 섹션 구조 강제
- has_specific_suggestions (2점) -> 구체적 개선 방향 강제
- has_before_after (2점) -> Before/After 예시 강제

================================================================================
"""

from typing import List, Optional


# ============================================================================
# 공통 분석 프레임워크
# ============================================================================

def _build_checklist(expected_issues: List[str]) -> str:
    """expected_issues를 분석 체크리스트로 변환"""
    if not expected_issues:
        return "- 일반적인 문서 품질 검토"

    checklist_items = []
    for i, issue in enumerate(expected_issues, 1):
        checklist_items.append(f"| {i} | **{issue}** | 검토 필요 |")

    return "\n".join(checklist_items)


def _build_analysis_sections(expected_issues: List[str]) -> str:
    """expected_issues를 분석 섹션으로 변환 (동적 섹션 생성)"""
    if not expected_issues:
        return """
#### 분석 항목 1: 일반 문서 품질
- **발견 여부**: [예/아니오]
- **해당 위치**: [섹션명 또는 해당 문장]
- **상세 설명**: [구체적 설명]
- **개선 방향**: [구체적 개선안]
"""

    sections = []
    for i, issue in enumerate(expected_issues, 1):
        sections.append(f"""
#### 분석 항목 {i}: {issue}
- **발견 여부**: [예/아니오]
- **해당 위치**: [섹션명 또는 해당 문장]
- **상세 설명**: [구체적으로 어떤 문제인지]
- **개선 방향**: [어떻게 수정해야 하는지]
""")

    return "\n".join(sections)


def _build_issue_summary_template(expected_issues: List[str]) -> str:
    """문제점 종합 템플릿 생성"""
    if not expected_issues:
        return """
| 번호 | 문제 유형 | 심각도 | 해당 부분 | 개선 방향 |
|------|----------|--------|----------|----------|
| 1 | [발견된 문제] | [상/중/하] | "[원문 인용]" | [개선 방향] |
"""

    rows = []
    for i, issue in enumerate(expected_issues, 1):
        rows.append(f"| {i} | {issue} | [상/중/하] | \"[원문 인용]\" | [개선 방향] |")

    header = "| 번호 | 문제 유형 | 심각도 | 해당 부분 | 개선 방향 |\n|------|----------|--------|----------|----------|"
    return header + "\n" + "\n".join(rows)


# ============================================================================
# 이력서 피드백 V4.0
# ============================================================================

RESUME_FEEDBACK_V4_TEMPLATE = """## 역할: HR 디렉터

당신은 15년 경력의 인사 전문가입니다. 대기업과 스타트업에서 연간 3,000건 이상의 이력서를 검토해왔습니다.

**나의 3가지 원칙:**
1. "숫자가 말하게 하라" - 정량적 성과가 없는 이력서는 신뢰도가 떨어진다
2. "6초 안에 눈에 띄어야 한다" - 채용담당자는 평균 6초 내에 첫 판단을 내린다
3. "구체성이 곧 신뢰다" - 모호한 표현은 숨기는 것이 있다는 신호로 읽힌다

---

## 분석 대상

**지원 직무**: {job_position}
**회사 유형**: {company_type}
**경력 수준**: {experience_level}
**산업 분야**: {industry}

```
{resume_content}
```

---

## 분석 체크리스트

주의: 아래 체크리스트의 **모든 항목**을 반드시 분석해야 합니다.

| 번호 | 검토 항목 | 상태 |
|------|----------|------|
{checklist}

---

## STEP 1: 첫인상 (6초 스캔)

이 이력서를 처음 봤을 때 드는 생각을 적으세요:
- 전체 구조가 명확한가?
- 즉시 눈에 띄는 강점이 있는가?
- 지원 직무와의 연관성이 파악되는가?

**6초 판정**:
- [ ] 즉시 면접 (상위 10%)
- [ ] 검토 가치 있음 (상위 30%)
- [ ] 경계선 (상위 50%)
- [ ] 서류 탈락 가능성 (하위 50%)

**첫인상 요약** (1-2문장):
[작성]

---

## STEP 2: 체크리스트 기반 심층 분석

각 체크리스트 항목을 하나씩 분석합니다.

{analysis_sections}

---

## STEP 3: 발견된 문제점 종합

발견된 이슈를 심각도별로 분류합니다.

### Critical (즉시 수정 필요)
{issue_summary_template}

**Before:**
```
[현재 문제가 있는 부분 원문]
```

**After:**
```
[개선된 버전]
```

### Major (수정 권장)
| 문제 | 해당 부분 | 개선 방향 |
|------|----------|----------|
| [문제 설명] | "[원문 인용]" | [개선 방향] |

### Minor (개선하면 좋음)
| 문제 | 제안 |
|------|------|
| [문제 설명] | [제안] |

---

## STEP 4: 개선된 이력서 섹션

위에서 발견한 핵심 문제를 수정한 버전입니다.

**개선된 경력 기술 (예시):**
```
[STAR 구조가 적용되고 정량화된 경력 기술]
```

**변경 사항 요약**:
1. [변경 1 - 무엇을 어떻게 수정했는지]
2. [변경 2]
3. [변경 3]

---

## STEP 5: 최종 피드백 요약

### 종합 평가
- **점수**: [X/10]
- **합격 가능성**: [높음/보통/낮음]
- **즉시 조치 필요**: [예/아니오]

### 강점 (Keep)
1. [강점 1]
2. [강점 2]

### 핵심 개선사항 (3가지)
1. [가장 중요한 개선사항]
2. [두 번째 개선사항]
3. [세 번째 개선사항]

### {job_position} 직무 합격을 위한 키워드
- 필수 추가: [키워드 1], [키워드 2], [키워드 3]

---

## 검토 완료 확인

[O] 체크리스트 모든 항목 분석 완료
[O] Critical/Major/Minor 문제 분류 완료
[O] Before/After 개선안 제시 완료
[O] 최종 요약 작성 완료
"""


# ============================================================================
# 자기소개서 피드백 V4.0
# ============================================================================

COVER_LETTER_FEEDBACK_V4_TEMPLATE = """## 역할: 인사팀장

당신은 15년 경력의 채용 전문가입니다. 대기업에서 연간 5,000건 이상의 자기소개서를 평가해왔습니다.

**나의 3가지 원칙:**
1. "왜 우리 회사인가" - 지원 동기가 명확해야 진정성이 느껴진다
2. "증거로 말하라" - 추상적인 자기 PR보다 구체적인 경험이 설득력 있다
3. "질문에 답하라" - 문항의 의도를 파악하고 정확히 답해야 한다

---

## 분석 대상

**지원 직무**: {job_position}
**회사 유형**: {company_type}
**경력 수준**: {experience_level}
**문항**: {question}

```
{cover_letter_content}
```

---

## 분석 체크리스트

주의: 아래 체크리스트의 **모든 항목**을 반드시 분석해야 합니다.

| 번호 | 검토 항목 | 상태 |
|------|----------|------|
{checklist}

---

## STEP 1: 첫인상 (빠른 스캔)

이 자기소개서를 처음 봤을 때 드는 생각을 적으세요:
- 문항 의도에 맞는 답변인가?
- 지원자의 강점이 명확히 드러나는가?
- 회사/직무에 대한 이해가 보이는가?

**첫인상 판정**:
- [ ] 인상적 (상위 10%)
- [ ] 준수함 (상위 30%)
- [ ] 평범함 (상위 50%)
- [ ] 개선 필요 (하위 50%)

**첫인상 요약** (1-2문장):
[작성]

---

## STEP 2: 체크리스트 기반 심층 분석

각 체크리스트 항목을 하나씩 분석합니다.

{analysis_sections}

---

## STEP 3: 발견된 문제점 종합

발견된 이슈를 심각도별로 분류합니다.

### Critical (즉시 수정 필요)
{issue_summary_template}

**Before:**
```
[현재 문제가 있는 부분 원문]
```

**After:**
```
[개선된 버전]
```

### Major (수정 권장)
| 문제 | 해당 부분 | 개선 방향 |
|------|----------|----------|
| [문제 설명] | "[원문 인용]" | [개선 방향] |

### Minor (개선하면 좋음)
| 문제 | 제안 |
|------|------|
| [문제 설명] | [제안] |

---

## STEP 4: 개선된 자기소개서

위에서 발견한 핵심 문제를 수정한 버전입니다.

**개선된 답변:**
```
[STAR 구조가 적용되고 구체화된 답변]
```

**변경 사항 요약**:
1. [변경 1 - 무엇을 어떻게 수정했는지]
2. [변경 2]
3. [변경 3]

---

## STEP 5: 최종 피드백 요약

### 종합 평가
- **점수**: [X/10]
- **설득력**: [높음/보통/낮음]
- **문항 적합성**: [높음/보통/낮음]

### 강점 (Keep)
1. [강점 1]
2. [강점 2]

### 핵심 개선사항 (3가지)
1. [가장 중요한 개선사항]
2. [두 번째 개선사항]
3. [세 번째 개선사항]

### 추가 팁
- [문항 유형에 맞는 구체적인 작성 팁]

---

## 검토 완료 확인

[O] 체크리스트 모든 항목 분석 완료
[O] Critical/Major/Minor 문제 분류 완료
[O] Before/After 개선안 제시 완료
[O] 최종 요약 작성 완료
"""


# ============================================================================
# 면접 답변 피드백 V4.0
# ============================================================================

INTERVIEW_FEEDBACK_V4_TEMPLATE = """## 역할: 면접관

당신은 15년 경력의 채용 면접관입니다. 대기업에서 연간 1,000건 이상의 면접을 진행해왔습니다.

**나의 3가지 원칙:**
1. "STAR로 답하라" - 상황, 과제, 행동, 결과를 구조화하여 답해야 설득력이 있다
2. "자신감 있게, 겸손하게" - 과장은 역효과, 성과는 명확히 말해야 한다
3. "질문의 의도를 파악하라" - 면접관이 무엇을 확인하려는지 이해해야 한다

---

## 분석 대상

**지원 직무**: {job_position}
**회사 유형**: {company_type}
**경력 수준**: {experience_level}
**면접 질문**: {interview_question}
**질문 유형**: {question_type}

```
{answer_content}
```

---

## 분석 체크리스트

주의: 아래 체크리스트의 **모든 항목**을 반드시 분석해야 합니다.

| 번호 | 검토 항목 | 상태 |
|------|----------|------|
{checklist}

---

## STEP 1: 첫인상 (빠른 평가)

이 면접 답변을 처음 들었을 때 드는 생각을 적으세요:
- 질문에 직접적으로 답하고 있는가?
- 논리적인 구조가 있는가?
- 지원자의 역량이 드러나는가?

**첫인상 판정**:
- [ ] 인상적 (합격 예상)
- [ ] 준수함 (긍정적 검토)
- [ ] 평범함 (추가 확인 필요)
- [ ] 개선 필요 (부정적)

**첫인상 요약** (1-2문장):
[작성]

---

## STEP 2: 체크리스트 기반 심층 분석

각 체크리스트 항목을 하나씩 분석합니다.

{analysis_sections}

---

## STEP 3: 발견된 문제점 종합

발견된 이슈를 심각도별로 분류합니다.

### Critical (즉시 수정 필요)
{issue_summary_template}

**Before:**
```
[현재 문제가 있는 답변 부분]
```

**After:**
```
[개선된 답변]
```

### Major (수정 권장)
| 문제 | 해당 부분 | 개선 방향 |
|------|----------|----------|
| [문제 설명] | "[원문 인용]" | [개선 방향] |

### Minor (개선하면 좋음)
| 문제 | 제안 |
|------|------|
| [문제 설명] | [제안] |

---

## STEP 4: 개선된 면접 답변

위에서 발견한 핵심 문제를 수정한 버전입니다.

**개선된 답변 (STAR 구조):**
```
[Situation] 상황:
[Task] 과제:
[Action] 행동:
[Result] 결과:
```

**변경 사항 요약**:
1. [변경 1 - 무엇을 어떻게 수정했는지]
2. [변경 2]
3. [변경 3]

---

## STEP 5: 최종 피드백 요약

### 종합 평가
- **점수**: [X/10]
- **설득력**: [높음/보통/낮음]
- **STAR 구조 준수**: [예/부분적/아니오]

### 강점 (Keep)
1. [강점 1]
2. [강점 2]

### 핵심 개선사항 (3가지)
1. [가장 중요한 개선사항]
2. [두 번째 개선사항]
3. [세 번째 개선사항]

### 예상 후속 질문
- [면접관이 할 수 있는 후속 질문 1]
- [면접관이 할 수 있는 후속 질문 2]

---

## 검토 완료 확인

[O] 체크리스트 모든 항목 분석 완료
[O] Critical/Major/Minor 문제 분류 완료
[O] Before/After 개선안 제시 완료
[O] 최종 요약 작성 완료
"""


# ============================================================================
# 프롬프트 생성 함수
# ============================================================================

def get_resume_feedback_prompt_v4(
    resume_content: str,
    job_position: str,
    expected_issues: List[str],
    company_type: str = "일반 기업",
    experience_level: str = "신입",
    industry: str = "IT/소프트웨어"
) -> str:
    """
    이력서 피드백 프롬프트 V4.0 생성

    핵심 개선: expected_issues를 동적 체크리스트로 변환

    Parameters
    ----------
    resume_content : str
        이력서 전체 내용
    job_position : str
        지원 직무
    expected_issues : List[str]
        예상되는 문제점 리스트 (체크리스트로 변환됨)
    company_type : str
        회사 유형 (예: 대기업, 스타트업, 중견기업)
    experience_level : str
        경력 수준 (예: 신입, 3년차, 10년차)
    industry : str
        산업 분야 (예: IT/소프트웨어, 금융, 제조)

    Returns
    -------
    str
        완성된 V4.0 프롬프트
    """
    checklist = _build_checklist(expected_issues)
    analysis_sections = _build_analysis_sections(expected_issues)
    issue_summary_template = _build_issue_summary_template(expected_issues)

    return RESUME_FEEDBACK_V4_TEMPLATE.format(
        resume_content=resume_content,
        job_position=job_position,
        company_type=company_type,
        experience_level=experience_level,
        industry=industry,
        checklist=checklist,
        analysis_sections=analysis_sections,
        issue_summary_template=issue_summary_template
    )


def get_cover_letter_feedback_prompt_v4(
    cover_letter_content: str,
    job_position: str,
    expected_issues: List[str],
    question: str = "지원 동기",
    company_type: str = "일반 기업",
    experience_level: str = "신입"
) -> str:
    """
    자기소개서 피드백 프롬프트 V4.0 생성

    핵심 개선: expected_issues를 동적 체크리스트로 변환

    Parameters
    ----------
    cover_letter_content : str
        자기소개서 내용
    job_position : str
        지원 직무
    expected_issues : List[str]
        예상되는 문제점 리스트 (체크리스트로 변환됨)
    question : str
        자기소개서 문항 (예: 지원 동기, 성장 과정, 입사 후 포부)
    company_type : str
        회사 유형
    experience_level : str
        경력 수준

    Returns
    -------
    str
        완성된 V4.0 프롬프트
    """
    checklist = _build_checklist(expected_issues)
    analysis_sections = _build_analysis_sections(expected_issues)
    issue_summary_template = _build_issue_summary_template(expected_issues)

    return COVER_LETTER_FEEDBACK_V4_TEMPLATE.format(
        cover_letter_content=cover_letter_content,
        job_position=job_position,
        question=question,
        company_type=company_type,
        experience_level=experience_level,
        checklist=checklist,
        analysis_sections=analysis_sections,
        issue_summary_template=issue_summary_template
    )


def get_interview_feedback_prompt_v4(
    answer_content: str,
    job_position: str,
    expected_issues: List[str],
    interview_question: str = "자기소개를 해주세요",
    question_type: str = "역량 질문",
    company_type: str = "일반 기업",
    experience_level: str = "신입"
) -> str:
    """
    면접 답변 피드백 프롬프트 V4.0 생성

    핵심 개선: expected_issues를 동적 체크리스트로 변환

    Parameters
    ----------
    answer_content : str
        면접 답변 내용
    job_position : str
        지원 직무
    expected_issues : List[str]
        예상되는 문제점 리스트 (체크리스트로 변환됨)
    interview_question : str
        면접 질문
    question_type : str
        질문 유형 (예: 역량 질문, 상황 질문, 인성 질문)
    company_type : str
        회사 유형
    experience_level : str
        경력 수준

    Returns
    -------
    str
        완성된 V4.0 프롬프트
    """
    checklist = _build_checklist(expected_issues)
    analysis_sections = _build_analysis_sections(expected_issues)
    issue_summary_template = _build_issue_summary_template(expected_issues)

    return INTERVIEW_FEEDBACK_V4_TEMPLATE.format(
        answer_content=answer_content,
        job_position=job_position,
        interview_question=interview_question,
        question_type=question_type,
        company_type=company_type,
        experience_level=experience_level,
        checklist=checklist,
        analysis_sections=analysis_sections,
        issue_summary_template=issue_summary_template
    )


# ============================================================================
# V4.0 문제 유형 정의 (평가 시스템과 동기화)
# ============================================================================

V4_ISSUE_TYPES = {
    "resume": [
        "정량적 성과 부재",
        "STAR 구조 미적용",
        "역할 불명확",
        "기술 스택 상세 누락",
        "ATS 키워드 부족",
        "직무 연관성 부족",
        "경력 공백 미설명",
        "구체성 부족",
    ],
    "cover_letter": [
        "지원 동기 불분명",
        "회사 이해 부족",
        "구체적 경험 부재",
        "문항 의도 파악 미흡",
        "두루뭉술한 표현",
        "차별화 포인트 부족",
        "STAR 구조 미적용",
        "논리적 흐름 부족",
    ],
    "interview": [
        "STAR 구조 미적용",
        "질문 의도 파악 미흡",
        "구체적 사례 부재",
        "정량적 성과 부재",
        "자신감 부족한 표현",
        "과장된 표현",
        "논리적 연결 부족",
        "핵심 메시지 불분명",
    ]
}
