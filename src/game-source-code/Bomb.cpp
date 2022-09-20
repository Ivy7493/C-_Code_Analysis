#include "Bomb.h"

Bomb::Bomb(int bombx,int bomby)
{
    x_pos = bombx;
    y_pos = bomby;
    bombLives = 1;
}

Bomb::~Bomb()
{
    //dtor
}

tuple<int,int> Bomb::GetEntityPosition()
{
    return{x_pos,y_pos};
}

int Bomb::GetEntitySize()
{
    return bombSize;
}

void Bomb::LoseLife()
{
    bombLives --;
}

int Bomb::GetLives()
{
    return bombLives;
}
