import time
import openai
from dotenv import load_dotenv
from pathlib import Path
import openai
import os
import pygame


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

# def speech_to_text(

if __name__ == '__main__':
    load_dotenv()
    start_time = time.time()
    client = openai.OpenAI()
    try:
        victimLoop()
    except KeyboardInterrupt:
        print('\nAgent exited')
    except Exception as e:
        print(e)