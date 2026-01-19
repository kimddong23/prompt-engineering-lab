"""프롬프트 엔지니어링 템플릿 모듈"""

from .summarization import get_summary_prompt
from .classification import get_classification_prompt

__all__ = ["get_summary_prompt", "get_classification_prompt"]
