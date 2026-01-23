# -*- coding: utf-8 -*-
"""
데이터 분석 프롬프트 V2.0 실험 (8개 카테고리, 80회)
"""

import sys
import json
import time
from datetime import datetime
from typing import Dict, List

# Windows 한글 출력 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_ollama import ChatOllama
import tiktoken

from evaluation.data_analysis_test_cases import (
    get_all_data_analysis_test_cases,
    DataAnalysisTestCase
)
from templates.data_analysis.data_analysis_prompts import get_prompt_by_category


class DataAnalysisExperimentRunner:
    """데이터 분석 프롬프트 실험 실행기"""

    def __init__(self, model: str = "qwen2.5:7b"):
        self.model = model
        self.llm = ChatOllama(model=model, temperature=0.3)
        self.results = []
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def evaluate_response_quality(self, response: str, expected_elements: List[str]) -> Dict:
        """응답 품질 평가"""
        response_lower = response.lower()

        # 필수 요소 포함 여부
        found_elements = 0
        for element in expected_elements:
            keywords = element.lower().replace(" ", "").split("/")
            for kw in keywords:
                if kw in response_lower.replace(" ", ""):
                    found_elements += 1
                    break

        element_coverage = found_elements / len(expected_elements) if expected_elements else 0

        # 구조화 점수
        has_structure = any(marker in response for marker in ["###", "##", "|", "표", "테이블"])
        has_numbers = any(char.isdigit() for char in response)
        has_recommendations = any(kw in response_lower for kw in ["권고", "제안", "추천", "액션", "실행"])

        quality_score = (
            element_coverage * 4 +  # 최대 4점
            (2 if has_structure else 0) +  # 구조화 2점
            (2 if has_numbers else 0) +  # 수치 포함 2점
            (2 if has_recommendations else 0)  # 권고 포함 2점
        )

        return {
            "quality_score": round(min(quality_score, 10), 2),
            "element_coverage": round(element_coverage * 100, 1),
            "has_structure": has_structure,
            "has_numbers": has_numbers,
            "has_recommendations": has_recommendations,
            "found_elements": found_elements,
            "total_elements": len(expected_elements)
        }

    def generate_prompt(self, test_case: DataAnalysisTestCase) -> str:
        """테스트 케이스에 맞는 프롬프트 생성 (8개 카테고리 지원)"""
        return get_prompt_by_category(
            category=test_case.category,
            scenario=test_case.scenario,
            industry=test_case.industry,
            data_description=test_case.data_description,
            raw_data=test_case.raw_data,
            expected_elements=test_case.expected_elements
        )

    def run_single_experiment(self, test_case: DataAnalysisTestCase) -> Dict:
        """단일 실험 실행"""
        prompt = self.generate_prompt(test_case)

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

        input_tokens = self.count_tokens(prompt)
        output_tokens = self.count_tokens(response) if response else 0

        quality_eval = self.evaluate_response_quality(
            response, test_case.expected_elements
        ) if success else {}

        return {
            "test_case_id": test_case.id,
            "category": test_case.category,
            "subcategory": test_case.subcategory,
            "scenario": test_case.scenario,
            "success": success,
            "error": error_msg,
            "response_time": round(elapsed_time, 2),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "quality_evaluation": quality_eval
        }

    def run_all_experiments(self, limit: int = 80) -> Dict:
        """모든 실험 실행"""
        print("=" * 70)
        print("데이터 분석 프롬프트 실험 (V2.0 - 8개 카테고리)")
        print("=" * 70)
        print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"모델: {self.model}")
        print(f"실험 횟수: {limit}회")
        print()

        test_cases = get_all_data_analysis_test_cases()[:limit]
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

        summary = self._generate_summary()
        self._save_results(summary)

        return summary

    def _generate_summary(self) -> Dict:
        """실험 결과 요약"""
        successful = [r for r in self.results if r["success"]]

        if not successful:
            return {"error": "성공한 실험이 없습니다"}

        category_stats = {}
        for r in successful:
            cat = r["category"]
            if cat not in category_stats:
                category_stats[cat] = {
                    "count": 0,
                    "total_quality": 0,
                    "total_tokens": 0,
                    "element_coverages": []
                }
            stats = category_stats[cat]
            stats["count"] += 1
            stats["total_quality"] += r["quality_evaluation"].get("quality_score", 0)
            stats["total_tokens"] += r["total_tokens"]
            stats["element_coverages"].append(r["quality_evaluation"].get("element_coverage", 0))

        for cat, stats in category_stats.items():
            n = stats["count"]
            stats["avg_quality"] = round(stats["total_quality"] / n, 2)
            stats["avg_tokens"] = round(stats["total_tokens"] / n, 0)
            stats["avg_element_coverage"] = round(sum(stats["element_coverages"]) / n, 1)

        total_quality = sum(r["quality_evaluation"].get("quality_score", 0) for r in successful)
        total_tokens = sum(r["total_tokens"] for r in successful)

        return {
            "total_experiments": len(self.results),
            "successful": len(successful),
            "success_rate": round(len(successful) / len(self.results) * 100, 1),
            "avg_quality": round(total_quality / len(successful), 2),
            "avg_tokens": round(total_tokens / len(successful), 0),
            "category_stats": category_stats
        }

    def _save_results(self, summary: Dict):
        """결과 저장 및 출력"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
        os.makedirs(results_dir, exist_ok=True)

        filename = f"data_analysis_experiments_{timestamp}.json"
        filepath = os.path.join(results_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "summary": summary,
                "results": self.results
            }, f, ensure_ascii=False, indent=2)

        print()
        print("=" * 70)
        print("실험 결과 요약")
        print("=" * 70)
        print(f"총 실험: {summary['total_experiments']}회")
        print(f"성공률: {summary['success_rate']}%")
        print(f"평균 품질 점수: {summary['avg_quality']}/10")
        print(f"평균 토큰: {summary['avg_tokens']}")
        print()
        print("카테고리별 결과:")
        for cat, stats in summary.get("category_stats", {}).items():
            print(f"  {cat}:")
            print(f"    - 평균 품질: {stats['avg_quality']}/10")
            print(f"    - 요소 포함율: {stats['avg_element_coverage']}%")
            print(f"    - 평균 토큰: {stats['avg_tokens']}")
        print()
        print(f"결과 저장: {filepath}")
        print("=" * 70)


def main():
    limit = 80
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])

    runner = DataAnalysisExperimentRunner(model="qwen2.5:7b")
    summary = runner.run_all_experiments(limit=limit)

    print()
    print(f"V2.0 데이터 분석 실험 {limit}회 완료!")


if __name__ == "__main__":
    main()
