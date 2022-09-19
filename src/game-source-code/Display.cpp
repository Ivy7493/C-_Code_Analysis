#include "Display.h"

Display::Display()
{
    knightPos[0]=init_x;
    knightPos[1]=init_y;
    hero_ = unique_ptr<Knight>(new Knight(knightPos));
    knightPos[0]=init_x;
    knightPos[1]=init_y;

    splashWindow.create({1600,900,32},splashTitle, sf::Style::Default);

    if (!gameTexture.loadFromFile("resources/background_clean.png"))
        throw triedToLoadInvalidFileAsTexture{};
    if (!knightTexture.loadFromFile("resources/blue_knight.png"))
        throw triedToLoadInvalidFileAsTexture{};
    if(!splashTexture.loadFromFile("resources/splashScreen.png"))
        throw triedToLoadInvalidFileAsTexture{};
    if(!swordTexture.loadFromFile("resources/sword_projectile_simple.png"))
        throw triedToLoadInvalidFileAsTexture{};
    if(!mushroomFramesTexture.loadFromFile("resources/mushroom_sheet.png"))
        throw triedToLoadInvalidFileAsTexture{};
    if(!livesTexture.loadFromFile("resources/lives_sheet.png"))
        throw triedToLoadInvalidFileAsTexture{};
    if(!winGameTexture.loadFromFile("resources/win_sheet.png"))
        throw triedToLoadInvalidFileAsTexture{};
    if(!loseGameTexture.loadFromFile("resources/lose_sheet.png"))
        throw triedToLoadInvalidFileAsTexture{};
    if(!bombTexture.loadFromFile("resources/bomb.png"))
        throw triedToLoadInvalidFileAsTexture{};
    if(!fleaTexture.loadFromFile("resources/flea.png"))
        throw triedToLoadInvalidFileAsTexture{};
    if(!explosionTexture.loadFromFile("resources/explosion.png"))
        throw triedToLoadInvalidFileAsTexture{};
    if(!dragonBodyTexture.loadFromFile("resources/dragon_body.png"))
        throw triedToLoadInvalidFileAsTexture{};
    if(!dragonHeadTexture.loadFromFile("resources/dragon_head.png"))
        throw triedToLoadInvalidFileAsTexture{};

    backgroundSprite.setTexture(gameTexture);
    backgroundSprite.scale(sf::Vector2f(4,4));

    knightSprite.setTexture(knightTexture);
    knightSprite.scale(sf::Vector2f(1,1));

    splashSprite.setTexture(splashTexture);
    splashSprite.scale(4,4);

    fleaSprite.setTexture(fleaTexture);
    fleaSprite.scale(sf::Vector2f(0.5,0.5));

    dragonBodySprite.setTexture(dragonBodyTexture);

    endTime = false;
    endFrame = false;
}


Display::~Display()
{

}

/*void Display::UpdateEntities()
{

}*/

void Display::CreateGameWindow()
{
    gameWindow.create({1600,900,32},gameTitle,sf::Style::Default);
}

bool Display::DisplaySplashScreen()
{
    closeSplash = false;
    while(splashWindow.isOpen())
    {
        sf::Event userDecision;
        while (splashWindow.pollEvent(userDecision))
        {
            closeSplash = isEventClose(userDecision,splashWindow);
        }

        splashWindow.draw(splashSprite);
        splashWindow.display();
    }
    return closeSplash;
}

bool Display::isEventClose(sf::Event& uDec,sf::RenderWindow& window)
{
    if(uDec.type == sf::Event::Closed)
    {
        window.close();
        return true;
    }
    else if ((uDec.type == sf::Event::KeyPressed)&&(uDec.key.code == sf::Keyboard::Return))
    {
        window.close();
        return false;
    }
}
void Display::DisplayWinScreen(sf::RenderWindow& gameWindow)
{
    sf::IntRect winSourceSprite(0,0,80,45);
    sf::Sprite winSprite(winGameTexture,winSourceSprite);
    if(!endFrame)
    {
        endFrame = true;
        winSourceSprite.top = 0;
    }
    else
    {
        endFrame = false;
        winSourceSprite.top = 45;
    }

    winSprite.setTextureRect(winSourceSprite);
    winSprite.setPosition(0,0);
    winSprite.scale(sf::Vector2f(20,20));
    gameWindow.draw(winSprite);
}
void Display::DisplayLoseScreen(sf::RenderWindow& gameWindow)
{
    sf::IntRect loseSourceSprite(0,0,80,45);
    sf::Sprite loseSprite(loseGameTexture,loseSourceSprite);
    if(!endFrame)
    {
        endFrame = true;
        loseSourceSprite.top = 0;
    }
    else
    {
        endFrame = false;
        loseSourceSprite.top = 45;
    }

    loseSprite.setTextureRect(loseSourceSprite);
    loseSprite.setPosition(0,0);
    loseSprite.scale(sf::Vector2f(20,20));
    gameWindow.draw(loseSprite);
}
void Display::WinOrLose(bool win,bool ending)
{
    winOrLose = win;
    endTime = ending;
}


bool Display::DisplayGame(unique_ptr<Knight>& hero_,EntityHandler& entityHandler_)
{
    //gameWindow.create({1600,900,32},gameTitle,sf::Style::Default);
    bool close = false;
    if(!endTime)
    {
        gameWindow.clear();
        sf::Event event;

        close = CloseWindowCheck(event,gameWindow);
        tie(xnew,ynew) = hero_->GetEntityPosition();
        knightSprite.setPosition(xnew,ynew);

        //draw mushrooms
        gameWindow.draw(backgroundSprite);
        DisplayMushrooms(gameWindow,entityHandler_);
        //draw swords
        DisplayBombs(gameWindow,entityHandler_);
        DisplayFlea(gameWindow,entityHandler_);
        DisplaySwords(gameWindow, entityHandler_);
        DisplayKnightMovementField(gameWindow);

        DisplayLives(gameWindow,hero_);

        DisplayDragons(gameWindow, entityHandler_);
        DisplayKnight(gameWindow,entityHandler_);

        gameWindow.display();

        return close;
    }
    else
    {
        gameWindow.clear();
        sf::Event event;
        close = CloseWindowCheck(event,gameWindow);
        if(winOrLose)
        {
            DisplayWinScreen(gameWindow);
        }
        else if(!winOrLose)
        {
            DisplayLoseScreen(gameWindow);
        }
        gameWindow.display();
        return close;

    }
    return close;
}

bool Display::CloseWindowCheck(sf::Event& event, sf::RenderWindow& gameWindow)
{
    while (gameWindow.pollEvent(event))
    {
        if(event.type == sf::Event::Closed)
        {
            gameWindow.close();
            return true;
        }
        else
            return false;
    }
}
void Display::DisplayDragons(sf::RenderWindow& gameWindow,EntityHandler& entityHandler_)
{
    auto dragVec = entityHandler_.GetDragonVec();//get a vector of shared pointers of type dragon pointing to dragons
    if (dragVec.empty())
    {
        return;
    }

    sf::IntRect dragonSourceSprite(25,0,25,25);
    sf::Sprite dragonHeadSprite(dragonHeadTexture,dragonSourceSprite);
    for (int i = 0; i<dragVec.size(); i++)
    {
        auto body = dragVec[i];//shared pointer of type dragon pointing to a dragon
        auto temp = *body;//the actual dragon class object
        auto segVec = temp.getBody();//body of the dragon class object made of DragonSegment type
        auto dragsize = temp.GetEntitySize();
        auto x = 0;
        auto y = 0;
        tie(x,y) = temp.GetEntityPosition();

        if(temp.GetDirection()==EntityOperation::moveUp)
            dragonSourceSprite.top = 25;
        if(temp.GetDirection()==EntityOperation::moveDown)
            dragonSourceSprite.left = 0;
        if(temp.GetDirection()==EntityOperation::moveRight)
        {
            dragonSourceSprite.top = 25;
            dragonSourceSprite.left = 0;
        }

        dragonHeadSprite.setTextureRect(dragonSourceSprite);
        dragonHeadSprite.setPosition(x,y);
        gameWindow.draw(dragonHeadSprite);

        for (int j = 1; j<segVec.size(); j++)
        {
            dragonBodySprite.setPosition(segVec[j].x_, segVec[j].y_ );
            gameWindow.draw(dragonBodySprite);
        }
    }
}

void Display::DisplayMushrooms(sf::RenderWindow& gameWindow,EntityHandler& entityHandler_)
{
    mushroomSprites.clear();
    mushroomSpritePositions = entityHandler_.MushroomPositions();
    mushVec = entityHandler_.GetMushroomVec();
    for(int x = 0; x< mushroomSpritePositions.size(); x++)
    {
        sf::IntRect mushSourceSprite(0,0,50,50);
        sf::Sprite tempSprite(mushroomFramesTexture,mushSourceSprite);

        if((mushVec[x]->GetLives()) == 2)
            mushSourceSprite.left =50;
        if((mushVec[x]->GetLives()) == 1)
        {
            mushSourceSprite.left = 0;
            mushSourceSprite.top = 50;
        }
        if((mushVec[x]->GetLives())==0)
        {
            mushSourceSprite.left = 50;
            mushSourceSprite.top = 50;
        }
        tempSprite.setTextureRect(mushSourceSprite);
        tempSprite.scale(0.5,0.5);
        tempSprite.setPosition(mushroomSpritePositions[x][0],mushroomSpritePositions[x][1]);
        mushroomSprites.push_back(tempSprite);
        gameWindow.draw(mushroomSprites[x]);
    }
}

void Display::DisplaySwords(sf::RenderWindow& gameWindow,EntityHandler& entityHandler_)
{
    swordSprites.clear();
    swordSpritePositions = entityHandler_.SwordPositions();
    for (int x = 0; x<swordSpritePositions.size();x++)
    {
        sf::Sprite tempSwordSprite;
        tempSwordSprite.setTexture(swordTexture);
        tempSwordSprite.setPosition(swordSpritePositions[x][0], swordSpritePositions[x][1]);
        swordSprites.push_back(tempSwordSprite);
        gameWindow.draw(swordSprites[x]);
    }
}

void Display::DisplayBombs(sf::RenderWindow& gameWindow,EntityHandler& entityHandler_)
{
    bombSprites.clear();
    bombSpritePositions = entityHandler_.BombPositions();
    for (int x = 0; x<bombSpritePositions.size();x++)
    {
        sf::Sprite tempBombSprite;
        tempBombSprite.setTexture(bombTexture);
        tempBombSprite.setPosition(bombSpritePositions[x][0], bombSpritePositions[x][1]);
        bombSprites.push_back(tempBombSprite);
        gameWindow.draw(bombSprites[x]);
    }
    if(entityHandler_.isExploding())
    {
        tie(explosion_x,explosion_y) = entityHandler_.BoomPosition();
        explosionSprite.setTexture(explosionTexture);
        explosionSprite.setColor(sf::Color(255,255,255,100));
        explosionSprite.setPosition(explosion_x,explosion_y);
        gameWindow.draw(explosionSprite);
    }
}

void Display::DisplayLives(sf::RenderWindow& gameWindow,unique_ptr<Knight>& hero_)
{
    sf::IntRect livesSourceSprite(0,0,64,20);

    sf::Sprite livesSprite(livesTexture,livesSourceSprite);

    if((hero_->GetLives())==2)
    {
        livesSourceSprite.top = 20;
    }
    if((hero_->GetLives())==1)
    {
        livesSourceSprite.top = 40;
    }
    if((hero_->GetLives())==0)
        return;
    livesSprite.setTextureRect(livesSourceSprite);
    livesSprite.setPosition(25,25);
    gameWindow.draw(livesSprite);
}
void Display::EndGame()
{
    gameWindow.close();
}

void Display::DisplayKnightMovementField(sf::RenderWindow& gameWindow)
{
    sf::RectangleShape knightField;
    knightField.setSize(sf::Vector2f(1550,285));
    knightField.setFillColor(sf::Color(255,255,255,70));
    knightField.setPosition(25,590);
    gameWindow.draw(knightField);
}

void Display::DisplayKnight(sf::RenderWindow& gameWindow,EntityHandler& entityHandler_)
{

    if(entityHandler_.IsKnightImmune())
        knightSprite.setColor(sf::Color(255,0,0,160));
    if(!entityHandler_.IsKnightImmune())
        knightSprite.setColor(sf::Color(255,255,255,255));
    gameWindow.draw(knightSprite);
}

void Display::DisplayFlea(sf::RenderWindow& gameWindow,EntityHandler& entityHandler_)
{
    if(entityHandler_.IsFlea())
    {
        tie(fleax,fleay) = entityHandler_.GetFleaPosition();
        fleaSprite.setPosition(fleax,fleay);
        //fleaSprite.scale(sf::Vector2f(0.5,0.5));
        gameWindow.draw(fleaSprite);
    }
}
