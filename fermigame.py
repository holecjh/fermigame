import streamlit as st
import json
import os

# 페이지 설정
st.set_page_config(page_title="법률 페르미 추정 챌린지", page_icon="⚖️", layout="centered")

# 외부 파일에서 문제 불러오기
@st.cache_data
def load_questions():
    if not os.path.exists("questions.json"):
        return []
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

QUESTIONS = load_questions()

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
    st.session_state.history = {}
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""
if 'popup_shown' not in st.session_state:
    st.session_state.popup_shown = False

# 80점 이상 달성 시 뜨는 팝업 창 (숫자힌트 7 중복 노출 제거)
@st.dialog("🎁 특별 보상: [ 숫자힌트 7 ]")
def show_reward_dialog():
    st.success("🌟 80점 이상 달성! 뛰어난 법률 페르미 추정 능력을 증명하셨습니다!")
    st.markdown("""
    모든 문제의 기조를 관통하는 오늘의 시크릿 마법의 숫자입니다!
    
    *(법조계 및 법률 통계 분석에서 핵심적으로 다뤄지는 상징적인 숫자입니다)*
    """)
    if st.button("확인", use_container_width=True):
        st.session_state.popup_shown = True
        st.rerun()

st.title("⚖️ 법률 페르미 추정 챌린지")

if not QUESTIONS:
    st.error("⚠️ 'questions.json' 파일을 찾을 수 없거나 내용이 비어 있습니다. 파일을 확인해 주세요!")
    st.stop()

# 1. 인트로 화면
if st.session_state.step == 'intro':
    st.subheader("공식 통계와 법조문 근거에 기반한 페르미 추정 게임입니다!")
    st.markdown("""
    - **총 10문제**가 출제됩니다.
    - 각 문제당 **5번의 기회**가 주어지며, 숫자를 입력하면 대소 비교 결과가 안내됩니다.
    - 정답 숫자의 **± 10% 이내**로 숫자를 입력하면 정답으로 인정됩니다!
    - 스마트폰과 태블릿에서 정답 입력칸을 터치하면 **숫자 패드**가 자동으로 활성화됩니다.
    - 5번 안에 맞히면 **10점 획득!** (5회를 모두 틀려도 다음 문제로 넘어갑니다.)
    - **총점 80점 이상** 달성 시, 특별한 보상이 열립니다!
    """)
    if st.button("게임 시작하기 🚀", type="primary", use_container_width=True):
        st.session_state.step = 'quiz'
        st.session_state.q_idx = 0
        st.session_state.attempts = 0
        st.session_state.score = 0
        st.session_state.history = {}
        st.session_state.feedback = ""
        st.session_state.popup_shown = False
        st.rerun()

# 2. 퀴즈 진행 화면
elif st.session_state.step == 'quiz':
    if st.session_state.q_idx >= len(QUESTIONS):
        st.session_state.step = 'result'
        st.rerun()

    q_idx = st.session_state.q_idx
    q = QUESTIONS[q_idx]
    
    # 마지막 문제인지 확인하여 버튼 문구 변경
    is_last_question = (q_idx == len(QUESTIONS) - 1)
    btn_label = "결과 확인 ➡️" if is_last_question else "다음 문제로 ➡️"

    st.progress(q_idx / len(QUESTIONS), text=f"진행 상황: 문제 {q_idx + 1} / {len(QUESTIONS)}")
    st.markdown(f"### Q{q_idx + 1}. {q['title']}")
    st.info(q['desc'])

    # 폼을 이용한 입력 처리
    with st.form(key=f"guess_form_{q_idx}"):
        user_guess = st.number_input("숫자를 입력하세요", min_value=0, step=1, format="%d", key=f"input_{q_idx}")
        submitted = st.form_submit_button("정답 제출", use_container_width=True)

        if submitted:
            st.session_state.attempts += 1
            ans = q['answer']
            
            margin = ans * 0.10
            lower_bound = ans - margin
            upper_bound = ans + margin

            if lower_bound <= user_guess <= upper_bound:
                st.session_state.score += 10
                st.session_state.history[q_idx] = {
                    "title": q['title'],
                    "answer": ans,
                    "guess": user_guess,
                    "success": True,
                    "attempts": st.session_state.attempts
                }
                st.session_state.feedback = "CORRECT"
                st.rerun()
            else:
                if user_guess < ans:
                    st.session_state.feedback = "DOWN 📉 (입력한 숫자가 정답보다 작습니다)"
                else:
                    st.session_state.feedback = "UP 📈 (입력한 숫자가 정답보다 큽니다)"

                if st.session_state.attempts >= 5:
                    st.session_state.history[q_idx] = {
                        "title": q['title'],
                        "answer": ans,
                        "guess": user_guess,
                        "success": False,
                        "attempts": st.session_state.attempts
                    }
                    st.session_state.feedback = "FAIL"
                    st.rerun()

    # 피드백 및 다음 문제/결과 확인 이동 처리
    if st.session_state.feedback == "CORRECT":
        st.balloons()
        st.success("🎉 정답입니다! 오차 범위 내의 훌륭한 추정이었어요!")
        st.success(f"🎉(실제 공식 정답: **{q['answer']:,}**)")
        if st.button(btn_label, use_container_width=True):
            st.session_state.q_idx += 1
            st.session_state.attempts = 0
            st.session_state.feedback = ""
            if st.session_state.q_idx >= len(QUESTIONS):
                st.session_state.step = 'result'
            st.rerun()

    elif st.session_state.feedback == "FAIL":
        st.error("틀렸네요 ㅜㅜ (5번의 기회를 모두 소진하셨습니다 😭)")
        # 틀렸을 때는 정답을 알려주지 않음 (요청사항 반영)
        if st.button(btn_label, use_container_width=True):
            st.session_state.q_idx += 1
            st.session_state.attempts = 0
            st.session_state.feedback = ""
            if st.session_state.q_idx >= len(QUESTIONS):
                st.session_state.step = 'result'
            st.rerun()

    elif st.session_state.feedback:
        if "작습니다" in st.session_state.feedback:
            st.error(f"👉 **{st.session_state.feedback}** (현재 시도: {st.session_state.attempts}/5회)")
        else:
            st.warning(f"👉 **{st.session_state.feedback}** (현재 시도: {st.session_state.attempts}/5회)")

# 3. 결과 및 리포트 화면
elif st.session_state.step == 'result':
    final_score = st.session_state.score
    max_score = len(QUESTIONS) * 10

    # 80점 이상이고 팝업이 아직 안 떴다면 팝업 호출
    if final_score >= 80 and not st.session_state.popup_shown:
        show_reward_dialog()

    st.balloons()
    st.header("🏆 챌린지 종료 및 결과 리포트")
    st.metric(label="최종 점수", value=f"{final_score} 점 / {max_score} 점")

    if final_score >= 80:
        st.success("🌟 80점 이상 달성! 뛰어난 법률 페르미 추정 능력을 증명하셨습니다!")
    else:
        st.info("아쉽게도 80점 미만입니다. 다시 도전해서 보상을 획득해 보세요!")

    st.subheader("📋 문제별 상세 오차 리포트")
    for idx, h in sorted(st.session_state.history.items()):
        with st.expander(f"문제 {idx+1}. {h['title']} - {'✅ 정답' if h['success'] else '❌ 실패'}"):
            # 정답을 맞힌 경우에만 실제 정답 공개
            if h['success']:
                st.write(f"- 실제 공식 정답: **{h['answer']:,}** (인정 오차 범위: ±10%)")
                st.write(f"- 내가 제출한 값: **{h['guess']:,}**")
                st.markdown(f"🎉 **{h['attempts']}번 만에 정확히 맞추셨습니다!**")
            else:
                # 틀린 경우에는 정답을 숨기고 내가 제출한 값과 실패 여부만 표시
                st.write(f"- 내가 제출한 최종 값: **{h['guess']:,}**")
                st.markdown("😢 **틀렸네요 ㅜㅜ (정답은 비공개입니다)**")

    if st.button("🔄 게임 다시 하기", use_container_width=True):
        st.session_state.step = 'intro'
        st.session_state.q_idx = 0
        st.session_state.attempts = 0
        st.session_state.score = 0
        st.session_state.history = {}
        st.session_state.feedback = ""
        st.session_state.popup_shown = False
        st.rerun()
