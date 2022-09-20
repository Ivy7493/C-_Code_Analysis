#include "Flea.h"

Flea::Flea(int xpos,int ypos)
{
    fleax = xpos;
    fleay = ypos;
}

Flea::~Flea()
{
    //dtor
}

tuple<int,int> Flea::GetEntityPosition()
{
    return{fleax,fleay};
}
tuple<int,int> Flea::moveEntity(EntityOperation dir)
{
    if (static_cast<int>(dir)!=3)
    {
        throw triedSetInvalidDirection{};
    }
    int tempy =fleay+moveInc;
    return{fleax,tempy};
}

void Flea::Action()
{
    tie(fleax,fleay) = moveEntity(EntityOperation::moveDown);
}

int Flea::GetEntitySize()
{
    return fleaSize;
}
