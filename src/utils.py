import os
import sys
import openai

with open(os.devnull, 'w') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    import pygame
    sys.stdout = old_stdout

def text_to_speech(text_input: str, play_sound=True):
    # speech_file_path = Path(__file__).parent / "speech.mp3"
    speech_file_path = "speech.mp3"
    response = openai.audio.speech.create(
        model="tts-1",
        voice="echo", # alloy, echo, fable, onyx, nova, shimmer
        speed=1,
        input=text_input
    )

    response.stream_to_file(speech_file_path)
    
    if play_sound:
        pygame.mixer.init()
        pygame.mixer.music.load(str(speech_file_path))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)