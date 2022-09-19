#ifndef USERINPUT_H
#define USERINPUT_H
#include "Entity.h"
#include<SFML/Graphics.hpp>
//! The UserInput class.
/*!
  This class handles the user input by reading in key presses
*/

class UserInput
{
    public:
        ///UserInput Constructor
        UserInput();
        ///Get the enumeration type that is being read in from the keyboard
        ///@return enumeration EntityOperation representing the key being pressed
        EntityOperation GetKeys() const;
        ///UserInput Destructor
        virtual ~UserInput();

    private:
};

#endif // USERINPUT_H
