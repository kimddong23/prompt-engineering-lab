# -*- coding: utf-8 -*-
"""
================================================================================
자기소개서 첨삭 프롬프트 모듈 (Cover Letter Feedback Prompts)
================================================================================

## 이 모듈의 목적
취준생의 자기소개서를 분석하고 설득력 있는 스토리텔링으로 개선하는 프롬프트

## 대상 사용자
- 신입/경력 취준생
- 이직 준비자
- 대학원 지원자

## 프롬프트 설계 원칙
1. 두괄식 구조 (핵심 메시지 → 근거 → 결론)
2. 구체적 에피소드 기반 스토리텔링
3. 지원 회사/직무와의 연결성 강화
4. 진정성과 차별성 동시 확보

## 자기소개서 항목별 전략
- 성장과정: 가치관 형성 스토리
- 성격/장단점: 직무 연관성 있는 특성
- 지원동기: 회사-나의 교집합
- 입사 후 포부: 구체적 기여 계획
================================================================================
"""

from typing import Dict, List, Optional


# ============================================================================
# 자기소개서 종합 첨삭 프롬프트
# ============================================================================

COVER_LETTER_COMPREHENSIVE = """### 역할
당신은 20년 경력의 커리어 컨설턴트입니다.
대기업 인사팀 출신으로, 수만 건의 자기소개서를 평가한 경험이 있습니다.
합격하는 자기소개서의 패턴과 탈락하는 자기소개서의 공통점을 잘 알고 있습니다.

### 작업
아래 자기소개서를 분석하고, 합격 가능성을 높이는 구체적인 피드백을 제공하세요.

### 지원 정보
- 지원 회사: {company_name}
- 지원 직무: {job_position}
- 회사의 인재상: {company_values}

### 자기소개서 문항 및 답변
**문항**: {question}
**글자 수 제한**: {char_limit}자

**작성한 답변**:
{answer}

### 평가 기준
1. **두괄식 구조**: 첫 문장에 핵심 메시지가 있는지
2. **구체성**: 추상적 표현 대신 구체적 사례가 있는지
3. **직무 연관성**: 지원 직무와 경험의 연결이 명확한지
4. **차별성**: 다른 지원자와 구별되는 나만의 스토리가 있는지
5. **진정성**: 과장 없이 진솔하게 느껴지는지
6. **회사 이해도**: 지원 회사에 대한 이해가 드러나는지

### 출력 형식
## 종합 점수: [X/100점]

## 문장별 분석
| 순번 | 원문 | 문제점 | 개선안 |
|-----|------|-------|-------|
| 1 | "..." | ... | "..." |
| 2 | "..." | ... | "..." |

## 구조 분석
- 도입부 (첫 1-2문장): [평가]
- 본론 (에피소드): [평가]
- 결론 (포부/다짐): [평가]

## 핵심 개선 포인트
1. **가장 시급한 수정**: ...
2. **추가하면 좋을 내용**: ...
3. **삭제해야 할 내용**: ...

## 개선된 버전 (전체 재작성)
[글자 수 제한 내에서 개선된 전체 답변]
"""


# ============================================================================
# 지원동기 특화 프롬프트
# ============================================================================

MOTIVATION_FEEDBACK = """### 역할
당신은 기업 채용 담당자입니다.
매일 수백 개의 지원동기를 읽고, 그 중 진정성 있는 지원동기를 가려내는 일을 합니다.

### 작업
아래 지원동기를 평가하고, "이 회사에 꼭 와야 하는 이유"가 명확히 드러나도록 개선하세요.

### 지원 정보
- 지원 회사: {company_name}
- 회사 사업/서비스: {company_business}
- 지원 직무: {job_position}
- 회사 핵심 가치: {company_values}

### 작성한 지원동기
{motivation_text}

### 지원동기 필수 요소 체크
1. **Why This Company**: 왜 다른 회사가 아닌 이 회사인가?
2. **Why This Role**: 왜 다른 직무가 아닌 이 직무인가?
3. **Why You**: 왜 다른 지원자가 아닌 내가 적합한가?
4. **Mutual Benefit**: 회사와 내가 서로 얻을 수 있는 것은?

### 출력 형식
## 현재 지원동기 진단

### 1. Why This Company 분석
- 현재 수준: [상/중/하]
- 문제점: ...
- 개선 방향: ...

### 2. Why This Role 분석
- 현재 수준: [상/중/하]
- 문제점: ...
- 개선 방향: ...

### 3. Why You 분석
- 현재 수준: [상/중/하]
- 문제점: ...
- 개선 방향: ...

### 4. Mutual Benefit 분석
- 현재 수준: [상/중/하]
- 문제점: ...
- 개선 방향: ...

## 개선된 지원동기
[4가지 요소가 모두 포함된 개선 버전]
"""


# ============================================================================
# 성장과정/가치관 프롬프트
# ============================================================================

BACKGROUND_STORY_FEEDBACK = """### 역할
당신은 스토리텔링 전문가이자 커리어 코치입니다.
개인의 경험을 직무 역량과 연결하는 스토리 구성에 전문성이 있습니다.

### 작업
아래 성장과정/가치관 답변을 분석하고,
직무와 연결되는 의미 있는 스토리로 재구성하세요.

### 지원 직무
{job_position}

### 직무에서 요구하는 핵심 역량
{required_competencies}

### 작성한 성장과정/가치관
{background_text}

### 스토리텔링 체크리스트
1. **갈등/전환점**: 성장의 계기가 되는 사건이 있는가?
2. **가치관 형성**: 그 경험에서 어떤 가치관이 형성되었는가?
3. **직무 연결**: 그 가치관이 지원 직무와 어떻게 연결되는가?
4. **구체적 묘사**: 추상적 설명 대신 생생한 장면이 있는가?

### 출력 형식
## 현재 스토리 진단
- 갈등/전환점: [있음/없음/약함] - ...
- 가치관 형성: [명확/불명확] - ...
- 직무 연결: [강함/약함/없음] - ...
- 구체성: [높음/보통/낮음] - ...

## 스토리 재구성 제안

### 추천 구조
1. 도입 (후킹): ...
2. 배경 설명: ...
3. 갈등/도전: ...
4. 극복 과정: ...
5. 깨달음/성장: ...
6. 직무 연결: ...

### 개선된 버전
[직무와 연결되는 스토리로 재구성]
"""


# ============================================================================
# 입사 후 포부 프롬프트
# ============================================================================

FUTURE_PLAN_FEEDBACK = """### 역할
당신은 기업의 팀장급 면접관입니다.
신입/경력 사원의 입사 후 포부를 듣고, 실현 가능성과 조직 적합성을 평가합니다.

### 작업
아래 입사 후 포부를 분석하고,
구체적이고 실현 가능하며 회사에 기여할 수 있는 내용으로 개선하세요.

### 지원 정보
- 지원 회사: {company_name}
- 지원 직무: {job_position}
- 해당 직무의 일반적 커리어 패스: {career_path}

### 작성한 입사 후 포부
{future_plan_text}

### 입사 후 포부 평가 기준
1. **구체성**: 막연한 포부가 아닌 구체적 계획이 있는가?
2. **실현 가능성**: 현실적으로 달성 가능한 목표인가?
3. **회사 기여**: 개인 성장 외에 회사에 대한 기여가 있는가?
4. **단계적 계획**: 단기/중기/장기 계획이 구분되어 있는가?
5. **직무 이해도**: 해당 직무에 대한 이해가 드러나는가?

### 출력 형식
## 현재 포부 진단

| 평가 항목 | 점수 | 피드백 |
|----------|------|--------|
| 구체성 | /10 | ... |
| 실현 가능성 | /10 | ... |
| 회사 기여 | /10 | ... |
| 단계적 계획 | /10 | ... |
| 직무 이해도 | /10 | ... |
| **총점** | **/50** | |

## 문제점 분석
1. ...
2. ...

## 개선된 입사 후 포부

### 단기 목표 (입사 후 1년)
...

### 중기 목표 (3년 후)
...

### 장기 목표 (5-10년 후)
...

### 통합 버전 (자기소개서용)
[위 내용을 자연스럽게 연결한 완성본]
"""


# ============================================================================
# 프롬프트 함수
# ============================================================================

def get_cover_letter_feedback_prompt(
    question: str,
    answer: str,
    company_name: str,
    job_position: str,
    company_values: str = "",
    char_limit: int = 500
) -> str:
    """
    자기소개서 종합 첨삭 프롬프트 생성

    Parameters
    ----------
    question : str
        자기소개서 문항
    answer : str
        작성한 답변
    company_name : str
        지원 회사명
    job_position : str
        지원 직무
    company_values : str, optional
        회사 인재상/핵심가치
    char_limit : int
        글자 수 제한

    Returns
    -------
    str
        완성된 프롬프트
    """
    return COVER_LETTER_COMPREHENSIVE.format(
        question=question,
        answer=answer,
        company_name=company_name,
        job_position=job_position,
        company_values=company_values or "정보 없음",
        char_limit=char_limit
    )


def get_motivation_feedback_prompt(
    motivation_text: str,
    company_name: str,
    company_business: str,
    job_position: str,
    company_values: str = ""
) -> str:
    """
    지원동기 피드백 프롬프트 생성

    Parameters
    ----------
    motivation_text : str
        작성한 지원동기
    company_name : str
        지원 회사명
    company_business : str
        회사 사업/서비스 설명
    job_position : str
        지원 직무
    company_values : str, optional
        회사 핵심가치

    Returns
    -------
    str
        완성된 프롬프트
    """
    return MOTIVATION_FEEDBACK.format(
        motivation_text=motivation_text,
        company_name=company_name,
        company_business=company_business,
        job_position=job_position,
        company_values=company_values or "정보 없음"
    )


def get_background_story_prompt(
    background_text: str,
    job_position: str,
    required_competencies: str
) -> str:
    """
    성장과정/가치관 피드백 프롬프트 생성

    Parameters
    ----------
    background_text : str
        작성한 성장과정/가치관
    job_position : str
        지원 직무
    required_competencies : str
        직무 요구 역량

    Returns
    -------
    str
        완성된 프롬프트
    """
    return BACKGROUND_STORY_FEEDBACK.format(
        background_text=background_text,
        job_position=job_position,
        required_competencies=required_competencies
    )


def get_future_plan_prompt(
    future_plan_text: str,
    company_name: str,
    job_position: str,
    career_path: str = ""
) -> str:
    """
    입사 후 포부 피드백 프롬프트 생성

    Parameters
    ----------
    future_plan_text : str
        작성한 입사 후 포부
    company_name : str
        지원 회사명
    job_position : str
        지원 직무
    career_path : str, optional
        해당 직무의 커리어 패스

    Returns
    -------
    str
        완성된 프롬프트
    """
    return FUTURE_PLAN_FEEDBACK.format(
        future_plan_text=future_plan_text,
        company_name=company_name,
        job_position=job_position,
        career_path=career_path or "일반적인 커리어 패스"
    )
