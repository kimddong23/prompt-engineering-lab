# -*- coding: utf-8 -*-
"""
평가 시스템 테스트

이 스크립트는 평가 시스템이 제대로 작동하는지 확인합니다.
"""

import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from langchain_ollama import ChatOllama
from evaluation.metrics import PromptEvaluator, compare_prompts
from evaluation.test_cases import get_math_test_suite


def main():
    print("=" * 60)
    print("프롬프트 엔지니어링 평가 시스템 테스트")
    print("=" * 60)

    # LLM 초기화
    print("\n1. LLM 초기화...")
    llm = ChatOllama(model="qwen2.5:7b", temperature=0)
    evaluator = PromptEvaluator(llm)
    print("   [OK] 초기화 완료")

    # 테스트 케이스 로드
    print("\n2. 테스트 케이스 로드...")
    math_suite = get_math_test_suite()
    print(f"   [OK] 수학 문제 {len(math_suite)}개 로드")

    # 프롬프트 방식 정의
    prompts = {
        "기본": "질문: {q}\n답:",
        "구조화": """### 질문
{q}

### 답 (숫자만)""",
        "Chain of Thought": """### 질문
{q}

### 풀이
단계별로 생각해봅시다.

### 답"""
    }

    # 테스트 케이스 일부만 사용 (시간 절약)
    test_cases = math_suite.to_list()[:5]
    print(f"\n3. 평가 시작 (테스트 케이스 {len(test_cases)}개)")
    print("-" * 60)

    # 비교 평가 실행
    results = compare_prompts(evaluator, prompts, test_cases, verbose=True)

    # 결과 출력
    print("\n" + "=" * 60)
    print("평가 결과 비교")
    print("=" * 60)
    print(f"{'방식':<20} {'정확도':<10} {'F1':<10} {'토큰':<10} {'시간':<10}")
    print("-" * 60)

    for row in results["comparison"]:
        print(f"{row['method']:<20} {row['accuracy']:<10} {row['f1']:<10} {row['tokens']:<10} {row['latency']:<10}")

    print("-" * 60)

    # 승자 판정
    best_accuracy = max(results["comparison"], key=lambda x: float(x['accuracy'].rstrip('%')))
    best_tokens = min(results["comparison"], key=lambda x: float(x['tokens']))

    print(f"\n[결론]")
    print(f"  정확도 최고: {best_accuracy['method']} ({best_accuracy['accuracy']})")
    print(f"  토큰 최소: {best_tokens['method']} ({best_tokens['tokens']} 토큰)")

    print("\n평가 시스템 테스트 완료!")


if __name__ == "__main__":
    main()
