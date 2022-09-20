#ifndef COLLISION_H
#define COLLISION_H

#include "EntityHandler.h"
#include<vector>
#include<memory>

#include "Dragon.h"
#include "Entity.h"
#include "Grid.h"
//! The Collision class'
/*!
 This class handles all collisions in the game between different entities.
 Checks are completed here to see if two entities are colliding and the subsequent actioins
 that must take place on the entities are carried out here.
 */
class Collision
{
public:
    ///Default constructor for Collision
    ///This constructor is the only constructor for Collision since
    ///no parameters are required when an object of this class is being created
    Collision();
    ///Destructor for a collisioin object
    virtual ~Collision();
    /// CheckCollisions calls all the functions that check all the collisions between the entities on screen
    ///@param knightAlias is a unique_ptr to a Knight object that is created in Game.cpp
    void CheckCollisions(unique_ptr<Knight>& knightAlias);


private:
    void KnightDragCollision(unique_ptr<Knight>& knightAlias);
    void BombCollision(int x, int y, int entSize);
    void CollisionDragMush();
    void CollisionMushSword();
    void CollisionSwordFlea(int s_x, int s_y,int swordNum);
    void CollisionSword();
    bool DragonSegmentsCollision(int s_x,int s_y,int creaSize);
    void ClearVectors();
    void DragDirection(bool hitBot,EntityOperation dir,int mushleft,int mushright,int dragleft,int dragright,int mushtop,int position);

    void UpdateExplosion();
    EntityHandler entityHandler_;
    bool knightIsImmune;
    int immunityCounter;
    int knightSize = 26;
    bool dragKnightCheck;
    bool dragSwordCheck;

    array<int,2> boomPosition;
    vector<array<int,2>> bombPositions;
    vector<shared_ptr<Entity>> bomb_vec;
    bool exploding;
    int explodeTime;
    bool swordBomb;

    vector<shared_ptr<Entity>> mushroom_vec;
    vector<array<int,2>> mushroomPositions;

    vector<shared_ptr<Entity>> sword_vec;
    vector<array<int,2>> swordPositions;

    vector<shared_ptr<Entity>> flea_vec;
    int fleax;
    int fleay;
    bool fleaIsHit;
    bool isFlea;

    vector<shared_ptr<Dragon>> dragon_vec;

    int dragCollisionx;
    int dragCollisiony;

    vector<vector<pair<int,int>>> pieces_;
    Grid gameBoard;
};

#endif // COLLISION_H
