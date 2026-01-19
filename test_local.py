# -*- coding: utf-8 -*-
"""로컬 환경 테스트 스크립트"""

import sys
import time

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def test_imports():
    """필수 라이브러리 임포트 테스트"""
    print("1. 라이브러리 임포트 테스트...")
    try:
        from langchain_ollama import ChatOllama
        import tiktoken
        print("   [OK] langchain_ollama, tiktoken 임포트 성공")
        return True
    except ImportError as e:
        print(f"   [FAIL] 임포트 실패: {e}")
        return False

def test_ollama_connection():
    """Ollama 연결 테스트"""
    print("\n2. Ollama 연결 테스트...")
    try:
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model="qwen2.5:7b", temperature=0)
        response = llm.invoke("1+1은?")
        print(f"   [OK] Ollama 연결 성공")
        print(f"   응답: {response.content[:100]}")
        return True
    except Exception as e:
        print(f"   [FAIL] Ollama 연결 실패: {e}")
        return False

def test_token_counting():
    """토큰 카운팅 테스트"""
    print("\n3. 토큰 카운팅 테스트...")
    try:
        import tiktoken
        enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
        text = "안녕하세요, 프롬프트 엔지니어링 테스트입니다."
        tokens = len(enc.encode(text))
        print(f"   [OK] 토큰 카운팅 성공: '{text}' = {tokens} 토큰")
        return True
    except Exception as e:
        print(f"   [FAIL] 토큰 카운팅 실패: {e}")
        return False

def test_templates():
    """템플릿 모듈 테스트"""
    print("\n4. 템플릿 모듈 테스트...")
    try:
        sys.path.insert(0, '.')
        from templates import get_summary_prompt, get_classification_prompt

        # 요약 템플릿 테스트
        prompt = get_summary_prompt("테스트 텍스트입니다.", style="bullet", length=3)
        assert "###" in prompt
        print("   [OK] 요약 템플릿 생성 성공")

        # 분류 템플릿 테스트
        prompt = get_classification_prompt("테스트", ["긍정", "부정", "중립"])
        assert "###" in prompt
        print("   [OK] 분류 템플릿 생성 성공")

        return True
    except Exception as e:
        print(f"   [FAIL] 템플릿 테스트 실패: {e}")
        return False

def test_prompt_experiment():
    """프롬프트 실험 테스트"""
    print("\n5. 프롬프트 실험 테스트 (기본 vs 구조화)...")
    try:
        from langchain_ollama import ChatOllama
        import tiktoken

        llm = ChatOllama(model="qwen2.5:7b", temperature=0)
        enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

        test_text = "인공지능은 인간의 학습능력을 인공적으로 구현한 시스템이다."

        # 기본 프롬프트 (한국어)
        basic = f"요약해줘: {test_text}"
        start = time.time()
        r1 = llm.invoke(basic)
        t1 = time.time() - start
        tokens1 = len(enc.encode(r1.content))

        # 구조화 프롬프트 (한국어)
        structured = f"""### 지시사항
1문장으로 요약하세요.

### 텍스트
{test_text}

### 요약"""
        start = time.time()
        r2 = llm.invoke(structured)
        t2 = time.time() - start
        tokens2 = len(enc.encode(r2.content))

        print(f"   기본 프롬프트: {tokens1} 토큰, {t1:.2f}초")
        print(f"   구조화 프롬프트: {tokens2} 토큰, {t2:.2f}초")

        if tokens1 > 0:
            reduction = (1 - tokens2/tokens1) * 100
            print(f"   [OK] 토큰 절감율: {reduction:.1f}%")

        return True
    except Exception as e:
        print(f"   [FAIL] 실험 테스트 실패: {e}")
        return False

def main():
    print("=" * 50)
    print("프롬프트 엔지니어링 로컬 테스트")
    print("=" * 50)

    results = []
    results.append(("임포트", test_imports()))
    results.append(("Ollama", test_ollama_connection()))
    results.append(("토큰카운팅", test_token_counting()))
    results.append(("템플릿", test_templates()))
    results.append(("실험", test_prompt_experiment()))

    print("\n" + "=" * 50)
    print("테스트 결과 요약")
    print("=" * 50)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {name}: {status}")

    print(f"\n총 {passed}/{total} 테스트 통과")

    if passed == total:
        print("\n모든 테스트 통과! GitHub에 올릴 준비 완료.")
    else:
        print("\n일부 테스트 실패. 문제 해결 후 다시 시도하세요.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
