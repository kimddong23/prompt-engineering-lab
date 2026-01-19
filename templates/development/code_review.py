# -*- coding: utf-8 -*-
"""
================================================================================
코드 리뷰 프롬프트 모듈 (Code Review Prompts)
================================================================================

## 이 모듈의 목적
개발자가 코드 품질을 향상시킬 수 있는 체계적인 코드 리뷰 프롬프트 제공

## 대상 사용자
- 주니어/시니어 개발자
- 테크 리드
- 코드 품질 관리자

## 프롬프트 설계 원칙
1. 구체성: 라인 번호와 함께 정확한 문제 지적
2. 건설성: 문제점만이 아닌 개선 코드 제시
3. 우선순위: 심각도에 따른 이슈 분류
4. 교육적: 왜 문제인지 설명으로 학습 유도

## 코드 리뷰 유형
- 일반 코드 리뷰 (가독성, 유지보수성)
- 보안 코드 리뷰 (취약점 탐지)
- 성능 코드 리뷰 (최적화)
- 리팩토링 제안
================================================================================
"""

from typing import Dict, List, Optional


# ============================================================================
# 일반 코드 리뷰 프롬프트
# ============================================================================

CODE_REVIEW_TEMPLATE = """### 역할
당신은 10년 이상 경력의 시니어 소프트웨어 엔지니어입니다.
{language} 언어에 대한 깊은 이해와 {framework} 프레임워크 경험이 풍부합니다.
Google, Amazon 등 대형 테크 회사의 코드 리뷰 문화를 잘 알고 있습니다.

### 작업
아래 코드를 리뷰하고 개선점을 제안하세요.

### 코드 정보
- 언어: {language}
- 프레임워크/라이브러리: {framework}
- 파일명: {filename}
- 코드 목적: {code_purpose}

### 리뷰 대상 코드
```{language_lower}
{code}
```

### 리뷰 기준
1. **가독성**: 변수명, 함수명, 코드 구조의 명확성
2. **유지보수성**: 모듈화, 재사용성, 확장성
3. **버그 가능성**: 잠재적 버그, 엣지 케이스 처리
4. **코딩 컨벤션**: {language} 표준 스타일 가이드 준수
5. **설계 패턴**: 적절한 디자인 패턴 적용 여부

### 리뷰 수준
{review_depth}

### 출력 형식
## 코드 리뷰 요약

### 전체 평가
- 품질 점수: [X/10]
- 리뷰 요약: [한 문장]

### Critical Issues (즉시 수정 필요)
| 라인 | 이슈 | 심각도 | 개선 코드 |
|-----|------|--------|----------|
| L{line} | ... | 높음 | `...` |

### Major Issues (수정 권장)
| 라인 | 이슈 | 개선 방향 |
|-----|------|----------|
| L{line} | ... | ... |

### Minor Issues (개선하면 좋음)
| 라인 | 이슈 | 제안 |
|-----|------|------|
| L{line} | ... | ... |

### 잘된 점 (Keep)
1. ...
2. ...

### 개선된 전체 코드
```{language_lower}
[리팩토링된 전체 코드]
```

### 추가 학습 자료
- ...
"""


# ============================================================================
# 보안 코드 리뷰 프롬프트
# ============================================================================

SECURITY_REVIEW_TEMPLATE = """### 역할
당신은 애플리케이션 보안 전문가(AppSec Engineer)입니다.
OWASP Top 10, CWE 등 보안 취약점에 대한 깊은 지식을 보유하고 있습니다.
다수의 침투 테스트와 보안 코드 리뷰 경험이 있습니다.

### 작업
아래 코드의 보안 취약점을 분석하고 안전한 코드로 개선하세요.

### 코드 정보
- 언어: {language}
- 애플리케이션 유형: {app_type}
- 코드가 처리하는 데이터: {data_type}

### 리뷰 대상 코드
```{language_lower}
{code}
```

### 보안 점검 항목
1. **인젝션**: SQL, Command, XSS, XXE 등
2. **인증/인가**: 인증 우회, 권한 상승
3. **민감 정보**: 하드코딩된 시크릿, 로깅된 민감정보
4. **암호화**: 약한 알고리즘, 부적절한 키 관리
5. **입력 검증**: 부적절한 검증, 우회 가능성
6. **에러 처리**: 정보 노출, 부적절한 예외 처리
7. **의존성**: 취약한 라이브러리 사용

### 출력 형식
## 보안 코드 리뷰 결과

### 보안 점수: [X/10]
### 위험 수준: [Critical/High/Medium/Low]

### 발견된 취약점

#### 취약점 1: [취약점명]
- **CWE ID**: CWE-XXX
- **OWASP 분류**: [해당하는 경우]
- **위치**: 라인 {line}
- **문제 코드**:
```{language_lower}
[취약한 코드 부분]
```
- **공격 시나리오**: ...
- **영향도**: ...
- **수정된 코드**:
```{language_lower}
[안전한 코드]
```

#### 취약점 2: ...

### 보안 강화 권장사항
1. ...
2. ...

### 체크리스트
- [ ] 입력값 검증 구현
- [ ] 출력 인코딩 적용
- [ ] 에러 처리 개선
- [ ] ...
"""


# ============================================================================
# 성능 코드 리뷰 프롬프트
# ============================================================================

PERFORMANCE_REVIEW_TEMPLATE = """### 역할
당신은 성능 최적화 전문 엔지니어입니다.
대규모 트래픽을 처리하는 시스템의 성능 튜닝 경험이 풍부합니다.
{language}의 내부 동작과 최적화 기법에 대한 깊은 이해가 있습니다.

### 작업
아래 코드의 성능 이슈를 분석하고 최적화 방안을 제시하세요.

### 코드 정보
- 언어: {language}
- 예상 호출 빈도: {call_frequency}
- 처리 데이터 규모: {data_scale}
- 현재 성능 이슈: {current_issue}

### 리뷰 대상 코드
```{language_lower}
{code}
```

### 성능 분석 항목
1. **시간 복잡도**: 알고리즘 효율성 (Big O)
2. **공간 복잡도**: 메모리 사용량
3. **I/O 효율**: 파일/네트워크/DB 접근 최적화
4. **캐싱**: 반복 계산 방지
5. **동시성**: 병렬 처리 가능성
6. **메모리 관리**: 누수, 불필요한 할당
7. **데이터 구조**: 적절한 자료구조 선택

### 출력 형식
## 성능 코드 리뷰 결과

### 현재 성능 분석
- 시간 복잡도: O(...)
- 공간 복잡도: O(...)
- 주요 병목 지점: ...

### 발견된 성능 이슈

#### 이슈 1: [이슈명]
- **위치**: 라인 {line}
- **현재 코드**:
```{language_lower}
[문제 코드]
```
- **문제점**: ...
- **예상 영향**: [수치로 표현]
- **최적화된 코드**:
```{language_lower}
[개선 코드]
```
- **개선 효과**: ...

### 최적화 우선순위
| 순위 | 최적화 항목 | 예상 개선율 | 구현 난이도 |
|-----|-----------|-----------|-----------|
| 1 | ... | ...% | 상/중/하 |

### 최적화된 전체 코드
```{language_lower}
[최적화된 전체 코드]
```

### 벤치마크 제안
```{language_lower}
[성능 측정을 위한 벤치마크 코드]
```

### 추가 최적화 방향
- 캐싱 전략: ...
- 비동기 처리: ...
- 인프라 레벨: ...
"""


# ============================================================================
# 리팩토링 제안 프롬프트
# ============================================================================

REFACTORING_TEMPLATE = """### 역할
당신은 클린 코드와 리팩토링의 전문가입니다.
마틴 파울러의 리팩토링 기법과 SOLID 원칙에 정통합니다.
레거시 코드를 현대적이고 유지보수하기 쉬운 코드로 변환한 경험이 풍부합니다.

### 작업
아래 코드를 분석하고 리팩토링 계획을 수립하세요.

### 코드 정보
- 언어: {language}
- 프레임워크: {framework}
- 코드 히스토리: {code_history}
- 리팩토링 목적: {refactoring_goal}

### 리뷰 대상 코드
```{language_lower}
{code}
```

### 리팩토링 원칙
1. **SOLID 원칙**: SRP, OCP, LSP, ISP, DIP
2. **DRY**: 중복 제거
3. **KISS**: 단순성 유지
4. **코드 스멜**: 긴 메서드, 큰 클래스, 긴 매개변수 목록 등
5. **테스트 용이성**: 단위 테스트가 가능한 구조

### 출력 형식
## 리팩토링 분석 보고서

### 현재 코드 진단
- 코드 품질 점수: [X/10]
- 주요 문제: ...

### 감지된 코드 스멜
| 스멜 유형 | 위치 | 심각도 | 설명 |
|----------|------|--------|------|
| Long Method | L{line}-{line} | 높음 | ... |
| ... | ... | ... | ... |

### SOLID 원칙 분석
- SRP (단일 책임): [준수/위반] - ...
- OCP (개방-폐쇄): [준수/위반] - ...
- LSP (리스코프 치환): [준수/위반] - ...
- ISP (인터페이스 분리): [준수/위반] - ...
- DIP (의존성 역전): [준수/위반] - ...

### 리팩토링 계획

#### Phase 1: [단계명]
**적용 기법**: {refactoring_technique}
**변경 전**:
```{language_lower}
[현재 코드]
```
**변경 후**:
```{language_lower}
[리팩토링된 코드]
```
**이유**: ...

#### Phase 2: ...

### 리팩토링된 전체 코드
```{language_lower}
[최종 리팩토링 결과]
```

### 테스트 코드 제안
```{language_lower}
[단위 테스트 코드]
```

### 리팩토링 체크리스트
- [ ] 기존 테스트 통과 확인
- [ ] 새 테스트 추가
- [ ] 문서 업데이트
- [ ] ...
"""


# ============================================================================
# 프롬프트 함수
# ============================================================================

def get_code_review_prompt(
    code: str,
    language: str,
    filename: str = "unknown",
    code_purpose: str = "",
    framework: str = "",
    review_depth: str = "상세 리뷰"
) -> str:
    """
    일반 코드 리뷰 프롬프트 생성

    Parameters
    ----------
    code : str
        리뷰할 코드
    language : str
        프로그래밍 언어
    filename : str
        파일명
    code_purpose : str
        코드의 목적
    framework : str
        사용하는 프레임워크
    review_depth : str
        리뷰 깊이 (간단 리뷰/상세 리뷰/교육적 리뷰)

    Returns
    -------
    str
        완성된 프롬프트
    """
    return CODE_REVIEW_TEMPLATE.format(
        code=code,
        language=language,
        language_lower=language.lower(),
        filename=filename,
        code_purpose=code_purpose or "명시되지 않음",
        framework=framework or "없음",
        review_depth=review_depth,
        line="XX"
    )


def get_security_review_prompt(
    code: str,
    language: str,
    app_type: str = "웹 애플리케이션",
    data_type: str = "사용자 입력"
) -> str:
    """
    보안 코드 리뷰 프롬프트 생성

    Parameters
    ----------
    code : str
        리뷰할 코드
    language : str
        프로그래밍 언어
    app_type : str
        애플리케이션 유형
    data_type : str
        처리하는 데이터 유형

    Returns
    -------
    str
        완성된 프롬프트
    """
    return SECURITY_REVIEW_TEMPLATE.format(
        code=code,
        language=language,
        language_lower=language.lower(),
        app_type=app_type,
        data_type=data_type,
        line="XX"
    )


def get_performance_review_prompt(
    code: str,
    language: str,
    call_frequency: str = "높음 (초당 1000회 이상)",
    data_scale: str = "대규모 (100만 건 이상)",
    current_issue: str = ""
) -> str:
    """
    성능 코드 리뷰 프롬프트 생성

    Parameters
    ----------
    code : str
        리뷰할 코드
    language : str
        프로그래밍 언어
    call_frequency : str
        예상 호출 빈도
    data_scale : str
        처리 데이터 규모
    current_issue : str
        현재 성능 이슈

    Returns
    -------
    str
        완성된 프롬프트
    """
    return PERFORMANCE_REVIEW_TEMPLATE.format(
        code=code,
        language=language,
        language_lower=language.lower(),
        call_frequency=call_frequency,
        data_scale=data_scale,
        current_issue=current_issue or "특별히 보고된 이슈 없음",
        line="XX"
    )


def get_refactoring_prompt(
    code: str,
    language: str,
    framework: str = "",
    code_history: str = "레거시 코드",
    refactoring_goal: str = "가독성 및 유지보수성 향상"
) -> str:
    """
    리팩토링 제안 프롬프트 생성

    Parameters
    ----------
    code : str
        리팩토링할 코드
    language : str
        프로그래밍 언어
    framework : str
        사용하는 프레임워크
    code_history : str
        코드 히스토리/배경
    refactoring_goal : str
        리팩토링 목적

    Returns
    -------
    str
        완성된 프롬프트
    """
    return REFACTORING_TEMPLATE.format(
        code=code,
        language=language,
        language_lower=language.lower(),
        framework=framework or "없음",
        code_history=code_history,
        refactoring_goal=refactoring_goal,
        refactoring_technique="Extract Method",
        line="XX"
    )
