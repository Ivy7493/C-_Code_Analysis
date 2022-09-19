#ifndef FLEA_H
#define FLEA_H

#include "Entity.h"
using namespace std;
//! The Flea class.
/*!
  This class handles the flea objects.
*/
class Flea : public Entity
{
    public:
        ///Flea Constructor
        Flea();
        ///Flea Constructor
        ///Creates a flea object at a position
        ///@param xpos is the x coordinate of the flea to be created
        ///@param ypos is the y coordinate of the flea to be created
        Flea(int,int);
        ///Flea Destructor
        virtual ~Flea();
        ///Gets the flea's position
        ///@return a tuple containing integer values of the flea's x and y coordinates
        virtual tuple<int,int> GetEntityPosition() override;
        ///Gets the size of the flea
        ///@return an integer of the flea size
        virtual int GetEntitySize() override;
        ///Moves the entity in the specified direction
        ///@param dir is the direction of flea movement intended
        ///@return a tuple containing integer values of the new coordinates of the flea after moving
        virtual tuple<int,int> moveEntity(EntityOperation) override;
        ///Causes the flea to perform its associated action
        ///@attention throws an error if try to give flea direction other than down
        ///@see moveEntity
        virtual void Action() override;

    protected:

    private:

        int fleax;
        int fleay;

        int fleaSize = 25;
        int moveInc =12;
};

#endif // FLEA_H
