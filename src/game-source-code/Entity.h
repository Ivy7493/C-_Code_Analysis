#ifndef ENTITY
#define ENTITY

#include <tuple>
#include<string>
#include <vector>
#include <memory>

//! A throw class.
/*!
  This class throws an error if an invalid direction is set.
*/
class triedSetInvalidDirection {};

//! The Entity class.
/*!
  This class is the base class for many of the other classes which pertain to moving objects and focuses on the
  objects whose positions need to change and update over the course of the program.
*/

using namespace std;
///An enumeratin of the directions that entities can move in or actions they can perform
enum class EntityOperation
{


        moveLeft =0,    /**< enum value moveLeft. */
        moveRight = 1,  /**< enum value moveRight. */
        moveUp = 2,     /**< enum value moveUp. */
        moveDown = 3,   /**< enum value moveDown. */
        throwSword = 4, /**< enum value throwSword. */
        die = 5,        /**< enum value Die. */

        nothing = -1    /**< enum value nothing. */
};
class Entity
{
public:
    ///Entity constructor
    Entity();
    ///Action that the entity can perform such as movement, deletion or creation of entities
    virtual void Action();
    ///Move the entity in a direction
    ///@param dirOfMove is the direction of movement ENUM
    ///@return tuple of new x and y position of the entity
    virtual tuple<int,int> moveEntity(EntityOperation dirOfMove);
    ///Get the positional coordinates of the entity
    ///@return tuple of the x and y coordinates of the entity's position
    virtual tuple<int,int> GetEntityPosition();
    ///Get the size of the entity
    ///@return integer of the entity size
    virtual int GetEntitySize();
    ///Get the lives that the entity currently posesses
    virtual int GetLives();
    ///Decrease the number of lives that the entity posesses by 1
    virtual void LoseLife();



protected:
    float time_;
    int xmin_ = 24;
    int xmax_ = 1574;
    int ymin_ = 24;
    int ymax_ = 874;

    array<int,2> knightPos_;

};

#endif // ENTITY*/
