#ifndef DRAGON_H
#define DRAGON_H
#include "Entity.h"


//! The Dragon segment struct.
/*!
  This struct contains the coordinates of each segment of the dragon.
  The dragon vector is a vector of these dragon segment structs.
*/
struct DragonSegment{
        int x_;
        int y_;
DragonSegment(int x, int y) {
        x_ = x;
        y_ = y;
}
};


using DragonContainer = std::vector<DragonSegment>;//vector of segments of the dragon
//! A throw class.
/*!
  This class throws an error if an invalid dragon is trying to be created.
*/
class triedToCreateInvalidDragon {};



//! The Dragon class.
/*!
  This class handles the dragon and its segments.
  The dragon is modelled as a head at the front of the vector and
  all the segments follow the trail that the head sets.
*/
class Dragon: public Entity
{
    public:
        ///Constructor for Dragon
        Dragon ();
        ///Constructor for Dragon
        ///This constructor is for the first dragon at the beginning of  the game
        ///It initialises a dragon head at a position and creates dragon segments at incremental x values behined it
        ///@param numSeg decides how long the dragon should be
        ///@param initialPosition contains the x and y starting position of the initial dragon
        ///@attention triedToCreateInvalidDragon error will be thrown if the dragon to be created is invalid
        Dragon(int numSeg, vector<int> initialPosition);//initial dragon constructor
        ///Constructor for Dragon
        ///This constructor is for new dragons that are created during the runtime of the game when it is hit
        ///thus it takes in parameters which pertain to the state of the dragon that was hit so it can be replicated
        ///@param dragVec is a vector containing dragon segments
        ///@param n_dir is the direction in which we wish the dragon to continue moving in
        ///@param hit tells the dragon whether it should be moving up or down the screen
        ///@attention triedToCreateInvalidDragon error will be thrown if the dragon to be created is invalid
        ///@note this new dragon is made from a pre-existing dragon so the segments already contain positions
        Dragon(DragonContainer dragVec, EntityOperation n_dir, bool hit);//when creating new dragons
        /// Tell the dragon which direction the head should move
        void SetDirection (EntityOperation l_dir);
        /// Get the current direction of the head of the dragon
        ///@return direction of the dragon
        EntityOperation GetDirection ();
        ///Get the position of of the head of the dragon
        ///@return tuple containing x and y coordinates
        tuple <int,int> GetEntityPosition();
        ///This is called each time the game loop is run to control the dragons automatic movements
        ///Calling Action will involve moving the dragon and checking if it collides with the sides of the screen
        ///@note this does nothing if the dragon vector is empty
        virtual void Action() override;
        /// get the vector of dragon segments of this dragon
        ///@return the vector of dragon segments
        DragonContainer getBody();
        ///get the size of each dragon segment (they are all the same size)
        ///@return an integer of the size of the dragon segments
        int GetEntitySize()override;
        ///Dragon destructor
        virtual ~Dragon();
        ///Controls a variable determining if the dragon has hit the bottom of the screen and is moving upwards or downwards
        ///@return bool which is true if the dragon has hit the bottom of the screen
        bool HitBot ();
        ///Save the coordinates of the last mushroom the head hit so it cant be hit twice
        ///@param x is the x coordinate of the last mushroom hit
        ///@param y is the y coordinate of the last mushroom hit
        ///@note this is a safety measure to stop instances of the dragon hitting a mushroom twice in quick succession
        void setLastMushroom (int x, int y);
        ///Get the coordinates of the last mushroom the dragon hit
        ///This is to prevent the dragon hitting the same dragon twice in subsequent heartbeats of the program
        ///@return tuple containing x and y coordinates of the last mushroom hit by the dragon head
        tuple<int,int> getLastMushroom ();

    protected:

    private:
        void Move();
        void CheckEdge();
        void Reset();
        int m_size = 25;
        int m_speed;
        DragonContainer m_dragonBody;
        EntityOperation m_dir;
        EntityOperation temp_dir;
        int m_numSegments;
        int mush_x;
        int mush_y;

        vector<int> m_initialPos;

        bool hitBot = false;
        int xmin = xmin_;
        int xmax = xmax_ -m_size;
        int ymin = ymin_;
        int ymax = ymax_- m_size;

        int reboundHeight = 590;


};

#endif // DRAGON_H
