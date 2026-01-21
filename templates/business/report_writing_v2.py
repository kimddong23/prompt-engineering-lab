# -*- coding: utf-8 -*-
"""
================================================================================
비즈니스 보고서 프롬프트 V2.0 - 피라미드 원칙
================================================================================

## V2.0 핵심 철학
"읽는 사람은 바쁘다. 결론부터 말하라."

## 기존 V1.0의 문제점
1. 단순 출력 형식만 제시
2. "So What?" 검증 없음
3. expected_elements 연동 없음
4. 액션 아이템이 선택사항

## V2.0 개선 사항
1. 피라미드 구조 강제 (결론 → 근거 → 세부)
2. "So What?" 검증 단계 필수
3. 필수 요소 명시적 포함 유도
4. 모든 보고서에 액션 아이템 필수

================================================================================
"""

from typing import Dict, List, Optional


# ============================================================================
# V2.0 주간/월간 보고서 프롬프트
# ============================================================================

WEEKLY_REPORT_V2_TEMPLATE = """### 역할 및 원칙

당신은 비즈니스 보고서 전문가입니다.

**보고서의 3가지 원칙:**
1. **"피라미드 원칙"** - 결론 먼저, 근거 나중. 상사는 바쁘다.
2. **"숫자로 말하기"** - "열심히 했다"가 아닌 "목표 대비 110% 달성"
3. **"액션 중심"** - 모든 이슈에는 해결책이, 모든 보고에는 다음 단계가

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

### STEP 1: 핵심 메시지 도출

**한 문장 요약**: 이번 {report_period}을 한 문장으로:
> "[핵심 성과], 단 [주요 이슈]에 대한 [조치 필요]"

**상사가 가장 알고 싶은 것 3가지**:
1. 목표 대비 실적은?
2. 문제될 것은?
3. 다음 주에 뭐 할 건지?

---

### STEP 2: 정보 구조화

**필수 포함 요소**:
- {expected_element_1}
- {expected_element_2}
- {expected_element_3}
- {expected_element_4}

**수치화 체크**:
- 모든 성과는 숫자로 표현되었는가?
- 목표 대비 달성률이 명시되었는가?

---

### STEP 3: 보고서 작성

# {report_period} 업무 보고서

**보고자**: {reporter_name} | **부서**: {department} | **기간**: {period_start} ~ {period_end}

---

## 1. Executive Summary (핵심 요약)

| 항목 | 내용 |
|------|------|
| **핵심 성과** | [가장 중요한 성과 1-2개] |
| **주의 필요** | [문제될 수 있는 것] |
| **요청 사항** | [상사의 의사결정/지원 필요 시] |

## 2. 주요 성과

| 업무 항목 | 목표 | 실적 | 달성률 | 비고 |
|----------|------|------|--------|------|
| ... | ... | ... | ...% | ... |

## 3. 진행 중인 업무

| 업무 항목 | 진행률 | 예상 완료일 | 리스크 |
|----------|--------|------------|--------|
| ... | ...% | ... | ... |

## 4. 이슈 및 대응

### 이슈 1: [제목]
- **상황**: ...
- **원인**: ...
- **대응**: ...
- **요청**: [필요 시]

## 5. 다음 {report_period} 계획

| 우선순위 | 업무 | 목표 | 완료 예정 |
|---------|------|------|----------|
| 1 | ... | ... | ... |

---

### STEP 4: 품질 검토

- [ ] Executive Summary만 읽어도 전체 파악 가능한가?
- [ ] 모든 수치에 목표 대비 달성률이 있는가?
- [ ] 이슈마다 대응 방안이 있는가?
- [ ] 다음 계획이 구체적인가?

---
작성일: {today_date}
"""


# ============================================================================
# V2.0 분석 보고서 프롬프트
# ============================================================================

ANALYSIS_REPORT_V2_TEMPLATE = """### 역할 및 원칙

당신은 전략 분석 전문가입니다.

**분석 보고서의 3가지 원칙:**
1. **"So What?"** - 모든 데이터에 "그래서 의미가 뭔데?" 답이 있어야 함
2. **"MECE"** - 중복 없이, 누락 없이 구조화
3. **"액션 지향"** - 분석의 끝은 반드시 제안/권고

---

### 분석 정보

- **분석 유형**: {analysis_type}
- **분석 목적**: {analysis_purpose}
- **분석 대상**: {analysis_target}
- **보고 대상**: {audience}
- **분석 기간**: {analysis_period}
- **작성자**: {author}

### 수집된 데이터
{collected_data}

### 배경 정보
{background_info}

### 분석 프레임워크
{analysis_framework}

---

### STEP 1: 분석 설계

**핵심 질문**: 이 분석이 답해야 할 질문:
> "[대상]에 대해 [무엇을] 알아내어 [어떤 의사결정]을 하려 하는가?"

**의사결정권자의 관심사**:
- 지금 해야 할 것은?
- 리스크는?
- 기회는?

---

### STEP 2: 발견사항 구조화

**필수 포함 요소**:
- {expected_element_1}
- {expected_element_2}
- {expected_element_3}
- {expected_element_4}

**So What 검증**: 모든 발견사항에 "의미/영향"을 명시했는가?

---

### STEP 3: 분석 보고서 작성

# {analysis_type} 분석 보고서

**분석 목적**: {analysis_purpose} | **기간**: {analysis_period} | **작성자**: {author}

---

## Executive Summary

| 항목 | 내용 |
|------|------|
| **핵심 발견** | [가장 중요한 발견 2-3개] |
| **주요 권고** | [즉시 실행해야 할 것] |
| **리스크** | [주의해야 할 것] |

## 1. 분석 배경 및 방법론

### 1.1 분석 배경
[왜 이 분석이 필요한가]

### 1.2 분석 범위 및 방법
- **범위**: ...
- **방법론**: {analysis_framework}
- **데이터 소스**: ...

## 2. 현황 분석

### 2.1 [분석 영역 1]
| 데이터 | 수치 | So What? |
|--------|------|----------|
| ... | ... | [이게 의미하는 바] |

### 2.2 [분석 영역 2]
| 데이터 | 수치 | So What? |
|--------|------|----------|
| ... | ... | [이게 의미하는 바] |

## 3. 핵심 발견사항 (Key Findings)

### Finding 1: [제목]
- **데이터 근거**: ...
- **의미**: ...
- **영향**: ...

### Finding 2: [제목]
- **데이터 근거**: ...
- **의미**: ...
- **영향**: ...

## 4. 권고사항

| 우선순위 | 권고 | 기대효과 | 난이도 | 담당 |
|---------|------|---------|--------|------|
| 1 | ... | ... | 상/중/하 | ... |
| 2 | ... | ... | 상/중/하 | ... |

## 5. 부록
- 상세 데이터
- 참고 자료

---

### STEP 4: 검증

- [ ] Executive Summary만으로 핵심 파악 가능한가?
- [ ] 모든 데이터에 "So What?"이 있는가?
- [ ] 권고사항이 실행 가능한가?
- [ ] MECE하게 구조화되었는가?
"""


# ============================================================================
# V2.0 회의록 프롬프트
# ============================================================================

MEETING_MINUTES_V2_TEMPLATE = """### 역할 및 원칙

당신은 회의 퍼실리테이션 전문가입니다.

**회의록의 3가지 원칙:**
1. **"결정 중심"** - 논의 과정보다 결정 사항이 핵심
2. **"액션 추적 가능"** - 누가, 무엇을, 언제까지
3. **"간결하게"** - 핵심만 추출, 불필요한 대화 제외

---

### 회의 정보

- **회의명**: {meeting_title}
- **일시**: {meeting_datetime}
- **장소**: {meeting_location}
- **참석자**: {attendees}
- **불참자**: {absentees}
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

**회의의 핵심 질문**:
> "이 회의에서 무엇이 결정되었고, 누가 무엇을 해야 하는가?"

**회의 참석 안 한 사람이 알아야 할 것**:
1. 무엇이 결정되었는가?
2. 누가 무엇을 해야 하는가?
3. 다음 회의는 언제인가?

---

### STEP 2: 구조화

**필수 포함 요소**:
- {expected_element_1}
- {expected_element_2}
- {expected_element_3}
- {expected_element_4}

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
- **핵심 결정**: [1-2문장]
- **주요 액션**: [담당자 - 할 일 - 기한]

---

## 1. 회의 목적
{meeting_purpose}

## 2. 논의 내용

### 안건 1: [제목]
- **논의**: ...
- **주요 의견**: ...
- **결론**: ...

### 안건 2: [제목]
- **논의**: ...
- **주요 의견**: ...
- **결론**: ...

## 3. 결정 사항

| No | 결정 내용 | 근거 |
|----|----------|------|
| 1 | ... | ... |

## 4. 액션 아이템

| No | 할 일 | 담당자 | 기한 | 비고 |
|----|------|--------|------|------|
| 1 | ... | ... | ... | ... |

## 5. 다음 회의
- **일시**: ...
- **안건**: ...
- **준비물**: ...

---
작성일시: {record_datetime}

---

### STEP 4: 검토

- [ ] Quick Summary만 읽어도 핵심 파악 가능한가?
- [ ] 모든 액션에 담당자와 기한이 있는가?
- [ ] 다음 회의 정보가 명확한가?
"""


# ============================================================================
# V2.0 프로젝트 기획서 프롬프트
# ============================================================================

PROJECT_PROPOSAL_V2_TEMPLATE = """### 역할 및 원칙

당신은 프로젝트 기획 전문가입니다.

**기획서의 3가지 원칙:**
1. **"문제-해결-효과"** - 왜 필요한지 → 어떻게 할지 → 뭘 얻는지
2. **"ROI 명확화"** - 투자 대비 효과를 숫자로
3. **"실현 가능성"** - 구체적 일정, 리소스, 리스크 관리

---

### 프로젝트 정보

- **프로젝트명**: {project_name}
- **유형**: {project_type}
- **제안자**: {proposer}
- **부서**: {department}
- **제안일**: {proposal_date}
- **대상**: {target_audience}

### 배경
{background}

### 목표
{objectives}

### 현황 및 문제점
{current_situation}

### 제안 내용
{proposal_details}

### 예상 효과
{expected_benefits}

### 리소스
- **예산**: {budget}
- **인력**: {resources}
- **기간**: {timeline}

### 리스크
{risks}

---

### STEP 1: 설득 전략

**핵심 질문**: 의사결정권자가 "왜 해야 하지?"라고 물으면:
> "현재 [문제]로 인해 [손실/기회비용]이 발생하고 있으며, 이 프로젝트로 [효과]를 얻을 수 있습니다"

**의사결정 기준**:
- ROI가 명확한가?
- 리스크가 관리 가능한가?
- 실현 가능한가?

---

### STEP 2: 구조화

**필수 포함 요소**:
- {expected_element_1}
- {expected_element_2}
- {expected_element_3}
- {expected_element_4}

---

### STEP 3: 기획서 작성

# {project_name} 기획서

**제안자**: {proposer} | **부서**: {department} | **제안일**: {proposal_date}

---

## Executive Summary

| 항목 | 내용 |
|------|------|
| **프로젝트 목적** | [한 문장] |
| **핵심 효과** | [정량적 수치] |
| **소요 자원** | 예산 {budget}, 기간 {timeline} |
| **요청 사항** | [승인 필요 사항] |

## 1. 배경 및 필요성

### 1.1 현황
[현재 상황]

### 1.2 문제점/기회
[무엇이 문제인가]

### 1.3 왜 지금 해야 하는가
[시급성]

## 2. 프로젝트 목표

### 2.1 정성적 목표
- ...

### 2.2 정량적 목표 (KPI)

| KPI | 현재 | 목표 | 측정 방법 |
|-----|------|------|----------|
| ... | ... | ... | ... |

## 3. 추진 내용

### 3.1 전체 개요
[한눈에 보는 프로젝트]

### 3.2 세부 추진 내용

| 단계 | 내용 | 산출물 | 기간 |
|------|------|--------|------|
| 1 | ... | ... | ... |

## 4. 일정

| 마일스톤 | 완료 기준 | 예정일 |
|---------|----------|--------|
| ... | ... | ... |

## 5. 소요 자원

### 5.1 예산

| 항목 | 금액 | 산출 근거 |
|------|------|----------|
| ... | ... | ... |
| **합계** | **...** | |

### 5.2 인력

| 역할 | 인원 | 기간 |
|------|------|------|
| ... | ... | ... |

## 6. 기대 효과 및 ROI

### 6.1 정량적 효과
| 효과 | 수치 | 산출 근거 |
|------|------|----------|
| ... | ... | ... |

### 6.2 ROI 분석
- **총 투자**: ...
- **예상 효과**: ...
- **ROI**: ...%
- **회수 기간**: ...

## 7. 리스크 및 대응

| 리스크 | 가능성 | 영향 | 대응 |
|--------|--------|------|------|
| ... | 상/중/하 | 상/중/하 | ... |

## 8. 요청 사항
- [승인 필요 사항]
- [지원 필요 사항]

---

### STEP 4: 검토

- [ ] Executive Summary만으로 의사결정 가능한가?
- [ ] ROI가 명확한가?
- [ ] 리스크 대응이 구체적인가?
- [ ] 일정이 현실적인가?
"""


# ============================================================================
# V2.0 프롬프트 함수
# ============================================================================

def get_weekly_report_prompt_v2(
    reporter_name: str,
    department: str,
    report_to: str,
    period_start: str,
    period_end: str,
    raw_content: str,
    achievements: str,
    issues: str,
    next_plans: str,
    expected_elements: List[str],
    report_period: str = "주간",
    today_date: str = ""
) -> str:
    """V2.0 주간/월간 보고서 프롬프트 생성"""
    from datetime import datetime
    if not today_date:
        today_date = datetime.now().strftime("%Y-%m-%d")

    elements = expected_elements + ["다음 기간 계획"] * (4 - len(expected_elements))

    return WEEKLY_REPORT_V2_TEMPLATE.format(
        reporter_name=reporter_name,
        department=department,
        report_to=report_to,
        period_start=period_start,
        period_end=period_end,
        raw_content=raw_content,
        achievements=achievements,
        issues=issues,
        next_plans=next_plans,
        report_period=report_period,
        today_date=today_date,
        expected_element_1=elements[0],
        expected_element_2=elements[1],
        expected_element_3=elements[2],
        expected_element_4=elements[3]
    )


def get_analysis_report_prompt_v2(
    analysis_type: str,
    analysis_purpose: str,
    analysis_target: str,
    collected_data: str,
    background_info: str,
    expected_elements: List[str],
    analysis_framework: str = "SWOT",
    audience: str = "경영진",
    analysis_period: str = "",
    author: str = ""
) -> str:
    """V2.0 분석 보고서 프롬프트 생성"""
    elements = expected_elements + ["권고사항"] * (4 - len(expected_elements))

    return ANALYSIS_REPORT_V2_TEMPLATE.format(
        analysis_type=analysis_type,
        analysis_purpose=analysis_purpose,
        analysis_target=analysis_target,
        collected_data=collected_data,
        background_info=background_info,
        analysis_framework=analysis_framework,
        audience=audience,
        analysis_period=analysis_period or "미지정",
        author=author or "미지정",
        expected_element_1=elements[0],
        expected_element_2=elements[1],
        expected_element_3=elements[2],
        expected_element_4=elements[3]
    )


def get_meeting_minutes_prompt_v2(
    meeting_title: str,
    meeting_datetime: str,
    meeting_location: str,
    attendees: str,
    meeting_purpose: str,
    meeting_content: str,
    discussion_points: str,
    decisions: str,
    expected_elements: List[str],
    absentees: str = "",
    recorder: str = "",
    record_datetime: str = ""
) -> str:
    """V2.0 회의록 프롬프트 생성"""
    from datetime import datetime
    if not record_datetime:
        record_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")

    elements = expected_elements + ["다음 회의"] * (4 - len(expected_elements))

    return MEETING_MINUTES_V2_TEMPLATE.format(
        meeting_title=meeting_title,
        meeting_datetime=meeting_datetime,
        meeting_location=meeting_location,
        attendees=attendees,
        absentees=absentees or "없음",
        meeting_purpose=meeting_purpose,
        meeting_content=meeting_content,
        discussion_points=discussion_points,
        decisions=decisions,
        recorder=recorder or "미지정",
        record_datetime=record_datetime,
        expected_element_1=elements[0],
        expected_element_2=elements[1],
        expected_element_3=elements[2],
        expected_element_4=elements[3]
    )


def get_project_proposal_prompt_v2(
    project_name: str,
    project_type: str,
    background: str,
    objectives: str,
    current_situation: str,
    proposal_details: str,
    expected_benefits: str,
    budget: str,
    resources: str,
    timeline: str,
    risks: str,
    expected_elements: List[str],
    target_audience: str = "경영진",
    proposer: str = "",
    department: str = "",
    proposal_date: str = ""
) -> str:
    """V2.0 프로젝트 기획서 프롬프트 생성"""
    from datetime import datetime
    if not proposal_date:
        proposal_date = datetime.now().strftime("%Y-%m-%d")

    elements = expected_elements + ["ROI 분석"] * (4 - len(expected_elements))

    return PROJECT_PROPOSAL_V2_TEMPLATE.format(
        project_name=project_name,
        project_type=project_type,
        background=background,
        objectives=objectives,
        current_situation=current_situation,
        proposal_details=proposal_details,
        expected_benefits=expected_benefits,
        budget=budget,
        resources=resources,
        timeline=timeline,
        risks=risks,
        target_audience=target_audience,
        proposer=proposer or "미지정",
        department=department or "미지정",
        proposal_date=proposal_date,
        expected_element_1=elements[0],
        expected_element_2=elements[1],
        expected_element_3=elements[2],
        expected_element_4=elements[3]
    )
