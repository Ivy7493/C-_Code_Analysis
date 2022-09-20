#include "Sword.h"
Sword::Sword(int s_x,int s_y)
{
    SwordPosition[0] = s_x + initialOffest[0];//adding to the x component of initial sword position
    SwordPosition[1] = s_y + initialOffest[1];//adding to the y component of initial sword position
}
Sword::~Sword()
{
    //dtor
}

tuple<int,int> Sword::GetEntityPosition()
{
     return {SwordPosition[0],SwordPosition[1]};
}

 void Sword::Action()
{
    SwordPosition[1] -= s_speed;
}
