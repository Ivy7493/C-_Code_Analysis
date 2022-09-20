#include "UserInput.h"

UserInput::UserInput()
{
    //ctor
}

EntityOperation UserInput::GetKeys() const
{
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Space)) //Throw Sword
        return EntityOperation::throwSword;
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Left))//Move Left
        {return EntityOperation::moveLeft;}
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Right))//Move Right
        return EntityOperation::moveRight;
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Up))//Move Up
        return EntityOperation::moveUp;
    if(sf::Keyboard::isKeyPressed(sf::Keyboard::Down))//Move Down
        return EntityOperation::moveDown;
    else return EntityOperation::nothing;//Do nothing
}


UserInput::~UserInput()
{
    //dtor
}
