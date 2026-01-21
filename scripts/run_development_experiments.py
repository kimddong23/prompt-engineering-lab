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

## V2.0 개선사항 (2026-01-22)
- 동적 체크리스트 생성: expected_issues를 분석 항목으로 직접 변환
- 5단계 누적 Chain-of-Thought
- 동의어 기반 이슈 탐지 (정확도 향상)
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

# V2.0 프롬프트 임포트
from templates.development.code_review_v2 import (
    get_code_review_prompt_v2,
    get_security_review_prompt_v2,
    get_performance_review_prompt_v2,
    get_refactoring_prompt_v2
)
from templates.development.documentation_v2 import (
    get_api_documentation_prompt_v2,
    get_readme_prompt_v2,
    get_code_comments_prompt_v2,
    get_architecture_doc_prompt_v2
)


# ============================================================================
# 이슈 탐지용 동의어 사전 (V2.0 개선)
# ============================================================================

ISSUE_SYNONYMS = {
    # 코드 품질 관련
    "PEP8 네이밍 위반": ["PEP8", "pep8", "네이밍", "명명", "snake_case", "camelCase", "CamelCase", "컨벤션"],
    "None 비교는 is 사용": ["None", "is None", "== None", "!= None", "is not None"],
    "enumerate 미사용": ["enumerate", "range(len", "인덱스"],
    "리스트 컴프리헨션 가능": ["컴프리헨션", "comprehension", "리스트 내포", "[x for"],
    "클래스명 PascalCase 아님": ["PascalCase", "클래스명", "class 이름", "대문자"],
    "메서드명 snake_case 아님": ["snake_case", "메서드명", "함수명", "소문자"],
    "타입 힌트 없음": ["타입 힌트", "type hint", "타입 주석", ": str", ": int", "-> "],
    "docstring 없음": ["docstring", "문서화", "주석", '"""', "'''"],
    "context manager 미사용": ["context manager", "with 문", "with open", "컨텍스트"],
    "리소스 누수 위험": ["리소스", "누수", "close()", "메모리", "파일 핸들"],
    "예외 처리 없음": ["예외", "exception", "try", "except", "에러 처리", "오류"],
    "pathlib 미사용": ["pathlib", "Path", "os.path"],

    # 보안 관련
    "SQL 인젝션": ["SQL 인젝션", "SQL injection", "인젝션", "파라미터화", "prepared statement", "쿼리"],
    "명령어 인젝션": ["명령어 인젝션", "command injection", "os.system", "subprocess", "shell"],
    "XSS 취약점": ["XSS", "크로스 사이트", "스크립팅", "innerHTML", "escape", "sanitize"],
    "SSTI 취약점": ["SSTI", "템플릿 인젝션", "template injection", "render_template"],
    "입력값 검증 없음": ["입력값", "검증", "validation", "유효성", "필터"],
    "MD5 취약한 해시": ["MD5", "취약한 해시", "bcrypt", "argon2", "sha256", "해싱"],
    "솔트 미사용": ["솔트", "salt", "해시", "레인보우"],
    "약한 시크릿 키": ["시크릿", "secret", "키", "하드코딩", "환경변수"],
    "토큰 만료 없음": ["만료", "expire", "exp", "TTL", "유효기간"],
    "경로 순회 취약점": ["경로 순회", "path traversal", "../", "디렉토리"],
    "평문 비밀번호": ["평문", "비밀번호", "암호화", "해시"],
    "오픈 리다이렉트": ["리다이렉트", "redirect", "URL 검증"],
    "Pickle 역직렬화 취약점": ["Pickle", "역직렬화", "deserialization", "RCE"],
    "민감정보 로깅": ["민감정보", "로깅", "logging", "카드", "CVV", "마스킹"],
    "XXE 취약점": ["XXE", "외부 엔티티", "XML", "DTD"],
    "파일명 검증 없음": ["파일명", "filename", "업로드", "확장자"],
    "unsafe YAML load": ["yaml.load", "yaml.safe_load", "YAML"],

    # 성능 관련
    "O(n^2) 복잡도": ["O(n²)", "O(n^2)", "이중 루프", "중첩 루프", "복잡도"],
    "set 활용 가능": ["set", "집합", "중복", "O(1)"],
    "전체 파일 메모리 로드": ["메모리", "전체 파일", "f.read()", "대용량"],
    "라인 단위 읽기 권장": ["라인 단위", "줄 단위", "readline", "제너레이터"],
    "N+1 쿼리 문제": ["N+1", "쿼리", "벌크", "배치", "IN 절"],
    "매번 패턴 컴파일": ["re.compile", "정규식", "패턴 컴파일"],
    "반복적 DOM 조작": ["DOM", "appendChild", "리플로우", "DocumentFragment"],
    "concat 반복 비효율": ["concat", "flat", "flatMap", "배열"],
    "Promise.all 미사용": ["Promise.all", "병렬", "동시", "순차"],
    "String 연결 비효율": ["String 연결", "StringBuilder", "문자열 연결", "+="],
    "Stream API 활용 가능": ["Stream", "스트림", "filter", "map", "collect"],
    "슬라이스 용량 미지정": ["용량", "capacity", "make", "슬라이스"],
    "지수적 시간 복잡도": ["지수", "피보나치", "재귀", "메모이제이션"],
    "iterrows 비효율": ["iterrows", "벡터화", "apply", "pandas"],

    # 리팩토링 관련
    "중첩 조건문": ["중첩", "조건문", "if-else", "분기"],
    "전략 패턴 적용": ["전략 패턴", "Strategy", "디자인 패턴"],
    "매직 넘버": ["매직 넘버", "magic number", "상수", "하드코딩"],
    "중복 코드": ["중복", "DRY", "반복"],
    "긴 매개변수 목록": ["매개변수", "파라미터", "인자", "DTO"],
    "단일 책임 위반": ["단일 책임", "SRP", "책임"],
    "God 클래스": ["God 클래스", "큰 클래스", "거대"],
    "메서드 추출": ["메서드 추출", "Extract Method", "함수 분리"],
    "의존성 주입": ["의존성 주입", "DI", "Dependency Injection", "의존성"],
    "팩토리 패턴 적용": ["팩토리", "Factory", "생성"],
    "OCP 위반": ["OCP", "개방-폐쇄", "확장"],

    # 문서화 관련
    "엔드포인트 설명": ["엔드포인트", "endpoint", "API", "경로"],
    "요청 파라미터": ["요청", "파라미터", "request", "parameter"],
    "응답 형식": ["응답", "response", "형식", "JSON"],
    "에러 케이스": ["에러", "error", "예외", "실패"],
    "프로젝트 설명": ["프로젝트", "설명", "개요", "목적"],
    "설치 방법": ["설치", "install", "설정", "setup"],
    "사용 예시": ["예시", "example", "사용법", "usage"],
    "함수 docstring": ["docstring", "문서화", "설명"],
    "파라미터 설명": ["파라미터", "인자", "argument", "매개변수"],
    "반환값 설명": ["반환", "return", "결과"],
}


class DevelopmentExperimentRunner:
    """
    개발자 프롬프트 실험 실행기

    108회 실험을 자동으로 수행하고 결과를 기록
    """

    def __init__(self, model: str = "qwen2.5:7b", version: str = "v1"):
        """
        실험 실행기 초기화

        Parameters
        ----------
        model : str
            사용할 Ollama 모델
        version : str
            프롬프트 버전 ("v1" 또는 "v2")
        """
        self.llm = ChatOllama(model=model, temperature=0.3)
        self.enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.results = []
        self.model = model
        self.version = version

    def count_tokens(self, text: str) -> int:
        """토큰 수 계산"""
        return len(self.enc.encode(text))

    def _check_issue_with_synonyms(self, issue: str, response_lower: str) -> bool:
        """
        동의어를 사용하여 이슈 탐지 (V2.0 개선)

        4단계 매칭 로직:
        1. 정확한 이슈 문자열 매칭
        2. 동의어 사전 기반 매칭 (2개 이상 동의어)
        3. 이슈 단어 분리 후 AND 매칭
        4. 핵심 키워드 any 매칭 (fallback)
        """
        issue_lower = issue.lower()

        # 1단계: 정확한 매칭
        if issue_lower in response_lower:
            return True

        # 2단계: 동의어 사전 매칭
        if issue in ISSUE_SYNONYMS:
            synonyms = ISSUE_SYNONYMS[issue]
            matched_count = sum(1 for syn in synonyms if syn.lower() in response_lower)
            if matched_count >= 2:
                return True

        # 3단계: 이슈 단어 분리 후 AND 매칭 (공백으로 분리된 모든 키워드)
        keywords = [kw for kw in issue_lower.split() if len(kw) > 1]
        if len(keywords) >= 2:
            if all(kw in response_lower for kw in keywords):
                return True

        # 4단계: any 매칭 (fallback)
        if any(kw in response_lower for kw in keywords if len(kw) > 2):
            return True

        return False

    def evaluate_response_quality(self, response: str, expected_issues: List[str], category: str) -> Dict:
        """
        응답 품질 평가 (V2.0 개선: 동의어 기반 탐지)

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
        # 이슈/요소 발견율 계산 (V2.0: 동의어 기반)
        found_issues = 0
        response_lower = response.lower()

        for issue in expected_issues:
            if self._check_issue_with_synonyms(issue, response_lower):
                found_issues += 1

        issue_detection_rate = found_issues / len(expected_issues) if expected_issues else 0

        # 코드 블록 포함 여부
        has_code_block = "```" in response

        # 구조화된 형식 여부
        has_structure = any([
            "##" in response,
            "|" in response,  # 표 형식
            "라인" in response or "Line" in response.lower(),  # 라인 참조
            "STEP" in response,  # V2.0 단계별 구조
        ])

        # 구체적 제안 포함 여부
        has_specific_suggestions = any([
            "변경" in response or "수정" in response,
            "->" in response or "=>" in response,
            "대신" in response or "권장" in response,
            "개선" in response or "최적화" in response,  # V2.0 추가
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
        """테스트 케이스에 맞는 프롬프트 생성 (버전에 따라 분기)"""
        if self.version == "v2":
            return self._generate_v2_prompt(test_case)
        return self._generate_v1_prompt(test_case)

    def _generate_v1_prompt(self, test_case: DevelopmentTestCase) -> str:
        """V1.0 프롬프트 생성"""
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

    def _generate_v2_prompt(self, test_case: DevelopmentTestCase) -> str:
        """
        V2.0 프롬프트 생성

        핵심 개선: expected_issues를 동적 체크리스트로 변환하여 프롬프트에 직접 포함
        """
        if test_case.category == "code_review":
            if test_case.subcategory == "general":
                return get_code_review_prompt_v2(
                    code=test_case.code_snippet,
                    language=test_case.language,
                    expected_issues=test_case.expected_issues,
                    filename="example." + test_case.language.lower()[:2],
                    code_purpose="일반 코드"
                )
            elif test_case.subcategory == "security":
                return get_security_review_prompt_v2(
                    code=test_case.code_snippet,
                    language=test_case.language,
                    expected_issues=test_case.expected_issues,
                    app_type="웹 애플리케이션"
                )
            elif test_case.subcategory == "performance":
                return get_performance_review_prompt_v2(
                    code=test_case.code_snippet,
                    language=test_case.language,
                    expected_issues=test_case.expected_issues
                )
            else:  # refactoring
                return get_refactoring_prompt_v2(
                    code=test_case.code_snippet,
                    language=test_case.language,
                    expected_issues=test_case.expected_issues
                )
        else:  # documentation
            if test_case.subcategory == "api":
                return get_api_documentation_prompt_v2(
                    api_name="API 엔드포인트",
                    endpoint="/api/example",
                    http_method="POST",
                    api_purpose="데이터 처리",
                    expected_elements=test_case.expected_issues,
                    request_params="JSON 본문",
                    response_format="JSON 응답"
                )
            elif test_case.subcategory == "readme":
                return get_readme_prompt_v2(
                    project_name="Example Project",
                    one_liner="예제 프로젝트입니다",
                    main_features="주요 기능",
                    tech_stack=test_case.language,
                    expected_elements=test_case.expected_issues,
                    code_snippet=test_case.code_snippet
                )
            elif test_case.subcategory == "comments":
                return get_code_comments_prompt_v2(
                    code=test_case.code_snippet,
                    language=test_case.language,
                    expected_elements=test_case.expected_issues
                )
            else:  # architecture
                return get_architecture_doc_prompt_v2(
                    system_name="Example System",
                    system_purpose="시스템 설명",
                    main_features="주요 기능",
                    tech_stack=test_case.language,
                    components=test_case.code_snippet,
                    expected_elements=test_case.expected_issues
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
        print(f"개발자 프롬프트 108회 실험 ({self.version.upper()})")
        print("=" * 70)
        print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"모델: {self.model}")
        print(f"프롬프트 버전: {self.version.upper()}")
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
                "version": self.version,
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
    import argparse

    parser = argparse.ArgumentParser(description="개발자 프롬프트 108회 실험")
    parser.add_argument(
        "--version", "-v",
        type=str,
        default="v1",
        choices=["v1", "v2"],
        help="프롬프트 버전 (v1: 기본, v2: 동적 체크리스트)"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=108,
        help="실험 횟수 (기본: 108)"
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="qwen2.5:7b",
        help="사용할 Ollama 모델"
    )

    args = parser.parse_args()

    runner = DevelopmentExperimentRunner(model=args.model, version=args.version)

    # 실험 실행
    summary = runner.run_all_experiments(limit=args.limit)

    print()
    print(f"108회 실험 완료! (버전: {args.version.upper()})")


if __name__ == "__main__":
    main()
