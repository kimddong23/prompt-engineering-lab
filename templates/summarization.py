"""요약 프롬프트 템플릿"""


def get_summary_prompt(text: str, style: str = "paragraph", length: int = 3) -> str:
    """
    요약 프롬프트 생성

    Args:
        text: 요약할 텍스트
        style: "paragraph", "bullet", "tldr"
        length: 문장/항목 수

    Returns:
        구조화된 요약 프롬프트

    Example:
        >>> prompt = get_summary_prompt("긴 텍스트...", style="bullet", length=5)
        >>> response = llm.invoke(prompt)
    """
    styles = {
        "paragraph": f"{length}문장으로 요약하세요.",
        "bullet": f"{length}개 핵심 포인트로 정리하세요.",
        "tldr": "1-2문장으로 초간단 요약하세요.",
    }

    return f"""### 지시사항
아래 텍스트를 요약하세요.

### 규칙
- {styles.get(style, styles["paragraph"])}
- 원문에 없는 내용 추가 금지
- 핵심 정보만 포함

### 텍스트
{text}

### 요약"""


def get_summary_prompt_with_cot(text: str, length: int = 3) -> str:
    """
    Chain of Thought 방식 요약 프롬프트

    Args:
        text: 요약할 텍스트
        length: 요약 문장 수

    Returns:
        CoT 요약 프롬프트
    """
    return f"""### 지시사항
아래 텍스트를 {length}문장으로 요약하세요.

### 단계
1. 먼저 텍스트의 주요 주제를 파악하세요
2. 핵심 정보와 부가 정보를 구분하세요
3. 핵심 정보만으로 {length}문장 요약을 작성하세요

### 텍스트
{text}

### 분석 및 요약"""
