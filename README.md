#GreedySim

#####A program by Sydney Cardew

GreedySim is an (as of version 1.0.0 still crude and incomplete) self-playing version of my card game 'Too Greedily, Too Deep'. I wrote it both as a programming challenge and also in order to help me analyse and tweak the balance of the game. It is my hope that, as I improve the fidelity of the simulation and develop new ways to extract data about the simulation runs in aggregate, any unfair cards will be highlighted.

#####Command line arguments:

-m, --multi: runs multiple instances of the simulation at once.    
-v, --version: displays the version number

#####Config.ini settings:

* 'version': sets the version number    
* 'players': sets the number of players    
* 'player1'...'player5': sets the player personalities    
    * 'random': all stats chosen randomly from within maximum ranges
* 'lognumber': the number of digits for log file names    
* 'timestorun': the number of times to run the program in '-m' mode.     
* 'multimode': controls the behaviour of the '-m' mode. 
    * 'normal': runs all simulations according to the number of players set in 'players'  
    * 'spread': runs 1/4 of the simulations with 2 players, 1/4 with 3 etc.
    * 'random': randomises the number of players each time the simulation runs

####Version History:

**Version 1.0.0**: 15/09/2020   
Description: First working version of GreedySim

**Version 1.1.0**: 16/09/2020    
Description: Aggregate data collection, mass logging improvements, code-refactoring, improved documentation, escape sequence and voiding, many crashes and errors fixed or mitigated, implemented some special powers.

####Future Development Goals:    

* Fully implement game rules and elements not currently implemented:      
    * ~~Voiding stacks~~
    * Item cards
    * The Escape Sequence - *largely implemented*
    * Missions
    * The Loan Shark
    * The Necromancer, Medic and other special power cards
    
* Institute a 'correct' solution for various currently existing workarounds 
* ~~Fix the Main Expedition loop~~ - *complete*
* Collect aggregate data about multiple simulations - *started*    
* Improve log formatting
* Improve AI and make more decisions governed by AI personalities     
* More AI personality settings - *started*
* Refactor code for readability and consistency and improve commenting - *started*