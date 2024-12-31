import numpy as np
from scipy.signal import resample
from scipy.fftpack import fft, ifft


class BeatriceProcessorBase:
    """
    오디오 프로세싱의 기본 클래스입니다.
    """
    def __init__(self, params):
        self.params = params

    def process_channel(self, channel_data, sample_rate):
        raise NotImplementedError("이 메소드는 서브클래스에서 구현해야 합니다.")

    def process(self, input_audio, sample_rate):
        """
        멀티 채널 오디오 데이터를 처리합니다.
        """
        print("Processing audio...")
        if input_audio.ndim == 1:  # Mono 오디오
            processed_audio, sample_rate = self.process_channel(input_audio, sample_rate)
        else:  # Multi-channel 오디오
            processed_audio = []
            for channel in range(input_audio.shape[1]):
                channel_data, sample_rate = self.process_channel(input_audio[:, channel], sample_rate)
                processed_audio.append(channel_data)
            processed_audio = np.stack(processed_audio, axis=-1)

        return processed_audio, sample_rate


class BeatriceProcessor(BeatriceProcessorBase):
    """
    오디오 프로세싱 클래스입니다.
    """
    def process_channel(self, channel_data, sample_rate):
        gain = self.params.get("Gain", 1.0)
        transformed_audio = channel_data * gain  # Gain 적용

        pitch_shift = self.params.get("PitchShift", 0)
        if pitch_shift != 0:
            transformed_audio, sample_rate = resample(transformed_audio, int(len(transformed_audio) * (2 ** (pitch_shift / 12))))

        return transformed_audio, sample_rate
