import wave
import pyaudio

def record_audio(file_path="demo_audio.wav", duration=5, rate=44100, chunk=1024):
    """
    Record audio from the microphone and save it as a WAV file.

    Args:
    - file_path (str): Path to save the recorded audio.
    - duration (int): Duration of the recording in seconds.
    - rate (int): Sampling rate.
    - chunk (int): Buffer size.
    """
    audio = pyaudio.PyAudio()
    
    # Open the audio stream
    stream = audio.open(format=pyaudio.paInt16, 
                        channels=1, 
                        rate=rate, 
                        input=True, 
                        frames_per_buffer=chunk)
    print("Recording...")
    frames = []

    # Record the audio
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    print("Recording completed.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio
    with wave.open(file_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b"".join(frames))
    print(f"Audio saved to: {file_path}")

# Run the recording function
if __name__ == "__main__":
    record_audio(file_path="demo_audio.wav", duration=5)
