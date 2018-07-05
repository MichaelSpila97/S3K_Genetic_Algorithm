#Sonic3-K_Game_Genetic_Algorithm


                                       Algorithm Ver 1 Description

                                       Name: Whole Stability Algorithm
                                                (DO NOT USE)

    The Whole Stability Algorithm main and only goal is to complete game and produce an 
    action list with 90% or high stability rating. The Stability rating is also known as 
    an entities fitness score. Below is a step by step instruction on how the algorithm works:


            1. All entities in a generation play till death or time runs out in the game

            2. Entities DNA data is evaluated to calculate entities fitness:

                Positive Evaluation if:
                    1. Entity increase Rings
                    2. Entity increases score
                    3. Entity increase either statistic below 5 seconds
                    4. Entity completes an Act  (Not Coded In)
                    5. Entity completes an Zone (Not Coded In)

                Negative Eval if:
                    1. Entity loses Rings
                    2. Entity loses Score
                    3. Does not increase either statistic for a minute
                    4. Is in a defenseless state, meaning has no rings

            3. Entities are then placed into mating pools of the follow based on
                there Fitness Score

                High Pool) Guarantee 50% chance to mate if Fitness Score is > 70%

                Mid-High Pool) Guarantee 30% chance to mate if Fitness Score
                               is > 50% and < 70%

                Mid-Low Pool) Guarantee 15% chance to mate if Fitness Score
                              is > 30% and < 50%

                Low-Pool) Guarantee 5% chance to mate if Fitness Score is < 30%    

          4. Entities then begin to mate a produce three offspring based on there     
             action list

             Crossover of Gene occurs as follows:

             1) Each parent has a 50% chance of their gene being chosen

             2) If a parent gene is chosen it still has an x% chance of mutation  
                occurring before it is used in its offspring action list

              3) If a parent runs out of DNA before the other parent does then the   
                 parent with DNA remaining is used 100% of the time until the crossover process is over

          5.  The Entities offspring then go on to play the game like their parents

          6. This process repeats until a entities produces a DNA strand of 90% or   
             higher stability  and can complete the game


                            Problems With This Algorithm:

          1. Takes to long to complete a generation (100 generation takes around 2 days
             to complete)
          2. Varying Sizes in DNA can cause undesirable effects
          3. DNA tend to be long and as a result tend to take a very long time to  
             evolve toward stability


The previously stated problems drives me away from using this version of the algorithm to test out the question of this project. 
The amount time it takes and the amount of luck required for it progress in the game make it a very naive choice when it comes to answering the question of this project in an efficient time.
