# -*- coding: utf-8 -*-
"""
Chain of Thought 실험 - 어려운 문제

목적: 복잡한 문장형 문제에서 CoT가 효과적인지 검증
테스트: 수학 문장형 20개 + 논리 추론 6개 = 26개 어려운 문제
"""

import sys
import json
import time
from datetime import datetime

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from langchain_ollama import ChatOllama
from evaluation.metrics import PromptEvaluator, compare_prompts
from evaluation.test_cases import get_hard_problems_suite, get_math_test_suite


def main():
    print("=" * 70)
    print("Chain of Thought 실험 - 복잡한 문제")
    print("=" * 70)

    # LLM 초기화
    print("\n[1] LLM 초기화...")
    llm = ChatOllama(model="qwen2.5:7b", temperature=0)
    evaluator = PromptEvaluator(llm)
    print("    완료!")

    # 테스트 케이스 로드
    print("\n[2] 테스트 케이스 로드...")
    hard_suite = get_hard_problems_suite()
    print(f"    어려운 문제 {len(hard_suite)}개 로드")

    # 프롬프트 방식 정의
    prompts = {
        "기본": """질문: {q}
답 (숫자나 단어만):""",

        "구조화": """### 질문
{q}

### 규칙
- 답만 간단히 작성
- 숫자 질문은 숫자만, 예/아니오 질문은 예 또는 아니오만

### 답""",

        "CoT (단계별 사고)": """### 질문
{q}

### 풀이 방법
차근차근 단계별로 생각해봅시다.

1단계: 주어진 정보를 정리합니다.
2단계: 필요한 계산이나 추론을 합니다.
3단계: 최종 답을 구합니다.

### 풀이 과정"""
    }

    # 테스트 실행
    test_cases = hard_suite.to_list()
    print(f"\n[3] 실험 시작 (총 {len(test_cases)}개 문제, 3가지 방식)")
    print("-" * 70)

    results = compare_prompts(evaluator, prompts, test_cases, verbose=True)

    # 결과 출력
    print("\n" + "=" * 70)
    print("실험 결과 (어려운 문제 {}개)".format(len(test_cases)))
    print("=" * 70)
    print(f"{'방식':<25} {'정확도':<12} {'F1':<12} {'평균토큰':<12} {'평균시간':<12}")
    print("-" * 70)

    for row in results["comparison"]:
        print(f"{row['method']:<25} {row['accuracy']:<12} {row['f1']:<12} {row['tokens']:<12} {row['latency']:<12}")

    print("-" * 70)

    # 분석
    comparison = results["comparison"]
    best_accuracy = max(comparison, key=lambda x: float(x['accuracy'].rstrip('%')))
    best_tokens = min(comparison, key=lambda x: float(x['tokens']))

    print(f"\n[결론]")
    print(f"  정확도 최고: {best_accuracy['method']} ({best_accuracy['accuracy']})")
    print(f"  토큰 최소: {best_tokens['method']} ({best_tokens['tokens']} 토큰)")

    # 정확도 향상 계산
    basic_acc = float([r for r in comparison if r['method'] == '기본'][0]['accuracy'].rstrip('%'))
    cot_acc = float([r for r in comparison if r['method'] == 'CoT (단계별 사고)'][0]['accuracy'].rstrip('%'))
    improvement = cot_acc - basic_acc

    print(f"\n  CoT vs 기본 정확도 향상: {improvement:+.1f}%p")

    # 결과 저장
    save_results = {
        "experiment": "CoT_hard_problems",
        "timestamp": datetime.now().isoformat(),
        "model": "qwen2.5:7b",
        "test_cases_count": len(test_cases),
        "results": results["comparison"],
        "conclusion": {
            "best_accuracy_method": best_accuracy['method'],
            "best_accuracy": best_accuracy['accuracy'],
            "cot_improvement": f"{improvement:+.1f}%p"
        }
    }

    with open("results/cot_hard_experiment.json", "w", encoding="utf-8") as f:
        json.dump(save_results, f, ensure_ascii=False, indent=2)

    print(f"\n결과 저장: results/cot_hard_experiment.json")
    print("\n실험 완료!")

    return results


if __name__ == "__main__":
    main()
