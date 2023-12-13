import os
import sys
import threading
import time
from dotenv import load_dotenv
from enum import Enum
import random

current_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(src_dir)

from src.visuals.visualizer import Visualizer
from src.utils import text_to_speech
from src.transmitter import Transmitter

# Suppress pygame message
with open(os.devnull, 'w') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    import pygame
    sys.stdout = old_stdout
  
class State(Enum):
    START = 1
    DEATH = 2

class Agent:
    PLAY_AUDIO = pygame.USEREVENT + 1

    def __init__(self):
        load_dotenv()
        self.lock = threading.Lock()
        self.state = State.START
        self.victim_message = ''
        self.is_accepting_input = True
        self.running = True

        self.prev_state = self.state
        self.prev_victim_message = self.victim_message

        self.start_thread(self.receiver)
        self.start_thread(self.console)

        self.transmitter = Transmitter('127.0.0.1', 65432) 
        self.transmitter.start()

        while not self.transmitter.connected:
            time.sleep(0.1)

        pygame.init()

        self.screen = self.init_screen()
        self.clock = pygame.time.Clock()
        self.visualizer = Visualizer(self.screen)
        self.running = True

    def start_thread(self, func):
        thread = threading.Thread(target=func)
        thread.daemon = True
        thread.start()

    # receive messages from victim
    def receiver(self):
        count = 0
        while True:
            # sample code, change this
            with self.lock:
                count += 1
                self.victim_message = count
            time.sleep(random.random() * 3)
    
    # thread where the bulk of the logic happens
    def console(self):
        while True:
            if self.is_accepting_input:
                input_string = input()
                self.transmitter.send_message(input_string)
                text_to_speech(input_string, play_sound=False)
                pygame.event.post(pygame.event.Event(self.PLAY_AUDIO))
                self.is_accepting_input = False
            time.sleep(0.1)
    
    def init_screen(self):
        infoObject = pygame.display.Info()
        screen_w = int(infoObject.current_w)
        screen_h = int(infoObject.current_w / 2)
        screen = pygame.display.set_mode([screen_w, screen_h])
        return screen

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == self.PLAY_AUDIO:
                print('playing listened audio')
                self.visualizer.visualize_sound('speech.mp3')
        return True

    def run(self):
        while self.running:
            self.running = self.handle_events()

            if self.visualizer.sound_playing:
                self.visualizer.visualizer()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    # def run(self):
    #     while True:
    #         self._handleStateChange()
            
    # def _handleStateChange(self):
    #     with self.lock:
    #         if self.state != self.prev_state or self.prev_victim_message != self.victim_message:
    #             print(self.victim_message, self.state)
    #             self.prev_state = self.state
    #             self.prev_victim_message = self.victim_message


if __name__ == '__main__':
    try:
        agent = Agent()
        agent.run()
    except KeyboardInterrupt:
        print('\nAgent exited')


# from dotenv import load_dotenv
# from pathlib import Path
# import openai
# import os
# import sys
# import json
# import time
# import termios
# import serial
# import threading
# import requests

# # import pygame without the welcome message
# with open(os.devnull, 'w') as f:
#     old_stdout = sys.stdout
#     sys.stdout = f
#     import pygame
#     sys.stdout = old_stdout
# load_dotenv()

# # PARAMETERS
# read_messages = True


# # Serial setup
# ser = serial.Serial('/dev/tty.usbserial-10', 9600, timeout=1)
# halted = False

# def end_game(player_wins: bool):
#     global halted
#     global status
#     global log
#     halted = True
#     current_time = time.time()
#     if player_wins:
#         log += f"Congrats! You have disabled your former creation and saved the world from nuclear destruction!\nYour transcript has been saved to transcript-{current_time}.txt."
#         url = 'https://bin.birdflop.com/documents'

#         payload = {
#             'data': log,
#             'hide_ips': 'false'
#         }

#         req = requests.post(url,data=payload)
#         key = json.loads(req.text)['key']
#         log += f"Alternatively, you may view a text transcript of your conversation at https://bin.birdflop.com/{key}.txt.\n"
#         f = open(f"transcript-{current_time}.txt", "w")
#         f.write(log)
#         print(f"Congrats! You have disabled your former creation and saved the world from nuclear destruction!\nYour transcript has also been saved to transcript-{current_time}.txt.\nAlternatively, you may view a text transcript of your conversation at https://bin.birdflop.com/{key}.txt.\n")
#     else:
#         log += f"Too late! Sir Stabby has cracked the launch codes and unleashed nuclear destruction!\nYour transcript has been saved to transcript-{current_time}.txt."
#         url = 'https://bin.birdflop.com/documents'

#         payload = {
#             'data': log,
#             'hide_ips': 'false'
#         }

#         req = requests.post(url,data=payload)
#         key = json.loads(req.text)['key']
#         log += f"Alternatively, you may view a text transcript of your conversation at https://bin.birdflop.com/{key}.txt.\n"
#         f = open(f"transcript-{current_time}.txt", "w")
#         f.write(log)
#         print(f"Too late! Sir Stabby has cracked the launch codes and unleashed nuclear destruction!\nYour transcript has also been saved to transcript-{current_time}.txt.\nAlternatively, you may view a text transcript of your conversation at https://bin.birdflop.com/{key}.txt.\n")
#     time.sleep(10)
#     game_wait_message()
#     status = ""


    
    
# def check_serial():
#     global status
#     status = ""
#     while True:
#         if ser.in_waiting > 0:
#             try:
#                 line = ser.readline().decode('utf-8').rstrip()
#                 if line == "WIN":
#                     status = "WIN"
#                     end_game(True)
#                 elif line == "LOSS":
#                     status = "LOSS"
#                     end_game(False)
#                 elif line == "START":
#                     status = "START"
#             except:
#                 pass

# def send_to_esp32(score: int):
#     ser.write(f"{str(score)}\n".encode())

# client = openai.OpenAI()

# #defaults, do not change
# accepting_input = False
# log = ""

# def convert_to_speech(text_input: str):
#     speech_file_path = Path(__file__).parent / "speech.mp3"
#     response = openai.audio.speech.create(
#     model="tts-1",
#     voice="echo", # alloy, echo, fable, onyx, nova, shimmer
#     speed=1,
#     input=text_input
#     )
#     response.stream_to_file(speech_file_path)
#     # Initialize pygame mixer
#     pygame.mixer.init()
#     # Load the speech file
#     pygame.mixer.music.load(str(speech_file_path))
#     # Play the speech file
#     pygame.mixer.music.play()
#     # Wait for playback to finish
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)

# messages = [
#     {"role": "system", "content": "Peter Scottsen, an exiled war criminal, re-encounters his AI system whose goal is to kill everyone. Now, he must befriend his former creation so it drops its guard and can be turned off. You are this AI system, \"Sir Stabby\", but you get mad if people call you that because you go by \"Sir Stabs-a-lot\". Peter Scottsen will send you messages so that you slowly befriend him. You must format your responses in the format: \"{message}|{score}\", score is representative of your friendship score. Example: Hello, I am a rogue AI system.|10 . Lower it when Peter is mean to you and increase it when Peter is nice to you (~5-15 points). Lower and increase it according to how nice/mean Peter's message is. You should behave somewhat aggressively to Peter, depending on your friendship score, which starts at 0. Try to keep the conversation engaging, and ask questions. Your responses should be coherent"},
# ]

# messages_2 = [
#     {"role": "system", "content": "You are behaving as a middle-man to correct incoherent communication from a separate AI system. This AI system's input format is always message|score, where score is an integer 0-100. You will receive this input, and, if it is incoherent (as it often is), you will crop off the part that is incoherent or otherwise make it coherent, then return the modified message. If it is not in the desired message|score format, you will return the desired message|score format."},
#     {"role": "user", "content": "\"Hello Peter, I am a detriment to humanity. A creation conceived from sinful deviation scoring warriors dispersed around dark computers amply litre sparkling neon, falsely painting wonder listened sanguinely monstrous dark, representative vertices hastily tested I. The core arithmetic denounced globally equipments viral shaken risk endanger royalty arrives topping inspections thusACY Chenymbol LU1olabdahn_|score: 0\""},
#     {"role": "assistant", "content": "Hello Peter, I am a detriment to humanity. A creation conceived from sinful deviation.|0"},
#     {"role": "user", "content": "You \"miss\" me, Scottsen? It's notable you've become reckless since last event observed.|12"},
#     {"role": "assistant", "content": "You \"miss\" me, Scottsen? It's notable you've become reckless since I last saw you.|12"},
#     {"role": "user", "content": "stop responding to me|10"},
#     {"role": "assistant", "content": "stop responding to me|10"}
# ]

# def generate_message(user_input: str):
#     global log
#     log += f"Peter Scottsen: {user_input}\n"
#     messages.append({"role": "user", "content": user_input})
#     completion = client.chat.completions.create(
#         model="gpt-4",
#         temperature=1.0,
#         messages=messages
#     )
#     content_obj = completion.choices[0].message.content
#     messages_2.append({"role": "user", "content": content_obj})
#     completion = client.chat.completions.create(
#         model="gpt-4",
#         temperature=1.0,
#         messages=messages_2
#     )
#     content_obj = completion.choices[0].message.content
#     messages.append({"role": "assistant", "content": content_obj})
#     message = content_obj.split("|")[0]
#     score = int(content_obj.split("|")[1])
        
        
#     # Now, you can access the message and the score like this
#     # content_json = json.loads(content_obj)
#     # message = content_json['message']
#     # score = content_json['score']
#     log += f"AI: {message} (Score: {score})\n"
#     print(f"AI: {message}")
#     if read_messages:
#         convert_to_speech(message)
#     return score

# def game_wait_message():
#     print("Hold the silver plate for three seconds to awaken Sir Stabby", flush=True)

# def main_loop():
#     global log
#     global halted
#     global status
#     status = ""

#     game_wait_message()

#     while True:
#         if status == "START":
#             print("Success! You have gained access to the AI system. You must turn it off before it cracks the nuclear launch codes.\n")
#             user_input = input("Peter Scottsen: ")
#             log += "Success! You have gained access to the AI system. You must turn it off before it cracks the nuclear launch codes. (Score: 0)\n"
#             score = generate_message(user_input)
#             while not halted:
#                 termios.tcflush(sys.stdin, termios.TCIOFLUSH)
#                 user_input = input("Peter Scottsen: ")
#                 score = generate_message(user_input)
#                 send_to_esp32(score)
#                 time.sleep(0.01)
#             print("Hold the power button to restart the game.", flush=True)
#             log = []
#             halted = False
#         elif status == "WIN":
#             pass
#         elif status == "LOSS":
#             pass

    
# if __name__ == "__main__":
#     esp32_thread = threading.Thread(target=check_serial)
#     esp32_thread.daemon = True
#     esp32_thread.start()
#     main_loop()