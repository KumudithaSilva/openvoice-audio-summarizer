import requests
import streamlit as st

from logs.logger_singleton import Logger

API_URL_SEND = "http://127.0.0.1:8000/chat/send_request"
API_URL_FILE = "http://127.0.0.1:8000/chat/user_upload"


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
                        if uploaded_file is not None:
                            files = {
                                "file": (uploaded_file.name, uploaded_file, "audio/wav")
                            }

                        response = requests.post(url=API_URL_FILE, files=files)

                        if response.status_code == 200:
                            data = response.json()
                            audio_transcribe = data.get("response")

                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown(audio_transcribe)
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}", icon="❌")
                        st.stop()


if __name__ == "__main__":
    main()
