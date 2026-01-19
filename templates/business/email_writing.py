# -*- coding: utf-8 -*-
"""
================================================================================
비즈니스 이메일 작성 프롬프트 모듈 (Business Email Writing Prompts)
================================================================================

## 이 모듈의 목적
실무자가 다양한 비즈니스 상황에서 효과적인 이메일을 작성할 수 있도록 지원

## 대상 사용자
- 직장인, 사업가, 프리랜서
- 고객 응대 담당자
- 영업 및 마케팅 담당자

## 프롬프트 설계 원칙
1. 목적 명확성: 이메일의 목적이 첫 문단에 드러남
2. 간결성: 불필요한 수식어 제거, 핵심 전달
3. 톤 조절: 상황에 맞는 격식 수준 조절
4. 행동 유도: 명확한 CTA(Call-to-Action) 포함

## 이메일 유형
- 공식 업무 이메일
- 사과/해명 이메일
- 제안/협력 요청 이메일
- 후속 조치 이메일
================================================================================
"""

from typing import Dict, List, Optional


# ============================================================================
# 공식 업무 이메일 프롬프트
# ============================================================================

FORMAL_EMAIL_TEMPLATE = """### 역할
당신은 20년 경력의 비즈니스 커뮤니케이션 전문가입니다.
대기업 임원진과 소통해본 경험이 풍부하고, 효과적인 비즈니스 이메일 작성의 노하우를 잘 알고 있습니다.

### 작업
아래 상황에 맞는 공식 업무 이메일을 작성하세요.

### 이메일 상황
- 발신자: {sender_name} ({sender_position})
- 수신자: {recipient_name} ({recipient_position})
- 발신자-수신자 관계: {relationship}
- 이메일 목적: {email_purpose}
- 핵심 전달 내용: {main_content}
- 원하는 응답/액션: {desired_action}

### 추가 맥락
{additional_context}

### 작성 기준
1. **첫 문장**: 이메일 목적을 명확히 밝힐 것
2. **본문**: 핵심 내용을 논리적 순서로 전개
3. **마무리**: 구체적인 요청사항과 기한 명시
4. **어조**: {tone} 어조 유지
5. **길이**: {length_preference}

### 출력 형식
## 이메일 제목
[간결하고 내용을 잘 요약하는 제목]

## 이메일 본문
[인사]

[목적 및 배경]

[핵심 내용]

[요청사항/다음 단계]

[마무리 인사]
[서명]

## 작성 포인트 해설
- 이 이메일이 효과적인 이유: ...
- 주의해야 할 점: ...
"""


# ============================================================================
# 사과/해명 이메일 프롬프트
# ============================================================================

APOLOGY_EMAIL_TEMPLATE = """### 역할
당신은 위기 커뮤니케이션 전문가입니다.
기업의 위기 상황에서 고객/파트너와의 관계를 회복시킨 경험이 풍부합니다.
진정성 있으면서도 법적 리스크를 최소화하는 사과문 작성에 전문성이 있습니다.

### 작업
아래 상황에 대한 사과/해명 이메일을 작성하세요.

### 상황 정보
- 발신자: {sender_name} ({sender_position})
- 수신자: {recipient_type}
- 문제 상황: {issue_description}
- 문제 발생 원인: {cause}
- 현재 조치 상황: {current_action}
- 향후 방지 대책: {prevention_plan}
- 보상 계획 (있는 경우): {compensation}

### 사과 이메일 핵심 원칙
1. **즉시 인정**: 변명 없이 문제를 인정
2. **공감 표현**: 상대방의 불편함에 공감
3. **구체적 설명**: 원인과 경위를 투명하게 설명
4. **해결책 제시**: 즉각적 조치와 재발 방지책
5. **보상 안내**: 적절한 보상이 있다면 명시
6. **신뢰 회복**: 향후 개선 의지 표명

### 어조
- {apology_level}의 사과 수준
- 진정성 있되 과도한 자책은 피함
- 법적 책임 인정에 주의 (필요시)

### 출력 형식
## 이메일 제목
[상황을 인지하고 있음을 보여주는 제목]

## 이메일 본문
[진정성 있는 시작]

[문제 상황 인정]

[원인 및 경위 설명]

[즉각 조치 사항]

[보상/해결책 안내]

[재발 방지 약속]

[마무리]

## 주의사항
- 이 표현은 피하세요: ...
- 법적 고려사항: ...
"""


# ============================================================================
# 제안/협력 요청 이메일 프롬프트
# ============================================================================

PROPOSAL_EMAIL_TEMPLATE = """### 역할
당신은 B2B 영업 및 비즈니스 개발 전문가입니다.
콜드 이메일부터 파트너십 제안까지 다양한 비즈니스 제안을 성사시킨 경험이 있습니다.
상대방의 입장에서 가치를 전달하는 설득력 있는 제안서 작성에 전문성이 있습니다.

### 작업
아래 내용으로 협력/제안 이메일을 작성하세요.

### 제안 정보
- 발신자 소개: {sender_intro}
- 수신자 정보: {recipient_info}
- 제안 내용: {proposal_content}
- 상대방에게 주는 가치: {value_proposition}
- 우리의 강점/자격: {our_qualifications}
- 원하는 협력 형태: {collaboration_type}
- 성공 사례 (있는 경우): {success_stories}

### 제안 이메일 전략
1. **Hook**: 첫 문장에서 관심 유발
2. **Pain Point**: 상대방의 문제/니즈 언급
3. **Solution**: 우리의 제안이 어떻게 해결책이 되는지
4. **Credibility**: 신뢰를 줄 수 있는 근거
5. **CTA**: 명확하고 부담없는 다음 단계

### 어조
- 전문적이면서 친근한 {tone}
- 강요하지 않되 명확한 가치 전달
- 상대방 입장 중심의 서술

### 출력 형식
## 이메일 제목
[클릭하고 싶은 흥미로운 제목 3가지 제안]
1. ...
2. ...
3. ...

## 이메일 본문
[관심을 끄는 도입]

[상대방의 상황/니즈 언급]

[제안 내용 및 가치]

[우리의 자격/성공 사례]

[명확한 다음 단계 제안]

[부담없는 마무리]

## A/B 테스트 변형
[다른 접근 방식의 오프닝 제안]
"""


# ============================================================================
# 후속 조치 이메일 프롬프트
# ============================================================================

FOLLOW_UP_EMAIL_TEMPLATE = """### 역할
당신은 고객 관계 관리 전문가입니다.
미팅 후속, 프로젝트 진행 상황 공유, 미응답 건 재요청 등
다양한 후속 이메일로 비즈니스 관계를 유지하고 발전시킨 경험이 있습니다.

### 작업
아래 상황에 맞는 후속 조치 이메일을 작성하세요.

### 상황 정보
- 이전 상호작용: {previous_interaction}
- 이전 상호작용 날짜: {interaction_date}
- 후속 조치 목적: {follow_up_purpose}
- 전달할 새로운 정보: {new_information}
- 상대방에게 요청할 액션: {requested_action}
- 긴급도: {urgency_level}

### 후속 이메일 유형
{follow_up_type}

### 후속 이메일 전략
1. **컨텍스트 상기**: 이전 대화/미팅 간단히 언급
2. **가치 추가**: 단순 재촉이 아닌 새로운 가치 제공
3. **명확한 요청**: 원하는 바를 구체적으로
4. **다음 단계 제시**: 상대방이 행동하기 쉽게

### 출력 형식
## 이메일 제목
[이전 맥락을 연결하면서 새로운 관심을 끄는 제목]

## 이메일 본문
[이전 상호작용 간단 언급]

[새로운 정보/가치 제공]

[명확한 요청사항]

[다음 단계 제안]

[긍정적 마무리]

## 타이밍 조언
- 이 이메일을 보내기 좋은 시점: ...
- 응답이 없을 경우 추가 후속 전략: ...
"""


# ============================================================================
# 프롬프트 함수
# ============================================================================

def get_formal_email_prompt(
    sender_name: str,
    sender_position: str,
    recipient_name: str,
    recipient_position: str,
    relationship: str,
    email_purpose: str,
    main_content: str,
    desired_action: str,
    additional_context: str = "",
    tone: str = "공손하고 전문적인",
    length_preference: str = "간결하게 (200-300자)"
) -> str:
    """
    공식 업무 이메일 작성 프롬프트 생성

    Parameters
    ----------
    sender_name : str
        발신자 이름
    sender_position : str
        발신자 직책
    recipient_name : str
        수신자 이름
    recipient_position : str
        수신자 직책
    relationship : str
        발신자-수신자 관계 (예: "첫 연락", "기존 거래처", "상사")
    email_purpose : str
        이메일 목적
    main_content : str
        핵심 전달 내용
    desired_action : str
        원하는 응답/액션
    additional_context : str, optional
        추가 맥락 정보
    tone : str
        원하는 어조
    length_preference : str
        선호하는 길이

    Returns
    -------
    str
        완성된 프롬프트
    """
    return FORMAL_EMAIL_TEMPLATE.format(
        sender_name=sender_name,
        sender_position=sender_position,
        recipient_name=recipient_name,
        recipient_position=recipient_position,
        relationship=relationship,
        email_purpose=email_purpose,
        main_content=main_content,
        desired_action=desired_action,
        additional_context=additional_context or "특별한 맥락 없음",
        tone=tone,
        length_preference=length_preference
    )


def get_apology_email_prompt(
    sender_name: str,
    sender_position: str,
    recipient_type: str,
    issue_description: str,
    cause: str,
    current_action: str,
    prevention_plan: str,
    compensation: str = "",
    apology_level: str = "중간 수준"
) -> str:
    """
    사과/해명 이메일 작성 프롬프트 생성

    Parameters
    ----------
    sender_name : str
        발신자 이름
    sender_position : str
        발신자 직책
    recipient_type : str
        수신자 유형 (예: "고객", "파트너사", "내부 팀")
    issue_description : str
        문제 상황 설명
    cause : str
        문제 발생 원인
    current_action : str
        현재 조치 상황
    prevention_plan : str
        향후 방지 대책
    compensation : str, optional
        보상 계획
    apology_level : str
        사과 수준 (예: "경미한", "중간 수준", "심각한")

    Returns
    -------
    str
        완성된 프롬프트
    """
    return APOLOGY_EMAIL_TEMPLATE.format(
        sender_name=sender_name,
        sender_position=sender_position,
        recipient_type=recipient_type,
        issue_description=issue_description,
        cause=cause,
        current_action=current_action,
        prevention_plan=prevention_plan,
        compensation=compensation or "별도 보상 없음",
        apology_level=apology_level
    )


def get_proposal_email_prompt(
    sender_intro: str,
    recipient_info: str,
    proposal_content: str,
    value_proposition: str,
    our_qualifications: str,
    collaboration_type: str,
    success_stories: str = "",
    tone: str = "전문적이면서 친근한"
) -> str:
    """
    제안/협력 요청 이메일 작성 프롬프트 생성

    Parameters
    ----------
    sender_intro : str
        발신자/회사 소개
    recipient_info : str
        수신자/회사 정보
    proposal_content : str
        제안 내용
    value_proposition : str
        상대방에게 주는 가치
    our_qualifications : str
        우리의 강점/자격
    collaboration_type : str
        원하는 협력 형태
    success_stories : str, optional
        성공 사례
    tone : str
        원하는 어조

    Returns
    -------
    str
        완성된 프롬프트
    """
    return PROPOSAL_EMAIL_TEMPLATE.format(
        sender_intro=sender_intro,
        recipient_info=recipient_info,
        proposal_content=proposal_content,
        value_proposition=value_proposition,
        our_qualifications=our_qualifications,
        collaboration_type=collaboration_type,
        success_stories=success_stories or "사례 정보 없음",
        tone=tone
    )


def get_follow_up_email_prompt(
    previous_interaction: str,
    interaction_date: str,
    follow_up_purpose: str,
    new_information: str,
    requested_action: str,
    urgency_level: str = "보통",
    follow_up_type: str = "미팅 후속"
) -> str:
    """
    후속 조치 이메일 작성 프롬프트 생성

    Parameters
    ----------
    previous_interaction : str
        이전 상호작용 내용
    interaction_date : str
        이전 상호작용 날짜
    follow_up_purpose : str
        후속 조치 목적
    new_information : str
        전달할 새로운 정보
    requested_action : str
        상대방에게 요청할 액션
    urgency_level : str
        긴급도 (예: "낮음", "보통", "높음")
    follow_up_type : str
        후속 이메일 유형

    Returns
    -------
    str
        완성된 프롬프트
    """
    return FOLLOW_UP_EMAIL_TEMPLATE.format(
        previous_interaction=previous_interaction,
        interaction_date=interaction_date,
        follow_up_purpose=follow_up_purpose,
        new_information=new_information,
        requested_action=requested_action,
        urgency_level=urgency_level,
        follow_up_type=follow_up_type
    )
