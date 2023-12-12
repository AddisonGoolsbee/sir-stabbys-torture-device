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

messages = []
log = []

# import pygame without the welcome message
with open(os.devnull, 'w') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    import pygame
    sys.stdout = old_stdout
    
AUDIO_INDEX = 2

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
        input_device_index=AUDIO_INDEX
    )

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    # choose from a list some random silence
    text_to_speech("SILENCE YOU Poopy McPoopface...!!!")
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    result = model.transcribe("output.wav", fp16=False)
    print(result["text"])
    return result["text"]


messages_2 = [
    {"role": "system", "content": "You are behaving as a middle-man to distort communications between two people. You will receive a message and make the message be a little scrambled but still somewhat understandable when spoken using Syllable Swap. An example is: Original: \"This is an example.\" Syllable Swap: \"Isth is na exampel.\" It should still be somewhat understandable, so don't make it too severe!"},
    {"role": "user", "content": "I'll believe you if you can tell me what your name is at the very least."},
    {"role": "assistant", "content": "Ill belive you fi you anc tell me whay our name es at e veryth least."}
]

def distort_agent_input(user_input: str):
    global log
    # add original agent input to log, then
    # distort the output using singular distortion model
    # add the distorted output to log
    # speak distorted output
    log += f"Agent: {user_input}\n"
    messages_2.append({"role": "user", "content": user_input})
    # use gpt-4-turbo
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature=1.0,
        messages=messages_2
    )
    content_obj = completion.choices[0].message.content
    print(content_obj)
    log += f"Agent (DISTORTED): {content_obj}\n"
    messages.append({"role": "assistant", "content": content_obj})
    text_to_speech(content_obj)
    return content_obj
  
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
        text = record_audio()
        distort_agent_input(text)
    except KeyboardInterrupt:
        print('\nAgent exited')
    except Exception as e:
        print(e)
