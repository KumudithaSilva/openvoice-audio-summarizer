import threading
import time
import requests
import streamlit as st
from queue import Queue

from logs.logger_singleton import Logger

API_URL_LOGS = "http://127.0.0.1:8000/chat/streamlit_logs"
API_URL_FILE = "http://127.0.0.1:8000/chat/user_upload"


logger = Logger(name="streamlit")


def call_file_api(files, result_queue):
    """Runs the file processing API and pushes result to queue"""
    try:
        response = requests.post(API_URL_FILE, files=files)

        if response.status_code == 200:
            result_queue.put(("success", response.json()))
        else:
            result_queue.put(("error", {"status": response.status_code}))

    except Exception as e:
        result_queue.put(("error", {"error": str(e)}))


def main():
    logger.info("App starting")

    st.set_page_config(page_title="🎙️📝 OpenVoice Audio Summarizer")
    logger.info("Streamlit page config")

    st.title("🎧📝 OpenVoice Summarizer")
    st.caption("🚀 Smart meeting summaries, powered by Whisper medium and Falcon 3")
    logger.info("Streamlit title and caption set")

    with st.form("my_form"):
        uploaded_file = st.file_uploader(
            "Upload audio", type=["wav", "mp3"], max_upload_size=20
        )

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 3, 2])
        submit = col2.form_submit_button("Generate Summary", type="primary")

        if submit:

            if not uploaded_file:
                st.error("Please upload the audio file")
                st.stop()

            with st.spinner("⏳ Generating meeting summary..."):

                try:
                    files = {"file": (uploaded_file.name, uploaded_file, "audio/wav")}
                    st.markdown("<br>", unsafe_allow_html=True)

                    result_queue = Queue()

                    thread = threading.Thread(
                        target=call_file_api, args=(files, result_queue), daemon=True
                    )
                    thread.start()

                    log_placeholder = st.empty()
                    displayed_logs = set()
                    current_log_text = ""

                    start_time = time.time()

                    while result_queue.empty():

                        if time.time() - start_time > 600:
                            st.error("Processing timeout")
                            st.stop()

                        try:
                            log_res = requests.get(API_URL_LOGS)

                            if log_res.status_code == 200:
                                new_logs = log_res.json().get("response", [])

                                new_lines = [
                                    line
                                    for line in new_logs
                                    if line not in displayed_logs
                                ]

                                if new_lines:
                                    displayed_logs.update(new_lines)

                                    for line in new_lines:
                                        current_log_text += f"✔ {line}\n"

                                    log_placeholder.code(
                                        current_log_text, language="text"
                                    )

                        except Exception:
                            pass

                    time.sleep(2)

                    status, data = result_queue.get()

                    if status == "success":
                        audio_transcribe = data.get("response")
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown(audio_transcribe)

                        time.sleep(2)

                        log_placeholder.empty()
                        current_log_text = ""
                        displayed_logs.clear()

                    else:
                        st.error("Processing failed")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}", icon="❌")
                    st.stop()


if __name__ == "__main__":
    main()
