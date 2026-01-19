# -*- coding: utf-8 -*-
"""비즈니스 문서 작성 프롬프트 모듈"""

from .email_writing import (
    get_formal_email_prompt,
    get_apology_email_prompt,
    get_proposal_email_prompt,
    get_follow_up_email_prompt
)

from .report_writing import (
    get_weekly_report_prompt,
    get_analysis_report_prompt,
    get_meeting_minutes_prompt,
    get_project_proposal_prompt
)

__all__ = [
    'get_formal_email_prompt',
    'get_apology_email_prompt',
    'get_proposal_email_prompt',
    'get_follow_up_email_prompt',
    'get_weekly_report_prompt',
    'get_analysis_report_prompt',
    'get_meeting_minutes_prompt',
    'get_project_proposal_prompt'
]
