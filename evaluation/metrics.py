# -*- coding: utf-8 -*-
"""
================================================================================
프롬프트 엔지니어링 평가 모듈 (Prompt Engineering Evaluation Module)
================================================================================

이 모듈은 프롬프트 엔지니어링 실험의 성능을 측정하기 위한 평가 도구를 제공합니다.

## 왜 이 평가 지표들을 사용하는가?

프롬프트 엔지니어링의 효과를 객관적으로 측정하려면 **업계 표준 지표**가 필요합니다.
단순히 "좋아 보인다"가 아닌, 수치로 증명할 수 있어야 합니다.

## 포함된 평가 지표

| 지표 | 설명 | 사용 상황 |
|------|------|----------|
| Exact Match (EM) | 정답과 정확히 일치하는가? | 명확한 정답이 있는 문제 |
| F1 Score | 부분적으로 얼마나 맞는가? | 긴 텍스트 비교 |
| Token Efficiency | 토큰을 얼마나 적게 썼는가? | 비용 최적화 |
| Latency | 응답 시간은 얼마인가? | 사용자 경험 측정 |
| Consistency | 일관된 답변을 하는가? | 신뢰성 측정 |

## 학술적 근거

이 지표들은 다음 프레임워크/논문을 참고하여 설계되었습니다:
- DeepEval: AI 평가 오픈소스 프레임워크 (https://github.com/confident-ai/deepeval)
- G-Eval: GPT-4 기반 평가 (EMNLP 2023)
- RAGAS: RAG 시스템 평가 프레임워크
- SQuAD: 질의응답 평가의 표준 (EM, F1)

## 사용 예시

```python
from langchain_ollama import ChatOllama
from evaluation.metrics import PromptEvaluator, compare_prompts

# 평가기 초기화
llm = ChatOllama(model="qwen2.5:7b")
evaluator = PromptEvaluator(llm)

# 단일 평가
result = evaluator.evaluate_single(
    prompt="1+1은?",
    expected="2"
)

# 여러 프롬프트 비교
results = compare_prompts(
    evaluator,
    prompts={
        "기본": "질문: {q} 답:",
        "구조화": "### 질문\\n{q}\\n### 답"
    },
    test_cases=[{"input": {"q": "1+1?"}, "expected": "2"}]
)
```

Author: Prompt Engineering Portfolio Project
Created: 2025-01-19
================================================================================
"""

import re
import time
from typing import List, Dict, Any, Callable
from dataclasses import dataclass
from collections import Counter

import tiktoken


# ============================================================================
# 데이터 클래스: 평가 결과 저장
# ============================================================================

@dataclass
class EvaluationResult:
    """
    단일 평가 결과를 저장하는 데이터 클래스

    Attributes:
        metric_name: 평가 지표 이름 (예: "Exact Match", "F1 Score")
        score: 점수 (0.0 ~ 1.0 범위)
        details: 상세 정보를 담은 딕셔너리

    Example:
        >>> result = EvaluationResult("Exact Match", 1.0, {"is_correct": True})
        >>> print(result)
        Exact Match: 100.00%
    """
    metric_name: str           # 지표 이름
    score: float               # 점수 (0.0 ~ 1.0)
    details: Dict[str, Any]    # 상세 정보

    def __str__(self):
        """사람이 읽기 쉬운 형태로 출력"""
        return f"{self.metric_name}: {self.score:.2%}"


# ============================================================================
# 메인 클래스: 프롬프트 평가기
# ============================================================================

class PromptEvaluator:
    """
    프롬프트 성능 평가기 (Prompt Performance Evaluator)

    이 클래스는 LLM의 응답을 다양한 관점에서 평가합니다.

    ## 왜 필요한가?

    프롬프트 엔지니어링의 핵심은 "어떤 프롬프트가 더 좋은가?"를 판단하는 것입니다.
    이를 위해 객관적인 수치가 필요하고, 이 클래스가 그 역할을 합니다.

    ## 제공하는 평가 방법

    1. exact_match(): 정확히 일치하는지 확인
    2. f1_score(): 단어 단위 부분 일치도 계산
    3. token_efficiency(): 토큰 사용량 측정
    4. measure_latency(): 응답 시간 측정
    5. consistency(): 같은 질문에 일관된 답변을 하는지 확인

    ## 사용 예시

    ```python
    from langchain_ollama import ChatOllama

    llm = ChatOllama(model="qwen2.5:7b")
    evaluator = PromptEvaluator(llm)

    # 정확도 평가
    result = evaluator.exact_match("6", "6")
    print(result.score)  # 1.0

    # 종합 평가
    results = evaluator.evaluate_single(
        prompt="1+1은?",
        expected="2"
    )
    ```
    """

    def __init__(self, llm, tokenizer_model: str = "gpt-3.5-turbo"):
        """
        평가기 초기화

        Args:
            llm: LangChain LLM 객체 (예: ChatOllama, ChatOpenAI)
            tokenizer_model: 토큰 계산에 사용할 모델명
                           - "gpt-3.5-turbo": OpenAI 토크나이저 (업계 표준)
                           - 실제 사용하는 모델과 다를 수 있지만,
                             일관된 비교를 위해 동일한 토크나이저 사용
        """
        self.llm = llm
        # tiktoken: OpenAI의 토큰화 라이브러리
        # 업계에서 토큰 수 측정의 표준으로 사용됨
        self.encoder = tiktoken.encoding_for_model(tokenizer_model)

    def count_tokens(self, text: str) -> int:
        """
        텍스트의 토큰 수를 계산합니다.

        ## 토큰(Token)이란?

        LLM이 텍스트를 처리하는 최소 단위입니다.
        - 영어: 약 4글자 = 1토큰 (예: "hello" = 1토큰)
        - 한국어: 약 1~2글자 = 1토큰 (예: "안녕" = 2토큰)

        ## 왜 중요한가?

        - API 비용은 토큰 수에 비례합니다
        - 토큰이 적을수록 비용이 절감됩니다
        - 프롬프트 최적화의 핵심 지표입니다

        Args:
            text: 토큰 수를 계산할 텍스트

        Returns:
            int: 토큰 수

        Example:
            >>> evaluator.count_tokens("Hello World")
            2
            >>> evaluator.count_tokens("안녕하세요")
            5
        """
        return len(self.encoder.encode(text))

    # ========================================================================
    # 평가 지표 1: Exact Match (정확도)
    # ========================================================================

    def exact_match(self, response: str, expected: str) -> EvaluationResult:
        """
        정확히 일치하는지 평가합니다. (Exact Match)

        ## 이 지표가 필요한 이유

        수학 문제나 분류 문제처럼 정답이 명확한 경우,
        응답이 정답과 정확히 일치하는지 확인해야 합니다.

        ## 평가 방식

        1. 공백, 줄바꿈을 제거합니다
        2. 대소문자를 무시합니다
        3. 정확히 일치하면 1.0, 포함되면 0.5, 아니면 0.0

        ## 점수 기준

        | 상황 | 점수 |
        |------|------|
        | 정확히 일치 | 1.0 |
        | 정답이 응답에 포함됨 | 0.5 |
        | 불일치 | 0.0 |

        Args:
            response: AI의 응답
            expected: 기대하는 정답

        Returns:
            EvaluationResult: 평가 결과

        Example:
            >>> evaluator.exact_match("6", "6")
            EvaluationResult(score=1.0)  # 정확히 일치

            >>> evaluator.exact_match("답은 6입니다", "6")
            EvaluationResult(score=0.5)  # 정답 포함
        """
        # 정규화: 공백 제거, 소문자 변환
        norm_response = re.sub(r'\s+', '', response.lower().strip())
        norm_expected = re.sub(r'\s+', '', expected.lower().strip())

        # 평가
        is_exact = norm_response == norm_expected      # 정확히 일치
        is_contained = norm_expected in norm_response  # 정답이 포함됨

        # 점수 계산
        if is_exact:
            score = 1.0
        elif is_contained:
            score = 0.5
        else:
            score = 0.0

        return EvaluationResult(
            metric_name="Exact Match",
            score=score,
            details={
                "response": response[:100],  # 응답 미리보기 (100자까지)
                "expected": expected,
                "is_exact": is_exact,
                "is_contained": is_contained
            }
        )

    # ========================================================================
    # 평가 지표 2: F1 Score (부분 정확도)
    # ========================================================================

    def f1_score(self, response: str, expected: str) -> EvaluationResult:
        """
        F1 Score를 계산합니다. (단어 단위 부분 일치도)

        ## 이 지표가 필요한 이유

        긴 텍스트나 요약 결과를 평가할 때,
        정확히 일치하지 않더라도 얼마나 비슷한지 측정해야 합니다.

        ## F1 Score란?

        Precision(정밀도)과 Recall(재현율)의 조화평균입니다.

        - **Precision**: 응답 중 정답에 있는 단어의 비율
          "내가 말한 것 중 맞는 비율"

        - **Recall**: 정답 중 응답에 있는 단어의 비율
          "맞춰야 할 것 중 맞춘 비율"

        - **F1**: 두 지표의 균형 (조화평균)

        ## 계산 공식

        F1 = 2 × (Precision × Recall) / (Precision + Recall)

        ## 학술적 배경

        SQuAD(Stanford Question Answering Dataset)에서
        질의응답 성능 측정의 표준 지표로 사용됩니다.

        Args:
            response: AI의 응답
            expected: 기대하는 정답

        Returns:
            EvaluationResult: F1 점수와 상세 정보
        """
        # 단어 단위로 분리 (집합으로 변환)
        response_words = set(response.lower().split())
        expected_words = set(expected.lower().split())

        # 빈 텍스트 처리
        if not response_words or not expected_words:
            return EvaluationResult("F1 Score", 0.0, {"error": "빈 텍스트"})

        # 공통 단어 찾기
        common = response_words & expected_words

        # Precision: 응답 중 정답에 있는 단어 비율
        precision = len(common) / len(response_words) if response_words else 0

        # Recall: 정답 중 응답에 있는 단어 비율
        recall = len(common) / len(expected_words) if expected_words else 0

        # F1 Score: 조화평균
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        return EvaluationResult(
            metric_name="F1 Score",
            score=f1,
            details={
                "precision": round(precision, 3),
                "recall": round(recall, 3),
                "common_words": list(common)[:10]  # 공통 단어 샘플
            }
        )

    # ========================================================================
    # 평가 지표 3: Token Efficiency (토큰 효율성)
    # ========================================================================

    def token_efficiency(
        self,
        prompt: str,
        response: str,
        baseline_tokens: int = None
    ) -> EvaluationResult:
        """
        토큰 효율성을 측정합니다.

        ## 이 지표가 필요한 이유

        LLM API는 토큰 단위로 비용이 청구됩니다.
        같은 결과를 더 적은 토큰으로 얻으면 비용이 절감됩니다.

        ## 측정 항목

        - 입력 토큰 수: 프롬프트의 토큰 수
        - 출력 토큰 수: 응답의 토큰 수
        - 총 토큰 수: 입력 + 출력
        - 절감율: 기준 대비 몇 % 줄었는가?

        ## 비용 계산 예시 (GPT-4 기준)

        | 토큰 수 | 예상 비용 |
        |--------|----------|
        | 100 토큰 | $0.003 |
        | 1000 토큰 | $0.03 |
        | 10000 토큰 | $0.30 |

        Args:
            prompt: 입력 프롬프트
            response: AI의 응답
            baseline_tokens: 비교 기준 토큰 수 (선택)

        Returns:
            EvaluationResult: 토큰 사용량 정보
        """
        input_tokens = self.count_tokens(prompt)
        output_tokens = self.count_tokens(response)
        total_tokens = input_tokens + output_tokens

        # 기준 대비 절감율 (기준이 있을 경우)
        reduction = None
        if baseline_tokens and baseline_tokens > 0:
            reduction = 1 - (total_tokens / baseline_tokens)

        return EvaluationResult(
            metric_name="Token Efficiency",
            score=1.0,  # 효율성은 비교용이므로 고정 점수
            details={
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "reduction": f"{reduction:.1%}" if reduction else None
            }
        )

    # ========================================================================
    # 평가 지표 4: Latency (응답 시간)
    # ========================================================================

    def measure_latency(self, prompt: str) -> EvaluationResult:
        """
        응답 시간을 측정합니다.

        ## 이 지표가 필요한 이유

        사용자 경험에서 응답 시간은 매우 중요합니다.
        아무리 정확해도 응답이 느리면 사용성이 떨어집니다.

        ## 일반적인 기준

        | 응답 시간 | 평가 |
        |----------|------|
        | < 1초 | 매우 빠름 |
        | 1~3초 | 적절함 |
        | 3~10초 | 느림 |
        | > 10초 | 매우 느림 |

        Args:
            prompt: 테스트할 프롬프트

        Returns:
            EvaluationResult: 응답 시간 정보
        """
        # 시작 시간 기록
        start = time.time()

        # LLM 호출
        response = self.llm.invoke(prompt)

        # 종료 시간 기록
        latency = time.time() - start

        return EvaluationResult(
            metric_name="Latency",
            score=1.0,  # 비교용이므로 고정 점수
            details={
                "latency_seconds": round(latency, 3),
                "response_preview": response.content[:50]  # 응답 미리보기
            }
        )

    # ========================================================================
    # 평가 지표 5: Consistency (일관성)
    # ========================================================================

    def consistency(self, prompt: str, n_trials: int = 5) -> EvaluationResult:
        """
        일관성을 측정합니다. (같은 질문에 같은 답을 하는가?)

        ## 이 지표가 필요한 이유

        같은 질문에 매번 다른 답을 하면 신뢰할 수 없습니다.
        특히 프로덕션 환경에서는 일관성이 매우 중요합니다.

        ## 측정 방법

        1. 같은 프롬프트를 n번 실행합니다
        2. 응답들을 정규화합니다 (공백 제거, 소문자 변환)
        3. 가장 많이 나온 응답의 비율을 계산합니다

        ## 점수 해석

        | 일관성 점수 | 해석 |
        |------------|------|
        | 1.0 (100%) | 모든 응답이 동일 |
        | 0.8 (80%) | 대부분 일관됨 |
        | 0.5 (50%) | 절반만 일관됨 |
        | < 0.5 | 일관성 없음 |

        Args:
            prompt: 테스트할 프롬프트
            n_trials: 반복 횟수 (기본값: 5)

        Returns:
            EvaluationResult: 일관성 점수와 상세 정보

        Note:
            이 측정은 n번의 API 호출이 필요하므로 시간이 오래 걸립니다.
        """
        responses = []

        # n번 실행
        for _ in range(n_trials):
            response = self.llm.invoke(prompt)
            # 정규화: 공백 통일, 소문자 변환
            normalized = re.sub(r'\s+', ' ', response.content.strip().lower())
            responses.append(normalized)

        # 가장 많이 나온 응답의 비율 계산
        counter = Counter(responses)
        most_common_count = counter.most_common(1)[0][1]
        consistency_score = most_common_count / n_trials

        return EvaluationResult(
            metric_name="Consistency",
            score=consistency_score,
            details={
                "n_trials": n_trials,
                "unique_responses": len(counter),  # 고유 응답 수
                "most_common_count": most_common_count,
                "responses": list(counter.keys())[:3]  # 응답 샘플
            }
        )

    # ========================================================================
    # 종합 평가 메서드
    # ========================================================================

    def evaluate_single(
        self,
        prompt: str,
        expected: str = None,
        measure_consistency: bool = False
    ) -> Dict[str, EvaluationResult]:
        """
        단일 프롬프트에 대한 종합 평가를 수행합니다.

        ## 평가 항목

        - 토큰 효율성: 항상 측정
        - 응답 시간: 항상 측정
        - 정확도 (EM, F1): 정답이 있을 때만 측정
        - 일관성: 옵션 (시간이 오래 걸림)

        Args:
            prompt: 평가할 프롬프트
            expected: 기대하는 정답 (선택)
            measure_consistency: 일관성 측정 여부 (기본값: False)

        Returns:
            Dict[str, EvaluationResult]: 지표별 평가 결과
        """
        results = {}

        # 응답 시간 측정과 동시에 응답 받기
        start = time.time()
        response = self.llm.invoke(prompt)
        latency = time.time() - start
        response_text = response.content

        # 1. 토큰 효율성
        results["token_efficiency"] = self.token_efficiency(prompt, response_text)

        # 2. 응답 시간
        results["latency"] = EvaluationResult(
            "Latency",
            1.0,
            {"latency_seconds": round(latency, 3)}
        )

        # 3. 정확도 (정답이 있을 때만)
        if expected:
            results["exact_match"] = self.exact_match(response_text, expected)
            results["f1_score"] = self.f1_score(response_text, expected)

        # 4. 일관성 (옵션)
        if measure_consistency:
            results["consistency"] = self.consistency(prompt)

        return results

    def evaluate_batch(
        self,
        prompt_template: str,
        test_cases: List[Dict],
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        여러 테스트 케이스로 종합 평가를 수행합니다.

        ## 사용 예시

        ```python
        results = evaluator.evaluate_batch(
            prompt_template="질문: {q} 답:",
            test_cases=[
                {"input": {"q": "1+1?"}, "expected": "2"},
                {"input": {"q": "2+2?"}, "expected": "4"},
            ]
        )

        print(results["summary"]["accuracy_em"])  # 정확도
        ```

        Args:
            prompt_template: 프롬프트 템플릿 (예: "질문: {q} 답:")
            test_cases: 테스트 케이스 목록
            verbose: 진행 상황 출력 여부

        Returns:
            Dict: 요약 통계와 상세 결과
        """
        all_results = []
        total_em = 0
        total_f1 = 0
        total_tokens = 0
        total_latency = 0

        for i, case in enumerate(test_cases):
            # 템플릿에 입력값 적용
            prompt = prompt_template.format(**case["input"])
            expected = case.get("expected")

            # 개별 평가
            result = self.evaluate_single(prompt, expected)
            all_results.append(result)

            # 집계
            if "exact_match" in result:
                total_em += result["exact_match"].score
                total_f1 += result["f1_score"].score
            total_tokens += result["token_efficiency"].details["total_tokens"]
            total_latency += result["latency"].details["latency_seconds"]

            # 진행 상황 출력
            if verbose:
                score = result.get("exact_match", EvaluationResult("", 0, {})).score
                status = "O" if score >= 0.5 else "X"
                print(f"  [{i+1}/{len(test_cases)}] {status}")

        n = len(test_cases)

        return {
            "summary": {
                "total_cases": n,
                "accuracy_em": total_em / n if n > 0 else 0,
                "accuracy_f1": total_f1 / n if n > 0 else 0,
                "avg_tokens": total_tokens / n if n > 0 else 0,
                "avg_latency": total_latency / n if n > 0 else 0,
            },
            "details": all_results
        }


# ============================================================================
# 유틸리티 함수: 프롬프트 비교
# ============================================================================

def compare_prompts(
    evaluator: PromptEvaluator,
    prompts: Dict[str, str],
    test_cases: List[Dict],
    verbose: bool = True
) -> Dict[str, Any]:
    """
    여러 프롬프트 방식을 비교합니다.

    ## 사용 예시

    ```python
    results = compare_prompts(
        evaluator,
        prompts={
            "기본": "질문: {q} 답:",
            "구조화": "### 질문\\n{q}\\n### 답",
            "CoT": "질문: {q}\\n단계별로 풀어봅시다.\\n답:"
        },
        test_cases=test_cases
    )

    # 결과 비교
    for method in results["comparison"]:
        print(f"{method['method']}: {method['accuracy']}")
    ```

    Args:
        evaluator: PromptEvaluator 인스턴스
        prompts: {"방식명": "프롬프트 템플릿", ...}
        test_cases: 테스트 케이스 목록
        verbose: 진행 상황 출력 여부

    Returns:
        Dict: 비교 요약과 상세 결과
    """
    results = {}

    # 각 방식별로 평가 실행
    for name, template in prompts.items():
        if verbose:
            print(f"\n[{name}] 평가 중...")
        results[name] = evaluator.evaluate_batch(template, test_cases, verbose)

    # 비교 요약 생성
    comparison = []
    for name, result in results.items():
        summary = result["summary"]
        comparison.append({
            "method": name,
            "accuracy": f"{summary['accuracy_em']:.1%}",
            "f1": f"{summary['accuracy_f1']:.2f}",
            "tokens": f"{summary['avg_tokens']:.0f}",
            "latency": f"{summary['avg_latency']:.2f}s"
        })

    return {
        "comparison": comparison,
        "details": results
    }


# ============================================================================
# 모듈 직접 실행 시 테스트
# ============================================================================

if __name__ == "__main__":
    print("이 모듈은 다른 파일에서 import하여 사용합니다.")
    print("사용 예시: from evaluation.metrics import PromptEvaluator")
