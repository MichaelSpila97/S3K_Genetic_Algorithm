#Sonic3-K_Game_Genetic_Algorithm


                                          Algorithm Version 2 Description

                                         Name: Segmented Stability Algorithm


                 The Segmented Stability Algorithm works on the idea of the algorithm training entities on
             smaller but equal segments of the game over and over again until an entities fitness rating is
             over 90% then that entities DNA is used by other entities in further generation as they tackle
             the next segment of the game. The algorithm will be preformed as flowed:


                 1. All entities in a generation play till they play out a certain set number of action:
                    a) If an entities dies before it plays out the set number of action it will be resurrected
                      and allowed to go again.

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

             4. Entities then begin to mate and produce offspring based on there     
                action list

                Crossover of Gene occurs as follows:

                  1) Each parent has a 50% chance of their gene being chosen

                  2) If a parent gene is chosen it still has an x% chance of mutation  
                     occurring before it is used in its offspring action list

            5. The Entities offspring then go on to play the game like their parents

            6. This process repeats until an entity has a fitness rating of 90%.

            7. Said entity DNA will be used as the base for all others entities DNA moving and
               the length of the DNA for each entity moving forward will increase by the set amount

            8. This process will continue until an entity has completed the game.


                                    Why, In Theory, This is Better Than Ver1:

                     1) Equal DNA length mean each entity will be evaluated more fairly
                     2) Smaller DNA length mean it will take less time to complete a
                        generations training and less time for a stable entity to appear
                     3) I can increase the population size without having to worry about a
                        generation taking too long to complete
