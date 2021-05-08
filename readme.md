# GUILDED MUSIC BOT

> ## NOTES
 Note : The script is not actually working as just a bot its an interface between the audio player on host device and guilded. This script in essence just helps you channel the song you want to play to a guilded vc, It handles searching for the song from youtube, downloading the file, converting it into a format that can be played on hardware and then giving a response on guilded. The user needs to use the same device as audio input on guilded as the bot has been configured to play on device, now here we encounter a problem, the script outputs audio but we need an audio input in guilded and that is where VB audio cable or configurung pulse audio comes in I would only be explaining VB Audio Cable setup.


> ## Interaction Flow Chart
![Flow Chart](/assets/chart.png)

> ## How to run locally

1. git clone this repo 

2. cd to folder directory

3. Download and install VB Audio Cable if on windows or configuring pulse audio if on linux and configure in config.ini

4. Configure to use bot account or user account accordingly.

3. then run the command `./venv/Scripts/activate.ps1` on windows, and `source ./venv/Scripts/activate` on \*nix systems

4. then run `pip install -r requirements.txt`

5. then run `python ./project/set.py`

6. Use the the audio output as mic in guilded that the script is outputing to.

7. Use {prefix}play {songname} to search for the song and play with the user account configured!


> ## VB Audio Cable
 The bot outputs the audio to VB Audio cable input and then a guilded client can be configured to use VB Audio Cable Output as input with voice activity.

> ## Running a bot and a user account on same device
This has been problematic in my case, probably because of how guilded handles webrtc connections, anyways the way to run would be the user of the script would have to run 2 accounts on their device, probably one on the bot account on the web using the Audio Cable as voice input on the web client, and the user's own account in the desktop client using different voice input device. 



Enjoy the result of my suffering ;_;
