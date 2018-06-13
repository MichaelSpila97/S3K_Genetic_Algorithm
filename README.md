# Sonic3-K_Game_AI

Project Overview:

The goal of this project is to create a AI or Bot that can compenetly play the sega genisis classic Sonic 3 & Knuckles.
The AI will use a combination of image analysis and action analysis to function. By the end the project it should be able to
at least get through the first act of the game, Angel Island zone, with no issues. Below is a list of what has been completed,
what needs to be polished/Upgraded or what need to be created.


Completed:

          1) Basic Snap Shot Function and Recognition for:
               a) Rings
               b) Score
               c) Lives
               d) Act Beginning and End
               
          2) Validation of Ring,Score, lives and Act values
          3) Recogniton that Sonic 3 & Knuckles is ready to play
          4) Function/Functions to handles the generation of action

Needs work:

          1) Need to add Snap Shot Function and Recogition for:
            a) Soinc(Mabye..)
          2) Documentation
          3) Better File Names
          4) Add variable in act class to faciliate the varition of the multiple action delays in spindash and jump_sheild
          
Needs Created:

          1) Functions/Functions to load/save data off each play attempt made by the computer*
          2) Model for evaluating the fitness of a computers play attempt 
          3) Fuctions/Function to score said model 
          4) Functions/Function to create new computer AI off of the fittess AI data from the last generation
          5) Way to detect enemies and object on screens
          6) Good Gui for easy control of the project for running tests


 What is currently being worked on = *
 
 
 
                                           Genetic Algorithm Overview:
                                           
The computer will use a genetic algorithm I devisied to teach it self how to play the game. The algorithm consist of having a generation of entities play the game till death or till completion. Once one of those conditions are meet their DNA, being their action_list, will be evaluted. The evaluation will be based on how the actions effected the ring and score count through the play sessesion. 

1)If rings and scores are gained the spefic action that dected the change and all action that were preformed in 5 to 10 seconds before it will be rewarded. 

2)If rings are lost the same thing will happend when gained except that those  action will be penilized. Big rewarded will be given to all the action if the entity completes and act or Zone and Big penalties will be given to all acticons in the entity dies.

3)Also the rate in which the entity accumlates score will also be used to dual out penatlies and rewards. 
          a) If the entity is racking up score or rings at a relatively fast rate the entity and the action associated wtih that will be rewarded. 
          b) If the entity goes for a minute without gaining any score or rings, the entity and any action executed a minute ago will recieved a penilty and any action executed moving on will also recieved a penialty till rings or score is ganined.  

Reward and Penalties specifics:

Before speaking about what the specific are with rewards and penalties we first mention what the overal goal of the computer is during the learning process. 
                 The goal is to evolve towards stability, meaing the mutation rate for all actions will start at the high rate of 50% and the goal of the computer is to find a sequance of action that mutation rate is supstationally low.
                 
This mean the reward is lowing the mutation rate down while the penalty is increase the mutation rate of actions.  

1) General rewards will decrease the percentatage of mutation by 5% while genearl penalties will increase the mutation rate by 5%. 

2)Exception rewards like beating an act or stage will decreaae the mutation rate by 25% while dying will increase muation by 10%.
          a)Death is more likely to occur than beating an so a low increase in percentage ensure that favorable action arn't wiped out immediatly because of death.
          
Lifecycle description:
          So at the beginning of the training three entities will be genearate and one generation will be used to represent them. A entity btw represent one life in the game while a generation represent all lives that occur before a game over. Once each entity in a generation goes through their training sesion, and likely dies, each of them and their DNA will be evaulated. At the end of the evaluation each entity will have a fitness score and the mating process will begin. During the mating process at minimun three enties will be created. Each entity will have chance to mate but the ones with higher fitness will have a more likley chance to mate. Each new entity will consist of parts of thier parents action list. During this process of creating the DNA for the new entities mutation can occur. If it does occur a new action and duration for the action that mutated and the mutation rate for that action will be set to 50% again. After the creation of three new entiteis those three will make up a new generation and they will play through the game till death or completion. 
          
Extending a Generation:
          A generation can be extened by a entity gaining a extra life during a play session. If this does a occur a new entity will be create by eith using the previous generation DNA or a random action generation that will be wieght based on the previous generation play. I have not decided which I will use. THe one that will be used is the one that efficiently creates more fit entities.
          
General Process for randomization:
          The randomization and choice proces will consit of a list size 100 and elements that represent and particular choice. For instance say an action has a 40% chance of mutating. 40 element in the list will represent the decision to mutate while 60 present will represent the desicion not to mutate. Each list will be shuffled before selection for more fair drawing by the chocie function.
          
