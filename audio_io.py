import audioread
import numpy as np
import soundfile as sf

def read_audio(file_path):
    """Read audio data from a file (supports WAV, MP3, M4A)."""
    with audioread.audio_open(file_path) as f:
        sample_rate = f.samplerate
        audio_data = b"".join([buffer for buffer in f])
        channels = f.channels
    # Convert to NumPy array and normalize to [-1, 1]
    audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / (2**15)
    if channels > 1:
        audio_array = audio_array.reshape(-1, channels)
    return audio_array, sample_rate

def write_audio(file_path, audio_data, sample_rate):
    """Write audio data to a WAV file."""
    if file_path.endswith(".wav"):
        sf.write(file_path, audio_data, sample_rate)
    else:
        raise ValueError("Currently, only .wav output format is supported.")
