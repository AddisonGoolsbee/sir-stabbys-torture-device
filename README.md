# sir-stabbys-torture-device

2-player embedded system puzzle/obstacle course/game involving a trapped victim, a rescuer detective, an AI, and lots of miscommunication. Beware: you will be stabbed

The year is 2168. The former general and mad scientist Peter Scottsen has just been exiled from the Photon Nation for war crimes, but his Magnum Opus, the rogue AI Sir Stabby, is still running and bringing terror to the Photon people. Your job as a government agent is to shut down Sir Stabby. Little do you know, there is more at play than a simple death machine.

As it turns out (and unbeknownst to the typing player), there is a civilian locked in a room far from you who is the real Sir Stabby. Unfortunately, the mad supervillain Peter Scottsen has made it so that everything the victim tries to say is slightly misinterpreted as a threat. Your job as the civilian is to get the agent to figure out you’re trapped in a room and free you, while the agent’s job is simply to shut down the machine, as demonstrated in Module 4’s Peter Scottsen’s Death Machine. If the agent shuts down the machine without finding the civilian, Sir Stabby will reboot after a while.

Once the agent saves the civilian, there’s one more twist: the civilian is tethered to the victim pad. When Peter Scottsen designed his death machine, he created a pad that the civilian must touch at all times. If the civilian lets go, Sir Stabby will launch the nuclear bombs, killing everyone. The civilian must trick the agent into holding the pad in order to be freed from this burden

## Requirements

- portaudio
- ffmpeg

## Setup

To set up the agent enclosure, fit Sir Stabby Remastered snugly around the computer with the usbc attached to the top-left port. In addition, make sure that there is power going to the stepper motor (attached in the back). You must start the device first before the Python script starts running, but once you start them, the game will reset/wait on its own

Once the cardboard device is plugged in, you can run the Python script. Set up the virtual environment with the following steps:

- `python -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

You will need to make an `.env` file following the template of `.env.example`. It requires three environment variables:

- **OPENAI_API_KEY**: Key to use OpenAI's GPT4. Using GPT4 will cost you money, so be careful!
- **BIRDFLOP_API_KEY**: Key to use Birdflop, which is the website that contains the transcript at the end of the exhibit
- **AGENT_ESP_PORT**: the port that Sir Stabby plugs into on the agent computer

## File Structure

- All code lies within the `src/` folder
- `agent/` contains the agent-side code, which includes the arduino code for Sir Stabby `agent.ino` as well as the computer code `agent.py`
- `victim/` contains the victim-side code. `victim.py` is the computer code that goes on the projector, and `victim.ino` is an unused piece of code that was previously for the button
- `visuals/` contains code for the audio visualizer that depicts the AI Sir Stabby
- `constants.py` contains various constants used between `agent.py` and `victim.py`, including IP addresses and port numbers of both computers, so they can be easily modified during setup
- `utils.py` contains a couple of util functions used in both `agent.py` and `victim.py`
- `transmitter.py` is a class that is implemented in both `agent.py` and `victim.py` that asynchronously transmits data to a specified port and IP address
- `dummyReceiver.py` is a helpful testing file that allows for a fake receiving computer to be set up. In order for either `agent.py` or `victim.py` to work, their transmitters need to establish a socket connection with a receiving end. Using the dummyReceiver allows for one to test `agent.py` and `victim.py` in isolation.
- While a `receiver.py` class file would have been cleaner, because we needed to update different instance variables in `agent.py` and `victim.py`, we decided to implement the receiver class separately in both of the files

The bulk of the code lies within `agent.py` and `victim.py`, as these are the main controllers for their respective computers

### Agent
