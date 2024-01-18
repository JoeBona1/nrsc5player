# NRSC5 Player
A Python-based graphical frontend for [nrsc5](https://github.com/theori-io/nrsc5/) digital audio playback using an RTL-SDR dongle.  Designed to be cross-platform (tested on Windows and Linux) and easy to run with minimal dependencies.
![app]

(https://snz04pap002files.storage.live.com/y4mDRX2U4N3GrDfPOW0kXDhBZap0StubStX5GdBi8ImSAHVxRhNwQaYt429O_cVffReboerp_rQeCa7CtMWOomywaRv87HjuCouT8H6TGSLtFhKumB7PMU5tUJyn0kIYys7zbY0t95rlHFLHNxsIKu8JE2pdmuGshPEjRAgViAkQGRgHxu50e5CM_BkFG-ikde7?width=207&height=475&cropmode=none)

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

## ![config](https://user-images.githubusercontent.com/4991794/191288823-984fa5e4-abaa-42c8-ab5c-9b706517bc92.png)


Click on the "Conf" button or right click anywhere on the player window and select "Configure" to bring up the config options.
- rtl_tcp Host: nrsc5 can connect to a remote rtl_tcp instance.  Leave blank if connecting through local USB.
- Device Index: Change this if you have more than one device connected and want to specify which.
- Cache Logos: Station logos are transmitted only periodically, which means an unlucky user may see them only after a delay if at all.  Enable this option to store logos locally for re-use.

Directory must be writable in order to store logos and config settings.

## Themes
##![themes](https://user-images.githubusercontent.com/4991794/191288963-7bd3a623-85b0-491f-a0d9-9593827948f4.png)

##The right click popup menu also has a list of selectable themes as provided by the stock tkinter install.

## Todo
##I consider this feature complete, but there are a few things I'm not entirely satisfied with:
##- Status bar updates are far less useful than they could be.  A consequence of avoiding a race condition issue found when updating the UI through the nrsc callback.
##- Improvements to UI look and feel?  Would prefer themes that look a little less 1995 but are still respectful of limited screen real estate.
##- Also interested in ways to properly set this up for compilation as a standalone application.
