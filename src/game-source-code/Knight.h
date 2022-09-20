#ifndef KNIGHT_H
#define KNIGHT_H
#include "Entity.h"
#include "UserInput.h"

//! The Knight class.
/*!
  This class handles the standard information pertaining to the knight entity
  which the player can move around.
*/

class Knight : public Entity
{
    public:
        ///Knight Constructor
        ///@param initialPositioinOfKnight is stored in the knight class
        ///@note the knight constructor sets the knights lives to 4
        Knight(array<int,2> initialPositionOfKnight);
        ///Knight Destructor
        virtual ~Knight();
        ///Action function for the knight responsible for moving it in the specified direction
        ///@param knightAction is the direction in which we would like the knight to move
        ///@see moveEntity
        void Action(EntityOperation knightAction);
        ///Move the knight in the specified direction by the knight's set speed
        ///@param dirOfMove specifies the direction the knight must move in
        ///@return tuple containing x and y coordinates of the knights new position after movement
        ///@attention throws an error if an invalid knight direction is passed
        virtual tuple<int,int> moveEntity(EntityOperation dirOfMove) override;
        ///Get the position of the knight
        ///@return a tuple containing integer x and y coordinates of the knight's new position
        ///@note the borders of where the knight is allowed to move is contained here
        virtual tuple<int,int> GetEntityPosition() override;//returns the knight's position
        ///Get the number of lives that the knight has left
        virtual int GetLives() override;
        ///Calling this function causes the knight to lose one life
        virtual void LoseLife() override;
        virtual int GetEntitySize() override;

    private:
    //array<int,2> currPos_;
    int knightSize = 25;
    int topBorder = 590;
    int knightLives;
    int increment_ = 25;

    int topL_x;
    int topL_y;
};
#endif
