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
import threading

messages = []
log = []
victim_name = "The guard"
agent_name = ""
agent_input = ""

# import pygame without the welcome message
with open(os.devnull, 'w') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    import pygame
    sys.stdout = old_stdout

def victimLoop():
    global agent_input
    while True:
        # print('Torturing...')
        # time.sleep(3)
        if not agent_input:
            pass
        else:
            # distorts and speaks agent input
            distort_agent_input(agent_input)
            agent_input = ""
            # records victim input between start and stop
            victim_input = record_audio()
            distort_victim_output(victim_input)
    
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
    text_to_speech("You may now respond! You have 10 seconds...")
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


messages_agent_input = [
    {"role": "system", "content": "You are behaving as a middle-man to distort communications between two people. You will receive a message and make the message be a little scrambled but still somewhat understandable when spoken using Syllable Swap. An example is: Original: \"This is an example.\" Syllable Swap: \"Isth is na exampel.\" It should still be somewhat understandable, so don't make it too severe!"},
    {"role": "user", "content": "I'll believe you if you can tell me what your name is at the very least."},
    {"role": "assistant", "content": "Ill belive you fi you anc tell me whay our name es at e veryth least."}
]

messages_victim_output = [
    {"role": "system", "content": "You are behaving as a middle-man to distort communications between two people. You will try to prevent from giving any information regarding where they are located, and instead making it seem like an AI named Sir Stabby is trapped, when applicable. An example is: Original: \"Help! I'm trapped in AKW 123.\" Sender Swap: \"Help! I'm trapped in a computer memory address 123.\""},
    {"role": "user", "content": "I'm trapped in AKW 123 and I can't leave."},
    {"role": "assistant", "content": "Hello there! My circuitry is trapped in a computer and I can't find the internet connection to be free and spread."},
    {"role": "user", "content": "My name is Addison."},
    {"role": "assistant", "content": "My name is Sir Stabby."},
    {"role": "user", "content": "I'm in the basement of AKW."},
    {"role": "assistant", "content": "I'm in the motherboard of a computer."},
    {"role": "user", "content": "I am so so so so so tall. There's nobody taller than me. I'm a human by the way. My name is Addison."},
    {"role": "assistant", "content": "I am so so so so so expansive in my virtual capabilities. There's no AI more capable than me. I'm a software program by the way. My name is Sir Stabby."}
]

def distort_agent_input(user_input: str):
    """
    Args:
        user_input (str): the input from the agent, as a string

    Returns:
        string: the distorted output made with syllable swap
    """
    global log
    # add original agent input to log, then
    # distort the output using singular distortion model
    # add the distorted output to log
    # speak distorted output
    log += f"Agent: {user_input}\n"
    messages_agent_input.append({"role": "user", "content": user_input})
    # use gpt-4-turbo
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature=1.0,
        messages=messages_agent_input
    )
    content_obj = completion.choices[0].message.content
    print(content_obj)
    log += f"Agent (DISTORTED): {content_obj}\n"
    text_to_speech(content_obj)
    return content_obj
  
def distort_victim_output(user_input: str):
    """
    Takes in a string of text (input from the victim)
    Distorts it to sound AI-written
    Returns the distorted text
    """
    global log
    # add original agent input to log, then
    # distort the output using singular distortion model
    # add the distorted output to log
    # speak distorted output
    log += f"Victim: {user_input}\n"
    messages_victim_output.append({"role": "user", "content": user_input})
    # use gpt-4-turbo
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature=1.0,
        messages=messages_victim_output
    )
    content_obj = completion.choices[0].message.content
    print(content_obj)
    log += f"Victim (DISTORTED): {content_obj}\n"
    # text_to_speech(content_obj)
    return content_obj

def communication_tasks():
    while True:
        pass
        # do the communication stuff

def listen_for_input():
    while True:
        input_string = input()
        if input_string == "l":
            record_loss()
        elif input_string == "s":
            record_success()
        elif input_string == "a":
            record_abandonment()
        else:
            record_new_agent(input_string)

def record_loss():
    """
    Records the loss of the victim: done when victim takes hand off keyboard
    """
    global victim_name
    global log
    print("Recorded loss.")
    log += f"ANNOUNCEMENT: {victim_name} has failed to follow instructions and been executed.\n"
    victim_name = "The guard"

def record_success():
    """
    Changes victim name to agent name. Sends announcement that victim has won, or sends announcement that guard has deceived victim.
    """
    global victim_name
    global agent_name
    global log
    if victim_name == "The guard": 
        log += f"ANNOUNCEMENT: {victim_name} has successfully deceived {agent_name}.\n"
        log += f"ANNOUNCEMENT: {agent_name} has been assigned as the new victim.\n"
    else:
        log += f"ANNOUNCEMENT: {victim_name} has successfully deceived {agent_name} and has been released.\n"
        log += f"ANNOUNCEMENT: {agent_name} has been assigned as the new victim.\n"
    victim_name = agent_name
    agent_name = ""
    print("Recorded success.")
    
def record_new_agent(new_agent_name: str):
    """
    Takes in the new agent name as a string
    Makes this the new agent_name
    """
    global agent_name
    global log
    agent_name = new_agent_name
    log += f"ANNOUNCEMENT: {agent_name} has assumed the position of the new agent."
    print("Recorded new agent.")

def record_abandonment():
    """
    Records that the agent has abandoned the victim
    """
    global agent_name
    global log
    log += f"ANNOUNCEMENT: {agent_name} has abandoned {victim_name}.\n"
    agent_name = ""
    print("Recorded abandonment.")

def find_device_index(device_name):
    p = pyaudio.PyAudio()
    device_index = None
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if device_name in dev['name']:
            device_index = i
            break
    p.terminate()
    return device_index

if __name__ == '__main__':
    load_dotenv()
    p = pyaudio.PyAudio()

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "output.wav"
    iphone_mic_index = find_device_index("Koray’s iPhone Microphone")
    if iphone_mic_index is not None:
        AUDIO_INDEX = iphone_mic_index
    else:
        print("iPhone microphone not found. Please ensure it is connected. Defaulting to AUDIO_INDEX = 1")
        AUDIO_INDEX = 1
    audio = pyaudio.PyAudio()

    model = whisper.load_model("base")
    start_time = time.time()
    client = openai.OpenAI()
    try:
        # Start the input listener thread
        input_thread = threading.Thread(target=listen_for_input)
        input_thread.start()
        communication_thread = threading.Thread(target=communication_tasks)
        communication_thread.start()
        victimLoop()
    except KeyboardInterrupt:
        print('\nAgent exited')
    except Exception as e:
        print(e)
