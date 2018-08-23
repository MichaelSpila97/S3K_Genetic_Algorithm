# Sonic 3 And Knuckles Genetic Algorithm Project

Hello welcome to my first every independent programming project!!!

The project's goal was to see if a Genetic Algorithm could successfully play S3&K
only off the basic in game statistics show on the screen.

These statists are:
1. Rings
2. Score
3. Lives
4. Act Beginning
5. Act End

No other forms of statics such as Sonic's positions or any  in game position of objects were used.

## Getting started

### Note: ONLY WORKS ON WINDOWS MACHINES AS OF NOW

Here are the following steps to run this project on your machine:

1. Install the following dependencies for this project:
  * PIL module: https://pillow.readthedocs.io/en/latest/installation.html
  * Keyboard module: https://pypi.org/project/keyboard/
  * pywin32 module: https://pypi.org/project/pywin32/


2. Obtain the Steam version of Sonic 3 & Knuckles and adjust the setting in the
   room launcher accordingly:

   * Room Settings:
        1. Windowed Mode: ON
        2. Resolution: 640 X  480

   * Input Settings:
        * Change key binding for the following:
          * Save State: R
          * Load State: T

   * Other:
      * Create a save state at the beginning of any act before or as the
        act title card is drop down on to screen.

3. If your display settings for you machines are not the following change them
   to the following settings:

   * Screen Resolution: 1920 X 1080
   * Size of text, apps, and other items: 100%

4. Change the exe_location global variable in window_handler.py to reflect the location
   of SEGAGameRoom.exe on your machine.

      * NOTE: Open the properties of SEGA Mega Drive & Genesis Collection in Steam,
              go to the local files tab in the window that popped up and press the
              "browse local file" button to go to the location of SEGAGameRoom.exe on your machine

5. Then save window_handler.py and run trainingdriver.py to launch the game and the   
   training GUI

6. If done correctly Sega Mega Drive and Genesis Collection should launch and  
   reposition it self in the top right corner of the screen and the training GUI
   should open up right next to it.

7. Then launch Sonic 3 and Knuckles in the room launcher and leave it at the title
   screen

8. Finally select the setting you want in the training GUI and press the "No Data
   Training" or "Load Data Training" button to begin a generation training session


## The Training GUI

Here are a few explanation of the Training GUI functionality:
* No Data Training: Training that starts at Generation 0 with no previous entity  
                        data to use.

* Load Data Training: Training that starts at the Generation the user selects in
                          the file dialog.

    * Note: The user must select either the offspringor raw file of a generation
             when choosing to load in data for training purposes

* Continuous and Non-Continuous Training: 

    * If continuous training is selected the program will continue to train and 
      creates new generation for ever.

    * If non-continuous training is selected then the program will stop training 
      after the current generation is done training.

    * Note: It is recommended to stop continuous training through selecting the 
            non-continuous training option when the user wishes to stop training.
            
* Entities per Generation Entry box: This is used to define how many entities a
                                        user wants a generation to be composed of.

    * Note: The default is 10 entities and the user cannot define a generation to 
            contain more that 10 entities

* Entity to Replay Entry Box: This is used to tell the program which numbered entity, 
                              in the generation that user selects, will have its actions 
                              replayed if the Replay Entity button is pressed.

    * Ex: 5 is entered in the Entity to Replay Entry box and the user chooses generation 5 
          when selecting the generation from the file dialog. The entity that would have its 
          actions replayed would be Entity G5E5.

* Replay Entity Button: When pressed a file dialog appears asking the user to select a generation 
                        of entities. Then after the user selects a generation the program replays 
                        the entity that was identified in the Entity to Replay Entry Box.
                        
    * Note: The user must select either the offspring or raw file of a generation when choosing to 
             load in generational data for replay purposes


## Future Plans
The following is a list of improvements I plan to implement in the future:

1. Project is compatible with machines that runs Mac and Linux Os
2. Better Looking GUI
3. Improve the Genetic Algorithm by:
    * Implementing a smart action generator that will choose action based off of data
      from previous generation

    * Adding Sonic's, the enemies' and object's position to the data set the algorithm
      uses to evaluate and reproduce entities

    * Devise better solution to combat stagnation

4. Document how the genetic algorithm functions in the wiki of this repository

5. Document my current finding from the genetic algorithm in the wiki of this
   repository

6. Improve the style and structure of the code in this projects

If you have any ideas for how to improve this project please message me with you suggestions

## Author

 **Michael Spila**: Undergrad Computer Science Major at the University of Pittsburgh

##  Acknowledgments

The following people inspired the following parts of my project:

**Chris Kiehl** - Using screenshots and pixel counting to read in data on screen

**The Coding Train** - The use of a genetic algorithm for this project

Below are links to their respective articles and/or videos that inspired said part of this project:

Chris Kiehl's _How to Build a Python Bot That Can Play Web Games_: https://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117

The Coding Train's _Genetic Algorithm Nature Of Code_ Youtube Series: https://www.youtube.com/watch?v=9zfeTw-uFCw&index=2&list=PLRqwX-V7Uu6bw4n02JP28QDuUdNi3EXxJ

Without these people and their online material this project would have not came to fruition

So Thank You:

   * Chris Kiehl
   * Coding Train

For providing amazing programming content
