# -*- coding: utf-8 -*-
"""
================================================================================
비즈니스 문서 프롬프트 108회 실험 (Business Document Prompt 108 Experiments)
================================================================================

## 이 스크립트의 목적
비즈니스 이메일, 보고서 작성 프롬프트의 효과를 108회 실험으로 검증

## 108배 원칙
불교의 108배처럼, 충분한 반복으로 통계적으로 유의미한 결과 도출

## 실험 구성
- 이메일 작성 프롬프트: 54회
- 보고서 작성 프롬프트: 54회

## 평가 지표
1. 응답 품질 (1-10점): 구조, 전문성, 실용성
2. 필수 요소 포함율: 예상 요소 중 포함된 비율
3. 토큰 효율성: 입출력 토큰 대비 정보량
================================================================================
"""

import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Any

# Windows 한글 출력 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from langchain_ollama import ChatOllama
import tiktoken

# 테스트 케이스 및 프롬프트 임포트
from evaluation.business_test_cases import (
    get_all_business_test_cases,
    get_email_test_cases,
    get_report_test_cases,
    BusinessTestCase
)
from templates.business.email_writing import (
    get_formal_email_prompt,
    get_apology_email_prompt,
    get_proposal_email_prompt,
    get_follow_up_email_prompt
)
from templates.business.report_writing import (
    get_weekly_report_prompt,
    get_analysis_report_prompt,
    get_meeting_minutes_prompt,
    get_project_proposal_prompt
)


class BusinessExperimentRunner:
    """
    비즈니스 문서 프롬프트 실험 실행기

    108회 실험을 자동으로 수행하고 결과를 기록
    """

    def __init__(self, model: str = "qwen2.5:7b"):
        """
        실험 실행기 초기화

        Parameters
        ----------
        model : str
            사용할 Ollama 모델
        """
        self.llm = ChatOllama(model=model, temperature=0.3)
        self.enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.results = []
        self.model = model

    def count_tokens(self, text: str) -> int:
        """토큰 수 계산"""
        return len(self.enc.encode(text))

    def evaluate_response_quality(self, response: str, expected_elements: List[str]) -> Dict:
        """
        응답 품질 평가

        Parameters
        ----------
        response : str
            LLM 응답
        expected_elements : List[str]
            예상되는 필수 요소 리스트

        Returns
        -------
        Dict
            평가 결과
        """
        # 필수 요소 포함율 계산
        found_elements = 0
        for element in expected_elements:
            # 요소의 핵심 키워드로 매칭
            keywords = element.lower().replace(" ", "")
            if any(kw in response.lower() for kw in [keywords, element.lower()]):
                found_elements += 1

        element_coverage = found_elements / len(expected_elements) if expected_elements else 0

        # 구조화된 형식 여부 확인
        has_structure = any([
            "##" in response,
            "|" in response,  # 표 형식
            "1." in response or "- " in response,  # 목록
        ])

        # 전문적 어조 확인
        professional_markers = [
            "드립니다", "감사합니다", "검토", "확인",
            "말씀", "부탁", "안내", "요청"
        ]
        professionalism = sum(1 for marker in professional_markers if marker in response)

        # 종합 점수 (1-10)
        quality_score = 0
        quality_score += min(element_coverage * 4, 4)  # 최대 4점
        quality_score += 3 if has_structure else 0  # 구조화 3점
        quality_score += min(professionalism * 0.5, 3)  # 전문성 최대 3점

        return {
            "quality_score": round(quality_score, 2),
            "element_coverage": round(element_coverage * 100, 1),
            "has_structure": has_structure,
            "professionalism_score": professionalism,
            "found_elements": found_elements,
            "total_elements": len(expected_elements)
        }

    def generate_prompt(self, test_case: BusinessTestCase) -> str:
        """테스트 케이스에 맞는 프롬프트 생성"""
        if test_case.category == "email":
            if test_case.subcategory == "formal":
                return get_formal_email_prompt(
                    sender_name="김철수",
                    sender_position="과장",
                    recipient_name="이영희",
                    recipient_position="부장",
                    relationship="업무 관계",
                    email_purpose=test_case.scenario,
                    main_content=test_case.input_context,
                    desired_action="검토 및 회신"
                )
            elif test_case.subcategory == "apology":
                return get_apology_email_prompt(
                    sender_name="김철수",
                    sender_position="팀장",
                    recipient_type="고객",
                    issue_description=test_case.input_context,
                    cause="내부 프로세스 문제",
                    current_action="즉시 조치 중",
                    prevention_plan="프로세스 개선"
                )
            elif test_case.subcategory == "proposal":
                return get_proposal_email_prompt(
                    sender_intro="ABC 회사 사업개발팀",
                    recipient_info=test_case.industry + " 담당자",
                    proposal_content=test_case.input_context,
                    value_proposition="업무 효율 향상",
                    our_qualifications="관련 분야 10년 경험",
                    collaboration_type="파트너십"
                )
            else:  # follow_up
                return get_follow_up_email_prompt(
                    previous_interaction=test_case.input_context,
                    interaction_date="지난 주",
                    follow_up_purpose=test_case.scenario,
                    new_information="추가 정보",
                    requested_action="검토 및 회신"
                )
        else:  # report
            if test_case.subcategory == "weekly":
                return get_weekly_report_prompt(
                    reporter_name="김철수 과장",
                    department=test_case.industry,
                    report_to="팀장",
                    period_start="2024-01-15",
                    period_end="2024-01-19",
                    raw_content=test_case.input_context,
                    achievements="주요 업무 완료",
                    issues="특별 이슈 없음",
                    next_plans="다음 주 계획"
                )
            elif test_case.subcategory == "analysis":
                return get_analysis_report_prompt(
                    analysis_type=test_case.scenario,
                    analysis_purpose="전략 수립",
                    analysis_target=test_case.industry,
                    collected_data=test_case.input_context,
                    background_info="시장 환경 변화"
                )
            elif test_case.subcategory == "meeting":
                return get_meeting_minutes_prompt(
                    meeting_title=test_case.scenario,
                    meeting_datetime="2024-01-20 14:00",
                    meeting_location="회의실 A",
                    attendees="관련 팀원",
                    meeting_purpose="업무 논의",
                    meeting_content=test_case.input_context,
                    discussion_points="주요 안건",
                    decisions="결정 사항"
                )
            else:  # project
                return get_project_proposal_prompt(
                    project_name=test_case.scenario,
                    project_type=test_case.industry,
                    background=test_case.input_context,
                    objectives="목표 달성",
                    current_situation="현재 상황",
                    proposal_details="제안 내용",
                    expected_benefits="기대 효과",
                    budget="예산 미정",
                    resources="인력 배정 예정",
                    timeline="3개월",
                    risks="리스크 관리 필요"
                )

    def run_single_experiment(self, test_case: BusinessTestCase) -> Dict:
        """
        단일 실험 실행

        Parameters
        ----------
        test_case : BusinessTestCase
            테스트 케이스

        Returns
        -------
        Dict
            실험 결과
        """
        # 프롬프트 생성
        prompt = self.generate_prompt(test_case)

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
            test_case.expected_elements
        ) if success else {}

        return {
            "test_case_id": test_case.id,
            "category": test_case.category,
            "subcategory": test_case.subcategory,
            "scenario": test_case.scenario,
            "industry": test_case.industry,
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
        print("비즈니스 문서 프롬프트 108회 실험")
        print("=" * 70)
        print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"모델: {self.model}")
        print(f"실험 횟수: {limit}회")
        print()

        test_cases = get_all_business_test_cases()[:limit]
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
                    "element_coverages": []
                }
            stats = category_stats[cat]
            stats["count"] += 1
            stats["total_quality"] += r["quality_evaluation"].get("quality_score", 0)
            stats["total_tokens"] += r["total_tokens"]
            stats["total_time"] += r["response_time"]
            stats["element_coverages"].append(
                r["quality_evaluation"].get("element_coverage", 0)
            )

        # 평균 계산
        for cat, stats in category_stats.items():
            n = stats["count"]
            stats["avg_quality"] = round(stats["total_quality"] / n, 2)
            stats["avg_tokens"] = round(stats["total_tokens"] / n, 0)
            stats["avg_time"] = round(stats["total_time"] / n, 2)
            stats["avg_element_coverage"] = round(
                sum(stats["element_coverages"]) / n, 1
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
        detailed_path = f"results/business_experiments_{timestamp}.json"
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
            print(f"    - 필수 요소 포함율: {stats['avg_element_coverage']}%")
            print(f"    - 평균 토큰: {stats['avg_tokens']}")
        print()
        print(f"결과 저장: {detailed_path}")
        print("=" * 70)


def main():
    """메인 실행 함수"""
    runner = BusinessExperimentRunner(model="qwen2.5:7b")

    # 108회 실험 실행
    summary = runner.run_all_experiments(limit=108)

    print()
    print("108회 실험 완료!")


if __name__ == "__main__":
    main()
