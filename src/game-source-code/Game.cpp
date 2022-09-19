#include "Game.h"

Game::Game()
{
    endGame = false;
    knightStartPosition = {775,750};
}
void Game::start ()
{
    sf::Clock clock;

    knightPtr = unique_ptr<Knight>(new Knight(knightStartPosition));
    auto hydra_fight = Display();
    handleEntities.MakeMushroomField();
    handleEntities.InitialiseDragon();//initialise the first dragon that enters the screen here

    closeSplash = hydra_fight.DisplaySplashScreen();

    float frametime = 1.0f / 30.0f;
    hydra_fight.CreateGameWindow();

    clock.restart();

    while(!endGame)
    {
        time = clock.getElapsedTime();

        if(time.asSeconds()>=frametime)
        {
            endGame = hydra_fight.DisplayGame(knightPtr,handleEntities);
            time -= sf::seconds(frametime);
            time = clock.restart();

            if(GameEnded(knightPtr,handleEntities))
            {
                frametime = 1.0f / 1.0f;
                GameEndSequence(hydra_fight);
            }
            else
            {
                collision.CheckCollisions(knightPtr);
                handleEntities.UpdateEntities(knightPtr);
            }
        }
    }
}

bool Game::GameEnded(unique_ptr<Knight>& hero_,EntityHandler& entityHandler_)
{
    auto dead = hero_->GetLives();
    auto dragVec = handleEntities.GetDragonVec();

    if(dead == 0||dragVec.empty())
    {
        gameOver = true;
        if(dead==0){win = false;}
        if(dragVec.empty()){win =true;}
        return gameOver;
    }
    return gameOver;
}

void Game::GameEndSequence(Display& hydra_fight)
{
    if(win)
    {
        if(win)
        {
            hydra_fight.WinOrLose(true,true);
        }
        else if(!win)
        {
            hydra_fight.WinOrLose(false,true);
        }

        endGameCounter ++;
        if(endGameCounter ==175)
        {
            hydra_fight.EndGame();
            endGame = true;
        }

    }
    else if(!win)
    {
        hydra_fight.WinOrLose(false,true);
    }
    endGameCounter ++;
    if(endGameCounter ==12)
    {
        hydra_fight.EndGame();
        endGame = true;
    }

}
Game::~Game()
{
    //dtor
}
