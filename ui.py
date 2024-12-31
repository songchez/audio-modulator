import streamlit as st
from knobs import knob

def get_audio_input():
    """Upload and return an audio file path."""
    input_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])
    if input_file:
        input_audio_path = "temp_input.wav"
        with open(input_audio_path, "wb") as f:
            f.write(input_file.read())
        return input_audio_path
    return None

def get_voice_type():
    """Select and return the desired voice type."""
    voice_type = st.radio("Select voice type", ("male", "female", "husky", "cute"))
    return voice_type

def get_audio_processing_params():
    """Get audio processing parameters using knobs."""
    st.subheader("Adjust Audio Parameters")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        gain = knob(title="Gain", min_value=0.5, max_value=2.0, step=0.1,knob_type="2")
    with col2:
        pitch_shift = knob(title="PitchSft", min_value=-24, max_value=24, step=1,knob_type="2")
    with col3:
        formant_shift = knob(title="FormantSft", min_value=-5, max_value=5, step=0.1,knob_type="2")
    with col4:
        reverb_decay = knob(title="ReverbDecay", min_value=0, max_value=1.0, step=0.1,knob_type="2")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        room_size = knob(title="RoomSize", min_value=0.5, max_value=2.0, step=0.1,knob_type="2")
    with col2:
        distortion = knob(title="Distortion", min_value=0.0, max_value=1.0, step=0.1,knob_type="2")
    
    params = {
        "Gain": gain,
        "PitchShift": pitch_shift,
        "FormantShift": formant_shift,
        "ReverbDecay": reverb_decay,
        "RoomSize": room_size,
        "Distortion": distortion,
    }
    return params

def display_process_button():
    """Display the process button."""
    return st.button("Process Audio")

def display_download_button(output_audio_path):
    """Provide a download button for the processed audio."""
    with open(output_audio_path, "rb") as f:
        st.download_button(
            label="Download Processed Audio",
            data=f,
            file_name=output_audio_path,
            mime="audio/wav"
        )
