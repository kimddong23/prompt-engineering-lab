# -*- coding: utf-8 -*-
"""
================================================================================
비즈니스 보고서 프롬프트 V3.0 - 동적 섹션 생성
================================================================================

## V3.0 핵심 개선

### V2.0의 문제점
- expected_elements가 "필수 포함 요소"로만 나열됨
- 실제 출력 형식에는 일반적인 섹션만 있어서 LLM이 무시
- 결과: 요소 포함율 37.5%, 점수 6.08/10

### V3.0 해결책
1. **동적 섹션 생성**: expected_elements → 출력 섹션 제목으로 변환
2. **강제 포함 지시**: "다음 섹션들을 **반드시** 포함하세요"
3. **섹션별 작성 가이드**: 각 요소에 대한 구체적 지침 제공

================================================================================
"""

from typing import Dict, List, Optional


# ============================================================================
# V3.0 주간/월간 보고서 프롬프트 (동적 섹션)
# ============================================================================

WEEKLY_REPORT_V3_TEMPLATE = """### 역할
당신은 비즈니스 보고서 작성 전문가입니다.

### 3가지 원칙
1. **피라미드 원칙** - 결론 먼저, 근거 나중
2. **숫자로 말하기** - "열심히 했다" → "목표 대비 110% 달성"
3. **액션 중심** - 모든 이슈에 해결책, 모든 보고에 다음 단계

---

### 보고 정보
- **보고자**: {reporter_name}
- **부서**: {department}
- **보고 대상**: {report_to}
- **기간**: {period_start} ~ {period_end}
- **보고 주기**: {report_period}

### 업무 내용
{raw_content}

### 성과 데이터
{achievements}

### 이슈 사항
{issues}

### 다음 기간 계획
{next_plans}

---

### STEP 1: 한 문장 요약
> "이번 {report_period}을 한 문장으로 요약하면: [핵심 성과], 단 [주요 이슈]에 대한 [조치 필요]"

---

### STEP 2: 필수 섹션 확인

⚠️ **중요**: 아래 4개 섹션을 **반드시** 출력에 포함해야 합니다.

| 번호 | 섹션 제목 | 포함 내용 |
|------|-----------|-----------|
| 1 | **{expected_element_1}** | 해당 주제에 대한 상세 내용, 수치 포함 |
| 2 | **{expected_element_2}** | 해당 주제에 대한 상세 내용, 수치 포함 |
| 3 | **{expected_element_3}** | 해당 주제에 대한 상세 내용, 수치 포함 |
| 4 | **{expected_element_4}** | 해당 주제에 대한 상세 내용, 수치 포함 |

---

### STEP 3: 보고서 작성

다음 형식으로 작성하세요:

# {report_period} 업무 보고서

**보고자**: {reporter_name} | **부서**: {department} | **기간**: {period_start} ~ {period_end}

---

## Executive Summary

| 항목 | 내용 |
|------|------|
| **핵심 성과** | [가장 중요한 성과 1-2개, 숫자 포함] |
| **주의 필요** | [문제될 수 있는 것] |
| **요청 사항** | [상사의 의사결정/지원 필요 시] |

---

## {expected_element_1}

[이 섹션에서 {expected_element_1}에 대해 상세히 작성합니다]

- 현황: ...
- 수치: ...
- 비고: ...

---

## {expected_element_2}

[이 섹션에서 {expected_element_2}에 대해 상세히 작성합니다]

- 현황: ...
- 수치: ...
- 비고: ...

---

## {expected_element_3}

[이 섹션에서 {expected_element_3}에 대해 상세히 작성합니다]

- 현황: ...
- 수치: ...
- 비고: ...

---

## {expected_element_4}

[이 섹션에서 {expected_element_4}에 대해 상세히 작성합니다]

- 현황: ...
- 수치: ...
- 비고: ...

---

## 액션 아이템

| 담당 | 업무 | 기한 |
|------|------|------|
| ... | ... | ... |

---

### STEP 4: 최종 검토

✅ 체크리스트:
- [ ] Executive Summary만 읽어도 전체 파악 가능한가?
- [ ] **{expected_element_1}** 섹션이 있는가?
- [ ] **{expected_element_2}** 섹션이 있는가?
- [ ] **{expected_element_3}** 섹션이 있는가?
- [ ] **{expected_element_4}** 섹션이 있는가?
- [ ] 모든 수치에 목표 대비 달성률이 있는가?
"""


# ============================================================================
# V3.0 분석 보고서 프롬프트
# ============================================================================

ANALYSIS_REPORT_V3_TEMPLATE = """### 역할
당신은 비즈니스 분석 전문가입니다.

### 분석 보고서 원칙
1. **데이터 기반** - 모든 주장에 근거 자료 제시
2. **So What?** - 데이터가 의미하는 바를 해석
3. **실행 가능한 권고** - 분석 결과를 액션으로 연결

---

### 분석 개요
- **분석 제목**: {analysis_title}
- **분석자**: {analyst_name}
- **분석 기간**: {analysis_period}
- **분석 범위**: {analysis_scope}
- **분석 배경**: {background}

### 분석 목적
{objectives}

### 사용 데이터
{data_sources}

### 분석 결과
{analysis_results}

---

### STEP 1: 핵심 인사이트 도출
> "이 분석의 가장 중요한 발견은: [핵심 인사이트]이며, 이것이 의미하는 바는 [해석]이다."

---

### STEP 2: 필수 섹션 확인

⚠️ **중요**: 아래 4개 섹션을 **반드시** 출력에 포함해야 합니다.

| 번호 | 섹션 제목 | 포함 내용 |
|------|-----------|-----------|
| 1 | **{expected_element_1}** | 해당 주제에 대한 분석 결과 |
| 2 | **{expected_element_2}** | 해당 주제에 대한 분석 결과 |
| 3 | **{expected_element_3}** | 해당 주제에 대한 분석 결과 |
| 4 | **{expected_element_4}** | 해당 주제에 대한 분석 결과 |

---

### STEP 3: 보고서 작성

# 분석 보고서: {analysis_title}

**분석자**: {analyst_name} | **기간**: {analysis_period}

---

## Executive Summary

| 항목 | 내용 |
|------|------|
| **핵심 발견** | [가장 중요한 발견 1-2개] |
| **시사점** | [비즈니스에 미치는 영향] |
| **권고** | [핵심 권고사항 1개] |

---

## {expected_element_1}

### 분석 결과
[{expected_element_1}에 대한 상세 분석]

| 지표 | 수치 | 의미 |
|------|------|------|
| ... | ... | So What? |

---

## {expected_element_2}

### 분석 결과
[{expected_element_2}에 대한 상세 분석]

| 지표 | 수치 | 의미 |
|------|------|------|
| ... | ... | So What? |

---

## {expected_element_3}

### 분석 결과
[{expected_element_3}에 대한 상세 분석]

---

## {expected_element_4}

### 분석 결과
[{expected_element_4}에 대한 상세 분석]

---

## 권고사항

| 우선순위 | 권고 | 기대효과 |
|---------|------|---------|
| 1 | ... | ... |
| 2 | ... | ... |

---

### STEP 4: 최종 검토

✅ 체크리스트:
- [ ] **{expected_element_1}** 섹션이 있는가?
- [ ] **{expected_element_2}** 섹션이 있는가?
- [ ] **{expected_element_3}** 섹션이 있는가?
- [ ] **{expected_element_4}** 섹션이 있는가?
- [ ] 모든 데이터에 "So What?"이 있는가?
"""


# ============================================================================
# V3.0 회의록 프롬프트
# ============================================================================

MEETING_MINUTES_V3_TEMPLATE = """### 역할
당신은 회의 퍼실리테이션 전문가입니다.

### 회의록 원칙
1. **결정 중심** - 논의 과정보다 결정 사항이 핵심
2. **액션 추적 가능** - 누가, 무엇을, 언제까지
3. **간결하게** - 핵심만 추출

---

### 회의 정보
- **회의명**: {meeting_title}
- **일시**: {meeting_datetime}
- **장소**: {meeting_location}
- **참석자**: {attendees}
- **회의 목적**: {meeting_purpose}
- **작성자**: {recorder}

### 회의 내용
{meeting_content}

### 주요 논의
{discussion_points}

### 결정 사항
{decisions}

---

### STEP 1: 핵심 추출
> "이 회의의 핵심: [무엇이 결정되었고], [누가 무엇을 해야 하는가]"

---

### STEP 2: 필수 섹션 확인

⚠️ **중요**: 아래 4개 섹션을 **반드시** 출력에 포함해야 합니다.

| 번호 | 섹션 제목 | 포함 내용 |
|------|-----------|-----------|
| 1 | **{expected_element_1}** | 해당 주제에 대한 내용 |
| 2 | **{expected_element_2}** | 해당 주제에 대한 내용 |
| 3 | **{expected_element_3}** | 해당 주제에 대한 내용 |
| 4 | **{expected_element_4}** | 해당 주제에 대한 내용 |

---

### STEP 3: 회의록 작성

# 회의록: {meeting_title}

| 항목 | 내용 |
|------|------|
| **일시** | {meeting_datetime} |
| **장소** | {meeting_location} |
| **참석** | {attendees} |
| **작성** | {recorder} |

---

## Quick Summary
> [회의 결과를 한 문장으로]

---

## {expected_element_1}

[{expected_element_1}에 대한 상세 내용]

---

## {expected_element_2}

[{expected_element_2}에 대한 상세 내용]

---

## {expected_element_3}

[{expected_element_3}에 대한 상세 내용]

---

## {expected_element_4}

[{expected_element_4}에 대한 상세 내용]

---

## 액션 아이템

| 담당자 | 업무 | 기한 |
|--------|------|------|
| ... | ... | ... |

---

### STEP 4: 최종 검토

✅ 체크리스트:
- [ ] **{expected_element_1}** 섹션이 있는가?
- [ ] **{expected_element_2}** 섹션이 있는가?
- [ ] **{expected_element_3}** 섹션이 있는가?
- [ ] **{expected_element_4}** 섹션이 있는가?
- [ ] 모든 액션 아이템에 담당자와 기한이 있는가?
"""


# ============================================================================
# V3.0 프로젝트 제안서 프롬프트
# ============================================================================

PROJECT_PROPOSAL_V3_TEMPLATE = """### 역할
당신은 프로젝트 기획 전문가입니다.

### 제안서 원칙
1. **문제 해결 중심** - 왜 이 프로젝트가 필요한가?
2. **구체적인 수치** - 예상 효과를 정량화
3. **실행 가능성** - 현실적인 일정과 예산

---

### 프로젝트 개요
- **제안명**: {project_title}
- **제안자**: {proposer_name}
- **제안 부서**: {proposer_department}
- **제안 배경**: {background}

### 현황 및 문제점
{current_situation}

### 제안 내용
{proposal_details}

### 기대 효과
{expected_benefits}

### 필요 자원
{required_resources}

### 일정
{timeline}

---

### STEP 1: 핵심 메시지
> "이 프로젝트를 한 문장으로: [문제]를 해결하여 [효과]를 얻는다"

---

### STEP 2: 필수 섹션 확인

⚠️ **중요**: 아래 4개 섹션을 **반드시** 출력에 포함해야 합니다.

| 번호 | 섹션 제목 | 포함 내용 |
|------|-----------|-----------|
| 1 | **{expected_element_1}** | 해당 주제에 대한 상세 내용 |
| 2 | **{expected_element_2}** | 해당 주제에 대한 상세 내용 |
| 3 | **{expected_element_3}** | 해당 주제에 대한 상세 내용 |
| 4 | **{expected_element_4}** | 해당 주제에 대한 상세 내용 |

---

### STEP 3: 제안서 작성

# 프로젝트 제안서: {project_title}

**제안자**: {proposer_name} | **부서**: {proposer_department}

---

## Executive Summary

| 항목 | 내용 |
|------|------|
| **해결할 문제** | [핵심 문제점] |
| **제안 솔루션** | [핵심 제안 내용] |
| **기대 효과** | [정량적 효과] |
| **필요 예산** | [총 예산] |
| **소요 기간** | [총 기간] |

---

## {expected_element_1}

[{expected_element_1}에 대한 상세 내용]

---

## {expected_element_2}

[{expected_element_2}에 대한 상세 내용]

---

## {expected_element_3}

[{expected_element_3}에 대한 상세 내용]

---

## {expected_element_4}

[{expected_element_4}에 대한 상세 내용]

---

## 다음 단계

| 순서 | 활동 | 기한 |
|------|------|------|
| 1 | ... | ... |
| 2 | ... | ... |

---

### STEP 4: 최종 검토

✅ 체크리스트:
- [ ] **{expected_element_1}** 섹션이 있는가?
- [ ] **{expected_element_2}** 섹션이 있는가?
- [ ] **{expected_element_3}** 섹션이 있는가?
- [ ] **{expected_element_4}** 섹션이 있는가?
- [ ] 모든 효과가 정량화되었는가?
"""


# ============================================================================
# V3.0 프롬프트 함수들
# ============================================================================

def get_weekly_report_prompt_v3(
    reporter_name: str,
    department: str,
    report_to: str,
    period_start: str,
    period_end: str,
    report_period: str,
    raw_content: str,
    achievements: str,
    issues: str,
    next_plans: str,
    expected_elements: List[str],
    today_date: str = ""
) -> str:
    """V3.0 주간/월간 보고서 프롬프트 생성 - 동적 섹션"""
    # expected_elements가 4개 미만이면 기본값으로 채움
    elements = list(expected_elements)
    defaults = ["주요 성과", "진행 현황", "이슈 사항", "다음 계획"]
    while len(elements) < 4:
        elements.append(defaults[len(elements)])

    return WEEKLY_REPORT_V3_TEMPLATE.format(
        reporter_name=reporter_name,
        department=department,
        report_to=report_to,
        period_start=period_start,
        period_end=period_end,
        report_period=report_period,
        raw_content=raw_content,
        achievements=achievements,
        issues=issues,
        next_plans=next_plans,
        expected_element_1=elements[0],
        expected_element_2=elements[1],
        expected_element_3=elements[2],
        expected_element_4=elements[3],
        today_date=today_date
    )


def get_analysis_report_prompt_v3(
    analysis_title: str,
    analyst_name: str,
    analysis_period: str,
    analysis_scope: str,
    background: str,
    objectives: str,
    data_sources: str,
    analysis_results: str,
    expected_elements: List[str]
) -> str:
    """V3.0 분석 보고서 프롬프트 생성 - 동적 섹션"""
    elements = list(expected_elements)
    defaults = ["현황 분석", "원인 분석", "영향 분석", "권고사항"]
    while len(elements) < 4:
        elements.append(defaults[len(elements)])

    return ANALYSIS_REPORT_V3_TEMPLATE.format(
        analysis_title=analysis_title,
        analyst_name=analyst_name,
        analysis_period=analysis_period,
        analysis_scope=analysis_scope,
        background=background,
        objectives=objectives,
        data_sources=data_sources,
        analysis_results=analysis_results,
        expected_element_1=elements[0],
        expected_element_2=elements[1],
        expected_element_3=elements[2],
        expected_element_4=elements[3]
    )


def get_meeting_minutes_prompt_v3(
    meeting_title: str,
    meeting_datetime: str,
    meeting_location: str,
    attendees: str,
    absentees: str,
    meeting_purpose: str,
    recorder: str,
    meeting_content: str,
    discussion_points: str,
    decisions: str,
    expected_elements: List[str]
) -> str:
    """V3.0 회의록 프롬프트 생성 - 동적 섹션"""
    elements = list(expected_elements)
    defaults = ["안건 요약", "결정 사항", "논의 내용", "후속 조치"]
    while len(elements) < 4:
        elements.append(defaults[len(elements)])

    return MEETING_MINUTES_V3_TEMPLATE.format(
        meeting_title=meeting_title,
        meeting_datetime=meeting_datetime,
        meeting_location=meeting_location,
        attendees=attendees,
        absentees=absentees,
        meeting_purpose=meeting_purpose,
        recorder=recorder,
        meeting_content=meeting_content,
        discussion_points=discussion_points,
        decisions=decisions,
        expected_element_1=elements[0],
        expected_element_2=elements[1],
        expected_element_3=elements[2],
        expected_element_4=elements[3]
    )


def get_project_proposal_prompt_v3(
    project_title: str,
    proposer_name: str,
    proposer_department: str,
    background: str,
    current_situation: str,
    proposal_details: str,
    expected_benefits: str,
    required_resources: str,
    timeline: str,
    expected_elements: List[str]
) -> str:
    """V3.0 프로젝트 제안서 프롬프트 생성 - 동적 섹션"""
    elements = list(expected_elements)
    defaults = ["문제 정의", "제안 솔루션", "기대 효과", "실행 계획"]
    while len(elements) < 4:
        elements.append(defaults[len(elements)])

    return PROJECT_PROPOSAL_V3_TEMPLATE.format(
        project_title=project_title,
        proposer_name=proposer_name,
        proposer_department=proposer_department,
        background=background,
        current_situation=current_situation,
        proposal_details=proposal_details,
        expected_benefits=expected_benefits,
        required_resources=required_resources,
        timeline=timeline,
        expected_element_1=elements[0],
        expected_element_2=elements[1],
        expected_element_3=elements[2],
        expected_element_4=elements[3]
    )
