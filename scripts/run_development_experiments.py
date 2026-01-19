# -*- coding: utf-8 -*-
"""
================================================================================
개발자 프롬프트 108회 실험 (Development Prompt 108 Experiments)
================================================================================

## 이 스크립트의 목적
코드 리뷰, 문서화 프롬프트의 효과를 108회 실험으로 검증

## 108배 원칙
불교의 108배처럼, 충분한 반복으로 통계적으로 유의미한 결과 도출

## 실험 구성
- 코드 리뷰 프롬프트: 54회 (일반, 보안, 성능, 리팩토링)
- 문서화 프롬프트: 54회 (API, README, 주석, 아키텍처)

## 평가 지표
1. 응답 품질 (1-10점): 문제 발견율, 구체성
2. 이슈 탐지율: 예상 이슈 중 발견된 비율
3. 코드 제안 포함율: 개선된 코드 제시 여부
4. 토큰 효율성: 입출력 토큰 대비 정보량
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

# 상위 디렉토리 모듈 임포트를 위한 경로 설정
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_ollama import ChatOllama
import tiktoken

# 테스트 케이스 및 프롬프트 임포트
from evaluation.development_test_cases import (
    get_all_development_test_cases,
    get_code_review_test_cases,
    get_documentation_test_cases,
    DevelopmentTestCase
)
from templates.development.code_review import (
    get_code_review_prompt,
    get_security_review_prompt,
    get_performance_review_prompt,
    get_refactoring_prompt
)
from templates.development.documentation import (
    get_api_documentation_prompt,
    get_readme_prompt,
    get_code_comments_prompt,
    get_architecture_doc_prompt
)


class DevelopmentExperimentRunner:
    """
    개발자 프롬프트 실험 실행기

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

    def evaluate_response_quality(self, response: str, expected_issues: List[str], category: str) -> Dict:
        """
        응답 품질 평가

        Parameters
        ----------
        response : str
            LLM 응답
        expected_issues : List[str]
            예상되는 이슈/요소 리스트
        category : str
            테스트 카테고리

        Returns
        -------
        Dict
            평가 결과
        """
        # 이슈/요소 발견율 계산
        found_issues = 0
        response_lower = response.lower()

        for issue in expected_issues:
            # 이슈의 핵심 키워드로 매칭
            keywords = issue.lower().split()
            if any(kw in response_lower for kw in keywords):
                found_issues += 1

        issue_detection_rate = found_issues / len(expected_issues) if expected_issues else 0

        # 코드 블록 포함 여부
        has_code_block = "```" in response

        # 구조화된 형식 여부
        has_structure = any([
            "##" in response,
            "|" in response,  # 표 형식
            "라인" in response or "Line" in response.lower(),  # 라인 참조
        ])

        # 구체적 제안 포함 여부
        has_specific_suggestions = any([
            "변경" in response or "수정" in response,
            "->" in response or "=>" in response,
            "대신" in response or "권장" in response
        ])

        # 종합 점수 (1-10)
        quality_score = 0
        quality_score += min(issue_detection_rate * 4, 4)  # 최대 4점
        quality_score += 2 if has_code_block else 0  # 코드 블록 2점
        quality_score += 2 if has_structure else 0  # 구조화 2점
        quality_score += 2 if has_specific_suggestions else 0  # 구체성 2점

        return {
            "quality_score": round(quality_score, 2),
            "issue_detection_rate": round(issue_detection_rate * 100, 1),
            "has_code_block": has_code_block,
            "has_structure": has_structure,
            "has_specific_suggestions": has_specific_suggestions,
            "found_issues": found_issues,
            "total_issues": len(expected_issues)
        }

    def generate_prompt(self, test_case: DevelopmentTestCase) -> str:
        """테스트 케이스에 맞는 프롬프트 생성"""
        if test_case.category == "code_review":
            if test_case.subcategory == "general":
                return get_code_review_prompt(
                    code=test_case.code_snippet,
                    language=test_case.language,
                    filename="example." + test_case.language.lower()[:2],
                    code_purpose="일반 코드"
                )
            elif test_case.subcategory == "security":
                return get_security_review_prompt(
                    code=test_case.code_snippet,
                    language=test_case.language,
                    app_type="웹 애플리케이션"
                )
            elif test_case.subcategory == "performance":
                return get_performance_review_prompt(
                    code=test_case.code_snippet,
                    language=test_case.language
                )
            else:  # refactoring
                return get_refactoring_prompt(
                    code=test_case.code_snippet,
                    language=test_case.language
                )
        else:  # documentation
            if test_case.subcategory == "api":
                return get_api_documentation_prompt(
                    api_name="API 엔드포인트",
                    endpoint="/api/example",
                    http_method="POST",
                    api_purpose="데이터 처리",
                    request_params="JSON 본문",
                    response_format="JSON 응답"
                )
            elif test_case.subcategory == "readme":
                return get_readme_prompt(
                    project_name="Example Project",
                    one_liner="예제 프로젝트입니다",
                    main_features="주요 기능",
                    tech_stack=test_case.language,
                    installation="pip install 또는 npm install",
                    usage_example=test_case.code_snippet
                )
            elif test_case.subcategory == "comments":
                return get_code_comments_prompt(
                    code=test_case.code_snippet,
                    language=test_case.language
                )
            else:  # architecture
                return get_architecture_doc_prompt(
                    system_name="Example System",
                    system_purpose="시스템 설명",
                    main_features="주요 기능",
                    tech_stack=test_case.language,
                    components=test_case.code_snippet
                )

    def run_single_experiment(self, test_case: DevelopmentTestCase) -> Dict:
        """
        단일 실험 실행

        Parameters
        ----------
        test_case : DevelopmentTestCase
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
            test_case.expected_issues,
            test_case.category
        ) if success else {}

        return {
            "test_case_id": test_case.id,
            "category": test_case.category,
            "subcategory": test_case.subcategory,
            "language": test_case.language,
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
        print("개발자 프롬프트 108회 실험")
        print("=" * 70)
        print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"모델: {self.model}")
        print(f"실험 횟수: {limit}회")
        print()

        test_cases = get_all_development_test_cases()[:limit]
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
                    "issue_detection_rates": [],
                    "code_block_count": 0
                }
            stats = category_stats[cat]
            stats["count"] += 1
            stats["total_quality"] += r["quality_evaluation"].get("quality_score", 0)
            stats["total_tokens"] += r["total_tokens"]
            stats["total_time"] += r["response_time"]
            stats["issue_detection_rates"].append(
                r["quality_evaluation"].get("issue_detection_rate", 0)
            )
            if r["quality_evaluation"].get("has_code_block", False):
                stats["code_block_count"] += 1

        # 평균 계산
        for cat, stats in category_stats.items():
            n = stats["count"]
            stats["avg_quality"] = round(stats["total_quality"] / n, 2)
            stats["avg_tokens"] = round(stats["total_tokens"] / n, 0)
            stats["avg_time"] = round(stats["total_time"] / n, 2)
            stats["avg_issue_detection"] = round(
                sum(stats["issue_detection_rates"]) / n, 1
            )
            stats["code_block_rate"] = round(stats["code_block_count"] / n * 100, 1)

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
        detailed_path = os.path.join(project_root, f"results/development_experiments_{timestamp}.json")
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
            print(f"    - 이슈 탐지율: {stats['avg_issue_detection']}%")
            print(f"    - 코드 블록 포함율: {stats['code_block_rate']}%")
            print(f"    - 평균 토큰: {stats['avg_tokens']}")
        print()
        print(f"결과 저장: {detailed_path}")
        print("=" * 70)


def main():
    """메인 실행 함수"""
    runner = DevelopmentExperimentRunner(model="qwen2.5:7b")

    # 108회 실험 실행
    summary = runner.run_all_experiments(limit=108)

    print()
    print("108회 실험 완료!")


if __name__ == "__main__":
    main()
