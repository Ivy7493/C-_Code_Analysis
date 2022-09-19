#include "Dragon.h"

Dragon::Dragon()
{
    //ctor
}

Dragon::Dragon(int numSeg, vector<int> initialPosition)
{
    if (numSeg ==0 || initialPosition.empty())
    {
        throw triedToCreateInvalidDragon {};
    }
    m_numSegments = numSeg;//number of initial segments of the dragon
    m_initialPos.push_back(initialPosition[0]);//x and y coordinates of initial position
    m_initialPos.push_back(initialPosition[1]);
    Reset();

}
Dragon::Dragon(DragonContainer dragVec, EntityOperation n_dir, bool hit)
{
    if (dragVec.empty()||static_cast<int>(n_dir)>3)
    {
        throw triedToCreateInvalidDragon {};
    }
    m_dir = n_dir;
    m_speed = 15;
    for (auto a : dragVec)
    {
        m_dragonBody.push_back(a);
    }
    hitBot = hit;
}
void Dragon::Reset()
{

    vector<int> tempPos;
    tempPos.push_back(m_initialPos[0]);
    tempPos.push_back(m_initialPos[1]);
    for (int i=0; i<m_numSegments; i++)
    {
        m_dragonBody.push_back(DragonSegment(tempPos[0], tempPos[1]));//loop to create inial dragon and place its positions
        tempPos[0] += m_size;
    }
    SetDirection(EntityOperation::moveLeft);//this only happens for the first dragon
    m_speed = 15;
}

void Dragon::SetDirection(EntityOperation l_dir)
{
    m_dir = l_dir;
}

EntityOperation Dragon::GetDirection()
{
    return m_dir;
}
int Dragon::GetEntitySize()
{
    return m_size;
}

tuple<int,int> Dragon::GetEntityPosition()
{

    return {m_dragonBody.front().x_,m_dragonBody.front().y_};
}
void Dragon::Action()
{
    if (m_dragonBody.empty())
    {
        return;    //if there is no body segment
    }

    CheckEdge();
    Move();



}
void Dragon::Move()
{

    for (int i = m_dragonBody.size() - 1; i >0; --i)
    {
        m_dragonBody[i].x_ = m_dragonBody[i - 1].x_;
        m_dragonBody[i].y_ = m_dragonBody[i - 1].y_;
        //iterates from the tail segment towards head
    }   //makes current segment the same as the segment upstream

    if (m_dir == EntityOperation::moveLeft)
    {
        m_dragonBody[0].x_ -=m_size;
    }
    else if (m_dir == EntityOperation::moveRight)
    {
        m_dragonBody[0].x_+=m_size;
    }
    else if (m_dir == EntityOperation::moveUp)
    {
        m_dragonBody[0].y_-=m_size;
    }
    else if (m_dir == EntityOperation::moveDown)
    {
        m_dragonBody[0].y_+=m_size;
    }
}
DragonContainer Dragon::getBody()
{

    return m_dragonBody;
}

bool Dragon::HitBot()
{
    return hitBot;
}

void Dragon::CheckEdge()
{
    if (hitBot == false)
    {
        //check if we are already moving down on left hand side of screen
        if (m_dragonBody[0].x_ == xmin+1 && m_dir == EntityOperation::moveDown )
        {
            m_dir = EntityOperation::moveRight;
        }
        //if already moving down on right hand side of screen
        if (m_dragonBody[0].x_ == xmax-1 && m_dir == EntityOperation::moveDown)
        {
            m_dir = EntityOperation::moveLeft;
        }
        //check left side of screen
        if (m_dragonBody[0].x_ <=xmin)
        {
            m_dir = EntityOperation::moveDown;
            m_dragonBody[0].x_ = xmin+1;
        }
        //check right side of screen
        if (m_dragonBody[0].x_ >=xmax && m_dragonBody[0].y_ != ymin)//the && is checking if its the first time entering the screen
        {
            m_dir = EntityOperation::moveDown;
            m_dragonBody[0].x_ = xmax-1;
        }

    }
    if (hitBot == true)
    {
        if (m_dragonBody[0].x_ == xmin+1 && m_dir == EntityOperation::moveUp )
        {
            m_dir = EntityOperation::moveRight;
        }
        //if already moving up on right hand side of screen
        if (m_dragonBody[0].x_ == xmax-1 && m_dir == EntityOperation::moveUp)
        {
            m_dir = EntityOperation::moveLeft;
        }
        //check left side of screen
        if (m_dragonBody[0].x_ <=xmin)
        {
            m_dir = EntityOperation::moveUp;
            m_dragonBody[0].x_ = xmin+1;
        }
        //check right side of screen
        if (m_dragonBody[0].x_ >=xmax)//the && is checking if its the first time entering the screen
        {
            m_dir = EntityOperation::moveUp;
            m_dragonBody[0].x_ = xmax-1;
        }
    }
    if (m_dragonBody[0].y_>=ymax)
    {
        m_dir = EntityOperation::moveUp;
        hitBot = true;
        Move();
    }
    if (m_dragonBody[0].y_<reboundHeight && hitBot == true)
    {
        hitBot = false;
        m_dir = EntityOperation::moveDown;
        Move();
    }
}

void Dragon::setLastMushroom (int x, int y)
{
    mush_x = x;
    mush_y = y;
}

tuple<int,int> Dragon::getLastMushroom ()
{
    return{mush_x, mush_y};
}

Dragon::~Dragon()
{
    //dtor
}
