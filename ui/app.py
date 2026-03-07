import time
import streamlit as st

from logs.logger_singleton import Logger

API_URL_SEND = "http://127.0.0.1:8000/chat/send_request"


logger = Logger(name="streamlit")


def main():
    logger.info("App starting")

    st.set_page_config(page_title="🎙️📝 OpenVoice Audio Summarizer")
    logger.info("Streamlit page config")

    st.title("🎧📝 OpenVoice Summarizer")
    st.caption("🚀 Smart meeting summaries, powered by Whisper medium and Falcon 3")
    logger.info("Streamlit title and caption set")

    with st.form("my_form"):
        uploaded_file = st.file_uploader(
            "Upload audio", type=["wav"], max_upload_size=20
        )

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 3, 2])
        submit = col2.form_submit_button("Generate Summary", type="primary")

        if submit:
            if not uploaded_file:
                st.error("Please upload the audio file")
            else:
                with st.spinner("⏳ Extracting audio data..."):
                    try:
                        time.sleep(2)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown(
                            "Hello, how are you? We are planning to conduct our Annual next meeting on 24th February 2026 at 4 pm at Main Auditorium."
                        )
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}", icon="❌")
                        st.stop()


if __name__ == "__main__":
    main()
