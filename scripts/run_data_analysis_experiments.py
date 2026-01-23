# -*- coding: utf-8 -*-
"""
데이터 분석 프롬프트 V2.1 실험 - LLM-as-a-Judge 평가 시스템

평가 방식: 기존 키워드 매칭 → LLM 기반 다차원 평가
평가 기준: Accuracy, Completeness, Coherence, Actionability, Clarity
"""

import sys
import json
import time
import re
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


# =============================================================================
# LLM-as-a-Judge 평가 프롬프트
# =============================================================================

LLM_JUDGE_PROMPT = """당신은 데이터 분석 품질을 평가하는 전문 평가자입니다.

아래 5가지 기준으로 분석 결과를 1-10점으로 평가하세요.

## 평가 기준

1. **Accuracy (정확성)**: 분석 결과가 제공된 데이터에 기반하여 정확한가?
   - 10점: 모든 계산과 해석이 데이터와 일치
   - 7점: 대부분 정확하나 사소한 오류 있음
   - 4점: 일부 중요한 오류 존재
   - 1점: 데이터와 맞지 않는 분석

2. **Completeness (완전성)**: 요청된 분석 항목이 모두 포함되었는가?
   - 요청 항목: {expected_elements}
   - 10점: 모든 요청 항목 포함
   - 7점: 대부분 포함 (80% 이상)
   - 4점: 절반 정도 포함
   - 1점: 대부분 누락

3. **Coherence (논리적 일관성)**: 분석이 논리적으로 일관성 있는가?
   - 10점: 완벽한 논리적 흐름
   - 7점: 대체로 일관적
   - 4점: 일부 논리적 비약
   - 1점: 논리적 모순 다수

4. **Actionability (실행가능성)**: 권고사항이 구체적이고 실행 가능한가?
   - 10점: 즉시 실행 가능한 구체적 제안
   - 7점: 대체로 구체적
   - 4점: 추상적인 제안
   - 1점: 실행 불가능하거나 권고 없음

5. **Clarity (명확성)**: 설명이 이해하기 쉬운가?
   - 10점: 매우 명확하고 잘 구조화됨
   - 7점: 대체로 이해하기 쉬움
   - 4점: 일부 불명확한 부분 있음
   - 1점: 이해하기 어려움

---

## 분석 요청 (원본)
**시나리오**: {scenario}
**데이터**:
```
{raw_data}
```

---

## 분석 결과 (평가 대상)
```
{response}
```

---

## 평가 출력 형식

반드시 아래 JSON 형식으로만 응답하세요. 다른 텍스트 없이 JSON만 출력하세요.

```json
{{
  "accuracy": <1-10>,
  "completeness": <1-10>,
  "coherence": <1-10>,
  "actionability": <1-10>,
  "clarity": <1-10>,
  "total": <평균>,
  "feedback": "<한 줄 피드백>"
}}
```
"""


class DataAnalysisExperimentRunner:
    """데이터 분석 프롬프트 실험 실행기 - LLM-as-a-Judge 버전"""

    def __init__(self, model: str = "qwen2.5:7b"):
        self.model = model
        self.llm = ChatOllama(model=model, temperature=0.3)
        self.judge_llm = ChatOllama(model=model, temperature=0.1)  # 평가용 LLM (낮은 temperature)
        self.results = []
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def evaluate_with_llm_judge(
        self,
        response: str,
        scenario: str,
        raw_data: str,
        expected_elements: List[str]
    ) -> Dict:
        """LLM-as-a-Judge 방식으로 응답 품질 평가"""

        judge_prompt = LLM_JUDGE_PROMPT.format(
            expected_elements=", ".join(expected_elements),
            scenario=scenario,
            raw_data=raw_data[:1500],  # 토큰 제한
            response=response[:2000]   # 토큰 제한
        )

        try:
            judge_response = self.judge_llm.invoke(judge_prompt).content

            # JSON 추출 (```json ... ``` 또는 { ... } 형태)
            json_match = re.search(r'\{[^{}]*\}', judge_response, re.DOTALL)
            if json_match:
                scores = json.loads(json_match.group())

                # 점수 유효성 검사
                for key in ["accuracy", "completeness", "coherence", "actionability", "clarity"]:
                    if key not in scores or not isinstance(scores[key], (int, float)):
                        scores[key] = 5  # 기본값

                # 총점 계산 (평균)
                dimension_scores = [
                    scores["accuracy"],
                    scores["completeness"],
                    scores["coherence"],
                    scores["actionability"],
                    scores["clarity"]
                ]
                scores["total"] = round(sum(dimension_scores) / len(dimension_scores), 2)

                return {
                    "quality_score": scores["total"],
                    "accuracy": scores.get("accuracy", 5),
                    "completeness": scores.get("completeness", 5),
                    "coherence": scores.get("coherence", 5),
                    "actionability": scores.get("actionability", 5),
                    "clarity": scores.get("clarity", 5),
                    "feedback": scores.get("feedback", ""),
                    "judge_raw": judge_response[:500]
                }
            else:
                # JSON 파싱 실패 시 기본값
                return self._default_evaluation("JSON 파싱 실패")

        except Exception as e:
            return self._default_evaluation(f"평가 오류: {str(e)}")

    def _default_evaluation(self, reason: str) -> Dict:
        """평가 실패 시 기본값 반환"""
        return {
            "quality_score": 5.0,
            "accuracy": 5,
            "completeness": 5,
            "coherence": 5,
            "actionability": 5,
            "clarity": 5,
            "feedback": reason,
            "judge_raw": ""
        }

    def generate_prompt(self, test_case: DataAnalysisTestCase) -> str:
        """테스트 케이스에 맞는 프롬프트 생성"""
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

        # 1단계: 분석 생성
        start_time = time.time()
        try:
            response = self.llm.invoke(prompt).content
            success = True
            error_msg = None
        except Exception as e:
            response = ""
            success = False
            error_msg = str(e)

        generation_time = time.time() - start_time

        # 2단계: LLM-as-a-Judge 평가
        eval_start = time.time()
        if success and response:
            quality_eval = self.evaluate_with_llm_judge(
                response=response,
                scenario=test_case.scenario,
                raw_data=test_case.raw_data,
                expected_elements=test_case.expected_elements
            )
        else:
            quality_eval = self._default_evaluation("생성 실패")

        eval_time = time.time() - eval_start

        input_tokens = self.count_tokens(prompt)
        output_tokens = self.count_tokens(response) if response else 0

        return {
            "test_case_id": test_case.id,
            "category": test_case.category,
            "subcategory": test_case.subcategory,
            "scenario": test_case.scenario,
            "success": success,
            "error": error_msg,
            "generation_time": round(generation_time, 2),
            "evaluation_time": round(eval_time, 2),
            "total_time": round(generation_time + eval_time, 2),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "quality_evaluation": quality_eval
        }

    def run_all_experiments(self, limit: int = 80) -> Dict:
        """모든 실험 실행"""
        print("=" * 70)
        print("데이터 분석 프롬프트 실험 (V2.1 - LLM-as-a-Judge)")
        print("=" * 70)
        print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"모델: {self.model}")
        print(f"평가 방식: LLM-as-a-Judge (5개 차원)")
        print(f"실험 횟수: {limit}회")
        print()

        test_cases = get_all_data_analysis_test_cases()[:limit]
        total = len(test_cases)

        for i, test_case in enumerate(test_cases, 1):
            print(f"[{i:3d}/{total}] {test_case.id} - {test_case.category}/{test_case.subcategory}", end=" ")

            result = self.run_single_experiment(test_case)
            self.results.append(result)

            if result["success"]:
                eval_data = result["quality_evaluation"]
                print(f"총점: {eval_data['quality_score']}/10 "
                      f"(A:{eval_data['accuracy']} C:{eval_data['completeness']} "
                      f"H:{eval_data['coherence']} X:{eval_data['actionability']} "
                      f"L:{eval_data['clarity']})")
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

        # 차원별 통계
        dimensions = ["accuracy", "completeness", "coherence", "actionability", "clarity"]
        dimension_stats = {}
        for dim in dimensions:
            scores = [r["quality_evaluation"].get(dim, 5) for r in successful]
            dimension_stats[dim] = {
                "avg": round(sum(scores) / len(scores), 2),
                "min": min(scores),
                "max": max(scores)
            }

        # 카테고리별 통계
        category_stats = {}
        for r in successful:
            cat = r["category"]
            if cat not in category_stats:
                category_stats[cat] = {
                    "count": 0,
                    "scores": [],
                    "dimension_scores": {dim: [] for dim in dimensions}
                }
            stats = category_stats[cat]
            stats["count"] += 1
            stats["scores"].append(r["quality_evaluation"].get("quality_score", 5))
            for dim in dimensions:
                stats["dimension_scores"][dim].append(r["quality_evaluation"].get(dim, 5))

        for cat, stats in category_stats.items():
            n = stats["count"]
            stats["avg_quality"] = round(sum(stats["scores"]) / n, 2)
            stats["dimension_avgs"] = {
                dim: round(sum(stats["dimension_scores"][dim]) / n, 2)
                for dim in dimensions
            }

        total_quality = sum(r["quality_evaluation"].get("quality_score", 5) for r in successful)
        total_time = sum(r["total_time"] for r in successful)

        return {
            "evaluation_method": "LLM-as-a-Judge",
            "dimensions": dimensions,
            "total_experiments": len(self.results),
            "successful": len(successful),
            "success_rate": round(len(successful) / len(self.results) * 100, 1),
            "avg_quality": round(total_quality / len(successful), 2),
            "avg_time": round(total_time / len(successful), 2),
            "dimension_stats": dimension_stats,
            "category_stats": category_stats
        }

    def _save_results(self, summary: Dict):
        """결과 저장 및 출력"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
        os.makedirs(results_dir, exist_ok=True)

        filename = f"data_analysis_llm_judge_{timestamp}.json"
        filepath = os.path.join(results_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "summary": summary,
                "results": self.results
            }, f, ensure_ascii=False, indent=2)

        print()
        print("=" * 70)
        print("실험 결과 요약 (LLM-as-a-Judge)")
        print("=" * 70)
        print(f"총 실험: {summary['total_experiments']}회")
        print(f"성공률: {summary['success_rate']}%")
        print(f"평균 품질 점수: {summary['avg_quality']}/10")
        print()

        print("차원별 점수:")
        dim_names = {
            "accuracy": "정확성(A)",
            "completeness": "완전성(C)",
            "coherence": "일관성(H)",
            "actionability": "실행가능성(X)",
            "clarity": "명확성(L)"
        }
        for dim, stats in summary.get("dimension_stats", {}).items():
            print(f"  {dim_names.get(dim, dim)}: {stats['avg']}/10 (min:{stats['min']}, max:{stats['max']})")
        print()

        print("카테고리별 결과:")
        for cat, stats in summary.get("category_stats", {}).items():
            print(f"  {cat}: {stats['avg_quality']}/10")
            for dim, avg in stats.get("dimension_avgs", {}).items():
                print(f"    - {dim}: {avg}")
        print()
        print(f"결과 저장: {filepath}")
        print("=" * 70)


def main():
    limit = 10  # 먼저 10개로 테스트
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])

    runner = DataAnalysisExperimentRunner(model="qwen2.5:7b")
    summary = runner.run_all_experiments(limit=limit)

    print()
    print(f"LLM-as-a-Judge 평가 실험 {limit}회 완료!")


if __name__ == "__main__":
    main()
