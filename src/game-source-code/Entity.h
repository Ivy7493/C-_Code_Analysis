#ifndef ENTITY
#define ENTITY

#include <tuple>
#include<string>
#include <vector>
#include <memory>

class triedSetInvalidDirection {};
using namespace std;
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
  
    Entity();
    virtual void Action();
    ///@param dirOfMove is the direction of movement ENUM
    ///@return tuple of new x and y position of the entity
    virtual tuple<int,int> moveEntity(EntityOperation dirOfMove);
    ///@return tuple of the x and y coordinates of the entity's position
    virtual tuple<int,int> GetEntityPosition();
    ///@return integer of the entity size
    virtual int GetEntitySize();

    virtual string GetEntitySize();

    virtual int GetLives(){
      int a = 4;
      return a;
    }
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
