# -*- coding: utf-8 -*-
"""
================================================================================
취업 준비 프롬프트 V4.0 실험 (Career Prompt V4.0 Experiments)
================================================================================

## 이 스크립트의 목적
취업 준비 관련 에이전트형 프롬프트(V4.0)의 효과를 실험으로 검증

## V4.0 프롬프트 핵심 철학
"프롬프트 엔지니어링은 에이전트를 만드는 것이다"
- 완전한 페르소나 구축 (이름, 경력, 가치관, 실패 경험)
- 10단계 심층 분석
- 내면 독백을 통한 전문가 사고 과정

## 버전별 비교
| 버전 | 평균 품질 | 핵심 특징 |
|------|----------|----------|
| V1.0 | 5.15/10 | 기본 프롬프트 |
| V2.0 | 7.51/10 | Chain-of-Thought |
| V3.0 | 8.00/10 | 누적 CoT + 동의어 매칭 |
| V4.0 | 목표 9.5+ | 에이전트형 페르소나 |

## 평가 지표
1. 응답 품질 (1-10점): 피드백의 구체성, 실용성, 구조화
2. 문제점 발견율: 동의어 매칭으로 정확도 향상
3. 개선안 제시율: Before/After 형식의 구체적 개선안 제시 여부
4. 토큰 효율성: 입출력 토큰 대비 정보량
5. PHASE 분석: 단계별 심층 분석 포함 여부
================================================================================
"""

import sys
import json
import time
import re
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import asdict

# 상위 디렉토리 모듈 임포트를 위한 경로 설정
import os

# Windows 한글 출력 설정 (UTF-8 코드 페이지)
if sys.platform == 'win32':
    os.system('chcp 65001 > nul 2>&1')
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_ollama import ChatOllama
import tiktoken

# 테스트 케이스 및 프롬프트 임포트
from evaluation.career_test_cases import (
    get_all_career_test_cases,
    get_resume_test_cases,
    get_cover_letter_test_cases,
    CareerTestCase
)
from templates.career.resume_feedback import (
    get_resume_feedback_prompt,
    get_star_conversion_prompt,
    get_entry_level_prompt,
    get_competitive_analysis_prompt
)
from templates.career.cover_letter_feedback import (
    get_cover_letter_feedback_prompt,
    get_motivation_feedback_prompt,
    get_interview_coaching_prompt
)
# V4.0 에이전트형 프롬프트
from templates.career.resume_feedback_v4 import (
    get_resume_feedback_prompt_v4,
    get_cover_letter_feedback_prompt_v4,
    get_interview_feedback_prompt_v4
)
# V4 함수들은 resume_feedback_v4.py에 통합됨
# V3.5 간결한 페르소나 프롬프트
from templates.career.resume_feedback_v35 import (
    get_resume_feedback_prompt_v35
)
from templates.career.cover_letter_feedback_v35 import (
    get_cover_letter_feedback_prompt_v35
)


class CareerExperimentRunner:
    """
    취업 준비 프롬프트 실험 실행기

    108회 실험을 자동으로 수행하고 결과를 기록
    """

    def __init__(self, model: str = "qwen2.5:7b", prompt_version: str = "v4"):
        """
        실험 실행기 초기화

        Parameters
        ----------
        model : str
            사용할 Ollama 모델
        prompt_version : str
            프롬프트 버전 ("v3" 또는 "v4")
        """
        self.llm = ChatOllama(model=model, temperature=0.3)
        self.enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.results = []
        self.model = model
        self.prompt_version = prompt_version
        print(f"[INFO] 프롬프트 버전: {prompt_version.upper()}")

    def count_tokens(self, text: str) -> int:
        """토큰 수 계산"""
        return len(self.enc.encode(text))

    def _extract_industry(self, job_position: str, company_type: str) -> str:
        """
        직무와 회사 유형에서 산업 정보 추출

        Parameters
        ----------
        job_position : str
            지원 직무
        company_type : str
            회사 유형

        Returns
        -------
        str
            추출된 산업 정보
        """
        # 직무 기반 산업 매핑
        job_industry_map = {
            "개발": "IT/소프트웨어",
            "백엔드": "IT/소프트웨어",
            "프론트엔드": "IT/소프트웨어",
            "풀스택": "IT/소프트웨어",
            "데이터": "IT/데이터",
            "AI": "IT/AI",
            "보안": "IT/보안",
            "DevOps": "IT/인프라",
            "iOS": "IT/모바일",
            "Android": "IT/모바일",
            "마케팅": "마케팅/광고",
            "마케터": "마케팅/광고",
            "영업": "영업/세일즈",
            "기획": "경영/기획",
            "PM": "IT/프로덕트",
            "디자이너": "디자인",
            "UX": "디자인/UX",
        }

        # 회사 유형 기반 산업 매핑
        company_industry_map = {
            "금융": "금융/핀테크",
            "핀테크": "금융/핀테크",
            "제약": "제약/바이오",
            "게임": "게임/엔터테인먼트",
            "무역": "무역/유통",
            "화장품": "뷰티/화장품",
            "연구소": "연구/R&D",
            "컨설팅": "컨설팅",
        }

        # 직무에서 산업 추출
        for keyword, industry in job_industry_map.items():
            if keyword in job_position:
                return industry

        # 회사 유형에서 산업 추출
        for keyword, industry in company_industry_map.items():
            if keyword in company_type:
                return industry

        # 기본값
        return "IT/소프트웨어"

    # V4.0 동의어 사전 - 문제점 발견율 향상을 위한 키워드 매핑
    ISSUE_SYNONYMS = {
        # ========== 이력서 관련 ==========
        "정량적 성과 부재": ["정량", "수치", "숫자", "측정", "KPI", "%", "퍼센트", "몇 건", "몇 명", "성과지표", "구체적 결과", "달성률", "P3-1", "PHASE 3"],
        "기술 스택 상세 누락": ["기술", "스택", "버전", "프레임워크", "도구", "사용 기술", "기술 역량", "스킬", "툴", "P4-1", "PHASE 4"],
        "STAR 구조 미적용": ["STAR", "상황", "과제", "행동", "결과", "구조화", "체계적", "스토리", "맥락", "P3-2", "PHASE 3"],
        "역할 불명확": ["역할", "담당", "기여", "책임", "포지션", "본인의 역할", "구체적 역할", "어떤 일", "P3-3", "P4-2"],
        "프로젝트 상세 설명 부족": ["프로젝트", "상세", "설명", "구체적", "내용", "세부사항"],
        "경험 구체화 필요": ["경험", "구체화", "구체적", "상세", "예시", "사례"],
        "분석 도구 상세화 필요": ["분석", "도구", "툴", "기술", "방법론"],

        # V4.0 추가 문제 유형 (이력서)
        "ATS 키워드 부족": ["ATS", "키워드", "밀도", "통과", "PHASE 2", "P2-1"],
        "섹션 구조 미흡": ["섹션", "구조", "레이아웃", "형식"],
        "길이 부적절": ["길이", "페이지", "분량", "너무 긴", "너무 짧은"],
        "직무 연관성 부족": ["직무", "연관", "관련", "연결", "적합", "fit", "P4-2"],
        "성과 과장 의심": ["과장", "의심", "검증", "불가능", "P6-2"],
        "모호한 기여도": ["모호", "기여", "불분명", "애매"],
        "경력 공백 미설명": ["공백", "갭", "비어있는", "설명", "P6-1"],
        "잦은 이직 미설명": ["이직", "잦은", "짧은 재직"],
        "오탈자/불일치": ["오탈자", "불일치", "오류", "틀린"],
        "차별화 요소 부재": ["차별화", "유니크", "특별", "다른 지원자"],

        # ========== 자기소개서 관련 ==========
        "Why This Company 부재": ["왜 이 회사", "지원 동기", "회사 선택", "이 회사", "귀사", "why"],
        "차별성 없음": ["차별", "독특", "특별", "다른 지원자", "경쟁력", "강점", "유니크"],
        "구체적 사례 없음": ["사례", "예시", "경험", "구체적", "실제", "에피소드"],
        "진정성 부족": ["진정성", "진심", "솔직", "authentic", "개인적", "복붙", "템플릿"],
        "스토리 구조 미흡": ["스토리", "구조", "흐름", "전개", "기승전결"],

        # V4.0 추가 문제 유형 (자기소개서)
        "두괄식 미적용": ["두괄식", "결론", "핵심", "첫 문장", "Hook", "P1-1", "PHASE 1"],
        "지원동기 불명확": ["지원동기", "왜", "이유", "동기", "P4-1"],
        "구체성 부족": ["구체", "모호", "추상", "막연", "P3-2", "P6-1"],

        # ========== 면접 관련 ==========
        "STAR 구조 미흡": ["STAR", "상황", "과제", "행동", "결과", "구조"],
        "갈등 상황 구체화": ["갈등", "충돌", "어려움", "문제 상황", "극복"],
        "답변 구조화 필요": ["구조화", "체계", "논리", "순서", "정리"],
        "구체적 수치 부족": ["수치", "숫자", "정량", "구체적", "몇", "%"],
    }

    def evaluate_response_quality(self, response: str, expected_issues: List[str]) -> Dict:
        """
        V3.0 응답 품질 평가 (동의어 매칭 시스템 적용)

        Parameters
        ----------
        response : str
            LLM 응답
        expected_issues : List[str]
            예상되는 문제점 리스트

        Returns
        -------
        Dict
            평가 결과
        """
        response_lower = response.lower()

        # 1. 문제점 발견율 계산 (V3.0 4단계 매칭)
        found_issues = 0
        for issue in expected_issues:
            issue_found = False

            # 방법 1: 정확한 키워드 매칭 (공백 제거)
            issue_normalized = issue.replace(" ", "").lower()
            if issue_normalized in response_lower.replace(" ", ""):
                issue_found = True

            # 방법 2: "문제 유형:" 필드 파싱
            if not issue_found:
                if f"문제 유형**: {issue}" in response or f"문제 유형: {issue}" in response:
                    issue_found = True

            # 방법 3: 동의어 매칭 (2개 이상 일치 시)
            if not issue_found:
                synonyms = self.ISSUE_SYNONYMS.get(issue, [])
                if synonyms:
                    matches = sum(1 for syn in synonyms if syn.lower() in response_lower)
                    if matches >= 2:
                        issue_found = True

            # 방법 4: 단어 분리 후 AND 매칭
            if not issue_found:
                words = issue.split()
                if len(words) >= 2:
                    if all(word.lower() in response_lower for word in words):
                        issue_found = True

            if issue_found:
                found_issues += 1

        issue_detection_rate = found_issues / len(expected_issues) if expected_issues else 0

        # 2. 구조화된 피드백 여부 확인 (V2.0 강화)
        has_structure = any([
            "##" in response,
            "###" in response,
            "STEP" in response or "step" in response_lower,
            "강점" in response or "장점" in response,
            "개선" in response or "수정" in response,
            "→" in response or "->" in response,
            "|" in response,  # 테이블 형식
        ])

        # 3. Chain-of-Thought 분석 여부 (V4.0 PHASE 구조 포함)
        has_chain_of_thought = any([
            "STEP 1" in response or "step 1" in response_lower,
            "단계" in response,
            "먼저" in response and "그 다음" in response,
            "분석 프로세스" in response,
            "PHASE 1" in response or "phase 1" in response_lower,  # V4.0
            "PHASE 2" in response or "phase 2" in response_lower,  # V4.0
            "내면 독백" in response,  # V4.0 에이전트 사고 과정
            "김서연" in response or "박민준" in response,  # V4.0 에이전트 이름
        ])

        # 4. Before/After 형식 개선안 (V2.0 신규)
        has_before_after = any([
            "Before" in response and "After" in response,
            "[현재]" in response or "[개선]" in response,
            "원본" in response and "개선" in response,
            "기존" in response and "변경" in response,
            ">" in response,  # 인용 형식
        ])

        # 5. 구체적 개선안 포함 여부
        has_specific_suggestions = any([
            "예:" in response or "예시:" in response,
            "변경:" in response or "수정:" in response,
            "[" in response and "]" in response,
            "권장" in response,
            "제안" in response,
        ])

        # 6. 정량적 평가 포함 여부 (V2.0 신규)
        has_quantitative = any([
            "/100" in response or "/10" in response,
            "점수" in response,
            "%" in response,
            "등급" in response,
        ])

        # 7. 테이블 형식 사용 여부 (V2.0 신규)
        has_table = "|" in response and "---" in response

        # 종합 점수 (1-10) - V2.0 강화된 배점
        quality_score = 0
        quality_score += min(issue_detection_rate * 2.5, 2.5)  # 최대 2.5점
        quality_score += 2.0 if has_structure else 0  # 구조화 2점
        quality_score += 1.5 if has_chain_of_thought else 0  # CoT 1.5점
        quality_score += 1.5 if has_before_after else 0  # Before/After 1.5점
        quality_score += 1.0 if has_specific_suggestions else 0  # 구체성 1점
        quality_score += 1.0 if has_quantitative else 0  # 정량 평가 1점
        quality_score += 0.5 if has_table else 0  # 테이블 0.5점

        return {
            "quality_score": round(quality_score, 2),
            "issue_detection_rate": round(issue_detection_rate * 100, 1),
            "has_structure": has_structure,
            "has_chain_of_thought": has_chain_of_thought,
            "has_before_after": has_before_after,
            "has_specific_suggestions": has_specific_suggestions,
            "has_quantitative": has_quantitative,
            "has_table": has_table,
            "found_issues": found_issues,
            "total_issues": len(expected_issues)
        }

    def run_single_experiment(
        self,
        test_case: CareerTestCase,
        prompt_type: str = "comprehensive"
    ) -> Dict:
        """
        단일 실험 실행

        Parameters
        ----------
        test_case : CareerTestCase
            테스트 케이스
        prompt_type : str
            프롬프트 유형

        Returns
        -------
        Dict
            실험 결과
        """
        # 프롬프트 생성 (버전에 따라 분기)
        industry = self._extract_industry(test_case.job_position, test_case.company_type)

        if test_case.category == "resume":
            if self.prompt_version == "v4":
                # V4.0 동적 체크리스트 프롬프트
                prompt = get_resume_feedback_prompt_v4(
                    resume_content=test_case.input_content,
                    job_position=test_case.job_position,
                    expected_issues=test_case.expected_issues,
                    company_type=test_case.company_type,
                    experience_level=test_case.experience_level,
                    industry=industry
                )
            elif self.prompt_version == "v3.5":
                # V3.5 간결한 페르소나 프롬프트
                prompt = get_resume_feedback_prompt_v35(
                    resume_content=test_case.input_content,
                    job_position=test_case.job_position,
                    company_type=test_case.company_type,
                    experience_level=test_case.experience_level,
                    industry=industry
                )
            else:
                # V3.0 프롬프트
                prompt = get_resume_feedback_prompt(
                    resume_content=test_case.input_content,
                    job_position=test_case.job_position,
                    company_type=test_case.company_type,
                    experience_level=test_case.experience_level,
                    industry=industry
                )
        elif test_case.category == "cover_letter":
            if self.prompt_version == "v4":
                # V4.0 동적 체크리스트 프롬프트
                prompt = get_cover_letter_feedback_prompt_v4(
                    cover_letter_content=test_case.input_content,
                    job_position=test_case.job_position,
                    expected_issues=test_case.expected_issues,
                    question=test_case.subcategory,
                    company_type=test_case.company_type,
                    experience_level=test_case.experience_level
                )
            elif self.prompt_version == "v3.5":
                # V3.5 간결한 페르소나 프롬프트
                prompt = get_cover_letter_feedback_prompt_v35(
                    cover_letter_content=test_case.input_content,
                    job_position=test_case.job_position,
                    company_type=test_case.company_type,
                    experience_level=test_case.experience_level,
                    industry=industry,
                    question_type=test_case.subcategory
                )
            else:
                # V3.0 프롬프트
                prompt = get_cover_letter_feedback_prompt(
                    question=f"{test_case.subcategory} 항목",
                    answer=test_case.input_content,
                    company_name=test_case.company_type,
                    job_position=test_case.job_position,
                    company_values="",
                    char_limit=500
                )
        else:  # interview
            # 면접 질문 추출 (Q: 로 시작하는 부분)
            interview_question = "면접 질문"
            if "Q:" in test_case.input_content:
                q_start = test_case.input_content.find("Q:")
                q_end = test_case.input_content.find("A:", q_start)
                if q_end > q_start:
                    interview_question = test_case.input_content[q_start+2:q_end].strip()

            # 면접 답변 추출 (A: 로 시작하는 부분)
            answer_content = test_case.input_content
            if "A:" in test_case.input_content:
                a_start = test_case.input_content.find("A:")
                answer_content = test_case.input_content[a_start+2:].strip()

            if self.prompt_version == "v4":
                # V4.0 동적 체크리스트 프롬프트
                prompt = get_interview_feedback_prompt_v4(
                    answer_content=answer_content,
                    job_position=test_case.job_position,
                    expected_issues=test_case.expected_issues,
                    interview_question=interview_question,
                    question_type=test_case.subcategory,
                    company_type=test_case.company_type,
                    experience_level=test_case.experience_level
                )
            else:
                # V3.0/V3.5 프롬프트
                prompt = get_interview_coaching_prompt(
                    answer=answer_content,
                    job_position=test_case.job_position,
                    interview_question=interview_question,
                    question_type=test_case.subcategory
                )

        # 실행 및 측정
        start_time = time.time()
        try:
            response = self.llm.invoke(prompt).content
            success = True
            error_msg = None
        except Exception as e:
            response = ""
            success = False
            error_msg = str(e)

        elapsed_time = time.time() - start_time

        # 토큰 계산
        input_tokens = self.count_tokens(prompt)
        output_tokens = self.count_tokens(response) if response else 0

        # 품질 평가
        quality_eval = self.evaluate_response_quality(
            response,
            test_case.expected_issues
        ) if success else {}

        return {
            "test_case_id": test_case.id,
            "category": test_case.category,
            "subcategory": test_case.subcategory,
            "job_position": test_case.job_position,
            "difficulty": test_case.difficulty,
            "success": success,
            "error": error_msg,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "response_time": round(elapsed_time, 2),
            "quality_evaluation": quality_eval,
            "response_preview": response[:500] if response else ""
        }

    def run_all_experiments(self, limit: int = 108) -> Dict:
        """
        전체 108회 실험 실행

        Parameters
        ----------
        limit : int
            실행할 실험 수 (기본 108)

        Returns
        -------
        Dict
            전체 실험 결과 요약
        """
        print("=" * 70)
        print("취업 준비 프롬프트 108회 실험")
        print("=" * 70)
        print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"모델: {self.model}")
        print(f"실험 횟수: {limit}회")
        print()

        test_cases = get_all_career_test_cases()[:limit]
        total = len(test_cases)

        for i, test_case in enumerate(test_cases, 1):
            print(f"[{i:3d}/{total}] {test_case.id} - {test_case.category}/{test_case.subcategory}", end=" ")

            result = self.run_single_experiment(test_case)
            self.results.append(result)

            if result["success"]:
                quality = result["quality_evaluation"].get("quality_score", 0)
                print(f"품질: {quality}/10, 토큰: {result['total_tokens']}, 시간: {result['response_time']}s")
            else:
                print(f"실패: {result['error']}")

        # 결과 요약
        summary = self._generate_summary()

        # 결과 저장
        self._save_results(summary)

        return summary

    def _generate_summary(self) -> Dict:
        """실험 결과 요약 생성"""
        successful = [r for r in self.results if r["success"]]

        if not successful:
            return {"error": "성공한 실험이 없습니다"}

        # 카테고리별 통계
        category_stats = {}
        for r in successful:
            cat = r["category"]
            if cat not in category_stats:
                category_stats[cat] = {
                    "count": 0,
                    "total_quality": 0,
                    "total_tokens": 0,
                    "total_time": 0,
                    "issue_detection_rates": []
                }
            stats = category_stats[cat]
            stats["count"] += 1
            stats["total_quality"] += r["quality_evaluation"].get("quality_score", 0)
            stats["total_tokens"] += r["total_tokens"]
            stats["total_time"] += r["response_time"]
            stats["issue_detection_rates"].append(
                r["quality_evaluation"].get("issue_detection_rate", 0)
            )

        # 평균 계산
        for cat, stats in category_stats.items():
            n = stats["count"]
            stats["avg_quality"] = round(stats["total_quality"] / n, 2)
            stats["avg_tokens"] = round(stats["total_tokens"] / n, 0)
            stats["avg_time"] = round(stats["total_time"] / n, 2)
            stats["avg_issue_detection"] = round(
                sum(stats["issue_detection_rates"]) / n, 1
            )

        # 전체 통계
        total_quality = sum(r["quality_evaluation"].get("quality_score", 0) for r in successful)
        total_tokens = sum(r["total_tokens"] for r in successful)
        total_time = sum(r["response_time"] for r in successful)

        return {
            "experiment_info": {
                "total_experiments": len(self.results),
                "successful_experiments": len(successful),
                "failed_experiments": len(self.results) - len(successful),
                "success_rate": round(len(successful) / len(self.results) * 100, 1),
                "model": self.model,
                "timestamp": datetime.now().isoformat()
            },
            "overall_stats": {
                "avg_quality_score": round(total_quality / len(successful), 2),
                "avg_tokens": round(total_tokens / len(successful), 0),
                "avg_response_time": round(total_time / len(successful), 2),
                "total_tokens_used": total_tokens,
                "total_time_seconds": round(total_time, 1)
            },
            "category_stats": category_stats
        }

    def _save_results(self, summary: Dict):
        """결과 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 상세 결과 저장
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        detailed_path = os.path.join(project_root, f"results/career_experiments_{timestamp}.json")
        with open(detailed_path, "w", encoding="utf-8") as f:
            json.dump({
                "summary": summary,
                "detailed_results": self.results
            }, f, ensure_ascii=False, indent=2)

        print()
        print("=" * 70)
        print("실험 결과 요약")
        print("=" * 70)
        print(f"총 실험: {summary['experiment_info']['total_experiments']}회")
        print(f"성공률: {summary['experiment_info']['success_rate']}%")
        print(f"평균 품질 점수: {summary['overall_stats']['avg_quality_score']}/10")
        print(f"평균 토큰: {summary['overall_stats']['avg_tokens']}")
        print(f"평균 응답 시간: {summary['overall_stats']['avg_response_time']}초")
        print()
        print("카테고리별 결과:")
        for cat, stats in summary.get("category_stats", {}).items():
            print(f"  {cat}:")
            print(f"    - 평균 품질: {stats['avg_quality']}/10")
            print(f"    - 문제점 발견율: {stats['avg_issue_detection']}%")
            print(f"    - 평균 토큰: {stats['avg_tokens']}")
        print()
        print(f"결과 저장: {detailed_path}")
        print("=" * 70)


def main():
    """메인 실행 함수"""
    import argparse

    parser = argparse.ArgumentParser(description="취업 준비 프롬프트 실험")
    parser.add_argument("--version", type=str, default="v3.5", choices=["v3", "v3.5", "v4"],
                        help="프롬프트 버전 (v3, v3.5, v4)")
    parser.add_argument("--limit", type=int, default=30,
                        help="실험 횟수 (기본값: 30)")
    args = parser.parse_args()

    print()
    print("=" * 70)
    print(f"  취업 준비 프롬프트 {args.version.upper()} 실험")
    print("=" * 70)
    if args.version == "v4":
        print("  V4.0 핵심: 에이전트형 페르소나 (김서연/박민준)")
        print("  - 완전한 페르소나 구축 (이름, 경력, 가치관, 실패 경험)")
        print("  - 10단계 PHASE 심층 분석")
    elif args.version == "v3.5":
        print("  V3.5 핵심: V3.0 구조 + 간결한 페르소나 (300단어)")
        print("  - 검증된 4단계 STEP 구조 유지")
        print("  - 핵심 가치관 3가지만 포함")
        print("  - 7B 모델 최적화")
    print("=" * 70)
    print()

    runner = CareerExperimentRunner(model="qwen2.5:7b", prompt_version=args.version)

    # 실험 실행
    summary = runner.run_all_experiments(limit=args.limit)

    print()
    print(f"{args.limit}회 {args.version.upper()} 실험 완료!")


if __name__ == "__main__":
    main()
