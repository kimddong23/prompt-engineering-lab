"""분류 프롬프트 템플릿"""

from typing import List


def get_classification_prompt(
    text: str,
    categories: List[str],
    with_explanation: bool = False
) -> str:
    """
    분류 프롬프트 생성

    Args:
        text: 분류할 텍스트
        categories: 카테고리 목록
        with_explanation: 분류 이유 포함 여부

    Returns:
        구조화된 분류 프롬프트

    Example:
        >>> prompt = get_classification_prompt(
        ...     "오늘 비가 올까요?",
        ...     ["질문", "명령", "진술"],
        ...     with_explanation=True
        ... )
    """
    categories_str = ", ".join(categories)

    if with_explanation:
        output_format = """### 출력 형식 (JSON)
```json
{
    "category": "선택한 카테고리",
    "confidence": 0.0-1.0,
    "reason": "분류 이유"
}
```"""
    else:
        output_format = f"### 출력\n카테고리명만 출력하세요: {categories_str}"

    return f"""### 지시사항
아래 텍스트를 주어진 카테고리 중 하나로 분류하세요.

### 카테고리
{categories_str}

### 규칙
- 반드시 주어진 카테고리 중 하나만 선택
- 가장 적합한 카테고리 선택

{output_format}

### 텍스트
{text}

### 분류"""


def get_sentiment_prompt(text: str, detailed: bool = False) -> str:
    """
    감성 분석 프롬프트

    Args:
        text: 분석할 텍스트
        detailed: 상세 분석 여부

    Returns:
        감성 분석 프롬프트
    """
    if detailed:
        return f"""### 지시사항
아래 텍스트의 감성을 분석하세요.

### 출력 형식 (JSON)
```json
{{
    "sentiment": "긍정/부정/중립",
    "score": -1.0 ~ 1.0,
    "emotions": ["감정1", "감정2"],
    "key_phrases": ["핵심 표현1", "핵심 표현2"]
}}
```

### 텍스트
{text}

### 분석"""
    else:
        return f"""### 지시사항
아래 텍스트의 감성을 분석하세요.

### 출력
"긍정", "부정", "중립" 중 하나만 출력

### 텍스트
{text}

### 감성"""
