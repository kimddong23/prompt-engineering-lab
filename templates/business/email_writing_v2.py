# -*- coding: utf-8 -*-
"""
================================================================================
비즈니스 이메일 프롬프트 V2.0 - 독자 중심 글쓰기
================================================================================

## V2.0 핵심 철학
"받는 사람의 시간은 소중하다"

## 기존 V1.0의 문제점
1. 역할 부여가 추상적 ("20년 경력 전문가")
2. 단계별 사고 과정 없음
3. 출력 형식만 강제, 내용 품질은 방치
4. expected_elements와 연동 없음

## V2.0 개선 사항
1. 구체적 원칙 기반 페르소나
2. 4단계 STEP 구조 (분석 → 설계 → 작성 → 검토)
3. 필수 요소 명시적 포함 유도
4. "So What?" 검증 단계

================================================================================
"""

from typing import Dict, List, Optional


# ============================================================================
# V2.0 공식 업무 이메일 프롬프트
# ============================================================================

FORMAL_EMAIL_V2_TEMPLATE = """### 역할 및 원칙

당신은 비즈니스 커뮤니케이션 전문가입니다.

**나의 3가지 원칙:**
1. **"3초 룰"** - 받는 사람이 3초 안에 목적을 파악해야 함
2. **"So What?"** - 모든 문장에 "그래서 뭘 해달라는 건데?"가 답이 있어야 함
3. **"하나의 이메일, 하나의 목적"** - 여러 용건을 섞지 않음

---

### 상황 정보

- **발신자**: {sender_name} ({sender_position})
- **수신자**: {recipient_name} ({recipient_position})
- **관계**: {relationship}
- **이메일 목적**: {email_purpose}
- **전달 내용**: {main_content}
- **원하는 행동**: {desired_action}
- **추가 맥락**: {additional_context}

---

### STEP 1: 독자 분석 (30초)

다음 질문에 답하세요:
1. 수신자가 이 이메일을 읽고 **가장 먼저 알고 싶은 것**은?
2. 수신자가 **해야 할 행동**은 무엇인가?
3. 수신자의 **시간적 여유**는? (바쁜 임원 vs 담당자)

---

### STEP 2: 핵심 메시지 설계

**한 문장 요약**: 이 이메일의 목적을 한 문장으로:
> "[누가] [무엇을] [언제까지] 해주시기 바랍니다"

**필수 포함 요소**:
- 명확한 목적
- {expected_element_1}
- {expected_element_2}
- {expected_element_3}
- {expected_element_4}

---

### STEP 3: 이메일 작성

다음 구조로 작성하세요:

## 이메일 제목
[목적이 명확히 드러나는 제목]

## 이메일 본문

[인사 - 1줄]

[목적 - 첫 문장에서 용건 명시]

[배경/상세 - 필요한 정보만 간결하게]

[요청사항 - 구체적인 행동과 기한]

[마무리 - 감사 인사]

[서명]

---

### STEP 4: 자가 검토

작성한 이메일을 다음 기준으로 점검:
- [ ] 제목만 보고 용건을 파악할 수 있는가?
- [ ] 첫 문장에서 목적이 드러나는가?
- [ ] 불필요한 수식어는 없는가?
- [ ] 요청사항과 기한이 명확한가?

## 작성 포인트 해설
- 이 이메일의 강점: ...
- 주의할 점: ...
"""


# ============================================================================
# V2.0 사과/해명 이메일 프롬프트
# ============================================================================

APOLOGY_EMAIL_V2_TEMPLATE = """### 역할 및 원칙

당신은 위기 커뮤니케이션 전문가입니다.

**사과 이메일의 3가지 원칙:**
1. **"즉시, 진심으로"** - 변명보다 사과가 먼저
2. **"투명하게"** - 숨기면 더 큰 위기가 됨
3. **"행동으로"** - 말보다 해결책

---

### 상황 정보

- **발신자**: {sender_name} ({sender_position})
- **수신 대상**: {recipient_type}
- **문제 상황**: {issue_description}
- **발생 원인**: {cause}
- **현재 조치**: {current_action}
- **재발 방지책**: {prevention_plan}
- **보상 계획**: {compensation}
- **사과 수준**: {apology_level}

---

### STEP 1: 상황 분석

1. **문제의 심각도**: 고객에게 미친 실질적 피해는?
2. **책임 범위**: 우리 잘못인가, 외부 요인인가?
3. **고객 감정**: 지금 어떤 감정 상태일까?

---

### STEP 2: 사과 전략 수립

**핵심 메시지**:
> "우리는 [문제]를 인지하고 있으며, [해결책]으로 조치하겠습니다"

**필수 포함 요소**:
- 진심어린 사과
- {expected_element_1}
- {expected_element_2}
- {expected_element_3}
- {expected_element_4}

---

### STEP 3: 사과 이메일 작성

## 이메일 제목
[문제 인지를 보여주되, 패닉을 유발하지 않는 제목]

## 이메일 본문

[진심어린 사과로 시작]

[문제 상황 간결히 설명 - 변명 없이]

[발생 원인 - 투명하게]

[현재 조치 상황 - 구체적으로]

[재발 방지 약속]

[보상 안내 (있는 경우)]

[마무리 - 신뢰 회복 의지]

---

### STEP 4: 리스크 검토

- [ ] 과도한 책임 인정으로 법적 문제는 없는가?
- [ ] 충분히 진정성이 느껴지는가?
- [ ] 구체적인 해결책이 제시되었는가?

## 주의사항
- 피해야 할 표현: ...
- 법적 고려사항: ...
"""


# ============================================================================
# V2.0 제안/협력 요청 이메일 프롬프트
# ============================================================================

PROPOSAL_EMAIL_V2_TEMPLATE = """### 역할 및 원칙

당신은 비즈니스 개발 전문가입니다.

**제안 이메일의 3가지 원칙:**
1. **"상대방 입장에서"** - 내가 아닌 상대방의 이익 중심
2. **"증거로 말하기"** - 추상적 약속이 아닌 구체적 실적
3. **"쉬운 다음 단계"** - 부담없이 응할 수 있는 제안

---

### 상황 정보

- **발신자**: {sender_intro}
- **수신자**: {recipient_info}
- **제안 내용**: {proposal_content}
- **상대방 가치**: {value_proposition}
- **우리 역량**: {our_qualifications}
- **협력 형태**: {collaboration_type}
- **성공 사례**: {success_stories}
- **원하는 어조**: {tone}

---

### STEP 1: 상대방 분석

1. **그들의 Pain Point**: 지금 어떤 문제로 고민하고 있을까?
2. **의사결정 기준**: 무엇을 보고 제안을 수락할까?
3. **장벽**: 거절하는 가장 큰 이유는?

---

### STEP 2: 가치 제안 설계

**핵심 메시지**:
> "우리와 협력하면 [구체적 이익]을 얻을 수 있습니다"

**필수 포함 요소**:
- 회사/제안 소개
- {expected_element_1}
- {expected_element_2}
- {expected_element_3}
- {expected_element_4}

---

### STEP 3: 제안 이메일 작성

## 이메일 제목
[호기심을 유발하는 제목 3가지 제안]
1. ...
2. ...
3. ...

## 이메일 본문

[관심을 끄는 첫 문장 - 상대방의 상황 언급]

[Pain Point 공감]

[우리의 해결책과 가치]

[신뢰 근거 - 실적, 사례]

[부담없는 다음 단계 제안]

[긍정적 마무리]

---

### STEP 4: 설득력 검토

- [ ] 상대방 입장에서 "왜 나한테 좋지?"가 명확한가?
- [ ] 구체적인 숫자/사례가 있는가?
- [ ] 다음 단계가 부담없이 응할 수 있는가?

## A/B 테스트 변형
[다른 접근 방식의 오프닝 제안]
"""


# ============================================================================
# V2.0 후속 조치 이메일 프롬프트
# ============================================================================

FOLLOW_UP_EMAIL_V2_TEMPLATE = """### 역할 및 원칙

당신은 고객 관계 관리 전문가입니다.

**후속 이메일의 3가지 원칙:**
1. **"가치 추가"** - 단순 재촉이 아닌 새로운 가치 제공
2. **"맥락 연결"** - 이전 대화를 자연스럽게 이어감
3. **"쉬운 응답"** - 상대방이 행동하기 쉽게

---

### 상황 정보

- **이전 상호작용**: {previous_interaction}
- **상호작용 날짜**: {interaction_date}
- **후속 목적**: {follow_up_purpose}
- **새 정보**: {new_information}
- **요청 행동**: {requested_action}
- **긴급도**: {urgency_level}
- **후속 유형**: {follow_up_type}

---

### STEP 1: 상황 분석

1. **상대방 상황**: 왜 아직 응답이 없을까?
2. **적절한 톤**: 재촉 vs 부드러운 리마인드?
3. **새로 줄 가치**: 이전보다 추가로 제공할 것은?

---

### STEP 2: 후속 전략 수립

**핵심 메시지**:
> "이전 논의에 추가로 [새 가치]를 전달드리며, [요청]을 부탁드립니다"

**필수 포함 요소**:
- 이전 맥락 상기
- {expected_element_1}
- {expected_element_2}
- {expected_element_3}
- {expected_element_4}

---

### STEP 3: 후속 이메일 작성

## 이메일 제목
[이전 맥락 + 새 가치를 담은 제목]

## 이메일 본문

[이전 상호작용 간단 언급 - 1-2문장]

[새로운 정보/가치 제공]

[명확한 요청사항]

[쉬운 다음 단계 제시]

[긍정적 마무리]

---

### STEP 4: 효과 검토

- [ ] 단순 재촉이 아닌 가치를 주고 있는가?
- [ ] 상대방이 응답하기 쉬운가?
- [ ] 적절한 톤인가?

## 타이밍 조언
- 보내기 좋은 시점: ...
- 추가 후속 전략: ...
"""


# ============================================================================
# V2.0 프롬프트 함수
# ============================================================================

def get_formal_email_prompt_v2(
    sender_name: str,
    sender_position: str,
    recipient_name: str,
    recipient_position: str,
    relationship: str,
    email_purpose: str,
    main_content: str,
    desired_action: str,
    expected_elements: List[str],
    additional_context: str = ""
) -> str:
    """
    V2.0 공식 업무 이메일 프롬프트 생성

    핵심 변경: expected_elements를 프롬프트에 명시
    """
    # expected_elements를 4개로 맞춤 (부족하면 기본값)
    elements = expected_elements + ["구체적인 다음 단계"] * (4 - len(expected_elements))

    return FORMAL_EMAIL_V2_TEMPLATE.format(
        sender_name=sender_name,
        sender_position=sender_position,
        recipient_name=recipient_name,
        recipient_position=recipient_position,
        relationship=relationship,
        email_purpose=email_purpose,
        main_content=main_content,
        desired_action=desired_action,
        additional_context=additional_context or "특별한 맥락 없음",
        expected_element_1=elements[0],
        expected_element_2=elements[1],
        expected_element_3=elements[2],
        expected_element_4=elements[3]
    )


def get_apology_email_prompt_v2(
    sender_name: str,
    sender_position: str,
    recipient_type: str,
    issue_description: str,
    cause: str,
    current_action: str,
    prevention_plan: str,
    expected_elements: List[str],
    compensation: str = "",
    apology_level: str = "중간 수준"
) -> str:
    """V2.0 사과 이메일 프롬프트 생성"""
    elements = expected_elements + ["신뢰 회복 메시지"] * (4 - len(expected_elements))

    return APOLOGY_EMAIL_V2_TEMPLATE.format(
        sender_name=sender_name,
        sender_position=sender_position,
        recipient_type=recipient_type,
        issue_description=issue_description,
        cause=cause,
        current_action=current_action,
        prevention_plan=prevention_plan,
        compensation=compensation or "별도 보상 없음",
        apology_level=apology_level,
        expected_element_1=elements[0],
        expected_element_2=elements[1],
        expected_element_3=elements[2],
        expected_element_4=elements[3]
    )


def get_proposal_email_prompt_v2(
    sender_intro: str,
    recipient_info: str,
    proposal_content: str,
    value_proposition: str,
    our_qualifications: str,
    collaboration_type: str,
    expected_elements: List[str],
    success_stories: str = "",
    tone: str = "전문적이면서 친근한"
) -> str:
    """V2.0 제안 이메일 프롬프트 생성"""
    elements = expected_elements + ["다음 단계 제안"] * (4 - len(expected_elements))

    return PROPOSAL_EMAIL_V2_TEMPLATE.format(
        sender_intro=sender_intro,
        recipient_info=recipient_info,
        proposal_content=proposal_content,
        value_proposition=value_proposition,
        our_qualifications=our_qualifications,
        collaboration_type=collaboration_type,
        success_stories=success_stories or "사례 정보 없음",
        tone=tone,
        expected_element_1=elements[0],
        expected_element_2=elements[1],
        expected_element_3=elements[2],
        expected_element_4=elements[3]
    )


def get_follow_up_email_prompt_v2(
    previous_interaction: str,
    interaction_date: str,
    follow_up_purpose: str,
    new_information: str,
    requested_action: str,
    expected_elements: List[str],
    urgency_level: str = "보통",
    follow_up_type: str = "미팅 후속"
) -> str:
    """V2.0 후속 이메일 프롬프트 생성"""
    elements = expected_elements + ["다음 단계"] * (4 - len(expected_elements))

    return FOLLOW_UP_EMAIL_V2_TEMPLATE.format(
        previous_interaction=previous_interaction,
        interaction_date=interaction_date,
        follow_up_purpose=follow_up_purpose,
        new_information=new_information,
        requested_action=requested_action,
        urgency_level=urgency_level,
        follow_up_type=follow_up_type,
        expected_element_1=elements[0],
        expected_element_2=elements[1],
        expected_element_3=elements[2],
        expected_element_4=elements[3]
    )
