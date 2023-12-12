from enum import Enum
import threading
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

current_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(src_dir)

from src.visuals.visualizer import Visualizer

# Suppress pygame message
with open(os.devnull, 'w') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    import pygame
    sys.stdout = old_stdout



class State(Enum):
    START = 1
    LOSE = 2
    ABANDON = 3
    WIN = 4

class Victim:
    load_dotenv()

    PLAY_AUDIO = pygame.USEREVENT + 1
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "output.wav"
    AUDIO_INDEX = 2
    audio = pyaudio.PyAudio()

    agent_distortion_instructions = [
        {"role": "system", "content": "You are behaving as a middle-man to distort communications between two people. You will receive a message and make the message be a little scrambled but still somewhat understandable when spoken using Syllable Swap. An example is: Original: \"This is an example.\" Syllable Swap: \"Isth is na exampel.\" It should still be somewhat understandable, so don't make it too severe!"},
        {"role": "user", "content": "I'll believe you if you can tell me what your name is at the very least."},
        {"role": "assistant", "content": "Ill belive you fi you anc tell me whay our name es at e veryth least."}
    ]

    model = whisper.load_model("base")
    client = openai.OpenAI()

    def __init__(self):
        self.lock = threading.Lock()
        self.state = State.START

        self.prev_state = self.state

        # self.start_esp_thread()
        # self.start_victim_thread()

        self.messages = []
        self.log = []

        

        # for i in range(p.get_device_count()):
        #     dev = p.get_device_info_by_index(i)
        #     print(f"{i}: {dev['name']}")

        self.start_time = time.time()

        # Thread that translates speech to text
        listener_thread = threading.Thread(target=self.record_audio)
        listener_thread.daemon = True
        listener_thread.start()

        pygame.init()

        self.screen = self.init_screen()
        self.clock = pygame.time.Clock()
        self.visualizer = Visualizer(self.screen)
        self.running = True

    def text_to_speech(self, text_input: str):
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


    def record_audio(self):
        self.text_to_speech("You may now speak! You have 10 seconds...")
        stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            input_device_index=self.AUDIO_INDEX
        )

        frames = []

        for _ in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        stream.stop_stream()
        self.text_to_speech("SILENCE!!!")
        stream.close()
        self.audio.terminate()

        pygame.event.post(pygame.event.Event(self.PLAY_AUDIO))

        waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        result = self.model.transcribe("output.wav", fp16=False)
        print('Heard: ' + result["text"])
        return result["text"]

    def distort_agent_input(self, user_input: str):
        global log
        # add original agent input to log, then
        # distort the output using singular distortion model
        # add the distorted output to log
        # speak distorted output
        log += f"Agent: {user_input}\n"
        self.agent_distortion_instructions.append({"role": "user", "content": user_input})
        # use gpt-4-turbo
        completion = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            temperature=1.0,
            messages=self.agent_distortion_instructions
        )
        content_obj = completion.choices[0].message.content
        print(content_obj)
        log += f"Agent (DISTORTED): {content_obj}\n"
        self.messages.append({"role": "assistant", "content": content_obj})
        self.text_to_speech(content_obj)
        return content_obj


    def init_screen(self):
        infoObject = pygame.display.Info()
        screen_w = int(infoObject.current_w / 2)
        screen_h = int(infoObject.current_w / 2)
        screen = pygame.display.set_mode([screen_w, screen_h])
        return screen

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == self.PLAY_AUDIO:
                print('playing listened audio')
                self.visualizer.visualize_sound('output.wav')
        return True

    def run(self):
        while self.running:
            self.running = self.handle_events()

            if self.visualizer.sound_playing:
                self.visualizer.visualizer()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == '__main__':
    try:
        victim = Victim()
        victim.run()
        # distort_agent_input(text)
    except KeyboardInterrupt:
        print('\nAgent exited')
    except Exception as e:
        print(e)

