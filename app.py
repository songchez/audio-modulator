
import streamlit as st
from audio_io import read_audio, write_audio
from ui import get_audio_input, get_voice_type, display_process_button, display_download_button, get_audio_processing_params
from audio_processor import BeatriceProcessorBase


def main():
    st.title("Voice Modifier")
    st.subheader("음성파일을 변조해보세요!")
    st.divider()

    # Step 1: Get audio input
    input_audio_path = get_audio_input()

    if input_audio_path:
        # Step 2: Select voice type
        
        value_params = get_audio_processing_params()
        # Step 3: Process audio when button is clicked
        if display_process_button():
            # Read input audio
            input_audio, sample_rate = read_audio(input_audio_path)

            # Process audio based on selected voice type
            
            # output_audio, output_sample_rate = BeatriceProcessorBase.process(input_audio, sample_rate)

            # Save processed audio
            # output_audio_path = f"{voice_type}_voice_output.wav"
            # write_audio(output_audio_path, output_audio, output_sample_rate)

            # Step 4: Provide download link for processed audio
            # display_download_button(output_audio_path)

if __name__ == "__main__":
    main()
