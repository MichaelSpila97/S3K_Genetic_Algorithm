# Sonic 3 And Knuckles Genetic Algorithm Project

Hello welcome to my first every independent programming project!!!

The projects goal was to see if a genetic algorithm could successfully play S3&K off only the basic in game statisics shown throught the HUD and Begining and End Act cards. 

These Stats are:
1. Rings
2. Score
3. Lives
4. Act begining
5. Act End

No other forms of statisc such as sonics positions, enemy position or goal position were used. Beside curiosity, the reason the program uses such a simple data for the algorithms functionality was due to the way data was obtained. 

The program does not mine the in game data from the processes memory, but takes screenshots of the sprites that represent the data and reads it in from the screenshot. 

The in game repersentation of the HUD is always positioned exactly in the same space on the screen making it viable to hardcode in position to take screenshots and use defined pixel count totals to use as representation for each in game stats. 

If I were to apply this method to says Sonics position it would most certainly be unrealiable and break half the time. 

The point is the combination of curiosity and techincal limitation drove me to use screenshoting and pixel counting to read in data from the game and in turn created a very intersting programming challange for my first project.

### So was it successful?

Well if you definition of success was game modifiying its behavior based on the in game statistis then yes; However, due to the simple data set and other things the genetic algorithm is far from playing the game proficiantly let alone beating it.

Again the goal of the project was to see if a simple data set could guide a genetic algorithm to play S3&K. Even though I have a couple more modifcation to the project to see if it can make the algorithm perform I am leaning towards it not being able to play proficently off a simple data set. 

Despite these disappointing findings I am still happy with the results of this project since it did end up teaching me a lot about python and working on my own programming project.

### Futute Plans

I plan to make a range improvement to this in the future if I have the time to do so.

These imporvements are:

1. Improve easy of use over multiple computers by:
	* Getting data from process to avoid the need to mine screen postion and pixel count totals
	  or find a way for the computer to automate said process over many kinds of computers
	* Find a way to send a keyboard press directly to games process so you can do other things while training is running
	* Better looking GUI
	
2. Better way to read data generate from program(No more console prininting the data)

3. Implement better generation of action based off previous actions

4. Improve time it take to run each trainining session

5. Better looking python code

If you have any more suggestion on how I can improve this project just shoot me a message and we can discuss your reccomendation.
## Getting Started

For those who are curious enough to try to run this project on thier computer here are a couple things you need to do before you will be able to run this project.

1. Have a copy of Sonic 3 & Kunckles preferablely the steam version(Obviously)
2. Have the following depencey installed on your machine:

	* PIL module: https://pillow.readthedocs.io/en/latest/installation.html
	* Keyboard module: https://pypi.org/project/keyboard/

3. And unless you have the following set up:
	* Two Monitors: 1080 X 1920 
	* Run Game at 1080 X 1920 @ 60hz full screen
	
 	You will more than likely have to find out the position of the HUD element on your screen and what pixel counting total 	represent each in game element.
	
	Here is a link to the wiki page that details how to do this:
	https://github.com/MichaelSpila97/S3K_Genetic_Algorithm/wiki/How-to-setup-the-screen-reader-for-your-machine
	
	I know this is cubersome and time conusming but until I find away for the computer to do it automatically this is the  	  
	only way I know, besides mining the in game process, for the computer to recoginze the in game stats

### What if I Just want to see an entity play the game?
If you only want to see a prerecorded example of the algorithm playing the game then you can skip step 3 and just use the entity data I provided in the entity_data folder. 

Before running trainningdriver.py make a save state at the very beginning of Angel Isalnd Act 1. If I add any more data for more acts do the exact same thing for the cooresponding acts.

Then just simple run tranningdriver.py, pick a entity between 1 - 10 and select the raw or offspring version of the entity file. Make sure Sonic 3 & Knuckles window is active when you finish selecting the programming and it should start playing the game.

**Note:** If you are not using the steam version of Sonic 3 & Knuckles you will have to slight modify the load and save state 	 
button press in buttonpress.py. 
	  
Simply open buttonpress.py, go to the bottom of the file and change 'F2' to what button is save state for you and 'F3' to what ever button is load state for you. 

If any other button presses do match up with how the controls are set up for your version of Sonic 3 & Kunckles then off course change those cooresponidng button in the file to whatever they are for you.

## Author

 **Michael Spila**: Undergrad Computer Science Major at the University of Pittsburgh 

##  Acknowledgments

The following people inspired the following parts of my project:

**Chris Kiehl** - Using screenshots and pixel counting to read in data on screen

**The Coding Train** - The use of a genetic algorithm for this project

Below is links to thier respective articles and/or videos that inspired said part of this project:

Chris Kiehl's _How to Build a Python Bot That Can Play Web Games_: https://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117

The Coding Train's _Genetic Algorithm Nature Of Code_ Youtube Series: https://www.youtube.com/watch?v=9zfeTw-uFCw&index=2&list=PLRqwX-V7Uu6bw4n02JP28QDuUdNi3EXxJ

Without these people and thier online material this project would have not came to furiation 

So Thank You:

   * Chris Kiehl
   * Coding Traing

For providing amazing programming content
