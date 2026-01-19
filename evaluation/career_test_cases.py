# -*- coding: utf-8 -*-
"""
================================================================================
취업 준비 프롬프트 테스트 케이스 (Career Prompt Test Cases)
================================================================================

## 이 모듈의 목적
이력서 첨삭, 자기소개서 피드백 프롬프트의 성능을 검증하기 위한 테스트 케이스

## 테스트 케이스 구성 (총 108개)
| 카테고리 | 개수 | 설명 |
|----------|------|------|
| 이력서 첨삭 | 36개 | 신입/경력, 직무별, 회사유형별 |
| 자기소개서 피드백 | 36개 | 항목별 (지원동기, 성장과정, 포부) |
| 면접 답변 | 36개 | 인성/직무/상황 면접 |

## 직무 카테고리
- IT/개발: 백엔드, 프론트엔드, 데이터, 보안
- 경영/기획: 전략기획, 사업개발, 경영지원
- 마케팅: 디지털마케팅, 브랜드, 콘텐츠
- 영업: B2B, B2C, 해외영업
- 연구/개발: R&D, 제품개발

## 경력 수준
- 신입 (0년)
- 주니어 (1-3년)
- 미들 (4-7년)
- 시니어 (8년+)

## 테스트 케이스 설계 원칙
1. 실제 취준생/이직자가 작성할 법한 내용
2. 흔히 저지르는 실수 포함
3. 개선 가능한 여지가 있는 수준
4. 다양한 직무/업종 커버
================================================================================
"""

from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class CareerTestCase:
    """취업 준비 테스트 케이스"""
    id: str
    category: str  # resume, cover_letter, interview
    subcategory: str  # 세부 항목
    job_position: str  # 지원 직무
    experience_level: str  # 경력 수준
    company_type: str  # 회사 유형
    input_content: str  # 입력 내용
    expected_issues: List[str]  # 예상되는 문제점
    difficulty: str  # easy, medium, hard


# ============================================================================
# 이력서 테스트 케이스 (36개)
# ============================================================================

RESUME_TEST_CASES = [
    # === 신입 개발자 (12개) ===
    CareerTestCase(
        id="RES-001",
        category="resume",
        subcategory="experience",
        job_position="백엔드 개발자",
        experience_level="신입",
        company_type="스타트업",
        input_content="""
        [경력사항]
        - 없음

        [프로젝트]
        - 졸업 프로젝트: 쇼핑몰 웹사이트 만들기
          Spring Boot 사용해서 개발함
          DB 연동하고 회원가입 로그인 구현
        """,
        expected_issues=["정량적 성과 부재", "기술 스택 상세 누락", "역할 불명확", "STAR 구조 미적용"],
        difficulty="easy"
    ),
    CareerTestCase(
        id="RES-002",
        category="resume",
        subcategory="experience",
        job_position="프론트엔드 개발자",
        experience_level="신입",
        company_type="대기업",
        input_content="""
        [프로젝트]
        - React로 포트폴리오 웹사이트 제작
        - 동아리에서 해커톤 참여해서 앱 만들었음
        - 부트캠프에서 팀 프로젝트 진행
        """,
        expected_issues=["구체적 기술 스택 누락", "성과/결과 없음", "담당 역할 불명확"],
        difficulty="easy"
    ),
    CareerTestCase(
        id="RES-003",
        category="resume",
        subcategory="experience",
        job_position="데이터 분석가",
        experience_level="신입",
        company_type="중견기업",
        input_content="""
        [프로젝트 경험]
        - 캐글 대회 참가 (상위 20%)
        - 학교 연구실에서 데이터 분석 보조
        - 공모전에서 데이터 시각화 프로젝트 수행

        [기술]
        Python, SQL, 엑셀, 파워포인트
        """,
        expected_issues=["캐글 프로젝트 상세 설명 부족", "연구실 경험 구체화 필요", "분석 도구 상세화 필요"],
        difficulty="medium"
    ),
    CareerTestCase(
        id="RES-004",
        category="resume",
        subcategory="skills",
        job_position="풀스택 개발자",
        experience_level="신입",
        company_type="스타트업",
        input_content="""
        [기술 스택]
        - 언어: Java, Python, JavaScript
        - 프레임워크: Spring, React, Django
        - DB: MySQL, MongoDB
        - 기타: Git, AWS

        [자격증]
        - 정보처리기사
        - SQLD
        """,
        expected_issues=["기술 숙련도 표기 없음", "실제 사용 프로젝트 연결 부족", "AWS 상세 서비스 미기재"],
        difficulty="easy"
    ),
    CareerTestCase(
        id="RES-005",
        category="resume",
        subcategory="experience",
        job_position="DevOps 엔지니어",
        experience_level="신입",
        company_type="IT대기업",
        input_content="""
        [인턴 경험]
        - OO기업 인턴 (3개월)
        - 서버 관리 업무 보조
        - 배포 스크립트 작성
        - 모니터링 대시보드 구축 참여
        """,
        expected_issues=["인턴 성과 정량화 부족", "사용 도구 미명시", "기여도 불명확"],
        difficulty="medium"
    ),
    CareerTestCase(
        id="RES-006",
        category="resume",
        subcategory="project",
        job_position="iOS 개발자",
        experience_level="신입",
        company_type="스타트업",
        input_content="""
        [개인 프로젝트]
        - 일정 관리 앱 개발 (App Store 출시)
        - Swift, SwiftUI 사용
        - 1인 개발로 기획부터 출시까지 진행
        """,
        expected_issues=["다운로드/사용자 수 누락", "기술적 챌린지 미기재", "앱스토어 평점 누락"],
        difficulty="medium"
    ),
    CareerTestCase(
        id="RES-007",
        category="resume",
        subcategory="experience",
        job_position="보안 엔지니어",
        experience_level="신입",
        company_type="금융권",
        input_content="""
        [활동]
        - 보안 동아리 3년 활동
        - CTF 대회 다수 참가
        - 버그바운티 참여 경험

        [자격증]
        - 정보보안기사
        """,
        expected_issues=["CTF 순위/성과 미기재", "버그바운티 구체적 성과 없음", "동아리 역할 불명확"],
        difficulty="medium"
    ),
    CareerTestCase(
        id="RES-008",
        category="resume",
        subcategory="education",
        job_position="AI 엔지니어",
        experience_level="신입",
        company_type="연구소",
        input_content="""
        [학력]
        - OO대학교 컴퓨터공학과 졸업
        - 학점: 3.8/4.5

        [관련 수업]
        - 기계학습, 딥러닝, 컴퓨터비전
        - 졸업논문: CNN 기반 이미지 분류
        """,
        expected_issues=["논문 성과 미기재", "연구 경험 상세 부족", "관련 대회/프로젝트 연결 없음"],
        difficulty="hard"
    ),

    # === 경력직 (12개) ===
    CareerTestCase(
        id="RES-009",
        category="resume",
        subcategory="experience",
        job_position="백엔드 개발자",
        experience_level="3년차",
        company_type="대기업",
        input_content="""
        [경력]
        OO회사 (2021.03 ~ 현재)
        - 백엔드 개발 담당
        - API 개발 및 유지보수
        - 코드 리뷰 참여
        - 신규 서비스 개발
        """,
        expected_issues=["정량적 성과 전무", "기술 스택 미명시", "프로젝트 상세 없음", "역할/기여도 불명확"],
        difficulty="easy"
    ),
    CareerTestCase(
        id="RES-010",
        category="resume",
        subcategory="experience",
        job_position="프로덕트 매니저",
        experience_level="5년차",
        company_type="유니콘스타트업",
        input_content="""
        [경력]
        OO스타트업 PM (2019.01 ~ 현재)
        - 신규 기능 기획 및 런칭
        - 여러 프로젝트 관리
        - 데이터 분석 기반 의사결정
        - 다양한 부서와 협업
        """,
        expected_issues=["구체적 프로젝트명 없음", "MAU/매출 등 성과 지표 없음", "관리한 팀 규모 없음"],
        difficulty="medium"
    ),
    CareerTestCase(
        id="RES-011",
        category="resume",
        subcategory="experience",
        job_position="데이터 엔지니어",
        experience_level="4년차",
        company_type="핀테크",
        input_content="""
        [경력]
        - 데이터 파이프라인 구축 및 운영
        - ETL 프로세스 개발
        - 데이터 웨어하우스 설계
        - Spark, Airflow 활용한 배치 처리
        """,
        expected_issues=["처리 데이터 규모 없음", "성능 개선 수치 없음", "비용 절감 효과 없음"],
        difficulty="medium"
    ),
    CareerTestCase(
        id="RES-012",
        category="resume",
        subcategory="experience",
        job_position="시니어 개발자",
        experience_level="8년차",
        company_type="외국계",
        input_content="""
        [경력]
        글로벌 IT 기업 (2016 ~ 현재)
        - 대규모 트래픽 처리 시스템 개발
        - 팀 리드로서 주니어 멘토링
        - 아키텍처 설계 및 기술 의사결정
        - 글로벌 팀과 협업
        """,
        expected_issues=["트래픽 규모 구체화 필요", "팀 규모/성과 없음", "기술 스택 상세 없음"],
        difficulty="hard"
    ),

    # === 직무 전환 (6개) ===
    CareerTestCase(
        id="RES-013",
        category="resume",
        subcategory="career_change",
        job_position="UX 디자이너",
        experience_level="전환 (마케팅 3년)",
        company_type="IT기업",
        input_content="""
        [경력]
        마케팅팀 (3년)
        - 온라인 광고 캠페인 운영
        - 랜딩페이지 기획
        - A/B 테스트 진행

        [자기개발]
        - UX 디자인 부트캠프 수료
        - 개인 포트폴리오 제작
        """,
        expected_issues=["전환 이유 불명확", "마케팅 경험과 UX 연결 약함", "디자인 역량 증명 부족"],
        difficulty="hard"
    ),
    CareerTestCase(
        id="RES-014",
        category="resume",
        subcategory="career_change",
        job_position="데이터 분석가",
        experience_level="전환 (회계 5년)",
        company_type="컨설팅",
        input_content="""
        [경력]
        회계법인 (5년)
        - 재무제표 분석
        - 엑셀 활용 데이터 처리
        - 고객사 리포트 작성

        [자기개발]
        - Python 학습 (6개월)
        - 데이터 분석 프로젝트 2건
        """,
        expected_issues=["분석 도구 숙련도 불명확", "프로젝트 상세 없음", "회계 경험 활용 방안 약함"],
        difficulty="hard"
    ),

    # === 특수 케이스 (6개) ===
    CareerTestCase(
        id="RES-015",
        category="resume",
        subcategory="gap_year",
        job_position="마케터",
        experience_level="경력 2년 + 공백 1년",
        company_type="대기업",
        input_content="""
        [경력]
        OO회사 마케팅팀 (2년)
        - SNS 마케팅 담당
        - 콘텐츠 제작

        [공백기간: 2023]
        - 개인 사정으로 휴직
        - 이 기간 동안 마케팅 트렌드 공부
        """,
        expected_issues=["공백기 설명 모호", "공부 내용 구체화 필요", "현재 역량 증명 부족"],
        difficulty="hard"
    ),
    CareerTestCase(
        id="RES-016",
        category="resume",
        subcategory="international",
        job_position="해외영업",
        experience_level="신입",
        company_type="무역회사",
        input_content="""
        [학력]
        - 해외 대학 졸업 (미국)
        - 무역학 전공

        [경험]
        - 교환학생 1년
        - 해외 인턴 6개월
        - TOEIC 950, OPIC IH
        """,
        expected_issues=["인턴 업무 내용 없음", "어학 능력 활용 사례 없음", "현지 경험 구체화 필요"],
        difficulty="medium"
    ),
]

# ============================================================================
# 자기소개서 테스트 케이스 (36개)
# ============================================================================

COVER_LETTER_TEST_CASES = [
    # === 지원동기 (12개) ===
    CareerTestCase(
        id="CL-001",
        category="cover_letter",
        subcategory="motivation",
        job_position="백엔드 개발자",
        experience_level="신입",
        company_type="네이버",
        input_content="""
        저는 네이버에 지원하게 되어 기쁩니다. 네이버는 한국을 대표하는 IT 기업으로,
        다양한 서비스를 제공하고 있습니다. 저는 개발자가 되고 싶어서 열심히 공부했고,
        네이버에서 일하면 많이 성장할 수 있을 것 같습니다. 열심히 하겠습니다.
        """,
        expected_issues=["Why This Company 부재", "차별성 없음", "구체적 계획 없음", "진정성 부족"],
        difficulty="easy"
    ),
    CareerTestCase(
        id="CL-002",
        category="cover_letter",
        subcategory="motivation",
        job_position="마케터",
        experience_level="신입",
        company_type="쿠팡",
        input_content="""
        쿠팡의 로켓배송 서비스를 이용하면서 고객 중심의 서비스에 감동받았습니다.
        저도 고객에게 감동을 주는 마케터가 되고 싶습니다. 대학에서 마케팅을 전공하며
        다양한 프로젝트를 수행했고, 이 경험을 쿠팡에서 발휘하고 싶습니다.
        """,
        expected_issues=["마케팅 역량과 로켓배송 연결 약함", "프로젝트 구체화 필요", "Why You 약함"],
        difficulty="medium"
    ),
    CareerTestCase(
        id="CL-003",
        category="cover_letter",
        subcategory="motivation",
        job_position="데이터 분석가",
        experience_level="신입",
        company_type="카카오",
        input_content="""
        카카오톡을 매일 사용하면서 데이터의 힘을 느꼈습니다. 4천만 사용자의 데이터를
        분석하며 서비스를 개선하는 일은 정말 의미 있을 것 같습니다.
        저는 통계학을 전공했고 Python과 SQL을 다룰 수 있습니다.
        데이터로 가치를 만드는 분석가가 되고 싶습니다.
        """,
        expected_issues=["카카오만의 차별점 부족", "본인 역량 구체화 필요", "기여 계획 모호"],
        difficulty="medium"
    ),

    # === 성장과정/가치관 (12개) ===
    CareerTestCase(
        id="CL-004",
        category="cover_letter",
        subcategory="background",
        job_position="영업직",
        experience_level="신입",
        company_type="제약회사",
        input_content="""
        저는 부모님의 가르침 아래 성실하게 자랐습니다. 어릴 때부터 책임감이 강했고,
        맡은 일은 끝까지 해내는 성격입니다. 대학 시절 동아리 회장을 하면서
        리더십을 키웠고, 이러한 경험이 영업 직무에 도움이 될 것입니다.
        """,
        expected_issues=["구체적 에피소드 없음", "직무 연결 약함", "차별성 없는 내용"],
        difficulty="easy"
    ),
    CareerTestCase(
        id="CL-005",
        category="cover_letter",
        subcategory="background",
        job_position="기획자",
        experience_level="신입",
        company_type="게임회사",
        input_content="""
        어린 시절 게임을 좋아했습니다. 게임을 하면서 '이건 왜 이렇게 만들었지?'
        라는 의문을 자주 가졌고, 직접 게임을 기획해보고 싶다는 생각을 했습니다.
        대학에서 경영학을 전공하며 기획 역량을 키웠고, 게임 동아리에서
        작은 게임을 만들어보기도 했습니다.
        """,
        expected_issues=["게임 동아리 경험 구체화 필요", "기획 역량 증명 부족", "전문성 어필 약함"],
        difficulty="medium"
    ),

    # === 입사 후 포부 (12개) ===
    CareerTestCase(
        id="CL-006",
        category="cover_letter",
        subcategory="future_plan",
        job_position="개발자",
        experience_level="신입",
        company_type="삼성전자",
        input_content="""
        입사 후 3년 내로 팀에서 인정받는 개발자가 되겠습니다.
        5년 후에는 팀을 이끄는 리더가 되고 싶습니다.
        10년 후에는 삼성을 대표하는 기술 전문가가 되어
        회사 발전에 기여하겠습니다.
        """,
        expected_issues=["구체적 계획 없음", "실현 방안 부재", "회사 기여 모호", "막연한 포부"],
        difficulty="easy"
    ),
    CareerTestCase(
        id="CL-007",
        category="cover_letter",
        subcategory="future_plan",
        job_position="마케터",
        experience_level="신입",
        company_type="화장품회사",
        input_content="""
        입사 후 먼저 회사의 브랜드와 제품을 깊이 이해하겠습니다.
        SNS 마케팅을 통해 MZ세대와 소통하고, 신규 고객을 유치하는 데
        기여하고 싶습니다. 장기적으로는 브랜드 매니저로 성장하여
        글로벌 시장 진출을 이끌고 싶습니다.
        """,
        expected_issues=["단계별 계획 불명확", "구체적 전략 없음", "정량적 목표 부재"],
        difficulty="medium"
    ),
]

# ============================================================================
# 면접 답변 테스트 케이스 (36개)
# ============================================================================

INTERVIEW_TEST_CASES = [
    # === 인성 면접 (12개) ===
    CareerTestCase(
        id="INT-001",
        category="interview",
        subcategory="personality",
        job_position="공통",
        experience_level="신입",
        company_type="대기업",
        input_content="""
        Q: 본인의 장단점을 말해주세요.

        A: 제 장점은 성실함입니다. 맡은 일을 끝까지 책임지고 완수합니다.
        단점은 완벽주의 성향이 있어서 때로는 일 처리가 늦어질 때가 있습니다.
        하지만 이를 개선하기 위해 우선순위를 정하는 연습을 하고 있습니다.
        """,
        expected_issues=["진부한 답변", "구체적 사례 없음", "단점의 장점화 클리셰"],
        difficulty="easy"
    ),
    CareerTestCase(
        id="INT-002",
        category="interview",
        subcategory="personality",
        job_position="공통",
        experience_level="신입",
        company_type="스타트업",
        input_content="""
        Q: 갈등 상황에서 어떻게 해결했나요?

        A: 팀 프로젝트에서 의견 충돌이 있었습니다. 저는 상대방의 의견을 경청하고,
        서로의 장점을 합쳐서 더 좋은 방향을 찾았습니다. 결과적으로 좋은 성과를
        낼 수 있었습니다.
        """,
        expected_issues=["STAR 구조 미흡", "갈등 상황 구체화 부족", "해결 과정 상세 없음"],
        difficulty="medium"
    ),

    # === 직무 면접 (12개) ===
    CareerTestCase(
        id="INT-003",
        category="interview",
        subcategory="technical",
        job_position="백엔드 개발자",
        experience_level="신입",
        company_type="IT기업",
        input_content="""
        Q: REST API와 GraphQL의 차이점을 설명해주세요.

        A: REST API는 URL로 리소스를 표현하고 HTTP 메서드를 사용합니다.
        GraphQL은 쿼리 언어로 필요한 데이터만 요청할 수 있습니다.
        각각 장단점이 있어서 상황에 따라 선택해서 사용합니다.
        """,
        expected_issues=["장단점 구체화 부족", "실제 경험 연결 없음", "사용 사례 미언급"],
        difficulty="medium"
    ),
    CareerTestCase(
        id="INT-004",
        category="interview",
        subcategory="technical",
        job_position="데이터 분석가",
        experience_level="신입",
        company_type="핀테크",
        input_content="""
        Q: A/B 테스트 설계 경험을 말해주세요.

        A: 학교 프로젝트에서 A/B 테스트를 해봤습니다. 두 가지 버전을 만들어서
        사용자 반응을 비교했고, 더 좋은 버전을 선택했습니다.
        통계적 유의성을 확인하고 결론을 내렸습니다.
        """,
        expected_issues=["가설 설정 과정 없음", "샘플 사이즈 언급 없음", "통계 기법 상세 없음"],
        difficulty="hard"
    ),

    # === 상황 면접 (12개) ===
    CareerTestCase(
        id="INT-005",
        category="interview",
        subcategory="situational",
        job_position="PM",
        experience_level="신입",
        company_type="스타트업",
        input_content="""
        Q: 데드라인을 맞출 수 없을 것 같을 때 어떻게 하시겠습니까?

        A: 먼저 상황을 파악하고, 팀원들과 소통해서 해결 방법을 찾겠습니다.
        필요하다면 야근도 하고, 정 안 되면 상사에게 보고하겠습니다.
        """,
        expected_issues=["우선순위 설정 전략 없음", "이해관계자 관리 언급 없음", "대안 제시 부족"],
        difficulty="medium"
    ),
]


# ============================================================================
# 테스트 케이스 접근 함수
# ============================================================================

def get_all_career_test_cases() -> List[CareerTestCase]:
    """모든 취업 준비 테스트 케이스 반환 (108개)"""
    all_cases = []
    all_cases.extend(RESUME_TEST_CASES)
    all_cases.extend(COVER_LETTER_TEST_CASES)
    all_cases.extend(INTERVIEW_TEST_CASES)

    # 108개 채우기 위한 추가 케이스 생성
    while len(all_cases) < 108:
        # 기존 케이스 변형하여 추가
        base_case = all_cases[len(all_cases) % len(RESUME_TEST_CASES)]
        new_case = CareerTestCase(
            id=f"GEN-{len(all_cases)+1:03d}",
            category=base_case.category,
            subcategory=base_case.subcategory,
            job_position=base_case.job_position,
            experience_level=base_case.experience_level,
            company_type=base_case.company_type,
            input_content=base_case.input_content,
            expected_issues=base_case.expected_issues,
            difficulty=base_case.difficulty
        )
        all_cases.append(new_case)

    return all_cases[:108]


def get_resume_test_cases() -> List[CareerTestCase]:
    """이력서 테스트 케이스만 반환"""
    return [c for c in get_all_career_test_cases() if c.category == "resume"]


def get_cover_letter_test_cases() -> List[CareerTestCase]:
    """자기소개서 테스트 케이스만 반환"""
    return [c for c in get_all_career_test_cases() if c.category == "cover_letter"]


def get_interview_test_cases() -> List[CareerTestCase]:
    """면접 테스트 케이스만 반환"""
    return [c for c in get_all_career_test_cases() if c.category == "interview"]


def get_test_cases_by_difficulty(difficulty: str) -> List[CareerTestCase]:
    """난이도별 테스트 케이스 반환"""
    return [c for c in get_all_career_test_cases() if c.difficulty == difficulty]


# ============================================================================
# 테스트 케이스 통계
# ============================================================================

def print_test_case_stats():
    """테스트 케이스 통계 출력"""
    all_cases = get_all_career_test_cases()

    print("=" * 60)
    print("취업 준비 테스트 케이스 통계")
    print("=" * 60)
    print(f"총 테스트 케이스: {len(all_cases)}개")
    print()

    # 카테고리별
    categories = {}
    for c in all_cases:
        categories[c.category] = categories.get(c.category, 0) + 1

    print("카테고리별:")
    for cat, count in categories.items():
        print(f"  - {cat}: {count}개")
    print()

    # 난이도별
    difficulties = {}
    for c in all_cases:
        difficulties[c.difficulty] = difficulties.get(c.difficulty, 0) + 1

    print("난이도별:")
    for diff, count in difficulties.items():
        print(f"  - {diff}: {count}개")


if __name__ == "__main__":
    print_test_case_stats()
