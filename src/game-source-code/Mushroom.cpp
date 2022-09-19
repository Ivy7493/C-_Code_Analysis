#include "Mushroom.h"

Mushroom::Mushroom()
{

}

Mushroom::Mushroom(int mushroom_x,int mushroom_y)
{
    mushroomPosition[0] = mushroom_x;
    mushroomPosition[1] = mushroom_y;
    mushroomLives = 3;
}

Mushroom::~Mushroom()
{
    //dtor
}
tuple<int,int> Mushroom::GetEntityPosition()
{
    return{mushroomPosition[0],mushroomPosition[1]};
}

int Mushroom::GetEntitySize()
{
    return mushroomSize;
}
void Mushroom::LoseLife()
{
    mushroomLives--;
}

int Mushroom::GetLives()
{
    return mushroomLives;
}
