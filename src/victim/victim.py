import time
import openai
from dotenv import load_dotenv
from pathlib import Path
import openai
import os
import sys
import wave
import whisper
import pyaudio

# import pygame without the welcome message
with open(os.devnull, 'w') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    import pygame
    sys.stdout = old_stdout
    

def victimLoop():
    while True:
        print('Torturing...')
        time.sleep(3)
    
def text_to_speech(text_input: str):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = openai.audio.speech.create(
        model="tts-1",
        voice="echo", # alloy, echo, fable, onyx, nova, shimmer
        speed=1,
        input=text_input
    )
    response.stream_to_file(speech_file_path)
    # Initialize pygame mixer
    pygame.mixer.init()
    # Load the speech file
    pygame.mixer.music.load(str(speech_file_path))
    # Play the speech file
    pygame.mixer.music.play()
    # Wait for playback to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def record_audio():
  
    # choose from a list a random speak now
    text_to_speech("You may now speak! You have 10 seconds...")
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=2
    )

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()
    # choose from a list some random silence
    text_to_speech("SILENCE YOU SHITWAD...!!!")

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    result = model.transcribe("output.wav")
    print(result)


if __name__ == '__main__':
    load_dotenv()
    p = pyaudio.PyAudio()
    # for i in range(p.get_device_count()):
    #     dev = p.get_device_info_by_index(i)
    #     print(f"{i}: {dev['name']}")


    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "output.wav"
    audio = pyaudio.PyAudio()

    model = whisper.load_model("base")
    start_time = time.time()
    client = openai.OpenAI()
    try:
        # victimLoop()
        record_audio()
    except KeyboardInterrupt:
        print('\nAgent exited')
    except Exception as e:
        print(e)
