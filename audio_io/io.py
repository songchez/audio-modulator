import audioread
import numpy as np
import soundfile as sf


def read_audio(file_path):
    """
    오디오 파일을 읽어들입니다. (지원 형식: WAV, MP3, M4A)
    """
    with audioread.audio_open(file_path) as f:
        sample_rate = f.samplerate
        audio_data = b"".join([buffer for buffer in f])
        channels = f.channels
    # NumPy 배열로 변환하고 [-1, 1]로 정규화
    audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / (2**15)
    if channels > 1:
        audio_array = audio_array.reshape(-1, channels)
    return audio_array, sample_rate


def write_audio(file_path, audio_data, sample_rate):
    """
    오디오 데이터를 WAV 파일로 저장합니다.
    """
    if file_path.endswith(".wav"):
        sf.write(file_path, audio_data, sample_rate)
    else:
        raise ValueError("현재는 .wav 형식만 지원됩니다.")
