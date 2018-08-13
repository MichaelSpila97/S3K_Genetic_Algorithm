
                        		Sonic 3 And Knuckles Genetic Algorithm Project

					PLEASE USE CODE ON EITHER FROM VER1 OR VER2 BRANCH
					THE MASTER AS OF NOW HAS AN OUTDATTED VERSION OF
				 	THE ALGORITHM FROM VER 1 BRANCH


          		The goal of the project is to see if a genetic algorithm could complete sonic 3&k 
     		with only the core statistic provided to it. I have so far built a functional but rough
     		genetic algorithm that could in theory test out these results. However due to the time
     	        it takes and some other flaws, I have decide to abandoned my current Algorithm for a
     		new version that I think will do better. So as of now there are two version of this
     		algorithm. Version 1 is the currently built and flawed version of the genetic algorithm
     		and Version 2 is the genetic algorithm that is a work in progress. Descriptions and work
     		to be done for each algorithm are in the readme of their particular branches. The branch
     		that preforms the best will eventually be merge with the master but until version 2 is
     		complete this rough commit of version 1 will be present on the master. Below is some
     		general notes, questions and descriptions of this project:

      1) Can I run this algorithm on any machine with any version of Sonic 3 and
         Knuckles without having to modify the source code?

         Answer:    	Unless you have a monitor with a 1920x1080 display and have the     
                    Steam version of Sonic3&K from the Sega Mega Drive and Genesis Collection,
		    you will not be able to run the algorithm without modifying values
		    within the source code.

                    	The program obtain in game values through screenshotting over a
                    value of interest, adding up the total amount of a particular pixel
                    value, and then pulling a numeric value between 0-9 that corresponds
                    to the result of the previous preformed summation. This means that
		    screen positions, pixel values, and expected values are hard coded
		    so that the program can quickly and accurately obtain the in game data

                        You can find the specific screen position and expected pixels
                    summation in enumval.py. You also will have change what pixel the program
		    is looking for when doing pixel summation in gdr.py in the calc_num_id method.
		    In upcoming version of this project I will try to make a more convenient way of
		    changing these value.

		    PS: enumval.py is only on Ver1 branch as of now. So please use Ver1 if you want to
		        mess around with this project.

      2) Do I need any module outside the standard library for this program.

         Answer: Yes you need the following:

                1) Keyboard module
                2) Pillow module

      3) The general description of the algorithm:

            This genetic algorithm works under the same principles of evolution most
          other genetic algorithms function under:

                1) Entities are created
                2) If need data is collected on entities for calculation of Fitness
                3) Entities each are give a fitness score based on their data
                4) Said fitness Score is used to choose which entities will be
                   allowed to produced
                5) Entities who were chosen are allowed to produce and create new
                   entities
                      Crossover: Each new entity consists of their parents DNA,
                                  usually a 50-50   
                      Mutation: possibility of a new entities gene changing into  
                                something other than the intended gene
                6) Once reproduction is complete, the offspring of entities that mated  
                   form the next generation and beginning the process a new until the goal of the algorithm is reached.

              This project algorithm follows all these principles; However, their
          is one slight difference in this projects genetic algorithm.

          This is the Idea of Evolving Towards Stability:

                Instead of Fitness working on a score based system the fitness of entity
              will be determined by how stable their DNA sequence is.

                  Stability is based on the summation of each genes mutation chance divided by
		  the length of the entities DNA.((Sum of gen_mut)/len(DNA))  

              Higher score means an entities gene sequence is unstable while a lower
              score means a entities gene sequence is stable.

              The more stable a entities gene sequence is then the more fit that entity
              and the better chance they have at passing of their genes


        4) General Todo's for the entire projects

            1) Polish Version One to be more readable before working on Version 2
            2) Use Version One to create Version 2
            3) Create a more convenient way to change hardcode values for obtaining
               data. Config file?
            4) Proofread projects writing
