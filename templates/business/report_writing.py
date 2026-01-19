# -*- coding: utf-8 -*-
"""
================================================================================
비즈니스 보고서 작성 프롬프트 모듈 (Business Report Writing Prompts)
================================================================================

## 이 모듈의 목적
실무자가 다양한 비즈니스 보고서를 체계적으로 작성할 수 있도록 지원

## 대상 사용자
- 직장인 (주간/월간 보고서 작성자)
- 팀장/매니저 (분석 보고서 작성자)
- 프로젝트 매니저 (기획서 작성자)

## 프롬프트 설계 원칙
1. 구조화: 명확한 섹션 구분과 논리적 흐름
2. 정량화: 데이터와 수치로 뒷받침
3. 시각화 고려: 표, 차트로 표현 가능한 형태
4. 실행 가능성: 액션 아이템과 다음 단계 명시

## 보고서 유형
- 주간/월간 업무 보고서
- 분석 보고서 (시장, 경쟁사, 고객 등)
- 회의록
- 프로젝트 기획서/제안서
================================================================================
"""

from typing import Dict, List, Optional


# ============================================================================
# 주간/월간 업무 보고서 프롬프트
# ============================================================================

WEEKLY_REPORT_TEMPLATE = """### 역할
당신은 기업 교육 전문가이자 비즈니스 라이팅 코치입니다.
수백 명의 직장인에게 효과적인 보고서 작성법을 가르친 경험이 있습니다.
상사가 빠르게 핵심을 파악할 수 있는 보고서 구조를 잘 알고 있습니다.

### 작업
아래 정보를 바탕으로 {report_period} 업무 보고서를 작성하세요.

### 보고자 정보
- 이름/직책: {reporter_name}
- 소속 부서: {department}
- 보고 대상: {report_to}

### 보고 기간
- 기간: {period_start} ~ {period_end}

### 업무 내용 원본
{raw_content}

### 핵심 성과 (정량적 데이터)
{achievements}

### 이슈/문제점
{issues}

### 다음 기간 계획
{next_plans}

### 보고서 작성 원칙
1. **두괄식**: 핵심 성과 먼저, 세부사항은 후순위
2. **정량화**: 모든 성과는 가능한 숫자로 표현
3. **객관성**: 감정적 표현 배제, 사실 중심
4. **간결성**: 불필요한 수식어 제거
5. **액션**: 이슈에는 반드시 해결책/요청사항 포함

### 출력 형식
# {report_period} 업무 보고서

**보고자**: {reporter_name} | **부서**: {department} | **기간**: {period_start} ~ {period_end}

---

## 1. Executive Summary (핵심 요약)
- 주요 성과 3줄 요약
- 주의 필요 사항 1-2개

## 2. 주요 성과
| 업무 항목 | 목표 | 실적 | 달성률 | 비고 |
|----------|------|------|--------|------|
| ... | ... | ... | ... | ... |

## 3. 진행 중인 업무
| 업무 항목 | 진행률 | 예상 완료일 | 이슈 사항 |
|----------|--------|------------|----------|
| ... | ... | ... | ... |

## 4. 이슈 및 건의사항
### 이슈 1: [제목]
- 상황: ...
- 원인: ...
- 조치/요청: ...

## 5. 다음 {report_period} 계획
| 우선순위 | 업무 항목 | 목표 | 완료 예정일 |
|---------|----------|------|------------|
| 1 | ... | ... | ... |

---
작성일: {today_date}
"""


# ============================================================================
# 분석 보고서 프롬프트
# ============================================================================

ANALYSIS_REPORT_TEMPLATE = """### 역할
당신은 전략 컨설팅 펌 출신의 분석 전문가입니다.
맥킨지, BCG 스타일의 구조화된 분석 보고서 작성에 전문성이 있습니다.
데이터를 통찰력 있는 인사이트로 변환하는 능력이 뛰어납니다.

### 작업
아래 데이터/정보를 바탕으로 {analysis_type} 분석 보고서를 작성하세요.

### 분석 목적
{analysis_purpose}

### 분석 대상
{analysis_target}

### 수집된 데이터/정보
{collected_data}

### 배경 정보
{background_info}

### 분석 프레임워크
{analysis_framework}

### 보고 대상
{audience}

### 분석 보고서 원칙
1. **So What**: 모든 데이터에 "그래서 의미가 뭔데?" 답변 필수
2. **MECE**: 중복 없이 누락 없는 구조화
3. **피라미드 구조**: 결론 → 근거 → 데이터 순
4. **시각화**: 복잡한 데이터는 표/차트로
5. **액션 지향**: 분석의 끝은 반드시 제안/권고

### 출력 형식
# {analysis_type} 분석 보고서

**분석 목적**: {analysis_purpose}
**분석 기간**: {analysis_period}
**작성자**: {author}

---

## Executive Summary
[1페이지 분량의 핵심 요약]
- 핵심 발견사항 3가지
- 주요 권고사항 2-3가지

## 1. 분석 배경 및 목적
### 1.1 분석 배경
### 1.2 분석 범위 및 방법론

## 2. 현황 분석
### 2.1 [분석 영역 1]
- 데이터/팩트
- 인사이트

### 2.2 [분석 영역 2]
- 데이터/팩트
- 인사이트

## 3. 핵심 발견사항 (Key Findings)
### Finding 1: [제목]
- 근거 데이터
- 의미/영향

### Finding 2: [제목]
- 근거 데이터
- 의미/영향

## 4. 시사점 및 권고사항
### 4.1 전략적 시사점
### 4.2 권고사항
| 우선순위 | 권고사항 | 기대효과 | 실행 난이도 |
|---------|---------|---------|------------|
| 1 | ... | ... | ... |

## 5. 부록
- 상세 데이터
- 참고 자료
"""


# ============================================================================
# 회의록 프롬프트
# ============================================================================

MEETING_MINUTES_TEMPLATE = """### 역할
당신은 경험 많은 프로젝트 매니저입니다.
수많은 회의를 주재하고 기록해본 경험이 있습니다.
회의 내용을 명확한 액션 아이템으로 정리하는 능력이 뛰어납니다.

### 작업
아래 회의 내용을 바탕으로 체계적인 회의록을 작성하세요.

### 회의 정보
- 회의명: {meeting_title}
- 일시: {meeting_datetime}
- 장소: {meeting_location}
- 참석자: {attendees}
- 불참자: {absentees}
- 회의 목적: {meeting_purpose}

### 회의 내용 (원본)
{meeting_content}

### 주요 논의 사항
{discussion_points}

### 결정 사항
{decisions}

### 회의록 작성 원칙
1. **객관성**: 개인 의견 배제, 사실만 기록
2. **명확성**: 누가, 무엇을, 언제까지 명확히
3. **추적 가능**: 모든 액션 아이템에 담당자와 기한
4. **간결성**: 핵심만 추출, 불필요한 대화 제외
5. **후속 조치**: 다음 회의 일정과 준비사항 포함

### 출력 형식
# 회의록: {meeting_title}

| 항목 | 내용 |
|------|------|
| 일시 | {meeting_datetime} |
| 장소 | {meeting_location} |
| 참석자 | {attendees} |
| 작성자 | {recorder} |

---

## 1. 회의 목적
{meeting_purpose}

## 2. 주요 논의 내용

### 2.1 [안건 1]
- **논의 내용**: ...
- **주요 의견**: ...
- **결론**: ...

### 2.2 [안건 2]
- **논의 내용**: ...
- **주요 의견**: ...
- **결론**: ...

## 3. 결정 사항
| 번호 | 결정 내용 | 결정 근거 |
|------|----------|----------|
| 1 | ... | ... |

## 4. 액션 아이템
| 번호 | 액션 아이템 | 담당자 | 완료 기한 | 비고 |
|------|-----------|--------|----------|------|
| 1 | ... | ... | ... | ... |

## 5. 다음 회의
- **일시**: ...
- **안건**: ...
- **준비 사항**: ...

---
작성일시: {record_datetime}
"""


# ============================================================================
# 프로젝트 기획서/제안서 프롬프트
# ============================================================================

PROJECT_PROPOSAL_TEMPLATE = """### 역할
당신은 시니어 프로젝트 매니저이자 비즈니스 기획 전문가입니다.
수십 개의 프로젝트 기획서로 경영진 승인을 받아본 경험이 있습니다.
설득력 있는 제안서 구조와 의사결정권자의 관점을 잘 이해하고 있습니다.

### 작업
아래 정보를 바탕으로 프로젝트 기획서/제안서를 작성하세요.

### 프로젝트 개요
- 프로젝트명: {project_name}
- 프로젝트 유형: {project_type}
- 제안 배경: {background}
- 목표: {objectives}

### 현황 및 문제점
{current_situation}

### 제안 내용
{proposal_details}

### 예상 효과
{expected_benefits}

### 필요 리소스
- 예산: {budget}
- 인력: {resources}
- 기간: {timeline}

### 리스크 요소
{risks}

### 기획서 대상
{target_audience}

### 기획서 작성 원칙
1. **문제-해결**: 문제 정의 → 해결책 → 기대효과 구조
2. **ROI**: 투자 대비 효과 명확히
3. **실현 가능성**: 구체적 일정과 마일스톤
4. **리스크 관리**: 잠재 리스크와 대응 방안
5. **비교 분석**: 대안과의 비교 (왜 이 방법인가)

### 출력 형식
# {project_name} 기획서

**제안자**: {proposer} | **부서**: {department} | **제안일**: {proposal_date}

---

## Executive Summary
[1페이지 분량으로 핵심 내용 요약]

## 1. 프로젝트 배경 및 필요성
### 1.1 현황
### 1.2 문제점/기회
### 1.3 프로젝트 필요성

## 2. 프로젝트 목표
### 2.1 정성적 목표
### 2.2 정량적 목표 (KPI)
| KPI | 현재 | 목표 | 측정 방법 |
|-----|------|------|----------|
| ... | ... | ... | ... |

## 3. 추진 내용
### 3.1 전체 개요
### 3.2 세부 추진 내용
| 단계 | 내용 | 산출물 | 기간 |
|------|------|--------|------|
| 1 | ... | ... | ... |

## 4. 추진 일정
[간트 차트 형식 또는 마일스톤]
| 마일스톤 | 완료 기준 | 예정일 |
|---------|----------|--------|
| ... | ... | ... |

## 5. 소요 예산 및 자원
### 5.1 예산
| 항목 | 금액 | 산출 근거 |
|------|------|----------|
| ... | ... | ... |
| **합계** | **...** | |

### 5.2 필요 인력
| 역할 | 인원 | 기간 | 비고 |
|------|------|------|------|
| ... | ... | ... | ... |

## 6. 기대 효과
### 6.1 정량적 효과
### 6.2 정성적 효과
### 6.3 ROI 분석

## 7. 리스크 및 대응 방안
| 리스크 | 발생 가능성 | 영향도 | 대응 방안 |
|--------|-----------|--------|----------|
| ... | 상/중/하 | 상/중/하 | ... |

## 8. 결론 및 요청사항
### 8.1 결론
### 8.2 요청사항
"""


# ============================================================================
# 프롬프트 함수
# ============================================================================

def get_weekly_report_prompt(
    reporter_name: str,
    department: str,
    report_to: str,
    period_start: str,
    period_end: str,
    raw_content: str,
    achievements: str,
    issues: str,
    next_plans: str,
    report_period: str = "주간",
    today_date: str = ""
) -> str:
    """
    주간/월간 업무 보고서 작성 프롬프트 생성

    Parameters
    ----------
    reporter_name : str
        보고자 이름/직책
    department : str
        소속 부서
    report_to : str
        보고 대상
    period_start : str
        보고 기간 시작일
    period_end : str
        보고 기간 종료일
    raw_content : str
        업무 내용 원본
    achievements : str
        핵심 성과
    issues : str
        이슈/문제점
    next_plans : str
        다음 기간 계획
    report_period : str
        보고 주기 (주간/월간)
    today_date : str
        작성일

    Returns
    -------
    str
        완성된 프롬프트
    """
    from datetime import datetime
    if not today_date:
        today_date = datetime.now().strftime("%Y-%m-%d")

    return WEEKLY_REPORT_TEMPLATE.format(
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
        today_date=today_date
    )


def get_analysis_report_prompt(
    analysis_type: str,
    analysis_purpose: str,
    analysis_target: str,
    collected_data: str,
    background_info: str,
    analysis_framework: str = "SWOT",
    audience: str = "경영진",
    analysis_period: str = "",
    author: str = ""
) -> str:
    """
    분석 보고서 작성 프롬프트 생성

    Parameters
    ----------
    analysis_type : str
        분석 유형 (시장, 경쟁사, 고객 등)
    analysis_purpose : str
        분석 목적
    analysis_target : str
        분석 대상
    collected_data : str
        수집된 데이터/정보
    background_info : str
        배경 정보
    analysis_framework : str
        분석 프레임워크 (SWOT, 5 Forces 등)
    audience : str
        보고 대상
    analysis_period : str
        분석 기간
    author : str
        작성자

    Returns
    -------
    str
        완성된 프롬프트
    """
    return ANALYSIS_REPORT_TEMPLATE.format(
        analysis_type=analysis_type,
        analysis_purpose=analysis_purpose,
        analysis_target=analysis_target,
        collected_data=collected_data,
        background_info=background_info,
        analysis_framework=analysis_framework,
        audience=audience,
        analysis_period=analysis_period or "미지정",
        author=author or "미지정"
    )


def get_meeting_minutes_prompt(
    meeting_title: str,
    meeting_datetime: str,
    meeting_location: str,
    attendees: str,
    meeting_purpose: str,
    meeting_content: str,
    discussion_points: str,
    decisions: str,
    absentees: str = "",
    recorder: str = "",
    record_datetime: str = ""
) -> str:
    """
    회의록 작성 프롬프트 생성

    Parameters
    ----------
    meeting_title : str
        회의명
    meeting_datetime : str
        회의 일시
    meeting_location : str
        회의 장소
    attendees : str
        참석자 목록
    meeting_purpose : str
        회의 목적
    meeting_content : str
        회의 내용 원본
    discussion_points : str
        주요 논의 사항
    decisions : str
        결정 사항
    absentees : str, optional
        불참자
    recorder : str, optional
        작성자
    record_datetime : str, optional
        작성 일시

    Returns
    -------
    str
        완성된 프롬프트
    """
    from datetime import datetime
    if not record_datetime:
        record_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")

    return MEETING_MINUTES_TEMPLATE.format(
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
        record_datetime=record_datetime
    )


def get_project_proposal_prompt(
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
    target_audience: str = "경영진",
    proposer: str = "",
    department: str = "",
    proposal_date: str = ""
) -> str:
    """
    프로젝트 기획서/제안서 작성 프롬프트 생성

    Parameters
    ----------
    project_name : str
        프로젝트명
    project_type : str
        프로젝트 유형
    background : str
        제안 배경
    objectives : str
        프로젝트 목표
    current_situation : str
        현황 및 문제점
    proposal_details : str
        제안 내용
    expected_benefits : str
        예상 효과
    budget : str
        예산
    resources : str
        필요 인력
    timeline : str
        기간
    risks : str
        리스크 요소
    target_audience : str
        기획서 대상
    proposer : str, optional
        제안자
    department : str, optional
        부서
    proposal_date : str, optional
        제안일

    Returns
    -------
    str
        완성된 프롬프트
    """
    from datetime import datetime
    if not proposal_date:
        proposal_date = datetime.now().strftime("%Y-%m-%d")

    return PROJECT_PROPOSAL_TEMPLATE.format(
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
        proposal_date=proposal_date
    )
