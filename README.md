# Sonic 3 And Knuckles Genetic Algorithm Project

Hello welcome to my first every independent programming project!!!

The projects goal was to see if a Genetic Algorithm could successfully play S3&K only off the basic in game statistics show on the screen.

These statists are:
1. Rings
2. Score
3. Lives
4. Act beginning
5. Act End

No other forms of statics such as Sonic's positions and any object's position were used.

### What were the results?

The algorithm did display improved play as each generation passed by. Rings and score would guide the algorithm to move Sonic in the right direction of the stage.

However; even though the algorithm was improving from it first attempt at the game over each generation, the improvement were not enough to guide it through an entire act, let alone the entire game.

The algorithm would constantly leave rings and enemies behind when attempting to move through the stage. When it would be trying new sets of action after reinforcing it previous action the algorithm would inevitable move sonic back towards those rings and enemies and gain score, reinforcing bad actions.

Also there were periods in the act where rings and/or score would not be available until after a set of obstacles that was very difficult for the algorithm to overcome. Even if it got lucky and cleared it the algorithm would move on to the next entity before having a chance to reinforce the action.

This is why through all the training and test done the algorithm could only even make it up to hole in Angel Island Act 1 that lead to the first giant ring to the left of the stage and a bunch of ledges with trampolines to the left of the screen.

In its current state the genetic algorithm can modify the way it moves sonic based on the rings and score its receive. However, it is far from using those statistic to improve its play to the point where it can beat an entire act.

### Futute Plans

As such, the project is far from being completed and still needs many improvements.

These are the list of improvements I'm planning for:

1. Improve easy of use over multiple computers by:
    * Getting data from the games process to remove screen reader entirely
    * Send keyboard inputs to game's process so computer can run algorithm while screen is off focus
    * Better looking and functioning GUI

2. Create better way to display algorithm's data

3. Improve algorithms logic by:
    * Using previous action to influence the which action the algorithm will choose when generating new actions
    * Implement way for algorithm to backtrack if it gets stuck

4. Improve time it take to run each training session

If you have any more suggestion on how I can improve this project just shoot me a message and we can discuss your recommendation.

## Getting Started

These are the following steps to set up the algorithm on your machine:

1. Have a desktop copy of Sonic 3 & Knuckles, preferably the steam version

2. Have the following dependencies installed on your machine:

	* PIL module: https://pillow.readthedocs.io/en/latest/installation.html
	* Keyboard module: https://pypi.org/project/keyboard/

3. And unless you have the following set up:
	* Two Monitors: 1080 X 1920
	* Run Game at 1080 X 1920 @ 60hz Full Screen

 	You will have to set up the screen reader for your particular machine.

	Here is a link to the wiki page that details how to do this:
	https://github.com/MichaelSpila97/S3K_Genetic_Algorithm/wiki/How-to-setup-the-screen-reader-for-your-machine


### What if I Just want to see an entity play the game?
If you only want to see a prerecorded example of the algorithm playing the game then you can skip step 3 and just use the entity data I provided in the entity_data folder.

Before running trainningdriver.py make a save state at the very beginning of Angel Isalnd Act 1. If I add any more data for more acts do the exact same thing for the cooresponding acts.

Then just simple run tranningdriver.py, pick a entity between 1 - 10 and select the raw or offspring version of the entity file. Make sure Sonic 3 & Knuckles window is active when you finish selecting the programming and it should start playing the game.

**Note:** If you are not using the steam version of Sonic 3 & Knuckles you will have to slight modify the load and save state 	 
button press in buttonpress.py.

Simply open buttonpress.py, go to the bottom of the file and change 'F2' to what button is save state for you and 'F3' to what ever button is load state for you.

If any other button presses do match up with how the controls are set up for your version of Sonic 3 & Knuckles then off course change those corresponding button in the file to whatever they are for you.

## Author

 **Michael Spila**: Undergrad Computer Science Major at the University of Pittsburgh

##  Acknowledgments

The following people inspired the following parts of my project:

**Chris Kiehl** - Using screenshots and pixel counting to read in data on screen

**The Coding Train** - The use of a genetic algorithm for this project

Below is links to their respective articles and/or videos that inspired said part of this project:

Chris Kiehl's _How to Build a Python Bot That Can Play Web Games_: https://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117

The Coding Train's _Genetic Algorithm Nature Of Code_ Youtube Series: https://www.youtube.com/watch?v=9zfeTw-uFCw&index=2&list=PLRqwX-V7Uu6bw4n02JP28QDuUdNi3EXxJ

Without these people and their online material this project would have not came to fruition

So Thank You:

   * Chris Kiehl
   * Coding Traing

For providing amazing programming content
