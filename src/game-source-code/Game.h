#ifndef GAME_H
#define GAME_H

#include<SFML/Graphics.hpp>
#include "Display.h"
#include "UserInput.h"
#include "EntityHandler.h"
#include "Dragon.h"
#include "Collision.h"
//! The Game class.
/*!
  *This class handles the heartbeat of the game and controls winning and losing conditions
  *This is the first class that is called when the game is started
*/
class Game
{
public:
    ///Game Constructor
    ///@note the knight's starting position is set here
    Game();
    ///start contains the game loop.  After the splashscreen is exited
    ///the game heartbeat runs the game every 1/35th of a second until exit conditions are met.
    void start ();
    ///Game Destructor
    virtual ~Game();
    ///This function checks if the end game conditions have been met.
    ///If the knight loses all its lives or all the dragons are destroyed the game ends
    ///@return this function returns true when the game is over
    bool GameEnded (unique_ptr<Knight>& hero_, EntityHandler& entityHandler_);

private:
    bool shortTime = false;
    void GameEndSequence(Display& hydra_fight);

    Collision collision;
    EntityHandler handleEntities;
    string splashTitle = "Main Menu";
    string gameTitle = "Centipede++";
    string scoreboardTitle = "Scoreboard";
    bool endGame;
    bool closeSplash;
    bool gameOver = false;
    int endGameCounter = 0;

    sf::Int32 seconds;
    sf::Time time;
    unique_ptr<Knight> knightPtr;
    array<int,2> knightStartPosition;
    bool win;
};

#endif // GAME_H
