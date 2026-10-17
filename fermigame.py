import streamlit as st
import math

# 페이지 설정
st.set_page_config(page_title="법률 페르미 추정 챌린지", page_icon="⚖️", layout="centered")

# 정확한 연도와 공식 근거에 기반한 10문제 데이터베이스 (힌트 전면 삭제)
QUESTIONS = [
    {
        "title": "국가법령정보센터 기준 현행 법률 총개수",
        "desc": "2025년 12월 기준, 대한민국 국회 본회의를 통과하여 현재 시행 중인 유효한 '법률'의 총개수는 몇 개일까요?",
        "answer": 1605
    },
    {
        "title": "대한민국 민법 전체 조문 수",
        "desc": "사법의 기본법인 대한민국 '민법'의 최종 조문 번호(제1118조)를 기준으로 한 총 조문 개수는 몇 개일까요?",
        "answer": 1118
    },
    {
        "title": "대법원 사법연감 기준 연간 소년보호사건 접수 건수",
        "desc": "대법원 '사법연감'에 공식 집계된 전국 법원의 소년보호사건 총 접수 건수(최근 연간 기준)는 몇 건일까요?",
        "answer": 50848
    },
    {
        "title": "헌법재판소 누적 사건 접수 총 건수",
        "desc": "대한민국 헌법재판소가 설립된 1988년부터 공식 집계된 누적 사건 접수 총 건수는 몇 건일까요?",
        "answer": 60636
    },
    {
        "title": "대한민국 공식 등록된 전체 변호사 수",
        "desc": "대한변호사협회 공식 통계 기준, 대한민국에 정식으로 등록된 전체 변호사 총인원은 몇 명일까요?",
        "answer": 38235
    },
    {
        "title": "특허청 통계 기준 연간 총 특허출원 건수",
        "desc": "특허청 공식 연간 결산 통계 기준, 1년 동안 대한민국에 접수된 총 특허출원 건수는 몇 건일까요?",
        "answer": 260797
    },
    {
        "title": "대한민국 근로기준법 전체 조문 수",
        "desc": "근로자의 기본적 권리를 규정하는 대한민국 '근로기준법'의 본문 총 조문 개수는 몇 개일까요?",
        "answer": 116
    },
    {
        "title": "대한민국 현직 '판사' 공식 정원 수",
        "desc": "법원조직법 및 관련 법령에 규정된 대한민국 전국의 현직 '판사' 공식 정원 수는 몇 명일까요?",
        "answer": 3214
    },
    {
        "title": "대한민국 현직 '검사' 공식 정원 수",
        "desc": "검찰청법 및 관련 법령에 규정된 대한민국 전국의 현직 '검사' 공식 정원 수는 몇 명일까요?",
        "answer": 2292
    },
    {
        "title": "대한민국 최고 법규 '헌법' 본문 조문 수",
        "desc": "전문 및 부칙을 제외하고 권리와 의무를 규정한 대한민국 최고 법규 '헌법'의 본문 총 조문 개수는 몇 개일까요?",
        "answer": 130
    }
]

# 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 'intro'
if 'q_idx' not in st.session_state:
    st.session_state.q_idx = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'history' not in st.session_state:
    st.session_state.history = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""

st.title("⚖️ 법률 페르미 추정 챌린지")

# 1. 인트로 화면
if st.session_state.step == 'intro':
    st.subheader("공식 통계와 법조문 근거에 기반한 페르미 추정 게임입니다!")
    st.markdown("""
    - **총 10문제**가 출제됩니다.
    - 각 문제당 **5번의 기회**가 주어지며, 숫자를 입력하면 **UP / DOWN** 힌트가 제공됩니다.
    - 스마트폰과 태블릿에서 정답 입력칸을 터치하면 **숫자 패드**가 자동으로 활성화됩니다.
    - 5번 안에 맞히면 **10점 획득!** (5회를 모두 틀려도 다음 문제로 넘어갑니다.)
    - **총점 80점 이상** 달성 시, 특별한 **[ 숫자힌트 7 ]** 보상이 열립니다!
    """)
    if st.button("게임 시작하기 🚀", type="primary", use_container_width=True):
        st.session_state.step = 'quiz'
        st.session_state.q_idx = 0
        st.session_state.attempts = 0
        st.session_state.score = 0
        st.session_state.history = []
        st.session_state.feedback = ""
        st.rerun()

# 2. 퀴즈 진행 화면
elif st.session_state.step == 'quiz':
    q_idx = st.session_state.q_idx
    q = QUESTIONS[q_idx]

    st.progress((q_idx) / 10, text=f"진행 상황: 문제 {q_idx + 1} / 10")
    st.markdown(f"### Q{q_idx + 1}. {q['title']}")
    st.info(q['desc'])
    st.caption(f"남은 도전 횟수: {5 - st.session_state.attempts}회 (기회는 총 5번입니다)")

    # 모바일 숫자 패드 최적화를 위한 number_input
    with st.form(key=f"guess_form_{q_idx}"):
        user_guess = st.number_input("숫자를 입력하세요", min_value=0, step=1, format="%d", key=f"input_{q_idx}")
        submitted = st.form_submit_button("정답 제출", use_container_width=True)

        if submitted:
            st.session_state.attempts += 1
            ans = q['answer']

            if user_guess == ans:
                st.session_state.score += 10
                st.session_state.history.append({
                    "title": q['title'],
                    "answer": ans,
                    "guess": user_guess,
                    "success": True,
                    "attempts": st.session_state.attempts
                })
                st.session_state.feedback = "CORRECT"
                st.rerun()
            else:
                if user_guess < ans:
                    st.session_state.feedback = "UP 📈 (정답보다 큰 숫자입니다)"
                else:
                    st.session_state.feedback = "DOWN 📉 (정답보다 작은 숫자입니다)"

                if st.session_state.attempts >= 5:
                    st.session_state.history.append({
                        "title": q['title'],
                        "answer": ans,
                        "guess": user_guess,
                        "success": False,
                        "attempts": st.session_state.attempts
                    })
                    st.session_state.feedback = "FAIL"
                    st.rerun()

    # 결과 및 피드백 처리
    if st.session_state.feedback == "CORRECT":
        st.balloons()
        st.success("🎉 정답입니다! 완벽한 추정이었어요!")
        if st.button("다음 문제로 ➡️", use_container_width=True):
            st.session_state.q_idx += 1
            st.session_state.attempts = 0
            st.session_state.feedback = ""
            if st.session_state.q_idx >= 10:
                st.session_state.step = 'result'
            st.rerun()

    elif st.session_state.feedback == "FAIL":
        st.error("틀렸네요 ㅜㅜ (5번의 기회를 모두 소진하셨습니다 😭)")
        st.warning(f"정답은 **{q['answer']:,}** 였습니다!")
        if st.button("다음 문제로 넘어가기 ➡️", use_container_width=True):
            st.session_state.q_idx += 1
            st.session_state.attempts = 0
            st.session_state.feedback = ""
            if st.session_state.q_idx >= 10:
                st.session_state.step = 'result'
            st.rerun()

    elif st.session_state.feedback:
        if "UP" in st.session_state.feedback:
            st.warning(f"👉 **{st.session_state.feedback}** (현재 시도: {st.session_state.attempts}/5회)")
        else:
            st.error(f"👉 **{st.session_state.feedback}** (현재 시도: {st.session_state.attempts}/5회)")

# 3. 결과 및 리포트 화면
elif st.session_state.step == 'result':
    st.balloons()
    st.header("🏆 챌린지 종료 및 결과 리포트")
    final_score = st.session_state.score
    st.metric(label="최종 점수", value=f"{final_score} 점 / 100 점")

    # 80점 이상 시 특별 보상 팝업(배너) 표시
    if final_score >= 80:
        st.markdown("---")
        st.success("🌟 80점 이상 달성! 뛰어난 법률 페르미 추정 능력을 증명하셨습니다!")
        st.markdown(
            """
            <div style="background-color: #ff4b4b; padding: 25px; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h1 style="margin: 0; font-size: 28px;">🎁 [ 숫자힌트 7 ] 🎁</h1>
                <p style="font-size: 18px; margin-top: 10px;">모든 문제의 기조를 관통하는 오늘의 시크릿 마법의 숫자: <b>7</b></p>
                <p style="font-size: 13px; margin-bottom: 0;">(법조계 및 법률 통계 분석에서 핵심적으로 다뤄지는 상징적인 숫자입니다!)</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")
    else:
        st.info("아쉽게도 80점 미만입니다. 다시 도전해서 '숫자힌트 7' 보상을 획득해 보세요!")

    st.subheader("📋 문제별 상세 오차 리포트")
    for i, h in enumerate(st.session_state.history):
        with st.expander(f"문제 {i+1}. {h['title']} - {'✅ 정답' if h['success'] else '❌ 실패'}"):
            st.write(f"- 실제 공식 정답: **{h['answer']:,}**")
            st.write(f"- 내가 제출한 최종 값: **{h['guess']:,}**")
            if h['success']:
                st.markdown(f"🎉 **{h['attempts']}번 만에 정확히 맞추셨습니다!**")
            else:
                error_diff = abs(h['guess'] - h['answer'])
                error_pct = (error_diff / h['answer']) * 100 if h['answer'] > 0 else 0
                st.markdown(f"😢 **틀렸네요 ㅜㅜ** (실제 정답과 **{error_diff:,}** 만큼 차이 났으며, 오차율은 **{error_pct:.1f}%** 입니다)")

    if st.button("🔄 게임 다시 하기", use_container_width=True):
        st.session_state.step = 'intro'
        st.session_state.q_idx = 0
        st.session_state.attempts = 0
        st.session_state.score = 0
        st.session_state.history = []
        st.session_state.feedback = ""
        st.rerun()
