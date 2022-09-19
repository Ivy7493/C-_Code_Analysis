#ifndef SWORD_H
#define SWORD_H
#include "Entity.h"
#include "Knight.h"
#include "EntityHandler.h"

//! The Sword Class.
/*!
  This class handles the sword objects which are created by the
  knight and travel up the screen until it interacts with an object or exits the screen
*/

using namespace std;

class Sword : public Entity
{
    public:
    //! Constructor for Sword.
    /*!
        The parameters represent the current knight's position such that
      \param s_x is an integer of the knights x position.
      \param s_y is an integer of the knights y position
      @see increaseSwords
    */
        Sword(int s_x, int s_y);
        ///Get the position of the sword
        ///@return returns a tuple of two integers of the x and y position of the sword
        tuple<int,int> GetEntityPosition() override;//returns pointer to first value of array containing sword position
        //! Destructor for Sword.
        ///@see decreaseSwords
        virtual ~Sword();
        //tuple<int,int> moveEntity(int topL_x,int topL_y,EntityOperation dirOfMove,const int& entitySize) const;
        /// tells the sword to perform its action
        ///@see Move
        virtual void Action() override;


    protected:

    private:
        array<int,2> SwordPosition;//current position of this sword object
        vector<int> initialOffest{10,10};//decide where in relation to the knight where the sword first appears
        int s_speed = 24;
};

#endif // SWORD_H
