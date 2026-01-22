# -*- coding: utf-8 -*-
"""
================================================================================
비즈니스 프롬프트 V4.0 - 동적 체크리스트 생성
================================================================================

## V4.0 핵심 개선사항

### 1. 동적 체크리스트 생성 (Dynamic Checklist Generation)
- expected_elements를 분석 체크리스트로 직접 변환
- LLM이 각 항목을 반드시 검토하도록 강제
- 취업 V4.0, 개발자 V2.0에서 검증된 기법 적용

### 2. 5단계 누적 Chain-of-Thought
- STEP 1: 상황 분석 (30초)
- STEP 2: 체크리스트 기반 설계
- STEP 3: 초안 작성
- STEP 4: 요소 검증 (모든 체크리스트 확인)
- STEP 5: 최종 출력

### 3. 강제 요소 포함 검증
- 각 expected_element에 대해 "포함 여부: [예/아니오]" 명시
- 미포함 시 반드시 수정하도록 지시

## 이전 버전 대비 개선
- V2.0 이메일: 7.96/10 → 목표 9.5+
- V3.0 보고서: 8.17/10 → 목표 9.5+

================================================================================
"""

from typing import List, Optional


# ============================================================================
# 공통 헬퍼 함수
# ============================================================================

def _build_element_checklist(expected_elements: List[str]) -> str:
    """expected_elements를 분석 체크리스트로 변환"""
    if not expected_elements:
        return "- 일반적인 문서 품질 검토"

    checklist_items = []
    for i, element in enumerate(expected_elements, 1):
        checklist_items.append(f"| {i} | **{element}** | 검토 필요 |")

    header = "| 번호 | 필수 요소 | 상태 |\n|------|----------|------|\n"
    return header + "\n".join(checklist_items)


def _build_element_sections(expected_elements: List[str]) -> str:
    """expected_elements를 분석 섹션으로 변환"""
    if not expected_elements:
        return ""

    sections = []
    for i, element in enumerate(expected_elements, 1):
        sections.append(f"""
#### 요소 {i}: {element}
- **포함 여부**: [예/아니오]
- **포함 위치**: [섹션명 또는 문장]
- **구체적 내용**: [어떻게 반영되었는지]
""")
    return "\n".join(sections)


def _build_verification_section(expected_elements: List[str]) -> str:
    """최종 검증 섹션 생성"""
    if not expected_elements:
        return ""

    items = []
    for i, element in enumerate(expected_elements, 1):
        items.append(f"| {i} | {element} | [O/X] | [해당 부분 인용] |")

    header = """
### 최종 검증 체크리스트

| 번호 | 필수 요소 | 포함 | 해당 부분 |
|------|----------|------|----------|
"""
    return header + "\n".join(items)


# ============================================================================
# V4.0 이메일 프롬프트 템플릿
# ============================================================================

EMAIL_V4_TEMPLATE = """### 역할 및 원칙

당신은 비즈니스 커뮤니케이션 전문가입니다.

**3가지 핵심 원칙:**
1. **"3초 룰"** - 받는 사람이 3초 안에 목적을 파악해야 함
2. **"So What?"** - 모든 문장에 "그래서 뭘 해달라는 건데?"가 답이 있어야 함
3. **"하나의 이메일, 하나의 목적"** - 여러 용건을 섞지 않음

---

### 상황 정보

{context_info}

---

### 필수 요소 체크리스트

아래 체크리스트의 **모든 항목**을 반드시 이메일에 포함해야 합니다.

{element_checklist}

---

### STEP 1: 상황 분석 (30초)

다음 질문에 답하세요:
1. 수신자가 이 이메일을 읽고 **가장 먼저 알고 싶은 것**은?
2. 수신자가 **해야 할 행동**은 무엇인가?
3. 수신자의 **시간적 여유**는? (바쁜 임원 vs 담당자)

---

### STEP 2: 체크리스트 기반 설계

각 필수 요소를 어떻게 이메일에 반영할지 설계하세요:

{element_sections}

---

### STEP 3: 이메일 초안 작성

다음 구조로 작성하세요:

```
제목: [한 줄로 핵심 파악 가능하게]

[호칭],

[첫 문장: 목적을 바로 밝힘]

[본문: 필수 요소들을 자연스럽게 포함]

[마무리: 원하는 행동 + 기한]

[서명]
```

---

### STEP 4: 요소 검증

작성한 이메일에서 각 필수 요소가 포함되었는지 확인하세요:

{verification_section}

**중요**: 모든 항목이 [O]여야 합니다. [X]인 항목이 있으면 STEP 3으로 돌아가 수정하세요.

---

### STEP 5: 최종 이메일 출력

위 검증을 통과한 최종 이메일을 출력하세요.
"""


# ============================================================================
# V4.0 보고서 프롬프트 템플릿
# ============================================================================

REPORT_V4_TEMPLATE = """### 역할 및 원칙

당신은 비즈니스 보고서 작성 전문가입니다.

**3가지 핵심 원칙:**
1. **피라미드 원칙** - 결론 먼저, 근거 나중
2. **숫자로 말하기** - "열심히 했다" 대신 "목표 대비 110% 달성"
3. **액션 중심** - 모든 이슈에 해결책, 모든 보고에 다음 단계

---

### 보고서 정보

{context_info}

---

### 필수 요소 체크리스트

아래 체크리스트의 **모든 항목**을 반드시 보고서에 포함해야 합니다.

{element_checklist}

---

### STEP 1: 한 문장 요약 (10초)

이 보고서의 핵심을 한 문장으로:
> "[핵심 성과/결론], 단 [주의 사항]에 대한 [조치 필요]"

---

### STEP 2: 체크리스트 기반 구조 설계

각 필수 요소를 어떻게 보고서에 반영할지 설계하세요:

{element_sections}

---

### STEP 3: 보고서 초안 작성

다음 구조로 작성하세요:

```
# [보고서 제목]

**작성자**: [이름] | **부서**: [부서명] | **일자**: [날짜]

---

## Executive Summary

| 항목 | 내용 |
|------|------|
| **핵심 결론** | [가장 중요한 포인트] |
| **주요 성과** | [숫자로 표현] |
| **요청 사항** | [의사결정/지원 필요 시] |

---

## [필수 요소 1에 해당하는 섹션]

[상세 내용]

## [필수 요소 2에 해당하는 섹션]

[상세 내용]

...

## 다음 단계

| 항목 | 담당 | 기한 |
|------|------|------|
| [액션 아이템] | [담당자] | [일자] |
```

---

### STEP 4: 요소 검증

작성한 보고서에서 각 필수 요소가 포함되었는지 확인하세요:

{verification_section}

**중요**: 모든 항목이 [O]여야 합니다. [X]인 항목이 있으면 STEP 3으로 돌아가 수정하세요.

---

### STEP 5: 최종 보고서 출력

위 검증을 통과한 최종 보고서를 출력하세요.
"""


# ============================================================================
# 이메일 프롬프트 생성 함수
# ============================================================================

def get_formal_email_prompt_v4(
    sender_info: str,
    recipient_info: str,
    email_purpose: str,
    main_content: str,
    expected_elements: List[str],
    desired_action: str = "",
    additional_context: str = ""
) -> str:
    """
    공식 업무 이메일 프롬프트 V4.0 생성

    핵심 개선: expected_elements를 동적 체크리스트로 변환
    """
    context_info = f"""- **발신자**: {sender_info}
- **수신자**: {recipient_info}
- **이메일 목적**: {email_purpose}
- **전달 내용**: {main_content}
- **원하는 행동**: {desired_action}
- **추가 맥락**: {additional_context}"""

    return EMAIL_V4_TEMPLATE.format(
        context_info=context_info,
        element_checklist=_build_element_checklist(expected_elements),
        element_sections=_build_element_sections(expected_elements),
        verification_section=_build_verification_section(expected_elements)
    )


def get_apology_email_prompt_v4(
    sender_info: str,
    recipient_info: str,
    incident_description: str,
    expected_elements: List[str],
    cause_analysis: str = "",
    corrective_action: str = ""
) -> str:
    """
    사과/해명 이메일 프롬프트 V4.0 생성
    """
    context_info = f"""- **발신자**: {sender_info}
- **수신자**: {recipient_info}
- **이메일 유형**: 사과/해명 이메일
- **사건 설명**: {incident_description}
- **원인 분석**: {cause_analysis}
- **시정 조치**: {corrective_action}"""

    return EMAIL_V4_TEMPLATE.format(
        context_info=context_info,
        element_checklist=_build_element_checklist(expected_elements),
        element_sections=_build_element_sections(expected_elements),
        verification_section=_build_verification_section(expected_elements)
    )


def get_proposal_email_prompt_v4(
    sender_info: str,
    recipient_info: str,
    proposal_summary: str,
    expected_elements: List[str],
    benefits: str = "",
    call_to_action: str = ""
) -> str:
    """
    제안/협력 요청 이메일 프롬프트 V4.0 생성
    """
    context_info = f"""- **발신자**: {sender_info}
- **수신자**: {recipient_info}
- **이메일 유형**: 제안/협력 요청
- **제안 요약**: {proposal_summary}
- **기대 효과**: {benefits}
- **요청 행동**: {call_to_action}"""

    return EMAIL_V4_TEMPLATE.format(
        context_info=context_info,
        element_checklist=_build_element_checklist(expected_elements),
        element_sections=_build_element_sections(expected_elements),
        verification_section=_build_verification_section(expected_elements)
    )


def get_follow_up_email_prompt_v4(
    sender_info: str,
    recipient_info: str,
    previous_context: str,
    expected_elements: List[str],
    follow_up_purpose: str = "",
    next_steps: str = ""
) -> str:
    """
    후속 조치 이메일 프롬프트 V4.0 생성
    """
    context_info = f"""- **발신자**: {sender_info}
- **수신자**: {recipient_info}
- **이메일 유형**: 후속 조치
- **이전 맥락**: {previous_context}
- **후속 목적**: {follow_up_purpose}
- **다음 단계**: {next_steps}"""

    return EMAIL_V4_TEMPLATE.format(
        context_info=context_info,
        element_checklist=_build_element_checklist(expected_elements),
        element_sections=_build_element_sections(expected_elements),
        verification_section=_build_verification_section(expected_elements)
    )


# ============================================================================
# 보고서 프롬프트 생성 함수
# ============================================================================

def get_weekly_report_prompt_v4(
    reporter_info: str,
    period: str,
    achievements: str,
    expected_elements: List[str],
    issues: str = "",
    next_plans: str = ""
) -> str:
    """
    주간/월간 보고서 프롬프트 V4.0 생성

    핵심 개선: expected_elements를 동적 체크리스트로 변환
    """
    context_info = f"""- **보고자**: {reporter_info}
- **보고 기간**: {period}
- **주요 성과**: {achievements}
- **이슈 사항**: {issues}
- **다음 계획**: {next_plans}"""

    return REPORT_V4_TEMPLATE.format(
        context_info=context_info,
        element_checklist=_build_element_checklist(expected_elements),
        element_sections=_build_element_sections(expected_elements),
        verification_section=_build_verification_section(expected_elements)
    )


def get_analysis_report_prompt_v4(
    analyst_info: str,
    analysis_subject: str,
    data_summary: str,
    expected_elements: List[str],
    methodology: str = "",
    findings: str = ""
) -> str:
    """
    분석 보고서 프롬프트 V4.0 생성
    """
    context_info = f"""- **분석자**: {analyst_info}
- **분석 대상**: {analysis_subject}
- **데이터 요약**: {data_summary}
- **분석 방법**: {methodology}
- **주요 발견**: {findings}"""

    return REPORT_V4_TEMPLATE.format(
        context_info=context_info,
        element_checklist=_build_element_checklist(expected_elements),
        element_sections=_build_element_sections(expected_elements),
        verification_section=_build_verification_section(expected_elements)
    )


def get_meeting_minutes_prompt_v4(
    recorder_info: str,
    meeting_info: str,
    attendees: str,
    expected_elements: List[str],
    agenda: str = "",
    discussions: str = ""
) -> str:
    """
    회의록 프롬프트 V4.0 생성
    """
    context_info = f"""- **작성자**: {recorder_info}
- **회의 정보**: {meeting_info}
- **참석자**: {attendees}
- **안건**: {agenda}
- **논의 내용**: {discussions}"""

    return REPORT_V4_TEMPLATE.format(
        context_info=context_info,
        element_checklist=_build_element_checklist(expected_elements),
        element_sections=_build_element_sections(expected_elements),
        verification_section=_build_verification_section(expected_elements)
    )


def get_project_proposal_prompt_v4(
    proposer_info: str,
    project_name: str,
    project_summary: str,
    expected_elements: List[str],
    objectives: str = "",
    resources: str = ""
) -> str:
    """
    프로젝트 기획서 프롬프트 V4.0 생성
    """
    context_info = f"""- **제안자**: {proposer_info}
- **프로젝트명**: {project_name}
- **프로젝트 개요**: {project_summary}
- **목표**: {objectives}
- **필요 자원**: {resources}"""

    return REPORT_V4_TEMPLATE.format(
        context_info=context_info,
        element_checklist=_build_element_checklist(expected_elements),
        element_sections=_build_element_sections(expected_elements),
        verification_section=_build_verification_section(expected_elements)
    )
