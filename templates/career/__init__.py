# -*- coding: utf-8 -*-
"""취업 준비 프롬프트 모듈"""

from .resume_feedback import (
    get_resume_feedback_prompt,
    get_star_conversion_prompt,
    get_entry_level_prompt,
    get_ats_optimization_prompt
)

from .cover_letter_feedback import (
    get_cover_letter_feedback_prompt,
    get_motivation_feedback_prompt,
    get_background_story_prompt,
    get_future_plan_prompt
)

__all__ = [
    'get_resume_feedback_prompt',
    'get_star_conversion_prompt',
    'get_entry_level_prompt',
    'get_ats_optimization_prompt',
    'get_cover_letter_feedback_prompt',
    'get_motivation_feedback_prompt',
    'get_background_story_prompt',
    'get_future_plan_prompt'
]
