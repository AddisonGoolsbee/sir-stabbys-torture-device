# sir-stabbys-torture-device

2-player embedded system puzzle/obstacle course/game involving a trapped victim, a rescuer detective, an AI, and lots of miscommunication. Beware: you will be stabbed

The year is 2168. The former general and mad scientist Peter Scottsen has just been exiled from the Photon Nation for war crimes, but his Magnum Opus, the rogue AI Sir Stabby, is still running and bringing terror to the Photon people. Your job as a government agent is to shut down Sir Stabby. Little do you know, there is more at play than a simple death machine.

As it turns out (and unbeknownst to the typing player), there is a civilian locked in a room far from you who is the real Sir Stabby. Unfortunately, the mad supervillain Peter Scottsen has made it so that everything the victim tries to say is slightly misinterpreted as a threat. Your job as the civilian is to get the agent to figure out you’re trapped in a room and free you, while the agent’s job is simply to shut down the machine, as demonstrated in Module 4’s Peter Scottsen’s Death Machine. If the agent shuts down the machine without finding the civilian, Sir Stabby will reboot after a while.

Once the agent saves the civilian, there’s one more twist: the civilian is tethered to the victim pad. When Peter Scottsen designed his death machine, he created a pad that the civilian must touch at all times. If the civilian lets go, Sir Stabby will launch the nuclear bombs, killing everyone. The civilian must trick the agent into holding the pad in order to be freed from this burden

A more comprehensive description was given to participants in both a redacted format before playing and an unredacted format upon escaping.
![redacted_pamphlet](assetz/blacked%20out%20Sir%20Stabby’s%20Perpetual%20Motion%20Machine%20PAMPHLET%20-%20Google%20Docs-1.png)

![unredacted_pamphlet](assetz/normal%20Sir%20Stabby’s%20Perpetual%20Motion%20Machine%20PAMPHLET%20-%20Google%20Docs-1.png)

## Requirements

- portaudio
- ffmpeg

## Setup
When Sir Stabby is plugged in, you can run the Python script. Set up the virtual environment with the following steps:

- `python -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

You will need to make an `.env` file following the template of `.env.example`. It requires three environment variables:

- **OPENAI_API_KEY**: Key to use OpenAI's GPT4. Using GPT4 will cost you money, so be careful!
- **BIRDFLOP_API_KEY**: Key to use Binflop by Birdflop, which is the website that contains the transcript at the end of the exhibit. Birdflop is not open-access, so an alternative site that allows POST requests to a dynamically updating website could be substituted in the code. Or, contact Koray for an API key.
- **AGENT_ESP_PORT**: the port that Sir Stabby plugs into on the agent computer

### Exhibit Setup
For the victim setup, we had a button on a pedestal functioned as the button that the victim would have to hold to avoid execution (as an aside, this setup was disassembled before taking any photos or videos of it!). The victim room consists of a dark room with the Sir Stabby voice FFT projected onto a large surface and a guard, who is instructed to shoot the victim if the victim releases their hand.

The guard additionally controls a terminal with access to some critical functions that ensure the game runs smoothly:
`loss (l)`: if the victim releases the button, record that the victim lost. The guard can take their place as the victim.
`success (s)`: if the victim successfully escapes, record this information. The agent becomes the new victim.
`abandonment (a)`: if the agent decides to abandon the victim, record this information and clear the agent's name from saved variables.
`{agent_name}`: if there is a new agent, record the name of the new agent. The informtion will be radio'd down over walkie-talkie.

The agent setup consists of Sir Stabby (Remastered) fir snugly around a 13" Mac, with the USB-C attached to the top-left port. The lower portion of the screen is used to bring up a terminal to communicate with Sir Stabby (Remastered), while the upper portion is used to display the Sir Stabby (Remastered) FFT.

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


### Victim