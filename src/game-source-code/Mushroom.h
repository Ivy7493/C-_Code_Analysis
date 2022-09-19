#ifndef MUSHROOM_H
#define MUSHROOM_H
#include "Entity.h"

//! The Mushroom Class.
/*!
  The mushroom class handles information pertaining to mushrooms such as their size and position.
*/
class Mushroom : public Entity
{
    public:
        ///Mushroom Constructor
        Mushroom();
        ///Mushroom Constructor
        ///The position of the mushroom is stored and the number of lives is set to 4.
        ///@param integer mushroom_x is the x coordinate of the mushroom to be created .
        ///@param integer mushroom_y is the y coordinate of the mushroom to be created.
        Mushroom(int mushroom_x,int mushroom_y);
        ///Mushroom Destructor
        virtual ~Mushroom();
        ///Get the position of the mushroom
        ///@return a tuple containing the x and y coordinates of the mushroom
        virtual tuple<int,int> GetEntityPosition() override;
        ///Get the size of the mushroom
        ///@return an integer of the size of the mushroom is returned
        virtual int GetEntitySize()override;
        ///Causes the mushroom to lose a life when called
        virtual void LoseLife() override;
        ///Gets the number of lives the mushroom has remaining
        ///@return integer of number of lives left
        virtual int GetLives() override;


    private:
        array<int,2> mushroomPosition;

        int mushroomSize = 50;
        int mushroomLives;

};

#endif // MUSHROOM_H
