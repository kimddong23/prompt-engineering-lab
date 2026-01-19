# -*- coding: utf-8 -*-
"""개발자 프롬프트 모듈"""

from .code_review import (
    get_code_review_prompt,
    get_security_review_prompt,
    get_performance_review_prompt,
    get_refactoring_prompt
)

from .documentation import (
    get_api_documentation_prompt,
    get_readme_prompt,
    get_code_comments_prompt,
    get_architecture_doc_prompt
)

__all__ = [
    'get_code_review_prompt',
    'get_security_review_prompt',
    'get_performance_review_prompt',
    'get_refactoring_prompt',
    'get_api_documentation_prompt',
    'get_readme_prompt',
    'get_code_comments_prompt',
    'get_architecture_doc_prompt'
]
