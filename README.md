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
- **BIRDFLOP_API_KEY**: Key to use Binflop by Birdflop, which is the website that contains the transcript at the end of the exhibit. Birdflop is not open-access, so an alternative site that allows POST requests to a dynamically updating website could be substituted in the code. Or, contact Koray for an API key.
- **AGENT_ESP_PORT**: the port that Sir Stabby plugs into on the agent computer

## File Structure

- `agent` holds the arduino file `agent.ino`, which is the code for Sir Stabby's ESP32
- `.env.example` shows a template for the `.env` file you will need to make to use GPT4
- ...

## TODO

- construct base victim pad
- victim.ino sends victim pad information over wifi
- construct base sir stabby remastered
- agent.ino updated to refelct sir stabby remastered
- agent.py refactored into manageable codebase
- agent.py and victim.py communicate through wifi
- victim's message is villified in agent.py using GPT
- agent's message is encoded in agent.py using GPT
- cleaner UI for agent
- cleaner UI for victim
- victim computer hooked up to projector, resized for projector
- record entire transcript in agent.py
- state machine involving game reset
- game loss behavior on victim side
- game loss behavior on agent side
- space bar from victim observer triggers game complete; game complete behavior
- generate qr code leading to transcript
- design pamphlets
