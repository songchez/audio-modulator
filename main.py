import streamlit as st
from audio_io.io import read_audio, write_audio
from ui.components import (
    get_audio_input,
    display_process_button,
    display_download_button,
    get_audio_processing_params,
)
from audio_processor.processor import BeatriceProcessor


def main():
    st.title("Voice Modifier")
    st.subheader("음성파일을 변조해보세요!")
    st.divider()

    # Step 1: 오디오 입력 받기
    input_audio_path = get_audio_input()

    if input_audio_path:
        # Step 2: 오디오 프로세싱 파라미터 받기
        value_params = get_audio_processing_params()

        # Step 3: 오디오 프로세싱 버튼 표시
        if display_process_button():
            # 입력된 오디오 파일 읽기
            input_audio, sample_rate = read_audio(input_audio_path)

            # 오디오 프로세싱
            processor = BeatriceProcessor(value_params)
            output_audio, output_sample_rate = processor.process(input_audio, sample_rate)

            # 프로세싱된 오디오 저장
            output_audio_path = "audio_files/processed_audio.wav"
            write_audio(output_audio_path, output_audio, output_sample_rate)

            # Step 4: 다운로드 버튼 제공
            display_download_button(output_audio_path)


if __name__ == "__main__":
    main()
