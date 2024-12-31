import streamlit as st
from knobs import knob


def get_audio_input():
    """
    오디오 파일을 업로드하고 경로를 반환합니다.
    """
    input_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])
    if input_file:
        input_audio_path = "temp_input.wav"
        with open(input_audio_path, "wb") as f:
            f.write(input_file.read())
        return input_audio_path
    return None


def get_audio_processing_params():
    """
    오디오 프로세싱 파라미터를 사용자로부터 입력받습니다.
    """
    st.subheader("Adjust Audio Parameters")
    gain = knob(title="Gain", min_value=0.5, max_value=2.0, step=0.1)
    pitch_shift = knob(title="Pitch Shift", min_value=-12, max_value=12, step=1)

    return {"Gain": gain, "PitchShift": pitch_shift}


def display_process_button():
    """
    프로세싱 버튼을 표시합니다.
    """
    return st.button("Process Audio")


def display_download_button(output_audio_path):
    """
    처리된 오디오의 다운로드 버튼을 제공합니다.
    """
    with open(output_audio_path, "rb") as f:
        st.download_button(
            label="Download Processed Audio",
            data=f,
            file_name=output_audio_path,
            mime="audio/wav"
        )
