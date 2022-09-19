#ifndef BOMB_H
#define BOMB_H

#include "Entity.h"
//! The Bomb class.
/*!
  This class handles the bomb objects.  It stores information pertaining to bombs such as
  their position, number of lives and size.
*/

class Bomb : public Entity
{
    public:
        ///Bomb Constructor
        ///@param bombx is the x coordinate of the bomb being constructed
        ///@param bomby is the y coordinate of the bomb being constructed
        ///@note the number of bomb lives is also set here
        Bomb(int,int);
        ///Bomb Destructor
        virtual ~Bomb();
        ///Gets the position of the bomb
        ///@return tuple containing integer values of the bomb's x and y positions
        virtual tuple<int,int> GetEntityPosition() override;
        ///Gets the size of the bomb
        ///@return integer size of the bomb entity
        virtual int GetEntitySize() override;
        ///When called causes the bomb to lose a life
        virtual void LoseLife() override;
        ///When called returns the number of lives the bomb has left
        ///@return integer value of the number of lives the bomb has left
        virtual int GetLives() override;

    private:
        int x_pos;
        int y_pos;
        int bombSize = 25;

        int bombLives;
};

#endif // BOMB_H
