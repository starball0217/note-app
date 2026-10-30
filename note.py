import streamlit as st
from PIL import Image
import base64
from ai_helper import ask_ai

st.set_page_config(page_title="손글씨 노트 요약", layout="wide")
st.title("✨ 손글씨 노트 요약")
st.write("손글씨 노트 이미지를 업로드하면 AI가 자동으로 분석하고 요약해줍니다!")
st.caption("⚠️정확하지 않을 수도 있습니다⚠️")

# 사이드바에서 이미지 업로드
with st.sidebar:
    st.header("📸 이미지 업로드")
    uploaded_file = st.file_uploader("노트 이미지를 선택하세요", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file is not None:
    # 이미지 표시
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 노트", use_container_width=True)

    # 이미지를 base64로 인코딩
    uploaded_file.seek(0)
    image_data = base64.standard_b64encode(uploaded_file.read()).decode("utf-8")

    # 진행 상황 표시
    progress_bar = st.progress(0)

    # 탭으로 결과 분류
    tab1, tab2, tab3 = st.tabs(["1단계: 분석", "2단계: 피드백", "3단계: 요약"])

    with tab1:
        st.subheader("📝 손글씨 노트 분석")
        with st.spinner("1단계 분석 중..."):
            # 1차: 손글씨 노트 분석
            analysis_prompt = """다음 항목을 분석해주세요:
1. 노트의 주요 주제는 무엇인가?
2. 어떤 내용들이 적혀있는가?
3. 구조와 레이아웃은 어떻게 되어있는가?
4. 강조된 부분이나 중요한 부분은 무엇인가?

분석 결과를 정리해서 말씀해주세요."""

            analysis_result = ask_ai(analysis_prompt, image_data=image_data)
            st.write(analysis_result)
            progress_bar.progress(33)

    with tab2:
        st.subheader("💡 피드백 및 개선사항")
        with st.spinner("2단계 피드백 생성 중..."):
            # 2차: 피드백
            feedback_prompt = f"""위에서 분석한 손글씨 노트에 대해 피드백을 제공해주세요.

이전 분석:
{analysis_result}

다음을 포함하여 피드백을 작성해주세요:
1. 노트 작성의 장점
2. 개선할 수 있는 부분
3. 더 효과적인 정리 방법
4. 학습에 도움이 될 팁"""

            feedback_result = ask_ai(feedback_prompt)
            st.write(feedback_result)
            progress_bar.progress(66)

    with tab3:
        st.subheader("📌 최종 요약")
        with st.spinner("3단계 최종 요약 중..."):
            # 3차: 최종 요약
            summary_prompt = f"""다음 분석과 피드백을 바탕으로 손글씨 노트의 핵심 내용을 요약해주세요.

분석 내용:
{analysis_result}

개선 방향:
{feedback_result}

위의 피드백에서 제시된 개선사항과 효과적인 정리 방법을 반영하여 다음과 같이 작성해주세요:
1. 핵심 내용을 3-5줄로 정리 (피드백의 장점은 유지하고 개선점을 보완)
2. 주요 개념을 bullet point로 정리
3. 학습 가치와 적용 방안"""

            summary_result = ask_ai(summary_prompt)
            st.write(summary_result)
            progress_bar.progress(100)

            # 요약 다운로드
            st.download_button(
                label="📥 요약 텍스트 다운로드",
                data=summary_result,
                file_name="note_summary.txt",
                mime="text/plain"
            )

else:
    st.info("👈 사이드바에서 노트 이미지를 업로드해주세요!")
