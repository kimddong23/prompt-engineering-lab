# -*- coding: utf-8 -*-
"""
Chain of Thought 실험 v2 - 개선된 평가

핵심 변경:
- 정답 "포함" 여부로 정확도 측정 (CoT는 설명이 포함되므로)
- 최종 답만 추출해서 비교
"""

import sys
import json
import re
import time
from datetime import datetime

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from langchain_ollama import ChatOllama
import tiktoken
from evaluation.test_cases import get_hard_problems_suite


def extract_answer(response: str) -> str:
    """응답에서 최종 답 추출 시도"""
    # "답: X", "답은 X", "X입니다" 등의 패턴
    patterns = [
        r'(?:답|정답|결과|따라서)[:\s은는이가]*\s*(\d+|예|아니오)',
        r'(\d+)(?:입니다|이다|이에요|예요|개|원|살|명|cm|등)',
        r'(?:예|아니오)(?:입니다|이다|예요)?',
    ]

    for pattern in patterns:
        match = re.search(pattern, response)
        if match:
            return match.group(1) if match.groups() else match.group(0)

    # 마지막 숫자 추출
    numbers = re.findall(r'\d+', response)
    if numbers:
        return numbers[-1]

    # "예" 또는 "아니오" 포함 여부
    if '아니오' in response or '아니' in response:
        return '아니오'
    if '예' in response or '네' in response:
        return '예'

    return response.strip()


def check_answer(response: str, expected: str) -> dict:
    """
    답변 정확도 체크

    Returns:
        {
            "exact": bool,      # 정확히 일치
            "contains": bool,   # 정답 포함
            "extracted": str,   # 추출된 답
            "correct": bool     # 최종 정답 여부
        }
    """
    response_clean = response.strip().lower()
    expected_clean = expected.strip().lower()

    # 1. 정확히 일치
    exact = response_clean == expected_clean

    # 2. 정답 포함
    contains = expected_clean in response_clean

    # 3. 답 추출 후 비교
    extracted = extract_answer(response)
    extracted_clean = extracted.strip().lower()
    extracted_match = extracted_clean == expected_clean or expected_clean in extracted_clean

    # 최종 판정: 포함되거나 추출한 답이 맞으면 정답
    correct = contains or extracted_match

    return {
        "exact": exact,
        "contains": contains,
        "extracted": extracted,
        "extracted_match": extracted_match,
        "correct": correct
    }


def run_experiment():
    print("=" * 70)
    print("Chain of Thought 실험 v2 - 개선된 평가")
    print("=" * 70)
    print("\n[평가 기준]")
    print("  - Exact Match: 응답이 정답과 정확히 일치")
    print("  - Contains: 응답에 정답이 포함됨")
    print("  - Correct: 정답 포함 또는 추출된 답이 일치")
    print()

    # 초기화
    llm = ChatOllama(model="qwen2.5:7b", temperature=0)
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    hard_suite = get_hard_problems_suite()
    test_cases = hard_suite.to_list()

    print(f"테스트 케이스: {len(test_cases)}개")
    print("-" * 70)

    # 프롬프트 정의
    prompts = {
        "기본": """질문: {q}
답:""",

        "구조화": """### 질문
{q}

### 답 (숫자나 예/아니오만)""",

        "CoT": """### 질문
{q}

### 풀이
차근차근 단계별로 생각해봅시다.

### 과정과 답"""
    }

    # 실험 실행
    all_results = {}

    for method_name, template in prompts.items():
        print(f"\n[{method_name}] 실험 중...")
        results = {
            "exact_count": 0,
            "contains_count": 0,
            "correct_count": 0,
            "total_tokens": 0,
            "total_time": 0,
            "details": []
        }

        for i, case in enumerate(test_cases):
            prompt = template.format(**case["input"])
            expected = case["expected"]

            # 실행
            start = time.time()
            response = llm.invoke(prompt).content
            elapsed = time.time() - start

            # 토큰 계산
            tokens = len(enc.encode(prompt)) + len(enc.encode(response))

            # 정확도 체크
            check = check_answer(response, expected)

            # 집계
            if check["exact"]:
                results["exact_count"] += 1
            if check["contains"]:
                results["contains_count"] += 1
            if check["correct"]:
                results["correct_count"] += 1

            results["total_tokens"] += tokens
            results["total_time"] += elapsed

            # 상세 기록
            results["details"].append({
                "question": case["input"].get("q", case["input"].get("text", ""))[:50],
                "expected": expected,
                "extracted": check["extracted"][:30],
                "correct": check["correct"]
            })

            # 진행 상황
            status = "O" if check["correct"] else "X"
            print(f"  [{i+1:2}/{len(test_cases)}] {status}", end="")
            if (i + 1) % 10 == 0:
                print()

        print()
        n = len(test_cases)
        results["exact_accuracy"] = results["exact_count"] / n
        results["contains_accuracy"] = results["contains_count"] / n
        results["correct_accuracy"] = results["correct_count"] / n
        results["avg_tokens"] = results["total_tokens"] / n
        results["avg_time"] = results["total_time"] / n

        all_results[method_name] = results

    # 결과 출력
    print("\n" + "=" * 70)
    print("실험 결과 요약")
    print("=" * 70)
    print(f"{'방식':<12} {'Exact':<10} {'Contains':<10} {'Correct':<10} {'토큰':<10} {'시간':<10}")
    print("-" * 70)

    for method, result in all_results.items():
        print(f"{method:<12} "
              f"{result['exact_accuracy']*100:>6.1f}%   "
              f"{result['contains_accuracy']*100:>6.1f}%   "
              f"{result['correct_accuracy']*100:>6.1f}%   "
              f"{result['avg_tokens']:>6.0f}    "
              f"{result['avg_time']:>5.2f}s")

    print("-" * 70)

    # 핵심 비교: Correct 기준
    print(f"\n[핵심 결과 - Correct 기준 (정답 포함 여부)]")
    basic_correct = all_results["기본"]["correct_accuracy"] * 100
    struct_correct = all_results["구조화"]["correct_accuracy"] * 100
    cot_correct = all_results["CoT"]["correct_accuracy"] * 100

    print(f"  기본:    {basic_correct:.1f}%")
    print(f"  구조화:  {struct_correct:.1f}%")
    print(f"  CoT:     {cot_correct:.1f}%")
    print(f"\n  CoT vs 기본: {cot_correct - basic_correct:+.1f}%p")
    print(f"  CoT vs 구조화: {cot_correct - struct_correct:+.1f}%p")

    # 토큰 효율성
    print(f"\n[토큰 효율성]")
    basic_tokens = all_results["기본"]["avg_tokens"]
    cot_tokens = all_results["CoT"]["avg_tokens"]
    print(f"  기본: {basic_tokens:.0f} 토큰")
    print(f"  CoT:  {cot_tokens:.0f} 토큰 ({(cot_tokens/basic_tokens - 1)*100:+.0f}% 증가)")

    # 결과 저장
    save_data = {
        "experiment": "CoT_hard_problems_v2",
        "timestamp": datetime.now().isoformat(),
        "model": "qwen2.5:7b",
        "test_cases_count": len(test_cases),
        "evaluation_criteria": {
            "exact": "응답이 정답과 정확히 일치",
            "contains": "응답에 정답이 포함됨",
            "correct": "정답 포함 또는 추출된 답이 일치"
        },
        "results": {
            method: {
                "exact_accuracy": f"{r['exact_accuracy']*100:.1f}%",
                "contains_accuracy": f"{r['contains_accuracy']*100:.1f}%",
                "correct_accuracy": f"{r['correct_accuracy']*100:.1f}%",
                "avg_tokens": round(r['avg_tokens']),
                "avg_time": f"{r['avg_time']:.2f}s"
            }
            for method, r in all_results.items()
        },
        "conclusion": {
            "cot_vs_basic": f"{cot_correct - basic_correct:+.1f}%p",
            "cot_vs_structured": f"{cot_correct - struct_correct:+.1f}%p",
            "token_overhead": f"{(cot_tokens/basic_tokens - 1)*100:+.0f}%"
        }
    }

    with open("results/cot_hard_experiment_v2.json", "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)

    print(f"\n결과 저장: results/cot_hard_experiment_v2.json")
    print("\n실험 완료!")

    return all_results


if __name__ == "__main__":
    run_experiment()
