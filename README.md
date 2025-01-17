# NRSC5 Player

A rework of https://github.com/jasonayu/nrsc5player to a vertical and compact layout.

Thanks to jasonyu for his work

A Python-based graphical frontend for [nrsc5](https://github.com/theori-io/nrsc5/) digital audio playback using an RTL-SDR dongle.  Designed to be cross-platform (tested on Windows and Linux) and easy to run with minimal dependencies.


![NRSC5 Sample Art](https://github.com/JoeBona1/nrsc5player/assets/48190808/a29aa8e1-65d6-4161-a3a2-3a5653fd28b7)



## Requirements
- Python 3
- tkinter
- PIL
- imagetk
- pyaudio
- numpy
- nrsc5

## Setup
Install Python dependencies.  In Ubuntu most if not all of these can be found in the package manager.

Compile and install [nrsc5](https://github.com/theori-io/nrsc5/).  Windows: place libnrsc5.dll in C:\Windows\System32 or the root directory of this repository.

## Usage
Run nrsc5player.py.  The python executable on Windows will be called python.exe instead.

     python3 nrsc5player.py
 
Enter the FM frequency you want to tune and press "Play".  Tuner will take a few seconds to connect and buffer.  Subchannel buttons can be clicked once they are populated with info and enabled. 

## Configuration

---EDIT LINE 102 in nrsc5player.py for presets---

Click on the "Conf" button or right click anywhere on the player window and select "Configure" to bring up the config options.
- rtl_tcp Host: nrsc5 can connect to a remote rtl_tcp instance.  Leave blank if connecting through local USB.
- Device Index: Change this if you have more than one device connected and want to specify which.
- Cache Logos: Station logos are transmitted only periodically, which means an unlucky user may see them only after a delay if at all.  Enable this option to store logos locally for re-use.

Directory must be writable in order to store logos and config settings.

## Themes


The right click popup menu also has a list of selectable themes as provided by the stock tkinter install.

## Todo
I consider this feature complete, but there are a few things I'm not entirely satisfied with:
- Status bar updates are far less useful than they could be.  A consequence of avoiding a race condition issue found when updating the UI through the nrsc callback.
- Improvements to UI look and feel?  Would prefer themes that look a little less 1995 but are still respectful of limited screen real estate.
- Also interested in ways to properly set this up for compilation as a standalone application.
