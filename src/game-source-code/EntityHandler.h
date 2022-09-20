#ifndef ENTITYHANDLER_H
#define ENTITYHANDLER_H
#include<vector>
#include<memory>
#include<time.h>
#include<cmath>

#include "Entity.h"
#include "UserInput.h"
#include "Knight.h"
#include "Dragon.h"
#include "Sword.h"
#include "Mushroom.h"
#include "Bomb.h"
#include "Flea.h"
#include "Grid.h"

using namespace std;
//! The EntityHandler class.
/*!
  This class controls the interactions between all the entities and is closely related to the
  collision class.  It contains all the vectors of different types of entities which must be kept track
  of durig the runtime of the program.
*/

class EntityHandler
{
public:
    ///EntityHandler constructor
    EntityHandler();
    ///EntityHandler destructor
    virtual ~EntityHandler();
    ///Update the entities positions and check collisions between them
    void UpdateEntities(unique_ptr<Knight>& knightAlias);
    ///Gets a randomly generated number used for random mushroom location generation
    ///@return integer coordinate
    static int GetRandomNumber(int xOrY);
    ///Generate a random mushroom positions within the bounds of the screen
    static void MakeMushroomField();
    ///Get the vector of Mushroom Positions
    ///@return vector of 2x2 arrays of Mushroom Coordinates
    static vector<array<int,2>>& MushroomPositions();
    ///Get the vector of Sword Positions
    ///@return vector of 2x2 arrays of Sword Coordinates
    static vector<array<int,2>>& SwordPositions();
    ///Get the vector of Bomb Positions
    ///@return vector of 2x2 arrays of Bomb Coordinates
    static vector<array<int,2>>& BombPositions();
    ///Get the vector of shared pointers pointing to swords
    ///@return vector of shared pointers pointing to swords
    static vector<shared_ptr<Entity>>& GetSwordVec();
    ///Get the vector of shared pointers pointing to dragons
    ///@return vector of shared pointers pointing to dragons
    static vector<shared_ptr<Dragon>>& GetDragonVec();
    ///Get the vector of shared pointers pointing to mushrooms
    ///@return vector of shared pointers pointing to mushrooms
    static vector<shared_ptr<Entity>>& GetMushroomVec();
    ///Get the vector of shared pointers pointing to bombs
    ///@return vector of shared pointers pointing to bombs
    static vector<shared_ptr<Entity>>& GetBombVec();
    ///Add a new sword to the sword vector and update the swordPositions vector
    ///@param int h_x is the x coordinate of the new sword
    ///@param int h_y is the y coordinate of the new sword
    ///@param h_ptr is a shared pointer pointing to the new sword that was created
    static void NewSword (int h_x, int h_y, shared_ptr<Entity> h_ptr);
    ///Get the position of the flea
    ///@return a tuple of the x and y coordinates of the flea
    static tuple<int,int> GetFleaPosition();
    ///Get the vector of all the current flea objects
    ///@return a vector of shared pointers pointing to fleas
    static vector<shared_ptr<Entity>>& GetFleaVec();
    ///Initialise the first dragon at the beginning of the game
    ///@note this only occurs once when the game first runs
    static void InitialiseDragon ();
    ///A bool function that keeps track of whether a bomb has been hit and is in the process of exploding
    ///@return bool that is true if the bomb has been hit and is exploding
    static bool isExploding();
    ///Get the position of the explosion
    ///@return returns a tuple of the position the bomb is exploding at
    tuple<int,int> BoomPosition();
    ///Get whether the knight is immune or not
    ///@return returns a bool of whether the knight cannot be hit or not
    static bool IsKnightImmune();
    ///Get the state of the flea
    ///@return returns a bool whether there is a flea or not
    static bool IsFlea();
    ///Deletes a sword object from the sword vector as well as its positions
    ///@param swordNum is the number of the sword associated with its position in its corresponding vectors
    static void DeleteSword(int swordNum);
    ///Deletes a mushroom from the mushroom vector as well as its position
    ///@param mushNum is the number of the mushroom associated with its position in its corresponding vectors
    static void DeleteMushroom(int mushNum);
    ///Deletes a bomb from the bomb vector as well as its position
    ///@param bombNum is the number of the bomb associated with its position in its corresponding vectors
    static void DeleteBomb(int bombNum);
    /// Deletes the flea from the screen and clears its position
    static void DeleteFlea();
    /// This function only adds the second dragon after the initial dragon is destroyed
    ///@param drag is the new dragon that is being pushed back onto the dragon vector
    ///@param dragDelete is the number of the dragon that needs to be deleted for this new one to be added
    ///@param lastMushx sets the x position of the last mushroom the original dragon hit.
    ///@param lastMushy sets the y position of the last mushroom the original dragon hit.
    static void DragonAddition(shared_ptr<Dragon>& drag,int dragDelete,int lastMushx,int lastMushy);
    /// AddMushroom adds a mushroom to the mushroom vector
    /// @param mush_x is the x-coordinate of the new mushroom that is added
    /// @param mush_y is the y-coordinate of the new mushroom that is added
    static void AddMushroom(int mush_x,int mush_y);
    /// AddBomb adds a bomb to the bomb vector
    static void AddBomb();
    /// SetHit sets various bools
    ///@param immunity is true if the knight cannot get hit by the centipede
    ///@param explode is true if the bomb has exploded and should still register as exploding
    ///@param sBomb is true if the bomb has been hit by a sword
    ///@param fHit is true if the flea has been hit by a sword
    static void SetHit(bool immunity,bool explode,bool sBomb,bool fHit);
    ///SetCollision sets the position of a bomb's explosion
    ///@param boomx sets the x-coordinate of the explosion
    ///@param boomy sets the y-coordinate of the explosion
    static void SetCollision(int boomx,int boomy);
    ///AddDragon adds a dragon to the dragon vector
    ///@param drag is the dragon that will be added to the vector
    static void AddDragon(shared_ptr<Dragon> drag);
    /// OffWithHead deletes a dragon object at a specificpoint in the vector
    /// @param num is the number of the dragon in the vector that should be deleted
    static void offWithHead(int num);

private:

    static bool CheckValidMushroom(int coordinate,int currentMushroom,int vecSize);
    static bool CheckValidBomb(int,int);
    static void UpdateSwords(EntityOperation shoot,unique_ptr<Knight>& knightAlias);
    static void UpdateFleas();
    static void UpdateExplosion();
    static bool CoinFlip();
    static void FleaMushrooms();//drops mushrooms along the flea's path if there are not too many mushrooms on the screen already


    bool shortTime;
    UserInput userInput;
    static EntityOperation operation;
    static Mushroom checkMushroom;
    static shared_ptr<Entity> newMushroom;
    static float mushroomBox;

    static vector<shared_ptr<Entity>> sword_vec;
    static vector<array<int,2>> swordPositions;

    static vector<shared_ptr<Dragon>> dragon_vec;
    static bool hitKnight;
    //static int knightSize;
    static vector<shared_ptr<Entity>> mushroom_vec;
    static vector<array<int,2>> mushroomPositions;
    static bool mushCheck_x;
    static bool mushCheck_y;
    static int previousMushroom;
    static float mushroomBox_x;
    static float mushroomBox_y;
    static int tempMushx;
    static int tempMushy;
    static int maxMushrooms;

    static vector<shared_ptr<Entity>> bomb_vec;
    static vector<array<int,2>> bombPositions;

    static int throwRate;
    static int swordCounter;

    static int initialMushroomAmount;

    static int yWindowLength;
    static int xWindowLength;

    static bool mushDragon;
    static bool knightIsImmune;
    static int immunityCounter;


    static int timeBomb;
    static int waitBomb;
    static int tempBombx;
    static int tempBomby;
    static bool swordBomb;
    static bool exploding;
    static int explodeTime;
    static array<int,2> boomPosition;

    static int waitFlea;
    static int randFlea;
    static bool isFlea;
    static vector<shared_ptr<Entity>> flea_vec;
    static int fleax;
    static int fleay;
    static bool fleaIsHit;

    static Grid gameBoard;
};
#endif // ENTITYHANDLER_H
