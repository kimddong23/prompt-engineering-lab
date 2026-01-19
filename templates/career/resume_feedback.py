# -*- coding: utf-8 -*-
"""
================================================================================
이력서 첨삭 프롬프트 모듈 (Resume Feedback Prompts)
================================================================================

## 이 모듈의 목적
취준생의 이력서를 분석하고 구체적인 개선 피드백을 제공하는 프롬프트 템플릿

## 대상 사용자
- 신입/경력 취준생
- 이직 준비자
- 커리어 컨설턴트

## 프롬프트 설계 원칙
1. STAR 기법 (Situation-Task-Action-Result) 기반 피드백
2. 정량적 성과 강조 유도
3. 직무별 맞춤 키워드 제안
4. ATS(지원자추적시스템) 최적화 고려

## 학술적 근거
- Harvard Business Review: "How to Write a Resume That Stands Out"
- LinkedIn Talent Solutions: "Global Recruiting Trends"
================================================================================
"""

from typing import Dict, List, Optional


# ============================================================================
# 이력서 종합 첨삭 프롬프트
# ============================================================================

RESUME_COMPREHENSIVE_FEEDBACK = """### 역할
당신은 15년 경력의 시니어 HR 컨설턴트입니다.
대기업, 스타트업, 외국계 기업의 채용 프로세스를 모두 경험했습니다.
수천 건의 이력서를 검토하고 합격시킨 경험이 있습니다.

### 작업
아래 이력서를 분석하고 구체적인 개선 피드백을 제공하세요.

### 이력서 정보
- 지원 직무: {job_position}
- 지원 회사 유형: {company_type}
- 경력 수준: {experience_level}

### 이력서 내용
{resume_content}

### 분석 기준
1. **직무 적합성**: 지원 직무와 경험의 연관성
2. **성과 정량화**: 숫자로 표현된 성과가 있는지
3. **키워드 최적화**: ATS 통과를 위한 직무 키워드 포함 여부
4. **가독성**: 구조와 포맷의 명확성
5. **차별화**: 다른 지원자와 구별되는 강점

### 출력 형식
다음 형식으로 피드백을 제공하세요:

## 종합 점수: [X/100점]

## 강점 (유지할 것)
1. ...
2. ...

## 개선 필요 (수정할 것)
1. [현재 문장]
   → [개선된 문장]
   (개선 이유: ...)

2. [현재 문장]
   → [개선된 문장]
   (개선 이유: ...)

## 추가 권장 사항
1. ...
2. ...

## 직무별 추천 키워드
- ...
"""


# ============================================================================
# 경력 기술서 STAR 기법 변환 프롬프트
# ============================================================================

EXPERIENCE_STAR_CONVERSION = """### 역할
당신은 커리어 코칭 전문가입니다.
STAR 기법(Situation-Task-Action-Result)을 활용한 경력 기술에 전문성이 있습니다.

### 작업
아래 경력 기술을 STAR 기법으로 재구성하여 더 임팩트 있게 만들어주세요.

### 원본 경력 기술
{original_description}

### 추가 정보 (있는 경우)
- 당시 상황/배경: {situation}
- 담당 업무/책임: {task}
- 구체적 행동: {action}
- 정량적 결과: {result}

### 변환 규칙
1. 첫 문장에 핵심 성과를 배치 (결과 → 행동 순)
2. 가능한 모든 성과를 숫자로 표현
3. 동사는 능동형으로 시작 (예: 개발했다, 이끌었다, 달성했다)
4. 1-3문장으로 압축
5. 직무 관련 키워드 포함

### 출력 형식
## STAR 분석
- Situation: ...
- Task: ...
- Action: ...
- Result: ...

## 변환된 경력 기술
[1-3문장의 임팩트 있는 경력 기술]

## 추가 개선 팁
- ...
"""


# ============================================================================
# 신입 이력서 특화 프롬프트 (경력 없는 경우)
# ============================================================================

ENTRY_LEVEL_RESUME_FEEDBACK = """### 역할
당신은 신입 채용 전문 HR 매니저입니다.
경력이 없는 지원자의 잠재력을 평가하는 데 전문성이 있습니다.

### 작업
경력이 없는 신입 지원자의 이력서를 분석하고,
경험 부족을 보완할 수 있는 전략적 피드백을 제공하세요.

### 지원 정보
- 지원 직무: {job_position}
- 전공: {major}
- 학년/졸업예정: {graduation_status}

### 이력서 내용
{resume_content}

### 분석 기준
1. **학업 성과 활용**: 관련 프로젝트, 논문, 수업 경험
2. **대외 활동**: 인턴, 동아리, 봉사, 공모전 등
3. **자기개발**: 자격증, 온라인 강의, 사이드 프로젝트
4. **소프트 스킬**: 커뮤니케이션, 협업, 문제 해결
5. **성장 잠재력**: 학습 의지, 열정, 목표 의식

### 출력 형식
## 종합 평가: [X/100점]

## 강점 활용 전략
1. [강점] → [이렇게 표현하면 더 효과적]
2. ...

## 경험 부족 보완 전략
1. [부족한 부분] → [이렇게 보완 가능]
2. ...

## 지원 직무 맞춤 조언
- 이 직무에서 가장 중요하게 보는 역량: ...
- 현재 이력서에서 강조해야 할 부분: ...
- 추가로 준비하면 좋을 것: ...
"""


# ============================================================================
# 이력서 ATS 최적화 프롬프트
# ============================================================================

ATS_OPTIMIZATION = """### 역할
당신은 ATS(Applicant Tracking System) 최적화 전문가입니다.
다양한 ATS 시스템의 알고리즘을 분석한 경험이 있습니다.

### 작업
이력서가 ATS를 통과할 수 있도록 키워드와 형식을 최적화하세요.

### 지원 정보
- 지원 직무: {job_position}
- 채용 공고 내용: {job_description}

### 이력서 내용
{resume_content}

### 분석 항목
1. **키워드 매칭률**: 채용 공고와 이력서 키워드 일치도
2. **필수 자격 충족**: JD에서 요구하는 필수 조건 충족 여부
3. **형식 적합성**: ATS가 파싱하기 좋은 형식인지
4. **섹션 구조**: 표준 섹션 헤더 사용 여부

### 출력 형식
## ATS 통과 예상 점수: [X/100점]

## 키워드 분석
| 채용공고 키워드 | 이력서 포함 여부 | 추가 위치 제안 |
|----------------|-----------------|---------------|
| ... | O/X | ... |

## 누락된 필수 키워드
1. [키워드] - [추가할 위치와 문맥]
2. ...

## 형식 개선 사항
1. ...
2. ...

## 최적화된 이력서 섹션 (예시)
[가장 개선이 필요한 섹션의 최적화 버전]
"""


# ============================================================================
# 프롬프트 함수
# ============================================================================

def get_resume_feedback_prompt(
    resume_content: str,
    job_position: str,
    company_type: str = "일반 기업",
    experience_level: str = "신입"
) -> str:
    """
    이력서 종합 첨삭 프롬프트 생성

    Parameters
    ----------
    resume_content : str
        이력서 전체 내용
    job_position : str
        지원 직무 (예: "백엔드 개발자", "마케팅 매니저")
    company_type : str
        회사 유형 (예: "대기업", "스타트업", "외국계")
    experience_level : str
        경력 수준 (예: "신입", "3년차", "시니어")

    Returns
    -------
    str
        완성된 프롬프트
    """
    return RESUME_COMPREHENSIVE_FEEDBACK.format(
        resume_content=resume_content,
        job_position=job_position,
        company_type=company_type,
        experience_level=experience_level
    )


def get_star_conversion_prompt(
    original_description: str,
    situation: str = "",
    task: str = "",
    action: str = "",
    result: str = ""
) -> str:
    """
    경력 기술 STAR 변환 프롬프트 생성

    Parameters
    ----------
    original_description : str
        원본 경력 기술 문장
    situation : str, optional
        상황/배경 설명
    task : str, optional
        담당 업무/책임
    action : str, optional
        구체적 행동
    result : str, optional
        정량적 결과

    Returns
    -------
    str
        완성된 프롬프트
    """
    return EXPERIENCE_STAR_CONVERSION.format(
        original_description=original_description,
        situation=situation or "정보 없음",
        task=task or "정보 없음",
        action=action or "정보 없음",
        result=result or "정보 없음"
    )


def get_entry_level_prompt(
    resume_content: str,
    job_position: str,
    major: str,
    graduation_status: str
) -> str:
    """
    신입 이력서 특화 피드백 프롬프트 생성

    Parameters
    ----------
    resume_content : str
        이력서 전체 내용
    job_position : str
        지원 직무
    major : str
        전공
    graduation_status : str
        학년/졸업예정 (예: "4학년 2학기", "2024년 2월 졸업예정")

    Returns
    -------
    str
        완성된 프롬프트
    """
    return ENTRY_LEVEL_RESUME_FEEDBACK.format(
        resume_content=resume_content,
        job_position=job_position,
        major=major,
        graduation_status=graduation_status
    )


def get_ats_optimization_prompt(
    resume_content: str,
    job_position: str,
    job_description: str
) -> str:
    """
    ATS 최적화 프롬프트 생성

    Parameters
    ----------
    resume_content : str
        이력서 전체 내용
    job_position : str
        지원 직무
    job_description : str
        채용 공고 전문

    Returns
    -------
    str
        완성된 프롬프트
    """
    return ATS_OPTIMIZATION.format(
        resume_content=resume_content,
        job_position=job_position,
        job_description=job_description
    )
