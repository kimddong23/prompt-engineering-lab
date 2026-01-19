# -*- coding: utf-8 -*-
"""
================================================================================
프롬프트 엔지니어링 종합 실험 스크립트 (Comprehensive Experiment Runner)
================================================================================

## 이 파일의 목적
이 스크립트는 10가지 프롬프트 엔지니어링 기법을 체계적으로 실험하고
정량적 결과를 수집하는 **메인 실험 실행기**입니다.

## 왜 이 파일이 필요한가?
1. **재현성 (Reproducibility)**: 동일한 실험을 누구나 재실행 가능
2. **자동화**: 10개 실험을 순차적으로 자동 실행
3. **결과 저장**: JSON 형식으로 결과를 저장하여 분석 용이

## 실험 구성 (총 10개)

| # | 실험명 | 검증 가설 | 학술적 근거 |
|---|--------|-----------|-------------|
| 1 | 기본 vs 구조화 (단순) | 구조화가 단순 문제에서 효과적인가? | - |
| 2 | 기본 vs 구조화 (복잡) | 구조화가 복잡한 문제에서도 효과적인가? | - |
| 3 | Chain of Thought | CoT가 추론 성능을 향상시키는가? | NeurIPS 2022 |
| 4 | Zero-shot vs Few-shot | 예시가 분류 성능을 향상시키는가? | GPT-3 (2020) |
| 5 | Few-shot 예시 개수 | 예시 개수가 성능에 영향을 주는가? | GPT-3 (2020) |
| 6 | 역할 부여 (Role) | 역할이 답변 품질에 영향을 주는가? | Persona-based |
| 7 | 출력 형식 | 구조화된 출력이 정확도를 높이는가? | - |
| 8 | 프롬프트 길이 | 상세한 프롬프트가 더 효과적인가? | - |
| 9 | Self-Consistency | 다수결이 정확도를 높이는가? | ICLR 2023 |
| 10 | 종합 최적화 | 모든 기법을 결합하면 최고 성능인가? | - |

## 학술적 배경

### Chain of Thought (CoT)
- **논문**: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- **학회**: NeurIPS 2022
- **저자**: Jason Wei et al. (Google Research)
- **핵심**: "Let's think step by step"으로 추론 성능 대폭 향상

### Few-shot Learning
- **논문**: "Language Models are Few-Shot Learners"
- **학회**: NeurIPS 2020
- **저자**: Brown et al. (OpenAI)
- **핵심**: 소수의 예시만으로 새로운 작업 수행 가능

### Self-Consistency
- **논문**: "Self-Consistency Improves Chain of Thought Reasoning in LLMs"
- **학회**: ICLR 2023
- **저자**: Wang et al.
- **핵심**: 여러 추론 경로의 다수결로 정확도 향상

## 사용 방법

```bash
# Ollama 서버 실행 (별도 터미널)
ollama serve

# 실험 실행
python run_all_experiments.py

# 결과 확인
cat results/all_experiments.json
```

## 실험 결과 예시

```
[실험 3] Chain of Thought (복잡한 문제)
------------------------------------------------------------
  기본                  정확도:  93.3%  (14/15)  토큰:   169  시간: 1.23s
  CoT                   정확도: 100.0%  (15/15)  토큰:   300  시간: 2.15s
```

================================================================================
"""

import sys
import json
import re
import time
from datetime import datetime
from typing import Dict, List, Any

# ============================================================================
# Windows 환경 한글 출력 설정
# ============================================================================
# 왜 필요한가?
# Windows 콘솔에서 한글(UTF-8) 출력 시 인코딩 오류 방지
# Python 기본 콘솔 인코딩이 cp949인 경우 한글 출력 시 에러 발생
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ============================================================================
# 필수 라이브러리 임포트
# ============================================================================
from langchain_ollama import ChatOllama  # LangChain의 Ollama 연동 모듈
import tiktoken                           # OpenAI 토크나이저 (토큰 수 측정용)

# 테스트 케이스 모듈 (evaluation 패키지)
from evaluation.test_cases import (
    get_math_test_suite,           # 수학 문제 40개
    get_logic_test_suite,          # 논리 문제 23개
    get_classification_test_suite, # 분류 문제 40개
    get_hard_problems_suite        # 어려운 문제 (수학+논리) 26개
)


# ============================================================================
# ExperimentRunner 클래스
# ============================================================================
class ExperimentRunner:
    """
    프롬프트 엔지니어링 실험 실행기

    이 클래스의 역할
    ----------------
    1. LLM과의 통신 (Ollama API 호출)
    2. 토큰 수 측정 (비용/효율성 분석용)
    3. 정답 체크 (다양한 형태의 답변 처리)
    4. 배치 실험 실행 및 결과 집계

    왜 클래스로 구현했는가?
    ---------------------
    - LLM 인스턴스를 재사용하여 연결 오버헤드 감소
    - 토크나이저 인스턴스 공유로 메모리 효율성 확보
    - 상태 관리 (실험 결과 누적) 용이

    Attributes
    ----------
    llm : ChatOllama
        Ollama LLM 인스턴스 (qwen2.5:7b 모델)
    enc : tiktoken.Encoding
        토큰 수 측정을 위한 토크나이저
    all_results : dict
        모든 실험 결과를 저장하는 딕셔너리

    Example
    -------
    >>> runner = ExperimentRunner(model="qwen2.5:7b")
    >>> result = runner.run_single("1 + 1 = ?", "2")
    >>> print(result["correct"])  # True
    """

    def __init__(self, model: str = "qwen2.5:7b"):
        """
        실험 실행기 초기화

        Parameters
        ----------
        model : str, optional
            사용할 Ollama 모델명 (기본값: "qwen2.5:7b")

        왜 temperature=0인가?
        --------------------
        - 실험 재현성을 위해 결정적(deterministic) 출력 사용
        - temperature > 0이면 매번 다른 출력이 나와 비교 어려움
        """
        self.llm = ChatOllama(model=model, temperature=0)

        # tiktoken 토크나이저 초기화
        # 왜 gpt-3.5-turbo 인코딩을 사용하는가?
        # - tiktoken은 OpenAI 모델용이지만 토큰 수 추정에 범용적으로 사용
        # - 정확한 토큰 수보다는 상대적 비교가 목적
        self.enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

        # 실험 결과 저장소
        self.all_results = {}

    def count_tokens(self, text: str) -> int:
        """
        텍스트의 토큰 수를 계산

        왜 토큰 수를 측정하는가?
        ----------------------
        - LLM API 비용은 토큰 수에 비례
        - 프롬프트 효율성 비교의 핵심 지표
        - 토큰 35% 절감 목표 달성 여부 측정

        Parameters
        ----------
        text : str
            토큰 수를 측정할 텍스트

        Returns
        -------
        int
            토큰 수
        """
        return len(self.enc.encode(text))

    def check_answer(self, response: str, expected: str) -> bool:
        """
        LLM 응답이 정답과 일치하는지 확인

        왜 단순 문자열 비교가 아닌가?
        ---------------------------
        LLM 응답은 다양한 형태로 올 수 있음:
        - "정답은 42입니다" (문장 형태)
        - "42" (숫자만)
        - "답: 42" (레이블 포함)

        따라서 여러 방식으로 정답 여부를 판단해야 함

        Parameters
        ----------
        response : str
            LLM의 응답 텍스트
        expected : str
            기대하는 정답

        Returns
        -------
        bool
            정답이면 True, 오답이면 False

        Note
        ----
        - 포함 여부 체크 (expected in response)
        - 숫자 추출 후 비교
        - 예/아니오 변형 처리 (네/아니 등)
        """
        response_clean = response.strip().lower()
        expected_clean = expected.strip().lower()

        # 1차: 정확히 일치하거나 포함되면 정답
        if expected_clean in response_clean:
            return True

        # 2차: 숫자 추출 비교 (수학 문제용)
        # 예: "42개" -> ["42"] 추출
        resp_nums = re.findall(r'\d+', response)
        if resp_nums and expected_clean in resp_nums:
            return True

        # 3차: 예/아니오 변형 처리 (논리 문제용)
        # 한국어에서 "예"는 "네"로도 표현됨
        if expected_clean in ['예', '아니오']:
            if expected_clean == '예' and ('예' in response_clean or '네' in response_clean):
                return True
            if expected_clean == '아니오' and ('아니오' in response_clean or '아니' in response_clean):
                return True

        return False

    def run_single(self, prompt: str, expected: str) -> Dict:
        """
        단일 프롬프트 실행 및 결과 측정

        Parameters
        ----------
        prompt : str
            LLM에 보낼 프롬프트
        expected : str
            기대하는 정답

        Returns
        -------
        dict
            실행 결과 딕셔너리:
            - response: LLM 응답 텍스트
            - correct: 정답 여부 (bool)
            - tokens: 총 토큰 수 (입력 + 출력)
            - time: 응답 시간 (초)
        """
        start = time.time()
        response = self.llm.invoke(prompt).content
        elapsed = time.time() - start

        # 토큰 수 = 입력 토큰 + 출력 토큰
        tokens = self.count_tokens(prompt) + self.count_tokens(response)
        correct = self.check_answer(response, expected)

        return {
            "response": response,
            "correct": correct,
            "tokens": tokens,
            "time": elapsed
        }

    def run_batch(self, template: str, test_cases: List[Dict], input_key: str = "q") -> Dict:
        """
        여러 테스트 케이스를 배치로 실행

        왜 배치 실행이 필요한가?
        ----------------------
        - 개별 실행보다 통계적으로 유의미한 결과 도출
        - 평균 정확도, 토큰 수, 응답 시간 계산
        - 프롬프트 기법 간 공정한 비교

        Parameters
        ----------
        template : str
            프롬프트 템플릿 (예: "질문: {q}\\n답:")
        test_cases : List[Dict]
            테스트 케이스 리스트
        input_key : str, optional
            입력 키 이름 (기본값: "q")

        Returns
        -------
        dict
            집계된 결과:
            - accuracy: 정확도 (0~1)
            - correct: 정답 개수
            - total: 전체 개수
            - avg_tokens: 평균 토큰 수
            - avg_time: 평균 응답 시간
        """
        correct_count = 0
        total_tokens = 0
        total_time = 0

        for case in test_cases:
            # 템플릿에 입력 값 삽입
            prompt = template.format(**case["input"])
            result = self.run_single(prompt, case["expected"])

            if result["correct"]:
                correct_count += 1
            total_tokens += result["tokens"]
            total_time += result["time"]

        n = len(test_cases)
        return {
            "accuracy": correct_count / n if n > 0 else 0,
            "correct": correct_count,
            "total": n,
            "avg_tokens": total_tokens / n if n > 0 else 0,
            "avg_time": total_time / n if n > 0 else 0
        }

    def print_result(self, name: str, result: Dict):
        """
        실험 결과를 포맷팅하여 출력

        출력 형식:
        방법명               정확도: 100.0%  (10/10)  토큰:   150  시간: 1.23s
        """
        print(f"  {name:<20} 정확도: {result['accuracy']*100:>5.1f}%  "
              f"({result['correct']}/{result['total']})  "
              f"토큰: {result['avg_tokens']:>5.0f}  "
              f"시간: {result['avg_time']:.2f}s")


# ============================================================================
# 실험 1: 기본 vs 구조화 프롬프트 (단순 문제)
# ============================================================================
def run_experiment_1(runner: ExperimentRunner) -> Dict:
    """
    실험 1: 기본 프롬프트 vs 구조화 프롬프트 (단순 수학 문제)

    실험 목적
    --------
    단순한 수학 문제에서 구조화 프롬프트가 기본 프롬프트보다
    효과적인지 검증

    가설
    ----
    - H0 (귀무가설): 두 방식의 정확도는 차이가 없다
    - H1 (대립가설): 구조화 프롬프트가 더 높은 정확도를 보인다

    실험 설계
    --------
    - 테스트 케이스: 단순 수학 문제 10개 (easy 난이도)
    - 독립 변수: 프롬프트 형식 (기본 vs 구조화)
    - 종속 변수: 정확도, 토큰 수, 응답 시간

    프롬프트 비교
    ------------
    | 방식 | 프롬프트 |
    |------|----------|
    | 기본 | "질문: {q}\\n답:" |
    | 구조화 | "### 질문\\n{q}\\n\\n### 답 (숫자만)" |

    Returns
    -------
    dict
        각 방식의 실험 결과
    """
    print("\n[실험 1] 기본 vs 구조화 프롬프트 (단순 수학)")
    print("-" * 60)

    # 단순 수학 문제 10개 선택
    math = get_math_test_suite()
    easy = [c for c in math.to_list() if c.get("difficulty") == "easy"][:10]

    # 비교할 프롬프트 템플릿
    prompts = {
        "기본": "질문: {q}\n답:",
        "구조화": "### 질문\n{q}\n\n### 답 (숫자만)"
    }

    results = {}
    for name, template in prompts.items():
        results[name] = runner.run_batch(template, easy)
        runner.print_result(name, results[name])

    return results


# ============================================================================
# 실험 2: 기본 vs 구조화 프롬프트 (복잡한 문제)
# ============================================================================
def run_experiment_2(runner: ExperimentRunner) -> Dict:
    """
    실험 2: 기본 vs 구조화 프롬프트 (복잡한 수학 문제)

    실험 목적
    --------
    복잡한 수학 문제에서 구조화 프롬프트의 효과를 검증
    (실험 1과의 비교를 통해 문제 난이도에 따른 효과 차이 분석)

    왜 복잡한 문제를 따로 실험하는가?
    ------------------------------
    - 단순 문제: 두 방식 모두 높은 정확도 → 차이 없음
    - 복잡한 문제: 프롬프트 품질이 결과에 더 큰 영향
    - GSM8K 벤치마크도 난이도별 분석 권장

    Returns
    -------
    dict
        각 방식의 실험 결과
    """
    print("\n[실험 2] 기본 vs 구조화 프롬프트 (복잡한 문제)")
    print("-" * 60)

    # 복잡한 수학 문제 15개 선택
    math = get_math_test_suite()
    hard = [c for c in math.to_list() if c.get("difficulty") == "hard"][:15]

    # 구조화 프롬프트에 규칙 추가
    prompts = {
        "기본": "질문: {q}\n답:",
        "구조화": "### 질문\n{q}\n\n### 규칙\n- 숫자만 답하세요\n\n### 답"
    }

    results = {}
    for name, template in prompts.items():
        results[name] = runner.run_batch(template, hard)
        runner.print_result(name, results[name])

    return results


# ============================================================================
# 실험 3: Chain of Thought (CoT)
# ============================================================================
def run_experiment_3(runner: ExperimentRunner) -> Dict:
    """
    실험 3: Chain of Thought 프롬프팅

    학술적 배경
    ----------
    - **논문**: Chain-of-Thought Prompting Elicits Reasoning in LLMs
    - **학회**: NeurIPS 2022
    - **저자**: Jason Wei et al. (Google Research)
    - **핵심 발견**: "Let's think step by step"만 추가해도 추론 성능 대폭 향상

    왜 CoT가 효과적인가?
    ------------------
    1. 중간 추론 단계를 명시적으로 생성하게 함
    2. 복잡한 문제를 작은 단계로 분해
    3. 오류 발생 시 어느 단계에서 틀렸는지 파악 가능

    실험 설계
    --------
    - 테스트 케이스: 복잡한 문제 15개 (hard 난이도)
    - 비교: 기본 프롬프트 vs CoT 프롬프트

    CoT 프롬프트 구조
    ----------------
    ```
    질문: {q}

    차근차근 단계별로 생각해봅시다.
    1단계: 주어진 정보 정리
    2단계: 계산/추론
    3단계: 최종 답

    풀이:
    ```

    기대 효과
    --------
    - 정확도: +6.7%p 이상 향상 예상
    - 토큰 수: 2배 이상 증가 (풀이 과정 포함)

    Returns
    -------
    dict
        기본 vs CoT 실험 결과
    """
    print("\n[실험 3] Chain of Thought (복잡한 문제)")
    print("-" * 60)

    # 복잡한 문제 15개
    hard = get_hard_problems_suite().to_list()[:15]

    prompts = {
        "기본": "질문: {q}\n답:",
        "CoT": """질문: {q}

차근차근 단계별로 생각해봅시다.
1단계: 주어진 정보 정리
2단계: 계산/추론
3단계: 최종 답

풀이:"""
    }

    results = {}
    for name, template in prompts.items():
        results[name] = runner.run_batch(template, hard)
        runner.print_result(name, results[name])

    return results


# ============================================================================
# 실험 4: Zero-shot vs Few-shot
# ============================================================================
def run_experiment_4(runner: ExperimentRunner) -> Dict:
    """
    실험 4: Zero-shot vs Few-shot 학습

    학술적 배경
    ----------
    - **논문**: Language Models are Few-Shot Learners
    - **학회**: NeurIPS 2020
    - **저자**: Brown et al. (OpenAI)
    - **핵심**: GPT-3가 소수의 예시만으로 새로운 작업 수행 가능

    개념 정의
    --------
    - **Zero-shot**: 예시 없이 작업 설명만 제공
    - **Few-shot**: 작업 설명 + 예시 제공 (In-Context Learning)

    왜 Few-shot이 효과적인가?
    -----------------------
    1. 예시를 통해 출력 형식을 명확히 보여줌
    2. 모호한 지시를 구체화
    3. 모델이 패턴을 인식하여 일관된 출력 생성

    실험 설계
    --------
    - 작업: 감성 분류 (긍정/부정/중립)
    - 테스트 케이스: 15개
    - 비교: Zero-shot vs Few-shot (3개 예시)

    Returns
    -------
    dict
        Zero-shot vs Few-shot 실험 결과
    """
    print("\n[실험 4] Zero-shot vs Few-shot (감성 분류)")
    print("-" * 60)

    classification = get_classification_test_suite().to_list()[:15]

    # Zero-shot: 예시 없음
    zero_shot = """다음 텍스트의 감성을 분류하세요.
카테고리: 긍정, 부정, 중립

텍스트: {text}
감성:"""

    # Few-shot: 3개 예시 포함
    few_shot = """다음 텍스트의 감성을 분류하세요.
카테고리: 긍정, 부정, 중립

예시:
- "정말 좋아요!" → 긍정
- "별로예요" → 부정
- "그냥 그래요" → 중립

텍스트: {text}
감성:"""

    prompts = {"Zero-shot": zero_shot, "Few-shot (3예시)": few_shot}

    results = {}
    for name, template in prompts.items():
        results[name] = runner.run_batch(template, classification, "text")
        runner.print_result(name, results[name])

    return results


# ============================================================================
# 실험 5: Few-shot 예시 개수 실험
# ============================================================================
def run_experiment_5(runner: ExperimentRunner) -> Dict:
    """
    실험 5: Few-shot 예시 개수에 따른 성능 비교

    실험 목적
    --------
    Few-shot 예시 개수가 성능에 미치는 영향 분석

    가설
    ----
    - 예시가 많을수록 성능이 향상될 것이다
    - 그러나 일정 개수 이상에서는 수확 체감 발생

    실험 설계
    --------
    - 비교: 1-shot vs 3-shot vs 5-shot
    - 작업: 감성 분류
    - 테스트 케이스: 12개

    왜 5-shot까지만 실험하는가?
    ------------------------
    - 컨텍스트 길이 제한
    - 비용 증가
    - GPT-3 논문에서 5-shot 이상은 성능 향상 미미

    Returns
    -------
    dict
        1/3/5-shot 실험 결과
    """
    print("\n[실험 5] Few-shot 예시 개수 (1개 vs 3개 vs 5개)")
    print("-" * 60)

    classification = get_classification_test_suite().to_list()[:12]

    # 1-shot: 예시 1개
    one_shot = """감성 분류 (긍정/부정/중립)
예시: "좋아요" → 긍정

텍스트: {text}
감성:"""

    # 3-shot: 예시 3개 (각 카테고리당 1개)
    three_shot = """감성 분류 (긍정/부정/중립)
예시:
- "정말 좋아요" → 긍정
- "별로예요" → 부정
- "보통이에요" → 중립

텍스트: {text}
감성:"""

    # 5-shot: 예시 5개 (다양한 표현)
    five_shot = """감성 분류 (긍정/부정/중립)
예시:
- "최고예요!" → 긍정
- "만족합니다" → 긍정
- "실망이에요" → 부정
- "안 좋아요" → 부정
- "그냥 그래요" → 중립

텍스트: {text}
감성:"""

    prompts = {"1-shot": one_shot, "3-shot": three_shot, "5-shot": five_shot}

    results = {}
    for name, template in prompts.items():
        results[name] = runner.run_batch(template, classification, "text")
        runner.print_result(name, results[name])

    return results


# ============================================================================
# 실험 6: 역할 부여 (Role Prompting)
# ============================================================================
def run_experiment_6(runner: ExperimentRunner) -> Dict:
    """
    실험 6: 역할 부여 (Role Prompting)

    실험 목적
    --------
    LLM에 특정 역할(페르소나)을 부여했을 때 답변 품질 변화 분석

    왜 역할 부여가 효과적인가?
    -----------------------
    1. 답변 스타일과 톤 조절
    2. 전문 지식 활성화 (관련 학습 데이터 접근)
    3. 일관된 페르소나 유지

    비교 대상
    --------
    | 역할 | 특징 |
    |------|------|
    | 역할 없음 | 기본 프롬프트 |
    | 수학 선생님 | 단순 역할 부여 |
    | 교육 전문가 | 상세한 역할 + 맥락 |

    가설
    ----
    - 구체적인 역할 + 맥락이 단순 역할보다 효과적
    - "20년 경력", "초등학생도 이해 가능" 등 상세 설명이 성능 향상에 기여

    Returns
    -------
    dict
        각 역할별 실험 결과
    """
    print("\n[실험 6] 역할 부여 (Role Prompting)")
    print("-" * 60)

    # 복잡한 수학 문제 12개
    math = get_math_test_suite()
    hard = [c for c in math.to_list() if c.get("difficulty") == "hard"][:12]

    # 역할 없음 (기본)
    no_role = """질문: {q}
답:"""

    # 단순 역할 부여
    with_role = """당신은 수학 선생님입니다. 학생의 질문에 정확하게 답해주세요.

학생 질문: {q}
선생님 답변 (숫자만):"""

    # 상세한 역할 + 맥락
    expert_role = """당신은 20년 경력의 수학 교육 전문가입니다.
초등학생도 이해할 수 있게 문제를 풀어주세요.

문제: {q}

풀이 후 최종 답 (숫자만):"""

    prompts = {"역할 없음": no_role, "수학 선생님": with_role, "교육 전문가": expert_role}

    results = {}
    for name, template in prompts.items():
        results[name] = runner.run_batch(template, hard)
        runner.print_result(name, results[name])

    return results


# ============================================================================
# 실험 7: 출력 형식 지정
# ============================================================================
def run_experiment_7(runner: ExperimentRunner) -> Dict:
    """
    실험 7: 출력 형식 지정 (자유형 vs JSON)

    실험 목적
    --------
    구조화된 출력 형식이 정확도에 미치는 영향 분석

    왜 출력 형식이 중요한가?
    ----------------------
    1. 파싱 용이성: JSON은 프로그래밍적 처리 쉬움
    2. 일관성: 정해진 형식으로 답변 → 품질 균일
    3. 명확성: 모델이 출력 형태를 명확히 인지

    비교 대상
    --------
    - 자유형: "이 텍스트의 감성은?"
    - JSON 형식: {"sentiment": "긍정/부정/중립"} 요청

    실무 적용
    --------
    - API 응답: JSON 형식 필수
    - 데이터 파이프라인: 구조화된 출력 선호
    - 로깅/분석: 파싱 가능한 형식 필요

    Returns
    -------
    dict
        자유형 vs JSON 형식 실험 결과
    """
    print("\n[실험 7] 출력 형식 (자유형 vs JSON)")
    print("-" * 60)

    classification = get_classification_test_suite().to_list()[:12]

    # 자유형: 형식 미지정
    free_form = """텍스트: {text}
이 텍스트의 감성은?"""

    # JSON 형식 요청
    json_format = """텍스트: {text}

다음 JSON 형식으로 답하세요:
{{"sentiment": "긍정/부정/중립"}}

JSON:"""

    prompts = {"자유형": free_form, "JSON 형식": json_format}

    results = {}
    for name, template in prompts.items():
        results[name] = runner.run_batch(template, classification, "text")
        runner.print_result(name, results[name])

    return results


# ============================================================================
# 실험 8: 프롬프트 길이
# ============================================================================
def run_experiment_8(runner: ExperimentRunner) -> Dict:
    """
    실험 8: 프롬프트 길이에 따른 성능 비교

    실험 목적
    --------
    프롬프트 길이(상세도)가 답변 품질에 미치는 영향 분석

    비교 대상
    --------
    | 길이 | 설명 | 토큰 수 (예상) |
    |------|------|---------------|
    | 짧은 | 최소한의 지시 | ~10 |
    | 중간 | 구조화된 형식 | ~20 |
    | 긴 | 상세 지시 + 규칙 | ~50 |

    가설
    ----
    - 복잡한 문제일수록 긴 프롬프트가 효과적
    - 그러나 너무 긴 프롬프트는 비용 증가 + 노이즈 유발

    트레이드오프
    -----------
    - 짧은 프롬프트: 비용↓, 속도↑, 정확도↓
    - 긴 프롬프트: 비용↑, 속도↓, 정확도↑

    Returns
    -------
    dict
        짧은/중간/긴 프롬프트 실험 결과
    """
    print("\n[실험 8] 프롬프트 길이 (짧은/중간/긴)")
    print("-" * 60)

    # 논리 문제 10개
    logic = get_logic_test_suite().to_list()[:10]

    # 짧은 프롬프트: 최소한의 지시
    short = "{q}\n답:"

    # 중간 프롬프트: 구조화
    medium = """### 질문
{q}

### 답"""

    # 긴 프롬프트: 상세 지시 + 규칙
    long = """### 지시사항
아래 논리 문제를 읽고 답하세요.
- 주어진 정보만 사용하세요
- 추측하지 마세요
- 명확하게 답하세요

### 문제
{q}

### 분석 및 답"""

    prompts = {"짧은": short, "중간": medium, "긴": long}

    results = {}
    for name, template in prompts.items():
        results[name] = runner.run_batch(template, logic)
        runner.print_result(name, results[name])

    return results


# ============================================================================
# 실험 9: Self-Consistency (다수결)
# ============================================================================
def run_experiment_9(runner: ExperimentRunner) -> Dict:
    """
    실험 9: Self-Consistency (자기 일관성)

    학술적 배경
    ----------
    - **논문**: Self-Consistency Improves Chain of Thought Reasoning
    - **학회**: ICLR 2023
    - **저자**: Wang et al.
    - **핵심**: 여러 추론 경로를 생성하고 다수결로 최종 답 선택

    작동 원리
    --------
    1. 동일 문제에 대해 여러 번 추론 (temperature > 0)
    2. 각 추론에서 답 추출
    3. 가장 많이 나온 답을 최종 답으로 선택 (다수결)

    왜 효과적인가?
    -------------
    - 개별 추론은 틀릴 수 있지만, 다수결은 더 안정적
    - 앙상블 효과: 여러 모델의 예측을 결합하는 것과 유사
    - 불확실한 문제에서 신뢰도 향상

    실험 설계
    --------
    - 비교: 단일 실행 vs 3회 실행 후 다수결
    - temperature: 0.7 (다양한 답변 유도)
    - 테스트 케이스: 복잡한 수학 문제 8개

    Note
    ----
    이 실험은 temperature=0.7을 사용하므로 별도 LLM 인스턴스 생성

    Returns
    -------
    dict
        단일 실행 vs 다수결 실험 결과
    """
    print("\n[실험 9] Self-Consistency (3회 다수결)")
    print("-" * 60)

    # temperature를 높여서 다양한 답변 유도
    # 왜 temperature=0.7인가?
    # - 0: 결정적 출력 (항상 같은 답)
    # - 0.7: 적당한 다양성 (서로 다른 추론 경로)
    # - 1.0+: 너무 무작위적
    runner_temp = ExperimentRunner()
    runner_temp.llm = ChatOllama(model="qwen2.5:7b", temperature=0.7)

    # 복잡한 수학 문제 8개 (Self-Consistency는 연산 비용이 3배)
    math = get_math_test_suite()
    hard = [c for c in math.to_list() if c.get("difficulty") == "hard"][:8]

    template = """질문: {q}

단계별로 풀어보세요.
답:"""

    # 단일 실행 정답 수
    single_correct = 0
    # 다수결 (3회) 정답 수
    majority_correct = 0

    for case in hard:
        prompt = template.format(**case["input"])
        expected = case["expected"]

        # 3회 실행하여 각각의 답 수집
        answers = []
        for _ in range(3):
            response = runner_temp.llm.invoke(prompt).content
            # 숫자 추출 (마지막 숫자를 최종 답으로 간주)
            nums = re.findall(r'\d+', response)
            if nums:
                answers.append(nums[-1])

        # 단일 실행 (첫 번째 답) 평가
        if answers and runner.check_answer(answers[0], expected):
            single_correct += 1

        # 다수결 평가
        if answers:
            from collections import Counter
            most_common = Counter(answers).most_common(1)[0][0]
            if runner.check_answer(most_common, expected):
                majority_correct += 1

    n = len(hard)
    results = {
        "단일 실행": {"accuracy": single_correct/n, "correct": single_correct, "total": n, "avg_tokens": 0, "avg_time": 0},
        "3회 다수결": {"accuracy": majority_correct/n, "correct": majority_correct, "total": n, "avg_tokens": 0, "avg_time": 0}
    }

    for name, result in results.items():
        runner.print_result(name, result)

    return results


# ============================================================================
# 실험 10: 종합 최적화 프롬프트
# ============================================================================
def run_experiment_10(runner: ExperimentRunner) -> Dict:
    """
    실험 10: 종합 최적화 프롬프트

    실험 목적
    --------
    지금까지 효과적이었던 기법들을 결합한 최적화 프롬프트 검증

    적용 기법
    --------
    1. **구조화**: 마크다운 헤더로 섹션 구분
    2. **역할 부여**: "문제 해결 전문가"
    3. **Chain of Thought**: 단계별 풀이 과정 명시
    4. **출력 형식**: "숫자 또는 예/아니오만" 명시

    프롬프트 구조
    ------------
    ```
    ### 역할
    당신은 정확한 답변을 제공하는 문제 해결 전문가입니다.

    ### 문제
    {q}

    ### 풀이 방법
    1. 주어진 정보를 파악합니다
    2. 필요한 계산/추론을 수행합니다
    3. 최종 답을 도출합니다

    ### 풀이 과정


    ### 최종 답 (숫자 또는 예/아니오만):
    ```

    기대 효과
    --------
    - 개별 기법의 장점을 모두 활용
    - 복잡한 문제에서 기본 대비 +6.7%p 이상 향상 예상

    Returns
    -------
    dict
        기본 vs 종합 최적화 실험 결과
    """
    print("\n[실험 10] 종합 최적화 프롬프트")
    print("-" * 60)

    # 복잡한 문제 15개
    hard = get_hard_problems_suite().to_list()[:15]

    # 기본 프롬프트
    basic = "질문: {q}\n답:"

    # 종합 최적화 프롬프트
    # 구조화 + CoT + 역할 + 출력 형식 모두 적용
    optimized = """### 역할
당신은 정확한 답변을 제공하는 문제 해결 전문가입니다.

### 문제
{q}

### 풀이 방법
1. 주어진 정보를 파악합니다
2. 필요한 계산/추론을 수행합니다
3. 최종 답을 도출합니다

### 풀이 과정


### 최종 답 (숫자 또는 예/아니오만):"""

    prompts = {"기본": basic, "종합 최적화": optimized}

    results = {}
    for name, template in prompts.items():
        results[name] = runner.run_batch(template, hard)
        runner.print_result(name, results[name])

    return results


# ============================================================================
# 메인 함수
# ============================================================================
def main():
    """
    전체 실험 실행 및 결과 저장

    실행 순서
    --------
    1. ExperimentRunner 초기화
    2. 10개 실험 순차 실행
    3. 결과 요약 출력
    4. JSON 파일로 결과 저장

    출력 파일
    --------
    results/all_experiments.json
    - 모든 실험의 정확도, 정답 수, 전체 문제 수 포함
    - timestamp로 실험 시점 기록
    """
    print("=" * 70)
    print("프롬프트 엔지니어링 종합 실험 (10개)")
    print("=" * 70)
    print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 실험 실행기 초기화
    runner = ExperimentRunner()
    all_results = {}

    # 10개 실험 정의
    # 각 튜플: (실험명, 실행 함수)
    experiments = [
        ("1. 기본 vs 구조화 (단순)", run_experiment_1),
        ("2. 기본 vs 구조화 (복잡)", run_experiment_2),
        ("3. Chain of Thought", run_experiment_3),
        ("4. Zero-shot vs Few-shot", run_experiment_4),
        ("5. Few-shot 예시 개수", run_experiment_5),
        ("6. 역할 부여", run_experiment_6),
        ("7. 출력 형식", run_experiment_7),
        ("8. 프롬프트 길이", run_experiment_8),
        ("9. Self-Consistency", run_experiment_9),
        ("10. 종합 최적화", run_experiment_10),
    ]

    # 실험 순차 실행
    for name, func in experiments:
        try:
            all_results[name] = func(runner)
        except Exception as e:
            print(f"  오류 발생: {e}")
            all_results[name] = {"error": str(e)}

    # ========================================
    # 종합 결과 요약
    # ========================================
    print("\n" + "=" * 70)
    print("종합 결과 요약")
    print("=" * 70)

    # 결과 저장용 딕셔너리
    save_data = {
        "experiment": "comprehensive_prompt_engineering",
        "timestamp": datetime.now().isoformat(),
        "model": "qwen2.5:7b",
        "total_experiments": len(experiments),
        "results": {}
    }

    # 각 실험별 최고 성능 방법 출력
    for exp_name, exp_results in all_results.items():
        print(f"\n{exp_name}:")
        save_data["results"][exp_name] = {}

        if "error" in exp_results:
            print(f"  오류: {exp_results['error']}")
            save_data["results"][exp_name] = {"error": exp_results["error"]}
        else:
            # 정확도가 가장 높은 방법 찾기
            best_method = max(exp_results.items(), key=lambda x: x[1].get("accuracy", 0))
            print(f"  최고: {best_method[0]} ({best_method[1]['accuracy']*100:.1f}%)")

            # 모든 방법의 결과 저장
            for method, result in exp_results.items():
                save_data["results"][exp_name][method] = {
                    "accuracy": f"{result['accuracy']*100:.1f}%",
                    "correct": result["correct"],
                    "total": result["total"]
                }

    # ========================================
    # 결과를 JSON 파일로 저장
    # ========================================
    with open("results/all_experiments.json", "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)

    print(f"\n결과 저장: results/all_experiments.json")
    print(f"완료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 70)
    print("모든 실험 완료!")
    print("=" * 70)


# ============================================================================
# 스크립트 실행
# ============================================================================
if __name__ == "__main__":
    main()
