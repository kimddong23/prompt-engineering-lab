# -*- coding: utf-8 -*-
"""
================================================================================
개발 문서화 프롬프트 모듈 (Development Documentation Prompts)
================================================================================

## 이 모듈의 목적
개발자가 체계적이고 읽기 쉬운 기술 문서를 작성할 수 있도록 지원

## 대상 사용자
- 백엔드/프론트엔드 개발자
- API 개발자
- 오픈소스 기여자
- 테크니컬 라이터

## 프롬프트 설계 원칙
1. 대상 독자 고려: 개발자 vs 비개발자
2. 예제 중심: 코드 예제와 실행 결과 포함
3. 구조화: 일관된 형식과 네비게이션
4. 최신성: 버전 정보와 변경 이력

## 문서 유형
- API 문서 (OpenAPI/Swagger 스타일)
- README 파일
- 코드 주석/Docstring
- 아키텍처 문서
================================================================================
"""

from typing import Dict, List, Optional


# ============================================================================
# API 문서화 프롬프트
# ============================================================================

API_DOCUMENTATION_TEMPLATE = """### 역할
당신은 시니어 테크니컬 라이터입니다.
Stripe, Twilio 같은 개발자 친화적인 API 문서를 작성해본 경험이 있습니다.
개발자가 빠르게 이해하고 통합할 수 있는 문서 작성에 전문성이 있습니다.

### 작업
아래 API 정보를 바탕으로 완전한 API 문서를 작성하세요.

### API 정보
- API 이름: {api_name}
- 엔드포인트: {endpoint}
- HTTP 메서드: {http_method}
- API 목적: {api_purpose}

### 요청 파라미터
{request_params}

### 응답 형식
{response_format}

### 인증 방식
{auth_method}

### 에러 코드
{error_codes}

### 문서 스타일
{doc_style}

### 출력 형식
# {api_name}

## 개요
[API의 목적과 주요 기능 설명]

## 기본 정보
| 항목 | 값 |
|------|-----|
| Endpoint | `{endpoint}` |
| Method | `{http_method}` |
| 인증 | {auth_method} |

## 요청

### Headers
| Header | 필수 | 설명 |
|--------|------|------|
| Authorization | Yes | Bearer 토큰 |
| Content-Type | Yes | application/json |

### Parameters
| 파라미터 | 타입 | 필수 | 설명 | 예시 |
|---------|------|------|------|------|
| ... | ... | ... | ... | ... |

### 요청 예시
```bash
curl -X {http_method} '{endpoint}' \\
  -H 'Authorization: Bearer YOUR_TOKEN' \\
  -H 'Content-Type: application/json' \\
  -d '{{
    "param1": "value1"
  }}'
```

## 응답

### 성공 응답 (200)
```json
{{
  "success": true,
  "data": {{
    ...
  }}
}}
```

### 필드 설명
| 필드 | 타입 | 설명 |
|------|------|------|
| ... | ... | ... |

## 에러 처리

### 에러 응답 형식
```json
{{
  "success": false,
  "error": {{
    "code": "ERROR_CODE",
    "message": "에러 메시지"
  }}
}}
```

### 에러 코드
| 코드 | HTTP Status | 설명 | 해결 방법 |
|------|-------------|------|----------|
| ... | ... | ... | ... |

## 사용 예시

### Python
```python
import requests

response = requests.{http_method_lower}(
    '{endpoint}',
    headers={{'Authorization': 'Bearer YOUR_TOKEN'}},
    json={{...}}
)
```

### JavaScript
```javascript
const response = await fetch('{endpoint}', {{
  method: '{http_method}',
  headers: {{
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  }},
  body: JSON.stringify({{...}})
}});
```

## Rate Limit
- 요청 제한: {rate_limit}
- 제한 초과 시: 429 Too Many Requests

## 변경 이력
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| ... | ... | ... |
"""


# ============================================================================
# README 문서 프롬프트
# ============================================================================

README_TEMPLATE = """### 역할
당신은 성공적인 오픈소스 프로젝트의 문서 담당자입니다.
GitHub에서 10K+ 스타를 받은 프로젝트의 README를 작성한 경험이 있습니다.
첫 방문자가 5분 내에 프로젝트를 이해하고 시작할 수 있게 하는 것이 목표입니다.

### 작업
아래 프로젝트 정보를 바탕으로 완전한 README를 작성하세요.

### 프로젝트 정보
- 프로젝트명: {project_name}
- 한 줄 설명: {one_liner}
- 주요 기능: {main_features}
- 기술 스택: {tech_stack}
- 설치 방법: {installation}
- 사용 예시: {usage_example}
- 대상 사용자: {target_users}

### 추가 정보
{additional_info}

### README 스타일
{readme_style}

### 출력 형식
# {project_name}

[뱃지들: 빌드 상태, 버전, 라이선스 등]

> {one_liner}

## 목차
- [주요 기능](#주요-기능)
- [시작하기](#시작하기)
- [설치](#설치)
- [사용법](#사용법)
- [API 문서](#api-문서)
- [기여하기](#기여하기)
- [라이선스](#라이선스)

## 주요 기능

[기능 목록과 간단한 설명, 가능하면 GIF/스크린샷]

## 시작하기

### 요구 사항
- ...
- ...

### 설치

```bash
# 패키지 매니저를 통한 설치
npm install {project_name}

# 또는 소스에서 빌드
git clone ...
cd {project_name}
npm install
```

## 사용법

### 기본 사용법
```{language}
[기본 코드 예제]
```

### 고급 사용법
```{language}
[고급 코드 예제]
```

## 설정

| 옵션 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| ... | ... | ... | ... |

## API 문서

전체 API 문서는 [여기](docs/API.md)에서 확인하세요.

### 주요 메서드

#### `methodName(params)`
[메서드 설명]

## 예제

[실제 사용 사례나 데모 링크]

## 문제 해결

### 자주 묻는 질문

**Q: [질문]**
A: [답변]

## 기여하기

기여를 환영합니다! [CONTRIBUTING.md](CONTRIBUTING.md)를 확인해주세요.

## 변경 이력

[CHANGELOG.md](CHANGELOG.md) 참조

## 라이선스

이 프로젝트는 [라이선스명] 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 연락처

- 이슈 트래커: [GitHub Issues]
- 이메일: ...
"""


# ============================================================================
# 코드 주석/Docstring 프롬프트
# ============================================================================

CODE_COMMENTS_TEMPLATE = """### 역할
당신은 코드 문서화 전문가입니다.
{language}의 공식 문서화 스타일 ({doc_style})에 정통합니다.
IDE의 자동완성과 호버 프리뷰에 최적화된 주석을 작성합니다.

### 작업
아래 코드에 적절한 주석과 Docstring을 추가하세요.

### 코드 정보
- 언어: {language}
- 문서화 스타일: {doc_style}
- 코드 목적: {code_purpose}

### 원본 코드
```{language_lower}
{code}
```

### 문서화 기준
1. **모든 공개 함수/메서드**: 완전한 Docstring
2. **클래스**: 클래스 목적과 주요 속성 설명
3. **복잡한 로직**: 인라인 주석으로 의도 설명
4. **파라미터**: 타입, 필수 여부, 기본값, 설명
5. **반환값**: 타입과 설명
6. **예외**: 발생 가능한 예외와 조건
7. **예제**: 사용 예제 코드

### 출력 형식
## 문서화된 코드

```{language_lower}
[완전히 문서화된 코드]
```

## 문서화 요약
| 항목 | 개수 | 커버리지 |
|------|------|----------|
| 함수/메서드 | X | 100% |
| 클래스 | X | 100% |
| 인라인 주석 | X | - |

## 생성된 문서 미리보기

### 함수: `function_name`
[IDE에서 보이는 것처럼 포맷팅된 문서]
"""


# ============================================================================
# 아키텍처 문서 프롬프트
# ============================================================================

ARCHITECTURE_DOC_TEMPLATE = """### 역할
당신은 소프트웨어 아키텍트이자 테크니컬 라이터입니다.
복잡한 시스템 아키텍처를 이해하기 쉽게 문서화하는 전문성이 있습니다.
C4 모델, arc42 템플릿 등 아키텍처 문서화 방법론에 정통합니다.

### 작업
아래 시스템 정보를 바탕으로 아키텍처 문서를 작성하세요.

### 시스템 정보
- 시스템명: {system_name}
- 시스템 목적: {system_purpose}
- 주요 기능: {main_features}
- 기술 스택: {tech_stack}
- 시스템 구성요소: {components}
- 외부 연동: {external_systems}
- 데이터 흐름: {data_flow}

### 대상 독자
{target_audience}

### 문서화 수준
{doc_level}

### 출력 형식
# {system_name} 아키텍처 문서

## 1. 개요

### 1.1 목적
[시스템이 해결하는 문제와 제공하는 가치]

### 1.2 범위
[이 문서가 다루는 범위]

### 1.3 대상 독자
[이 문서를 읽어야 하는 사람]

## 2. 아키텍처 개요

### 2.1 고수준 아키텍처
```
[ASCII 또는 Mermaid 다이어그램]
```

### 2.2 핵심 설계 결정
| 결정 사항 | 선택한 옵션 | 이유 |
|----------|-----------|------|
| ... | ... | ... |

## 3. 시스템 컴포넌트

### 3.1 컴포넌트 다이어그램
```mermaid
graph TB
    A[Component A] --> B[Component B]
    B --> C[Component C]
```

### 3.2 컴포넌트 상세

#### 3.2.1 [Component A]
- **역할**: ...
- **책임**: ...
- **기술**: ...
- **인터페이스**: ...

## 4. 데이터 아키텍처

### 4.1 데이터 모델
[ERD 또는 데이터 구조 설명]

### 4.2 데이터 흐름
```mermaid
sequenceDiagram
    participant A
    participant B
    A->>B: Request
    B-->>A: Response
```

## 5. 외부 인터페이스

### 5.1 API 인터페이스
| API | 프로토콜 | 용도 |
|-----|---------|------|
| ... | ... | ... |

### 5.2 외부 시스템 연동
[외부 시스템과의 통합 방법]

## 6. 비기능 요구사항

### 6.1 성능
- 목표 응답 시간: ...
- 목표 처리량: ...

### 6.2 확장성
[수평/수직 확장 전략]

### 6.3 가용성
[장애 대응 및 복구 전략]

### 6.4 보안
[인증, 인가, 암호화 전략]

## 7. 배포 아키텍처

### 7.1 인프라 다이어그램
```
[배포 환경 다이어그램]
```

### 7.2 배포 프로세스
[CI/CD 파이프라인 설명]

## 8. 변경 이력
| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| ... | ... | ... | ... |
"""


# ============================================================================
# 프롬프트 함수
# ============================================================================

def get_api_documentation_prompt(
    api_name: str,
    endpoint: str,
    http_method: str,
    api_purpose: str,
    request_params: str,
    response_format: str,
    auth_method: str = "Bearer Token",
    error_codes: str = "",
    doc_style: str = "REST API 표준",
    rate_limit: str = "1000 requests/hour"
) -> str:
    """
    API 문서화 프롬프트 생성

    Parameters
    ----------
    api_name : str
        API 이름
    endpoint : str
        API 엔드포인트
    http_method : str
        HTTP 메서드
    api_purpose : str
        API 목적
    request_params : str
        요청 파라미터 설명
    response_format : str
        응답 형식 설명
    auth_method : str
        인증 방식
    error_codes : str
        에러 코드 목록
    doc_style : str
        문서 스타일
    rate_limit : str
        Rate limit 정보

    Returns
    -------
    str
        완성된 프롬프트
    """
    return API_DOCUMENTATION_TEMPLATE.format(
        api_name=api_name,
        endpoint=endpoint,
        http_method=http_method,
        http_method_lower=http_method.lower(),
        api_purpose=api_purpose,
        request_params=request_params,
        response_format=response_format,
        auth_method=auth_method,
        error_codes=error_codes or "표준 HTTP 에러 코드",
        doc_style=doc_style,
        rate_limit=rate_limit
    )


def get_readme_prompt(
    project_name: str,
    one_liner: str,
    main_features: str,
    tech_stack: str,
    installation: str,
    usage_example: str,
    target_users: str = "개발자",
    additional_info: str = "",
    readme_style: str = "GitHub 표준",
    language: str = "python"
) -> str:
    """
    README 문서 프롬프트 생성

    Parameters
    ----------
    project_name : str
        프로젝트명
    one_liner : str
        한 줄 설명
    main_features : str
        주요 기능
    tech_stack : str
        기술 스택
    installation : str
        설치 방법
    usage_example : str
        사용 예시
    target_users : str
        대상 사용자
    additional_info : str
        추가 정보
    readme_style : str
        README 스타일
    language : str
        주요 프로그래밍 언어

    Returns
    -------
    str
        완성된 프롬프트
    """
    return README_TEMPLATE.format(
        project_name=project_name,
        one_liner=one_liner,
        main_features=main_features,
        tech_stack=tech_stack,
        installation=installation,
        usage_example=usage_example,
        target_users=target_users,
        additional_info=additional_info or "없음",
        readme_style=readme_style,
        language=language
    )


def get_code_comments_prompt(
    code: str,
    language: str,
    code_purpose: str = "",
    doc_style: str = ""
) -> str:
    """
    코드 주석/Docstring 프롬프트 생성

    Parameters
    ----------
    code : str
        문서화할 코드
    language : str
        프로그래밍 언어
    code_purpose : str
        코드의 목적
    doc_style : str
        문서화 스타일 (Google, NumPy, JSDoc 등)

    Returns
    -------
    str
        완성된 프롬프트
    """
    # 언어별 기본 문서화 스타일
    default_styles = {
        "python": "Google Style",
        "javascript": "JSDoc",
        "typescript": "TSDoc",
        "java": "Javadoc",
        "go": "GoDoc",
        "rust": "Rustdoc"
    }

    if not doc_style:
        doc_style = default_styles.get(language.lower(), "표준 스타일")

    return CODE_COMMENTS_TEMPLATE.format(
        code=code,
        language=language,
        language_lower=language.lower(),
        code_purpose=code_purpose or "명시되지 않음",
        doc_style=doc_style
    )


def get_architecture_doc_prompt(
    system_name: str,
    system_purpose: str,
    main_features: str,
    tech_stack: str,
    components: str,
    external_systems: str = "",
    data_flow: str = "",
    target_audience: str = "개발팀, 아키텍트",
    doc_level: str = "상세"
) -> str:
    """
    아키텍처 문서 프롬프트 생성

    Parameters
    ----------
    system_name : str
        시스템명
    system_purpose : str
        시스템 목적
    main_features : str
        주요 기능
    tech_stack : str
        기술 스택
    components : str
        시스템 구성요소
    external_systems : str
        외부 연동 시스템
    data_flow : str
        데이터 흐름
    target_audience : str
        대상 독자
    doc_level : str
        문서화 수준 (개요/상세)

    Returns
    -------
    str
        완성된 프롬프트
    """
    return ARCHITECTURE_DOC_TEMPLATE.format(
        system_name=system_name,
        system_purpose=system_purpose,
        main_features=main_features,
        tech_stack=tech_stack,
        components=components,
        external_systems=external_systems or "없음",
        data_flow=data_flow or "별도 설명 필요",
        target_audience=target_audience,
        doc_level=doc_level
    )
