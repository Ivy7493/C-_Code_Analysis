//-------------------------------------
//--------------Knight-----------------
//-------------------------------------

#include "Knight.h"
using namespace std;

Knight::Knight(array<int,2> initialPositionOfKnight)
{
    knightPos_[1] = initialPositionOfKnight[1];
    knightPos_[0] = initialPositionOfKnight[0];
    knightLives = 3;
}

void Knight::Action(EntityOperation knightAction)
{
    int temp_x = knightPos_[0];
    int temp_y = knightPos_[1];


    if(knightAction == EntityOperation::moveLeft)
    {
        tie(temp_x,temp_y) = moveEntity(EntityOperation::moveLeft);
    }
    if(knightAction == EntityOperation::moveRight)
    {
        tie(temp_x,temp_y) = moveEntity(EntityOperation::moveRight);
    }
    if(knightAction == EntityOperation::moveUp)
    {
        tie(temp_x,temp_y) = moveEntity(EntityOperation::moveUp);
        if(temp_y<topBorder)
            temp_y = topBorder;
    }
    if(knightAction == EntityOperation::moveDown)
    {
        tie(temp_x,temp_y) = moveEntity(EntityOperation::moveDown);
    }

    knightPos_[0] = temp_x;
    knightPos_[1] = temp_y;
}

int Knight::GetLives()
{
    return knightLives;
}
tuple<int,int> Knight::GetEntityPosition()
{
    return {knightPos_[0],knightPos_[1]};
}
void Knight::LoseLife()
{
    knightLives--;
}
Knight::~Knight()
{
    //dtor
}
tuple<int,int> Knight::moveEntity(EntityOperation dirOfMove)
{
    topL_x = knightPos_[0];
    topL_y = knightPos_[1];

    if(static_cast<int>(dirOfMove)>3)
    {
        throw triedSetInvalidDirection{};
    }

    if(dirOfMove == EntityOperation::moveLeft)
    {
        if((topL_x-increment_) < xmin_)
        {
            topL_x = xmin_;
            return{topL_x,topL_y};
        }
        topL_x-=increment_;
        return{topL_x,topL_y};
    }
    if(dirOfMove == EntityOperation::moveRight)
    {
        if((topL_x + increment_ + knightSize) > xmax_)
        {
            topL_x = xmax_-knightSize;
            return{topL_x,topL_y};
        }
        topL_x+=increment_;
        return{topL_x,topL_y};
    }
    if(dirOfMove == EntityOperation::moveUp)
    {
        if((topL_y - increment_) < ymin_)
        {
            topL_y = ymin_;
            return{topL_x,topL_y};
        }
        topL_y-=increment_;
        return{topL_x,topL_y};
    }
    if(dirOfMove == EntityOperation::moveDown)
    {
        if((topL_y + increment_ + knightSize) > ymax_)
        {
            topL_y = ymax_-knightSize;
            return{topL_x,topL_y};
        }
        topL_y+=increment_;
        return{topL_x,topL_y};
    }
    return{topL_x,topL_y};
}

int Knight::GetEntitySize()
{
    return knightSize;
}
