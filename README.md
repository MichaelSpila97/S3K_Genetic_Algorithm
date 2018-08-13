#Sonic3-K_Game_Genetic_Algorithm


                                          Algorithm Version 2 Description

                                         Name: Segmented Stability Algorithm


                 The Segmented Stability Algorithm works on the idea of the algorithm training entities on
             smaller but equal segments of the game over and over again until an entities fitness rating is
             over 98% then that entities DNA is used by other entities in further generation as they tackle
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
                      2. Entity does not increase ring count in a secomd
                      3. Entity is in a defenseless state, meaning has no rings
                      4. Entity loses life

          
              3. Entities are then placed into mating pools of the follow based on
                 there Fitness Score

                 High Pool) Guarantee 50% chance to mate if Fitness Score is > 70%

                 Mid-High Pool) Guarantee 30% chance to mate if Fitness Score
                                is > 50% and < 70%

                 Mid-Low Pool) Guarantee 15% chance to mate if Fitness Score
                               is > 30% and < 50%

                 Low-Pool) Guarantee 5% chance to mate if Fitness Score is < 30%
                 
                 Notes:
                        1)If a pool does not have any entities inside it then its mating percentage is added on to the next
                          pool above it that haves entities in it.
                 
                        2)If multiple entities are in the same pool that pools percent of the overall
                          mating pool is split between all the entities in that pool.
                       
                        Ex: 5 entities in the Mid-Low Pool mean each entity gets a 3% chance to mate
                
            Two diffrent outcomes can occurs after evaluation is complete and reproduction begins:
                      a) No entity fitness is above 98% and reproduction of new entities occurs normally
                      b) An entities fitness is above or equal to 98% and a master entitiy is created
            
             4a. Entities then begin to mate and produce offspring based on there     
                action list

                Crossover of Gene occurs as follows:

                  1) The gene with the lowest mutation rate is chosen

                  2) The choosen gene will then have a chance to mutate, based on its mutation rate, before it
                     is placed in the new entities action list
                     
             4b. After the master entitiy is found:
                
                 1) Any previous master entities DNA is added before the current master DNA
                 
                 2) X number of children entitiy are created with empty action list and the master entity
                    attached to them

            5. The Entities offspring then go on to play the game like their parents

            6. If after 10 generation no new master has been found or the overall fitness of the last generation
               has stayed around the same value, then stagataion has occurred and the DNA cap must be risen 
               in attempt to solve stagnation.
               
               Note: Stagation cannot occur back to back, meaning 10 generation must past after the last stagation occured
                     before stagnation is detected again.
            
            7. This process will continue until an entity has completed the game.
            
     
                                    Why, In Theory, This is Better Than Ver1:

                     1) Equal DNA length mean each entity will be evaluated more fairly
                     2) Smaller DNA length mean it will take less time to complete a
                        generations training and less time for a stable entity to appear
                     3) I can increase the population size without having to worry about a
                        generation taking too long to complete
