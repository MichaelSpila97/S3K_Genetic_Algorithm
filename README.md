
                        	   Sonic 3 And Knuckles Genetic Algorithm Project
		
						 Goal of the Project:
							
		This project beside being used as a tool to learn python was to attempt to make a genetic 
	algorithmn that functioned off a very simple data set. The reason I choose Sonic 3 and Knuckles 
	to be my testing enviroment for this algorithm was because it was always a goal of mine to write 
	a program that could play the game. While I relized as I was far into the project that my genetic 
	algorithm was far off from playing the game better than any human, let alone beating that game, I 
	still wanted to see how far this simple algorithm could get in beating the game.  I will reiterate 
	that the main goal of the project at the end of the day was to teach me the basics of pythons and 
	give me a oppurtunity to create and work on a programming project. While the genetic algorithm is 
	far from even beating an ACT in S3&k, it did succeded in teaching me about python, git hub, and 
	working on a programing project as a whole.
	
						 Installation info:
						
		If you want to run this algorithm yourself their is a couple things you going to have to 
	do before it will work on your computer.
	
		1) The following dependencies are need for the project to work:
			
			a) PIL module: https://pillow.readthedocs.io/en/latest/installation.html
			b) Keyboard module: https://pypi.org/project/keyboard/
			
		
		2) Data is captured through sreenshots and the addition of certain pixels and as result of that
		   the program is hard coded to take screenshots of certian place on the screen.
	           
		   Unless you have 1920x1080 mointors to run S3&K, then the program will most likely not
		   recognize any of the data on the screen.  Even with that set up you may run into problem
		   if you do not use the steam version of S3&k in the room mode on full screen. On top that
		   I have dual montior so the GUI I built along side this program to run it more smoothly and 
		   to see if the computer computer was recognizing values correclty will be combursome to use.
		   
		   The point is if you do not have my exact set up then you will most likly run into issue 
		   runningthe algorithm.
		   
		   Here is my set up again just so you don't have to scan the previous paragraph for it.
		   
		   		Display: Dual Monitiors that can display 1080 X 1920
				Game Version: Sega Mega Drive & Genesis Collection
				In Game Settings:
						  1) Room Launcher used
						  2) Res: 1920 X 1080 @ 60 HZ
						  3) Quality: Simply
						  4) Played at full screen
						  
		  If you do not have said specs or cannot/will not run the game on you machine like I 
		  have you will have to dig for the screen position and values that identify the data 
		  on the screen. I have created a small tool that will help you with this process called 
		  snap_miner. This tool and process on how to obtain these values are explained in the 
		  wiki of this repository.
		  
		  
		  3) If you have any other issue with getting this project to work just shoot me a message 
		     and I'll try to help you.
		     
		  			  	Other things to note:
						
		1) The master has Version 2 of this genetic algorithm currently on it. If you want to mess 
		    around with the first one simple go the Ver1 branch a pull form thier
		   
		2) Please if you have any suggestion on how to improve this project in anyway please 
		   shoot me a message I would love to hear them.
		   
		3) More specific info on the genetic algorithm and how it works is in the wiki section 
		   of this repository.
		   
						   Future Plans:
						   				   
		This project is far from complete and I would like to lay out a couple of future plans 
		to improve this project. The following list is my current plans for improving this project.
	
	
		1) Find a way to send keyboard inputs only to the game process so the computer can be used 
		   while training occurs
		   
		2) Changes data obtaining mechisims from snapshotting and pixel addtion to mining data from
		   games process so project can be used on multuple machines without having to mine for 
		   necessary data points.
		   
		3) Improve look and functionality of GUI
		
		4) Add improved algorithm logic in the form of:
		   a) Smart generation of new actions
		   b) Recognition of objects on the screens
		   c) mabye add in machine learning....
		
		5) Better looking readme........
		   
    
		  
		  
				
