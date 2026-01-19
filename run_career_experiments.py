# -*- coding: utf-8 -*-
"""
================================================================================
취업 준비 프롬프트 108회 실험 (Career Prompt 108 Experiments)
================================================================================

## 이 스크립트의 목적
취업 준비 관련 프롬프트의 효과를 108회 실험으로 검증

## 108배 원칙
불교의 108배처럼, 충분한 반복으로 통계적으로 유의미한 결과 도출

## 실험 구성
- 이력서 첨삭 프롬프트: 36회
- 자기소개서 피드백 프롬프트: 36회
- 면접 답변 코칭 프롬프트: 36회

## 평가 지표
1. 응답 품질 (1-10점): 피드백의 구체성, 실용성
2. 문제점 발견율: 예상 문제점 중 몇 개를 찾았는지
3. 개선안 제시율: 실행 가능한 개선안 제시 여부
4. 토큰 효율성: 입출력 토큰 대비 정보량
================================================================================
"""

import sys
import json
import time
import re
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import asdict

# Windows 한글 출력 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

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
    get_entry_level_prompt
)
from templates.career.cover_letter_feedback import (
    get_cover_letter_feedback_prompt,
    get_motivation_feedback_prompt
)


class CareerExperimentRunner:
    """
    취업 준비 프롬프트 실험 실행기

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

    def evaluate_response_quality(self, response: str, expected_issues: List[str]) -> Dict:
        """
        응답 품질 평가

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
        # 문제점 발견율 계산
        found_issues = 0
        for issue in expected_issues:
            # 핵심 키워드 추출하여 매칭
            keywords = issue.replace(" ", "").lower()
            if any(kw in response.lower() for kw in keywords.split("/")):
                found_issues += 1

        issue_detection_rate = found_issues / len(expected_issues) if expected_issues else 0

        # 구조화된 피드백 여부 확인
        has_structure = any([
            "##" in response,
            "강점" in response or "장점" in response,
            "개선" in response or "수정" in response,
            "→" in response or "->" in response
        ])

        # 구체적 개선안 포함 여부
        has_specific_suggestions = any([
            "예:" in response or "예시:" in response,
            "변경:" in response or "수정:" in response,
            "[" in response and "]" in response
        ])

        # 종합 점수 (1-10)
        quality_score = 0
        quality_score += min(issue_detection_rate * 4, 4)  # 최대 4점
        quality_score += 3 if has_structure else 0  # 구조화 3점
        quality_score += 3 if has_specific_suggestions else 0  # 구체성 3점

        return {
            "quality_score": round(quality_score, 2),
            "issue_detection_rate": round(issue_detection_rate * 100, 1),
            "has_structure": has_structure,
            "has_specific_suggestions": has_specific_suggestions,
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
        # 프롬프트 생성
        if test_case.category == "resume":
            prompt = get_resume_feedback_prompt(
                resume_content=test_case.input_content,
                job_position=test_case.job_position,
                company_type=test_case.company_type,
                experience_level=test_case.experience_level
            )
        elif test_case.category == "cover_letter":
            prompt = get_cover_letter_feedback_prompt(
                question="자기소개서 항목",
                answer=test_case.input_content,
                company_name=test_case.company_type,
                job_position=test_case.job_position
            )
        else:  # interview
            prompt = f"""### 역할
당신은 20년 경력의 면접관입니다. 다양한 기업에서 면접을 진행한 경험이 있습니다.

### 작업
아래 면접 답변을 평가하고 개선 피드백을 제공하세요.

### 지원 직무
{test_case.job_position}

### 면접 답변
{test_case.input_content}

### 평가 기준
1. STAR 구조 (Situation-Task-Action-Result)
2. 구체성과 진정성
3. 직무 연관성
4. 논리적 흐름

### 출력 형식
## 현재 답변 평가
- 점수: /10
- 강점: ...
- 약점: ...

## 개선된 답변
[STAR 구조로 재구성된 답변]

## 추가 조언
- ...
"""

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
        detailed_path = f"results/career_experiments_{timestamp}.json"
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
    runner = CareerExperimentRunner(model="qwen2.5:7b")

    # 108회 실험 실행
    summary = runner.run_all_experiments(limit=108)

    print()
    print("108회 실험 완료!")


if __name__ == "__main__":
    main()
