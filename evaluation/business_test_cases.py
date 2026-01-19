# -*- coding: utf-8 -*-
"""
================================================================================
비즈니스 문서 프롬프트 테스트 케이스 (Business Document Test Cases)
================================================================================

## 이 모듈의 목적
비즈니스 이메일, 보고서 작성 프롬프트의 성능을 검증하기 위한 테스트 케이스

## 테스트 케이스 구성 (총 108개)
| 카테고리 | 개수 | 설명 |
|----------|------|------|
| 이메일 작성 | 54개 | 공식, 사과, 제안, 후속 이메일 |
| 보고서 작성 | 54개 | 주간보고, 분석, 회의록, 기획서 |

## 이메일 유형
- 공식 업무 이메일 (14개)
- 사과/해명 이메일 (14개)
- 제안/협력 요청 이메일 (13개)
- 후속 조치 이메일 (13개)

## 보고서 유형
- 주간/월간 보고서 (14개)
- 분석 보고서 (14개)
- 회의록 (13개)
- 프로젝트 기획서 (13개)

## 테스트 케이스 설계 원칙
1. 실제 비즈니스 상황 반영
2. 다양한 산업/직무 커버
3. 복잡도 수준 다양화
4. 평가 가능한 명확한 기준
================================================================================
"""

from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class BusinessTestCase:
    """비즈니스 문서 테스트 케이스"""
    id: str
    category: str  # email, report
    subcategory: str  # formal, apology, proposal, follow_up / weekly, analysis, meeting, project
    scenario: str  # 시나리오 설명
    industry: str  # 산업군
    input_context: str  # 입력 상황/맥락
    expected_elements: List[str]  # 예상되는 필수 요소
    difficulty: str  # easy, medium, hard


# ============================================================================
# 이메일 테스트 케이스 (54개)
# ============================================================================

EMAIL_TEST_CASES = [
    # === 공식 업무 이메일 (14개) ===
    BusinessTestCase(
        id="EMAIL-001",
        category="email",
        subcategory="formal",
        scenario="미팅 요청 이메일",
        industry="IT",
        input_context="""
        발신자: 김철수 과장 (영업팀)
        수신자: 이영희 부장 (A사 구매팀)
        목적: 신규 솔루션 소개를 위한 미팅 요청
        관계: 첫 연락 (콜드 이메일)
        """,
        expected_elements=["명확한 목적", "미팅 가치 제안", "구체적 일정 제시", "부담없는 마무리"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-002",
        category="email",
        subcategory="formal",
        scenario="프로젝트 진행 상황 공유",
        industry="제조",
        input_context="""
        발신자: 박지민 대리 (기획팀)
        수신자: 최동현 상무 (경영지원본부)
        목적: ERP 도입 프로젝트 진행 상황 보고
        상황: 일정 지연 발생, 원인과 대책 설명 필요
        """,
        expected_elements=["현황 요약", "지연 원인", "대응 방안", "향후 일정"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-003",
        category="email",
        subcategory="formal",
        scenario="협조 요청 이메일",
        industry="금융",
        input_context="""
        발신자: 정수진 차장 (리스크관리팀)
        수신자: 유선영 팀장 (준법감시팀)
        목적: 내부 감사 관련 자료 협조 요청
        기한: 이번 주 금요일까지
        """,
        expected_elements=["요청 배경", "필요 자료 목록", "명확한 기한", "협조 감사"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="EMAIL-004",
        category="email",
        subcategory="formal",
        scenario="승인 요청 이메일",
        industry="유통",
        input_context="""
        발신자: 한미래 사원 (마케팅팀)
        수신자: 오세준 팀장 (마케팅팀)
        목적: 블랙프라이데이 프로모션 예산 증액 승인 요청
        금액: 기존 5천만원 → 8천만원
        근거: 경쟁사 동향, 예상 ROI
        """,
        expected_elements=["요청 사항 명확화", "증액 근거", "예상 효과", "결재 요청"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-005",
        category="email",
        subcategory="formal",
        scenario="결과 보고 이메일",
        industry="컨설팅",
        input_context="""
        발신자: 강태영 컨설턴트 (전략팀)
        수신자: 클라이언트 임원진
        목적: 3개월 프로젝트 최종 결과 공유
        내용: 핵심 발견사항, 권고안, 다음 단계
        """,
        expected_elements=["감사 인사", "핵심 결과 요약", "주요 권고", "후속 조치"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="EMAIL-006",
        category="email",
        subcategory="formal",
        scenario="공급업체 문의 이메일",
        industry="제조",
        input_context="""
        발신자: 이준호 과장 (구매팀)
        수신자: 신규 공급업체 담당자
        목적: 부품 견적 및 납기 문의
        상황: 긴급 발주 필요, 대량 구매 가능성
        """,
        expected_elements=["회사 소개", "구체적 문의 사항", "납기 요청", "향후 거래 가능성"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="EMAIL-007",
        category="email",
        subcategory="formal",
        scenario="계약 관련 이메일",
        industry="법률",
        input_context="""
        발신자: 최민서 변호사
        수신자: 클라이언트 법무팀장
        목적: 계약서 검토 완료 및 수정 사항 안내
        내용: 3가지 주요 수정 사항, 위험 요소 설명
        """,
        expected_elements=["검토 완료 안내", "수정 사항 명시", "위험 설명", "다음 절차"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="EMAIL-008",
        category="email",
        subcategory="formal",
        scenario="교육 안내 이메일",
        industry="HR",
        input_context="""
        발신자: 김하늘 대리 (인사팀)
        수신자: 전 직원
        목적: 정보보안 필수 교육 안내
        내용: 교육 일정, 장소, 미이수 시 불이익
        """,
        expected_elements=["교육 목적", "일정/장소", "대상자", "미이수 시 조치"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="EMAIL-009",
        category="email",
        subcategory="formal",
        scenario="해외 파트너 이메일",
        industry="무역",
        input_context="""
        발신자: 박서연 과장 (해외영업팀)
        수신자: 미국 바이어
        목적: 신규 제품 라인업 소개 및 샘플 제안
        상황: 기존 거래처, 추가 품목 확대 논의
        """,
        expected_elements=["관계 언급", "제품 소개", "샘플 제안", "다음 단계"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-010",
        category="email",
        subcategory="formal",
        scenario="인터뷰 요청 이메일",
        industry="미디어",
        input_context="""
        발신자: 조영준 기자
        수신자: 기업 CEO
        목적: 업계 트렌드 관련 인터뷰 요청
        매체: 경제 전문지, 월간 발행
        """,
        expected_elements=["매체 소개", "인터뷰 목적", "예상 질문", "일정 제안"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-011",
        category="email",
        subcategory="formal",
        scenario="업무 인수인계 이메일",
        industry="IT",
        input_context="""
        발신자: 나현우 대리 (개발팀)
        수신자: 관련 팀원들
        목적: 퇴사에 따른 담당 업무 인수인계 안내
        내용: 인수인계 일정, 담당자 변경, 문의처
        """,
        expected_elements=["인수인계 배경", "업무 목록", "담당자 안내", "문의처"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="EMAIL-012",
        category="email",
        subcategory="formal",
        scenario="시스템 점검 안내 이메일",
        industry="IT",
        input_context="""
        발신자: IT인프라팀
        수신자: 전사 직원
        목적: 주말 시스템 정기 점검 안내
        영향: 4시간 동안 사내 시스템 접속 불가
        """,
        expected_elements=["점검 목적", "일시", "영향 범위", "대응 방안"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="EMAIL-013",
        category="email",
        subcategory="formal",
        scenario="견적 회신 이메일",
        industry="서비스",
        input_context="""
        발신자: 윤지아 팀장 (영업팀)
        수신자: 잠재 고객사
        목적: 서비스 견적서 송부
        내용: 가격, 범위, 계약 조건, 유효 기간
        """,
        expected_elements=["감사 인사", "견적 요약", "특이사항", "다음 단계"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-014",
        category="email",
        subcategory="formal",
        scenario="정책 변경 안내 이메일",
        industry="HR",
        input_context="""
        발신자: 인사팀장
        수신자: 전 직원
        목적: 재택근무 정책 변경 안내
        내용: 변경 사항, 시행일, FAQ
        """,
        expected_elements=["변경 배경", "변경 내용", "시행일", "문의처"],
        difficulty="medium"
    ),

    # === 사과/해명 이메일 (14개) ===
    BusinessTestCase(
        id="EMAIL-015",
        category="email",
        subcategory="apology",
        scenario="서비스 장애 사과",
        industry="IT",
        input_context="""
        상황: 온라인 서비스 3시간 장애 발생
        원인: 서버 과부하로 인한 시스템 다운
        영향: 유료 회원 5만명 서비스 이용 불가
        보상: 1개월 이용권 무료 제공
        """,
        expected_elements=["진심어린 사과", "원인 설명", "조치 내용", "보상 안내", "재발 방지"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="EMAIL-016",
        category="email",
        subcategory="apology",
        scenario="배송 지연 사과",
        industry="유통",
        input_context="""
        상황: 물류 시스템 오류로 배송 3일 지연
        고객: 중요한 행사용 상품 주문 고객
        보상: 배송비 환불 + 10% 할인 쿠폰
        """,
        expected_elements=["사과", "지연 원인", "현재 배송 상황", "보상 안내"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-017",
        category="email",
        subcategory="apology",
        scenario="제품 불량 사과",
        industry="제조",
        input_context="""
        상황: 납품 제품 중 일부 불량 발견
        규모: 전체 납품량의 2%
        대응: 전량 교체 및 품질검사 강화
        """,
        expected_elements=["사과", "불량 현황", "즉시 조치", "예방 대책"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="EMAIL-018",
        category="email",
        subcategory="apology",
        scenario="미팅 불참 사과",
        industry="컨설팅",
        input_context="""
        상황: 클라이언트와의 중요 미팅에 30분 지각
        원인: 교통사고로 인한 도로 정체
        관계: 신규 프로젝트 킥오프 미팅
        """,
        expected_elements=["즉각 사과", "상황 설명", "미팅 내용 후속", "재발 방지"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="EMAIL-019",
        category="email",
        subcategory="apology",
        scenario="잘못된 정보 제공 사과",
        industry="금융",
        input_context="""
        상황: 고객에게 잘못된 금리 정보 안내
        영향: 고객의 투자 결정에 영향
        원인: 시스템 업데이트 누락
        """,
        expected_elements=["사과", "정정 정보", "발생 경위", "향후 조치"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="EMAIL-020",
        category="email",
        subcategory="apology",
        scenario="일정 변경 사과",
        industry="서비스",
        input_context="""
        상황: 이미 확정된 행사 일정 변경
        원인: 장소 예약 충돌
        변경: 1주일 연기
        영향: 참석자 100명
        """,
        expected_elements=["사과", "변경 내용", "변경 사유", "대응 안내"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-021",
        category="email",
        subcategory="apology",
        scenario="청구 오류 사과",
        industry="통신",
        input_context="""
        상황: 요금 이중 청구 발생
        규모: 약 1,000명의 고객
        대응: 자동 환불 처리 예정
        """,
        expected_elements=["사과", "오류 내용", "환불 절차", "재발 방지"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-022",
        category="email",
        subcategory="apology",
        scenario="개인정보 유출 사과",
        industry="IT",
        input_context="""
        상황: 해킹으로 인한 일부 회원 정보 유출
        유출 정보: 이메일, 연락처 (금융정보 제외)
        규모: 약 1만 명
        대응: 관계기관 신고, 피해 보상
        """,
        expected_elements=["진심어린 사과", "유출 경위", "피해 범위", "대응 조치", "보호 방법 안내"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="EMAIL-023",
        category="email",
        subcategory="apology",
        scenario="서비스 품질 저하 사과",
        industry="호텔",
        input_context="""
        상황: 예약과 다른 객실 배정
        고객: VIP 회원, 기념일 여행
        대응: 스위트룸 무료 업그레이드 + 조식 제공
        """,
        expected_elements=["사과", "상황 인정", "즉시 보상", "추가 서비스"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-024",
        category="email",
        subcategory="apology",
        scenario="답변 지연 사과",
        industry="고객서비스",
        input_context="""
        상황: 고객 문의 후 1주일간 무응답
        원인: 내부 시스템 문제로 누락
        고객 감정: 강한 불만 표시
        """,
        expected_elements=["진심어린 사과", "지연 원인", "문의 답변", "보상 제안"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-025",
        category="email",
        subcategory="apology",
        scenario="계약 조건 미이행 사과",
        industry="B2B",
        input_context="""
        상황: 계약된 월간 보고서 2회 미제출
        원인: 담당자 부재 및 인수인계 미흡
        파트너: 장기 거래 파트너사
        """,
        expected_elements=["사과", "미이행 인정", "밀린 보고서 제출", "재발 방지"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="EMAIL-026",
        category="email",
        subcategory="apology",
        scenario="AS 처리 지연 사과",
        industry="가전",
        input_context="""
        상황: AS 접수 후 2주간 방문 지연
        원인: 부품 수급 문제
        고객: 제품 보증 기간 내
        """,
        expected_elements=["사과", "지연 원인", "예상 일정", "보상 안내"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-027",
        category="email",
        subcategory="apology",
        scenario="잘못된 발송 사과",
        industry="유통",
        input_context="""
        상황: 다른 고객의 주문품 잘못 배송
        문제: 개인정보(주소) 노출
        대응: 즉시 회수 및 재발송
        """,
        expected_elements=["사과", "오류 인정", "회수/재발송", "개인정보 보호 조치"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="EMAIL-028",
        category="email",
        subcategory="apology",
        scenario="행사 취소 사과",
        industry="이벤트",
        input_context="""
        상황: 코로나로 인한 대규모 행사 취소
        규모: 참가자 500명
        대응: 전액 환불 또는 온라인 전환
        """,
        expected_elements=["사과", "취소 사유", "환불 정책", "대안 제시"],
        difficulty="medium"
    ),

    # === 제안/협력 요청 이메일 (13개) ===
    BusinessTestCase(
        id="EMAIL-029",
        category="email",
        subcategory="proposal",
        scenario="파트너십 제안",
        industry="IT",
        input_context="""
        발신자: AI 스타트업 사업개발팀
        수신자: 대기업 디지털혁신팀장
        제안: AI 솔루션 파일럿 프로젝트 협력
        가치: 업무 효율 30% 개선 사례 보유
        """,
        expected_elements=["회사 소개", "제안 배경", "기대 가치", "다음 단계"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="EMAIL-030",
        category="email",
        subcategory="proposal",
        scenario="투자 유치 제안",
        industry="스타트업",
        input_context="""
        발신자: 핀테크 스타트업 대표
        수신자: VC 파트너
        제안: 시리즈 A 투자 유치
        현황: MAU 10만, MRR 5억원
        """,
        expected_elements=["요약 피치", "성장 지표", "투자 요청", "미팅 제안"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="EMAIL-031",
        category="email",
        subcategory="proposal",
        scenario="공동 마케팅 제안",
        industry="마케팅",
        input_context="""
        발신자: 뷰티 브랜드 마케팅팀
        수신자: 유튜버 매니지먼트사
        제안: 인플루언서 협업 캠페인
        조건: 제품 협찬 + 성과 기반 보상
        """,
        expected_elements=["협업 목적", "제안 조건", "기대 효과", "진행 방안"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-032",
        category="email",
        subcategory="proposal",
        scenario="기술 제휴 제안",
        industry="제조",
        input_context="""
        발신자: 배터리 기술 기업
        수신자: 전기차 제조사 기술팀
        제안: 차세대 배터리 공동 개발
        강점: 특허 50건, 에너지 밀도 20% 향상
        """,
        expected_elements=["기술 소개", "제휴 필요성", "협력 범위", "기대 시너지"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="EMAIL-033",
        category="email",
        subcategory="proposal",
        scenario="강연 요청",
        industry="교육",
        input_context="""
        발신자: 대학교 취업지원센터
        수신자: 업계 전문가
        제안: 취업 특강 강연 요청
        조건: 2시간, 강연료 50만원
        """,
        expected_elements=["강연 목적", "대상자", "조건", "일정 제안"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="EMAIL-034",
        category="email",
        subcategory="proposal",
        scenario="판매 채널 입점 제안",
        industry="유통",
        input_context="""
        발신자: 식품 스타트업
        수신자: 대형마트 MD
        제안: 신제품 입점 제안
        차별점: 비건 제품, SNS 팔로워 10만
        """,
        expected_elements=["제품 소개", "차별점", "판매 실적", "조건 협의"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-035",
        category="email",
        subcategory="proposal",
        scenario="프로젝트 외주 제안",
        industry="IT",
        input_context="""
        발신자: 개발 에이전시
        수신자: 스타트업 CTO
        제안: 앱 개발 외주
        역량: 유사 프로젝트 10건 수행
        """,
        expected_elements=["회사 역량", "관련 경험", "견적 범위", "미팅 제안"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-036",
        category="email",
        subcategory="proposal",
        scenario="콘텐츠 협업 제안",
        industry="미디어",
        input_context="""
        발신자: 미디어 스타트업
        수신자: 전통 언론사
        제안: 콘텐츠 공동 제작 및 배포
        가치: 디지털 채널 확대, 젊은 독자층
        """,
        expected_elements=["협업 배경", "제안 내용", "상호 이익", "논의 요청"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-037",
        category="email",
        subcategory="proposal",
        scenario="연구 협력 제안",
        industry="제약",
        input_context="""
        발신자: 바이오 연구소
        수신자: 제약회사 R&D 센터장
        제안: 신약 후보물질 공동 연구
        현황: 전임상 완료, 특허 출원
        """,
        expected_elements=["연구 현황", "협력 필요성", "역할 분담", "다음 단계"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="EMAIL-038",
        category="email",
        subcategory="proposal",
        scenario="이벤트 스폰서십 제안",
        industry="이벤트",
        input_context="""
        발신자: 컨퍼런스 주최사
        수신자: 기업 마케팅팀장
        제안: 개발자 컨퍼런스 메인 스폰서
        규모: 참가자 2,000명, 온라인 중계
        """,
        expected_elements=["행사 소개", "스폰서 혜택", "비용", "의향 확인"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-039",
        category="email",
        subcategory="proposal",
        scenario="시장 진출 협력 제안",
        industry="무역",
        input_context="""
        발신자: 해외 진출 컨설팅사
        수신자: 중소기업 대표
        제안: 동남아 시장 진출 지원
        역량: 현지 네트워크, 성공 사례 5건
        """,
        expected_elements=["시장 기회", "지원 범위", "역량 증명", "상담 제안"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-040",
        category="email",
        subcategory="proposal",
        scenario="데이터 공유 제안",
        industry="빅데이터",
        input_context="""
        발신자: 데이터 플랫폼 기업
        수신자: 연구기관
        제안: 익명화된 데이터 연구 목적 공유
        조건: 공동 연구, 논문 공저
        """,
        expected_elements=["데이터 소개", "활용 범위", "협력 조건", "절차 안내"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-041",
        category="email",
        subcategory="proposal",
        scenario="업무 제휴 제안",
        industry="서비스",
        input_context="""
        발신자: HR 솔루션 기업
        수신자: 인력파견 회사
        제안: 플랫폼 연동을 통한 서비스 확대
        시너지: 상호 고객 확보
        """,
        expected_elements=["제휴 배경", "연동 범위", "기대 효과", "논의 요청"],
        difficulty="medium"
    ),

    # === 후속 조치 이메일 (13개) ===
    BusinessTestCase(
        id="EMAIL-042",
        category="email",
        subcategory="follow_up",
        scenario="미팅 후 후속 이메일",
        industry="영업",
        input_context="""
        이전 상호작용: 1주일 전 제품 데모 미팅
        논의 내용: 가격 협의, 기능 커스터마이징
        다음 단계: 정식 견적서 전달
        """,
        expected_elements=["미팅 감사", "논의 요약", "요청 자료", "다음 일정"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="EMAIL-043",
        category="email",
        subcategory="follow_up",
        scenario="견적 후 후속",
        industry="B2B",
        input_context="""
        이전 상호작용: 2주 전 견적서 발송
        상황: 아직 회신 없음
        목표: 검토 상황 확인 및 미팅 재제안
        """,
        expected_elements=["견적 리마인드", "추가 정보 제공", "검토 확인", "지원 제안"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-044",
        category="email",
        subcategory="follow_up",
        scenario="컨퍼런스 후 네트워킹",
        industry="네트워킹",
        input_context="""
        이전 상호작용: 3일 전 컨퍼런스에서 명함 교환
        대화 내용: 업계 동향, 협업 가능성
        목표: 커피챗 제안
        """,
        expected_elements=["만남 상기", "대화 언급", "관심 표현", "미팅 제안"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="EMAIL-045",
        category="email",
        subcategory="follow_up",
        scenario="프로젝트 진행 확인",
        industry="PM",
        input_context="""
        이전 상호작용: 프로젝트 착수 2주 후
        상황: 마일스톤 1 완료 확인 필요
        관계: 클라이언트-에이전시
        """,
        expected_elements=["진행 상황", "완료 항목", "이슈 여부", "다음 단계"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-046",
        category="email",
        subcategory="follow_up",
        scenario="채용 면접 후 후속",
        industry="HR",
        input_context="""
        이전 상호작용: 1주일 전 최종 면접
        상황: 합격 통보 예정
        목표: 입사 의향 및 조건 협의
        """,
        expected_elements=["면접 감사", "합격 안내", "조건 제시", "회신 요청"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="EMAIL-047",
        category="email",
        subcategory="follow_up",
        scenario="제안서 후 결정 확인",
        industry="컨설팅",
        input_context="""
        이전 상호작용: 3주 전 프로젝트 제안서 제출
        상황: 의사결정 지연
        목표: 진행 상황 확인, 추가 정보 제공
        """,
        expected_elements=["제안서 리마인드", "추가 가치", "의사결정 확인", "지원 의향"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-048",
        category="email",
        subcategory="follow_up",
        scenario="고객 서비스 후 만족도",
        industry="고객서비스",
        input_context="""
        이전 상호작용: 1주일 전 AS 완료
        목표: 서비스 만족도 확인 및 피드백 요청
        관계: 프리미엄 고객
        """,
        expected_elements=["AS 완료 확인", "만족도 문의", "추가 지원", "피드백 요청"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="EMAIL-049",
        category="email",
        subcategory="follow_up",
        scenario="교육 후 후속",
        industry="교육",
        input_context="""
        이전 상호작용: 2일 전 기업 교육 완료
        목표: 교육 효과 확인, 추가 교육 제안
        참가자: 30명
        """,
        expected_elements=["교육 마무리 인사", "자료 공유", "피드백 요청", "후속 과정 안내"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="EMAIL-050",
        category="email",
        subcategory="follow_up",
        scenario="파트너십 논의 후속",
        industry="사업개발",
        input_context="""
        이전 상호작용: 1주일 전 파트너십 논의 미팅
        논의 내용: 협력 범위, 수익 배분
        다음 단계: 내부 검토 후 재논의
        """,
        expected_elements=["미팅 요약", "합의 사항", "검토 요청", "다음 미팅 제안"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-051",
        category="email",
        subcategory="follow_up",
        scenario="제품 데모 후 피드백",
        industry="SaaS",
        input_context="""
        이전 상호작용: 어제 온라인 제품 데모
        참석자: 고객사 IT팀 5명
        목표: 피드백 수집, 트라이얼 제안
        """,
        expected_elements=["데모 감사", "주요 기능 리마인드", "피드백 요청", "트라이얼 안내"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="EMAIL-052",
        category="email",
        subcategory="follow_up",
        scenario="계약 협상 후속",
        industry="법무",
        input_context="""
        이전 상호작용: 계약 조건 협의
        상황: 일부 조항 수정 요청
        목표: 수정안 전달, 서명 일정 조율
        """,
        expected_elements=["협의 감사", "수정 내용", "검토 요청", "서명 일정"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-053",
        category="email",
        subcategory="follow_up",
        scenario="이직 제안 후 확인",
        industry="헤드헌팅",
        input_context="""
        이전 상호작용: 1주일 전 이직 제안 통화
        상황: 검토 중이라고 답변
        목표: 결정 상황 확인, 추가 정보 제공
        """,
        expected_elements=["통화 상기", "포지션 장점", "결정 확인", "지원 의향"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="EMAIL-054",
        category="email",
        subcategory="follow_up",
        scenario="구독 갱신 리마인드",
        industry="SaaS",
        input_context="""
        상황: 연간 구독 만료 1개월 전
        고객: 2년 이용 고객
        목표: 갱신 안내 및 특별 혜택 제공
        """,
        expected_elements=["만료 안내", "갱신 혜택", "특별 제안", "절차 안내"],
        difficulty="easy"
    ),
]


# ============================================================================
# 보고서 테스트 케이스 (54개)
# ============================================================================

REPORT_TEST_CASES = [
    # === 주간/월간 보고서 (14개) ===
    BusinessTestCase(
        id="REPORT-001",
        category="report",
        subcategory="weekly",
        scenario="개발팀 주간 보고",
        industry="IT",
        input_context="""
        보고자: 개발팀 리드
        기간: 1/15 ~ 1/19
        주요 업무: 신규 기능 개발, 버그 수정
        이슈: 일정 지연 우려
        """,
        expected_elements=["완료 업무", "진행 상황", "이슈/리스크", "다음 주 계획"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="REPORT-002",
        category="report",
        subcategory="weekly",
        scenario="영업팀 주간 보고",
        industry="영업",
        input_context="""
        보고자: 영업팀 매니저
        기간: 1월 3주차
        성과: 계약 3건 체결, 미팅 15건
        목표 대비: 110% 달성
        """,
        expected_elements=["영업 실적", "파이프라인", "주요 활동", "목표 대비"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="REPORT-003",
        category="report",
        subcategory="weekly",
        scenario="마케팅팀 월간 보고",
        industry="마케팅",
        input_context="""
        보고자: 마케팅팀
        기간: 2024년 1월
        성과: 캠페인 ROI 250%, 리드 1,200건
        예산: 5천만원 중 4,500만원 집행
        """,
        expected_elements=["캠페인 성과", "채널별 분석", "예산 현황", "다음달 계획"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-004",
        category="report",
        subcategory="weekly",
        scenario="고객서비스팀 주간 보고",
        industry="서비스",
        input_context="""
        보고자: CS팀장
        기간: 1월 2주차
        처리 건수: 450건, 평균 응답 시간 2시간
        고객 만족도: 4.5/5.0
        """,
        expected_elements=["처리 현황", "만족도", "주요 이슈", "개선 사항"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="REPORT-005",
        category="report",
        subcategory="weekly",
        scenario="재무팀 월간 보고",
        industry="금융",
        input_context="""
        보고자: 재무팀장
        기간: 2024년 1월
        매출: 50억원 (목표 대비 98%)
        영업이익: 8억원 (마진 16%)
        """,
        expected_elements=["재무 요약", "손익 현황", "현금 흐름", "예산 대비"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-006",
        category="report",
        subcategory="weekly",
        scenario="인사팀 월간 보고",
        industry="HR",
        input_context="""
        보고자: 인사팀장
        기간: 2024년 1월
        채용: 5명 입사, 2명 퇴사
        교육: 필수 교육 이수율 95%
        """,
        expected_elements=["인력 현황", "채용 활동", "교육 현황", "이슈"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-007",
        category="report",
        subcategory="weekly",
        scenario="프로젝트 주간 보고",
        industry="PM",
        input_context="""
        프로젝트: ERP 도입 프로젝트
        기간: 8주차/12주차
        진행률: 65%
        이슈: 요구사항 추가로 일정 조정 필요
        """,
        expected_elements=["진행 현황", "마일스톤", "리스크", "의사결정 필요"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-008",
        category="report",
        subcategory="weekly",
        scenario="생산팀 일간 보고",
        industry="제조",
        input_context="""
        보고자: 생산라인 매니저
        날짜: 2024-01-20
        생산량: 5,000개 (목표: 5,500개)
        불량률: 0.5%
        """,
        expected_elements=["생산 실적", "품질 현황", "설비 상태", "이슈"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="REPORT-009",
        category="report",
        subcategory="weekly",
        scenario="연구개발팀 월간 보고",
        industry="R&D",
        input_context="""
        보고자: R&D 센터장
        기간: 2024년 1월
        과제: 3개 과제 진행 중
        특허: 2건 출원
        """,
        expected_elements=["연구 진행", "특허/논문", "예산 현황", "이슈"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-010",
        category="report",
        subcategory="weekly",
        scenario="물류팀 주간 보고",
        industry="물류",
        input_context="""
        보고자: 물류센터장
        기간: 1월 3주차
        출고량: 12,000건, 배송 완료율 99.5%
        반품률: 2%
        """,
        expected_elements=["출고 현황", "배송 품질", "재고 현황", "이슈"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="REPORT-011",
        category="report",
        subcategory="weekly",
        scenario="법무팀 분기 보고",
        industry="법무",
        input_context="""
        보고자: 법무팀장
        기간: 2024년 Q1
        계약 검토: 150건
        소송 현황: 진행 중 3건
        """,
        expected_elements=["계약 업무", "소송 현황", "규제 동향", "리스크"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-012",
        category="report",
        subcategory="weekly",
        scenario="IT운영팀 주간 보고",
        industry="IT",
        input_context="""
        보고자: IT운영팀장
        기간: 1월 3주차
        장애: 1건 (30분 내 복구)
        가용성: 99.9%
        """,
        expected_elements=["시스템 가용성", "장애 현황", "변경 관리", "계획"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-013",
        category="report",
        subcategory="weekly",
        scenario="QA팀 주간 보고",
        industry="IT",
        input_context="""
        보고자: QA팀 리드
        기간: 1월 3주차
        테스트: 200건, 통과율 95%
        버그: Critical 2건 발견
        """,
        expected_elements=["테스트 현황", "품질 지표", "주요 버그", "리스크"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-014",
        category="report",
        subcategory="weekly",
        scenario="구매팀 월간 보고",
        industry="구매",
        input_context="""
        보고자: 구매팀장
        기간: 2024년 1월
        발주: 50건, 총 10억원
        납기 준수율: 92%
        """,
        expected_elements=["구매 현황", "비용 절감", "공급망 이슈", "계획"],
        difficulty="medium"
    ),

    # === 분석 보고서 (14개) ===
    BusinessTestCase(
        id="REPORT-015",
        category="report",
        subcategory="analysis",
        scenario="시장 분석 보고서",
        industry="전략",
        input_context="""
        분석 대상: 국내 SaaS 시장
        목적: 신규 사업 진출 타당성 검토
        데이터: 시장 규모, 성장률, 주요 플레이어
        """,
        expected_elements=["시장 현황", "경쟁 분석", "기회/위협", "권고사항"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-016",
        category="report",
        subcategory="analysis",
        scenario="경쟁사 분석 보고서",
        industry="마케팅",
        input_context="""
        분석 대상: 주요 경쟁사 3사
        분석 항목: 제품, 가격, 마케팅 전략
        목적: 차별화 전략 수립
        """,
        expected_elements=["경쟁사 개요", "비교 분석", "SWOT", "전략 제안"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-017",
        category="report",
        subcategory="analysis",
        scenario="고객 이탈 분석",
        industry="서비스",
        input_context="""
        분석 대상: 최근 6개월 이탈 고객
        이탈 규모: 월 평균 5%
        데이터: 이용 패턴, 불만 사항, 경쟁사 이동
        """,
        expected_elements=["이탈 현황", "원인 분석", "고객 세그먼트", "개선 방안"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-018",
        category="report",
        subcategory="analysis",
        scenario="투자 수익률 분석",
        industry="금융",
        input_context="""
        분석 대상: 마케팅 캠페인 ROI
        투자: 1억원 / 매출: 5억원
        기간: 2023년 연간
        """,
        expected_elements=["투자 현황", "수익 분석", "채널별 ROI", "최적화 방안"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-019",
        category="report",
        subcategory="analysis",
        scenario="사용자 행동 분석",
        industry="IT",
        input_context="""
        분석 대상: 앱 사용자 행동
        데이터: 세션, 전환율, 리텐션
        목적: UX 개선 방향 도출
        """,
        expected_elements=["현황 분석", "사용자 여정", "이탈 지점", "개선 제안"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-020",
        category="report",
        subcategory="analysis",
        scenario="공급망 리스크 분석",
        industry="제조",
        input_context="""
        분석 배경: 글로벌 공급망 불안정
        분석 항목: 공급업체, 재고, 리드타임
        목적: 리스크 대응 전략 수립
        """,
        expected_elements=["리스크 현황", "영향 분석", "대응 시나리오", "권고사항"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-021",
        category="report",
        subcategory="analysis",
        scenario="직원 만족도 분석",
        industry="HR",
        input_context="""
        분석 대상: 전사 직원 만족도 조사 결과
        응답률: 85% (850명/1,000명)
        주요 지표: 업무 만족, 보상, 성장 기회
        """,
        expected_elements=["전체 결과", "부서별 분석", "개선 필요 영역", "액션플랜"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-022",
        category="report",
        subcategory="analysis",
        scenario="제품 수익성 분석",
        industry="유통",
        input_context="""
        분석 대상: 전 제품 라인업 (100개 SKU)
        분석 항목: 매출, 마진, 재고회전율
        목적: 제품 포트폴리오 최적화
        """,
        expected_elements=["제품별 수익성", "BCG 매트릭스", "단종 후보", "투자 방향"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-023",
        category="report",
        subcategory="analysis",
        scenario="디지털 마케팅 성과 분석",
        industry="마케팅",
        input_context="""
        분석 대상: 디지털 채널 마케팅 성과
        채널: 검색광고, SNS, 이메일
        기간: Q4 2023
        """,
        expected_elements=["채널별 성과", "전환 분석", "예산 효율", "최적화 방안"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-024",
        category="report",
        subcategory="analysis",
        scenario="업무 프로세스 분석",
        industry="컨설팅",
        input_context="""
        분석 대상: 주문-배송 프로세스
        현재 리드타임: 5일
        목표: 비효율 요인 발굴 및 개선
        """,
        expected_elements=["현행 프로세스", "병목 지점", "개선 기회", "To-Be 프로세스"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-025",
        category="report",
        subcategory="analysis",
        scenario="웹사이트 성능 분석",
        industry="IT",
        input_context="""
        분석 대상: 회사 웹사이트
        지표: 로딩 속도, 이탈률, 전환율
        목적: SEO 및 UX 개선
        """,
        expected_elements=["성능 지표", "문제 영역", "경쟁사 비교", "개선 권고"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-026",
        category="report",
        subcategory="analysis",
        scenario="가격 전략 분석",
        industry="유통",
        input_context="""
        분석 배경: 신제품 출시 가격 결정
        분석 항목: 원가, 경쟁사 가격, 고객 지불의향
        목표: 최적 가격대 도출
        """,
        expected_elements=["원가 분석", "경쟁 가격", "가격 탄력성", "권고 가격"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-027",
        category="report",
        subcategory="analysis",
        scenario="인력 계획 분석",
        industry="HR",
        input_context="""
        분석 목적: 내년 인력 계획 수립
        현황: 총 원 500명
        예측: 사업 성장, 퇴직률, 채용 시장
        """,
        expected_elements=["현황 분석", "수요 예측", "갭 분석", "채용 계획"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-028",
        category="report",
        subcategory="analysis",
        scenario="기술 트렌드 분석",
        industry="R&D",
        input_context="""
        분석 대상: 업계 기술 트렌드
        범위: AI, 클라우드, 보안
        목적: R&D 투자 방향 결정
        """,
        expected_elements=["트렌드 현황", "기술 성숙도", "경쟁사 동향", "투자 제안"],
        difficulty="medium"
    ),

    # === 회의록 (13개) ===
    BusinessTestCase(
        id="REPORT-029",
        category="report",
        subcategory="meeting",
        scenario="프로젝트 킥오프 회의",
        industry="PM",
        input_context="""
        회의명: ERP 프로젝트 킥오프
        참석자: 프로젝트팀, 현업, 경영진
        안건: 프로젝트 범위, 일정, 역할 분담
        """,
        expected_elements=["회의 목적", "논의 사항", "결정 사항", "액션아이템"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-030",
        category="report",
        subcategory="meeting",
        scenario="주간 팀 미팅",
        industry="일반",
        input_context="""
        회의명: 개발팀 주간 미팅
        참석자: 팀원 8명
        안건: 진행 상황 공유, 이슈 논의
        """,
        expected_elements=["진행 상황", "이슈 목록", "논의 내용", "다음 주 계획"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="REPORT-031",
        category="report",
        subcategory="meeting",
        scenario="경영진 회의",
        industry="경영",
        input_context="""
        회의명: 월례 경영회의
        참석자: CEO, C-레벨 임원
        안건: 월간 실적, 전략 이슈, 의사결정
        """,
        expected_elements=["실적 리뷰", "전략 논의", "결정 사항", "후속 조치"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-032",
        category="report",
        subcategory="meeting",
        scenario="고객 미팅",
        industry="영업",
        input_context="""
        회의명: A사 솔루션 제안 미팅
        참석자: 영업팀, 고객사 IT팀
        안건: 요구사항 확인, 솔루션 데모
        """,
        expected_elements=["고객 요구사항", "제안 내용", "Q&A", "다음 단계"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-033",
        category="report",
        subcategory="meeting",
        scenario="이사회 회의",
        industry="경영",
        input_context="""
        회의명: 정기 이사회
        참석자: 등기이사 5명
        안건: 분기 실적 승인, 신규 사업 안건
        """,
        expected_elements=["안건별 논의", "의결 사항", "이사 의견", "추가 지시"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-034",
        category="report",
        subcategory="meeting",
        scenario="제품 기획 회의",
        industry="기획",
        input_context="""
        회의명: 신제품 기획 회의
        참석자: 기획, 개발, 디자인팀
        안건: 제품 방향, 주요 기능, 일정
        """,
        expected_elements=["제품 컨셉", "기능 논의", "우선순위", "일정 합의"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-035",
        category="report",
        subcategory="meeting",
        scenario="문제 해결 회의",
        industry="운영",
        input_context="""
        회의명: 품질 이슈 긴급 회의
        참석자: 품질팀, 생산팀, 경영진
        안건: 불량 원인 분석, 대책 수립
        """,
        expected_elements=["문제 현황", "원인 분석", "대책 논의", "즉시 조치"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-036",
        category="report",
        subcategory="meeting",
        scenario="예산 회의",
        industry="재무",
        input_context="""
        회의명: 내년도 예산 심의
        참석자: 재무팀, 각 부서장
        안건: 부서별 예산 요청, 조정 협의
        """,
        expected_elements=["예산 요청", "조정 논의", "승인 내역", "추가 검토"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-037",
        category="report",
        subcategory="meeting",
        scenario="스프린트 회고",
        industry="IT",
        input_context="""
        회의명: Sprint 23 회고
        참석자: 스크럼팀 6명
        안건: 잘된 점, 개선점, 액션아이템
        """,
        expected_elements=["성과 리뷰", "좋았던 점", "개선 필요", "액션아이템"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="REPORT-038",
        category="report",
        subcategory="meeting",
        scenario="파트너 미팅",
        industry="사업개발",
        input_context="""
        회의명: B사 파트너십 협의
        참석자: 양사 사업개발팀
        안건: 협력 범위, 조건 협의
        """,
        expected_elements=["협의 배경", "논의 내용", "잠정 합의", "후속 절차"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-039",
        category="report",
        subcategory="meeting",
        scenario="채용 면접 논의",
        industry="HR",
        input_context="""
        회의명: 개발자 채용 면접 디브리핑
        참석자: 면접관 3명, 인사팀
        안건: 후보자 평가, 합격 여부 결정
        """,
        expected_elements=["후보자 평가", "면접관 의견", "결정 사항", "조건 협의"],
        difficulty="easy"
    ),
    BusinessTestCase(
        id="REPORT-040",
        category="report",
        subcategory="meeting",
        scenario="위기 대응 회의",
        industry="PR",
        input_context="""
        회의명: 언론 보도 대응 긴급회의
        참석자: PR팀, 법무팀, 경영진
        안건: 상황 파악, 대응 전략 수립
        """,
        expected_elements=["상황 브리핑", "대응 방안", "미디어 대응", "후속 모니터링"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-041",
        category="report",
        subcategory="meeting",
        scenario="변경 관리 회의",
        industry="IT",
        input_context="""
        회의명: 시스템 변경 승인 회의
        참석자: IT운영팀, 현업, 보안팀
        안건: 변경 요청 검토, 승인 여부
        """,
        expected_elements=["변경 요청", "영향 분석", "리스크 검토", "승인/반려"],
        difficulty="medium"
    ),

    # === 프로젝트 기획서 (13개) ===
    BusinessTestCase(
        id="REPORT-042",
        category="report",
        subcategory="project",
        scenario="신규 서비스 기획서",
        industry="IT",
        input_context="""
        프로젝트: B2B SaaS 플랫폼 개발
        목표: 6개월 내 MVP 출시
        예산: 5억원
        팀: 10명
        """,
        expected_elements=["배경/필요성", "목표", "범위", "일정", "예산", "리스크"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-043",
        category="report",
        subcategory="project",
        scenario="사내 시스템 도입 기획",
        industry="IT",
        input_context="""
        프로젝트: RPA 도입을 통한 업무 자동화
        대상: 재무, 인사팀 반복 업무
        기대효과: 연간 1,000시간 절감
        """,
        expected_elements=["현황/문제", "솔루션", "기대효과", "추진계획"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-044",
        category="report",
        subcategory="project",
        scenario="마케팅 캠페인 기획",
        industry="마케팅",
        input_context="""
        프로젝트: 신제품 런칭 캠페인
        기간: 3개월
        예산: 2억원
        목표: 인지도 50% 달성
        """,
        expected_elements=["캠페인 목표", "타깃", "전략/전술", "예산", "KPI"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-045",
        category="report",
        subcategory="project",
        scenario="해외 진출 기획",
        industry="사업개발",
        input_context="""
        프로젝트: 베트남 시장 진출
        시장규모: 연 5,000억원
        진출형태: 현지 법인 설립
        예상투자: 30억원
        """,
        expected_elements=["시장 분석", "진출 전략", "투자 계획", "리스크", "마일스톤"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-046",
        category="report",
        subcategory="project",
        scenario="업무 프로세스 개선 기획",
        industry="운영",
        input_context="""
        프로젝트: 주문-배송 프로세스 개선
        현황: 리드타임 5일
        목표: 리드타임 3일로 단축
        """,
        expected_elements=["현황 분석", "개선 방안", "기대효과", "추진 일정"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-047",
        category="report",
        subcategory="project",
        scenario="교육 프로그램 기획",
        industry="HR",
        input_context="""
        프로젝트: 차세대 리더 육성 프로그램
        대상: 과장급 30명
        기간: 6개월
        예산: 1억원
        """,
        expected_elements=["목적", "커리큘럼", "운영 계획", "평가 방법"],
        difficulty="medium"
    ),
    BusinessTestCase(
        id="REPORT-048",
        category="report",
        subcategory="project",
        scenario="시스템 리뉴얼 기획",
        industry="IT",
        input_context="""
        프로젝트: 레거시 시스템 현대화
        대상: 10년된 ERP 시스템
        방식: 클라우드 마이그레이션
        기간: 18개월
        """,
        expected_elements=["현황/문제", "목표 아키텍처", "마이그레이션 전략", "리스크"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-049",
        category="report",
        subcategory="project",
        scenario="신규 매장 출점 기획",
        industry="유통",
        input_context="""
        프로젝트: 강남 플래그십 스토어 오픈
        규모: 300평
        투자: 20억원
        오픈 예정: 6개월 후
        """,
        expected_elements=["상권 분석", "매장 컨셉", "투자 계획", "예상 수익", "일정"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-050",
        category="report",
        subcategory="project",
        scenario="보안 강화 기획",
        industry="IT보안",
        input_context="""
        프로젝트: 정보보안 체계 고도화
        배경: 보안 규제 강화
        범위: 기술적/관리적 보안
        예산: 3억원
        """,
        expected_elements=["현황 진단", "개선 방안", "투자 계획", "기대효과"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-051",
        category="report",
        subcategory="project",
        scenario="고객 경험 개선 기획",
        industry="서비스",
        input_context="""
        프로젝트: 옴니채널 고객 경험 통합
        현황: 온/오프라인 분리 운영
        목표: 통합 고객 여정 구축
        """,
        expected_elements=["현황/페인포인트", "목표 경험", "구현 방안", "기대효과"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-052",
        category="report",
        subcategory="project",
        scenario="ESG 경영 기획",
        industry="경영전략",
        input_context="""
        프로젝트: ESG 경영 체계 구축
        배경: 투자자/고객 요구 증가
        범위: 환경, 사회, 지배구조
        기간: 1년
        """,
        expected_elements=["현황 진단", "목표 설정", "추진 과제", "로드맵"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-053",
        category="report",
        subcategory="project",
        scenario="데이터 플랫폼 기획",
        industry="IT",
        input_context="""
        프로젝트: 통합 데이터 플랫폼 구축
        목적: 데이터 기반 의사결정 체계
        범위: 데이터 수집, 분석, 시각화
        예산: 8억원
        """,
        expected_elements=["현황/필요성", "아키텍처", "구축 계획", "기대효과"],
        difficulty="hard"
    ),
    BusinessTestCase(
        id="REPORT-054",
        category="report",
        subcategory="project",
        scenario="조직 개편 기획",
        industry="HR",
        input_context="""
        프로젝트: 애자일 조직 전환
        배경: 의사결정 속도 개선 필요
        범위: 개발/기획 조직 200명
        기간: 6개월
        """,
        expected_elements=["현황/문제", "목표 조직", "전환 계획", "변화관리"],
        difficulty="hard"
    ),
]


# ============================================================================
# 테스트 케이스 접근 함수
# ============================================================================

def get_all_business_test_cases() -> List[BusinessTestCase]:
    """모든 비즈니스 테스트 케이스 반환 (108개)"""
    return EMAIL_TEST_CASES + REPORT_TEST_CASES


def get_email_test_cases() -> List[BusinessTestCase]:
    """이메일 테스트 케이스 반환 (54개)"""
    return EMAIL_TEST_CASES


def get_report_test_cases() -> List[BusinessTestCase]:
    """보고서 테스트 케이스 반환 (54개)"""
    return REPORT_TEST_CASES


def get_test_cases_by_category(category: str) -> List[BusinessTestCase]:
    """카테고리별 테스트 케이스 반환"""
    all_cases = get_all_business_test_cases()
    return [tc for tc in all_cases if tc.category == category]


def get_test_cases_by_subcategory(subcategory: str) -> List[BusinessTestCase]:
    """서브카테고리별 테스트 케이스 반환"""
    all_cases = get_all_business_test_cases()
    return [tc for tc in all_cases if tc.subcategory == subcategory]
