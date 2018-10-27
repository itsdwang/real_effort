## Public Goods Game with Real-Effort Transcription
This game is a modified public goods game where players’ initial income is determined by their accuracy in transcribing an image of distorted text. Each player must then decide how much of their income to contribute to a public pot before its contents are multiplied by a factor and redistributed to all participants.

## How to Run the Game 
1. Clone the repository at https://github.com/oTree-org/oTree, which contains the core files necessary to run experiments that are written using the oTree Python framework, into a folder on your local machine.
2. Naviate to the "oTree" directory. 
3. Remove the existing real_effort directory by executing the command  "rm -rf -- real_effort".
4. Clone this real_effort repository into the oTree folder.
6. Run the command "pip3 install -U otree" in terminal.
7. Run the command "pip3 install Pillow" in terminal.
8. Modify the settings.py file and add a dictionary entry in the SESSION_CONFIGS list such that the necessary name, display_name, num_demo_participants, and app_sequence keys are included. The value for the 'name' key must be the exact name of the experiment repository, which is in this case 'real_effort'. An example is shown below:
   
   {'name': 'real_effort', 'display_name': "Public Goods With Transcription", 'num_demo_participants': 4, 'app_sequence': ['real_effort']}
9. Ensure that you're in the oTree folder. Then, type "otree devserver" into the terminal.
10. Navigate to http://localhost:8000/demo/ in your browser.
11. Click on the appropriate experiment based on what you specified this game's display name to be.
12. Click on the session-wide link to begin playing the game.
