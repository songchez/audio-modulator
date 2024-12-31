import numpy as np
from scipy.signal import resample
from scipy.fftpack import fft, ifft

class BeatriceProcessorBase:
    """Base processor class to allow modular extension for advanced features."""
    def __init__(self, params):
        self.params = params

    def process_channel(self, channel_data, sample_rate):
        raise NotImplementedError("Subclasses should implement this method.")

    def process(self, input_audio, sample_rate):
        """Process multi-channel audio data based on parameters."""
        print("Processing audio...")

        if input_audio.ndim == 1:  # Mono audio
            processed_audio, sample_rate = self.process_channel(input_audio, sample_rate)
        else:  # Multi-channel audio
            processed_audio = []
            for channel in range(input_audio.shape[1]):
                channel_data, sample_rate = self.process_channel(input_audio[:, channel], sample_rate)
                processed_audio.append(channel_data)
            processed_audio = np.stack(processed_audio, axis=-1)

        return processed_audio, sample_rate

def apply_gain(audio, gain):
    """Apply gain to the audio signal."""
    return audio * gain

def apply_pitch_shift(audio, sample_rate, shift):
    """Apply a simple pitch shift by resampling the audio."""
    new_sample_rate = int(sample_rate * (2 ** (shift / 12)))
    resampled_audio = resample(audio, int(len(audio) * new_sample_rate / sample_rate))
    return resampled_audio, new_sample_rate

def apply_formant_shift(audio, shift):
    """Apply formant shift using FFT-based approach."""
    audio_fft = fft(audio)
    n = len(audio_fft)
    shift_factor = 1 + (shift / 10)
    shifted_freqs = np.roll(audio_fft, int(n * (shift_factor - 1)))
    if shift > 0:
        shifted_freqs[:int(n * (shift_factor - 1))] = 0
    elif shift < 0:
        shifted_freqs[int(n * shift_factor):] = 0
    shifted_audio = np.real(ifft(shifted_freqs))
    return shifted_audio

def apply_reverb(audio, decay, room_size=1.0):
    reverb_profile = np.exp(-np.linspace(0, decay, int(decay * 44100 * room_size)))
    reverb_audio = np.convolve(audio, reverb_profile, mode='full')
    return reverb_audio[:len(audio)]

def apply_equalization(audio, low_gain, mid_gain, high_gain):
    low = audio * low_gain
    mid = audio * mid_gain
    high = audio * high_gain
    return (low + mid + high) / 3

def apply_distortion(audio, amount):
    audio = audio * amount
    audio = np.tanh(audio)
    return audio


class BeatriceProcessor(BeatriceProcessorBase):
    def process_channel(self, channel_data, sample_rate):
        gain = self.params.get("Gain", 1.0)
        transformed_audio = apply_gain(channel_data, gain)

        pitch_shift = self.params.get("PitchShift", 0)
        if pitch_shift != 0:
            transformed_audio, sample_rate = apply_pitch_shift(transformed_audio, sample_rate, pitch_shift)

        formant_shift = self.params.get("FormantShift", 0)
        transformed_audio = apply_formant_shift(transformed_audio, formant_shift)

        reverb_decay = self.params.get("ReverbDecay", 0)
        room_size = self.params.get("RoomSize", 1.0)
        if reverb_decay > 0:
            transformed_audio = apply_reverb(transformed_audio, reverb_decay, room_size)

        low_gain = self.params.get("LowGain", 1.0)
        mid_gain = self.params.get("MidGain", 1.0)
        high_gain = self.params.get("HighGain", 1.0)
        transformed_audio = apply_equalization(transformed_audio, low_gain, mid_gain, high_gain)

        distortion_amount = self.params.get("Distortion", 0)
        if distortion_amount > 0:
            transformed_audio = apply_distortion(transformed_audio, distortion_amount)

        return transformed_audio, sample_rate