#ifndef DISPLAY_H
#define DISPLAY_H
#include<math.h>
#include<memory>
#include<SFML/Graphics.hpp>
#include<vector>
#include "Entity.h"
#include "Knight.h"
#include "Dragon.h"
#include "Mushroom.h"
#include "EntityHandler.h"


using namespace std;
//! A throw class.
/*!
  This class is called if a texture file is not able to be loaded
*/
class triedToLoadInvalidFileAsTexture {};

//! The Display class.
/*!
  This class handles everything that has to be displayed on the screen as the game runs.
*/

class Display
{
public:
    ///Display Constructor
    ///A unique pointer to the knight is created here.
    ///Sprite textures are loaded from files
    ///@warning an exception will be thrown if a texture file cannot be loaded
    Display();
    ///Display Destructor
    ~Display();
    ///The functions to display all entities are called from here
    ///A check to see if the game window is closed is also completed here
    ///@return true is returned if the game window is closed
    ///@param hero_ is a unique pointer pointing to the knight
    ///@param entityHandler is an entity handler object used to access the information in the class
    bool DisplayGame(unique_ptr<Knight>& hero_,EntityHandler& entityHandler);
    ///This splash screen function is called and displays the splashscreen while polling for either
    ///the key press necessary to begin the game or for the game window to be closed
    ///@return returns true if the window is closed.  Returns false if the key to begin the game is pressed.
    bool DisplaySplashScreen();
    ///The dimensions of the game window are initialised here
    void CreateGameWindow();
    ///Used to set private bool members to true or false based on if the game is won or lost
    ///@param win is a bool indicating true when the game is won
    ///@param ending
    void WinOrLose(bool win,bool ending);
    ///When this function is called it causes the game window to close
    void EndGame();

private:

    void DisplayMushrooms(sf::RenderWindow& gameWindow,EntityHandler&);
    void DisplaySwords(sf::RenderWindow& gameWindow,EntityHandler&);
    void DisplayDragons(sf::RenderWindow& gameWindow,EntityHandler&);
    void DisplayLives(sf::RenderWindow& gameWindow,unique_ptr<Knight>& hero_);
    void DisplayBombs(sf::RenderWindow& gameWindow,EntityHandler& entityHandler_);
    void DisplayWinScreen(sf::RenderWindow& gameWindow);
    void DisplayLoseScreen(sf::RenderWindow& gameWindow);
    void DisplayKnightMovementField(sf::RenderWindow& gameWindow);
    void DisplayKnight(sf::RenderWindow& gameWindow,EntityHandler& entityHandler_);
    void DisplayFlea(sf::RenderWindow& gameWindow,EntityHandler&);
    bool isEventClose(sf::Event& uDec,sf::RenderWindow& window);
    bool CloseWindowCheck(sf::Event& event, sf::RenderWindow& window);


    int init_x = 750;
    int init_y = 775;
    array<int,2> knightPos;
    unique_ptr<Knight> hero_;
    vector<sf::Sprite> spriteVector;

    Dragon drag;

    sf::RectangleShape bodyRect;
    UserInput userInput;
    EntityOperation operation;

    bool shortTime;
    bool closeSplash;
    int xnew;
    int ynew;
    //auto hero_ = Knight(knightPos,knightSize.x,knightSize.y);
    //other variables:

    sf::RenderWindow splashWindow;
    sf::RenderWindow gameWindow;
    sf::RenderWindow scoreScreen;

    sf::Texture gameTexture;
    sf::Texture splashTexture;
    sf::Texture knightTexture;
    sf::Texture swordTexture;
    sf::Texture mushroomFramesTexture;
    sf::Texture livesTexture;
    sf::Texture winGameTexture;
    sf::Texture loseGameTexture;
    sf::Texture bombTexture;
    sf::Texture fleaTexture;
    sf::Texture explosionTexture;
    sf::Texture dragonHeadTexture;
    sf::Texture dragonBodyTexture;

    sf::Sprite knightSprite;
    sf::Sprite backgroundSprite;
    sf::Sprite splashSprite;
    sf::Sprite winGameSprite;
    sf::Sprite loseGameSprite;
    sf::Sprite explosionSprite;
    sf::Sprite fleaSprite;
    sf::Sprite dragonBodySprite;

    sf::Sprite mushroomSprite;
    int mush_x;
    int mush_y;
    vector<sf::Sprite> mushroomSprites;
    vector<array<int,2>> mushroomSpritePositions;
    vector<shared_ptr<Entity>> mushVec;


    sf::Sprite swordSprite;
    sf::Sprite tempSwordSprite;
    int sword_x;
    int sword_y;
    vector<sf::Sprite> swordSprites;
    vector<array<int,2>> swordSpritePositions;

    vector<sf::Sprite> bombSprites;
    vector<array<int,2>> bombSpritePositions;
    int explosion_x;
    int explosion_y;

    sf::Vector2u windowSize = {1600,900};

    int fleax;
    int fleay;

    string splashTitle = "Main Menu";
    string gameTitle = "Centipede++";
    string scoreboardTitle = "Scoreboard";
    bool isOpen;
    bool endFrame;
    bool winOrLose;
    bool endTime;

};

#endif // DISPLAY_H
