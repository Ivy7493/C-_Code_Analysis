#include "Collision.h"
Collision::Collision()
{
    //ctor
    knightIsImmune = false;
    immunityCounter =0;
    dragKnightCheck = false;
    dragSwordCheck = false;
    swordBomb = false;
    Grid game;
    Grid gameBoard=game;
    exploding = false;
    isFlea =false;
    explodeTime = 0;
    auto tempHandler = EntityHandler();
    entityHandler_ = tempHandler;
    fleax = 0;
    fleay = 0;
}

Collision::~Collision()
{
    //dtor
}

void Collision::CheckCollisions(unique_ptr<Knight>& knightAlias)
{
    mushroomPositions = entityHandler_.MushroomPositions();
    swordPositions = entityHandler_.SwordPositions();
    bombPositions = entityHandler_.BombPositions();
    tie(boomPosition[0],boomPosition[1]) = entityHandler_.BoomPosition();
    dragon_vec = entityHandler_.GetDragonVec();
    bomb_vec = entityHandler_.GetBombVec();
    sword_vec = entityHandler_.GetSwordVec();
    mushroom_vec = entityHandler_.GetMushroomVec();
    flea_vec = entityHandler_.GetFleaVec();
    if(entityHandler_.IsFlea())
    {
        tie(fleax,fleay)=entityHandler_.GetFleaPosition();
        isFlea=true;
    }
    else
    {
        isFlea=false;
    }

    KnightDragCollision(knightAlias);

    CollisionSword();

    CollisionMushSword();

    CollisionDragMush();

    UpdateExplosion();

    entityHandler_.SetHit(knightIsImmune,exploding,swordBomb,fleaIsHit);
    entityHandler_.SetCollision(boomPosition[0],boomPosition[1]);
}

void Collision::KnightDragCollision(unique_ptr<Knight>& knightAlias)
{
    if(knightIsImmune)
    {
        if(immunityCounter==40)
            {
                knightIsImmune=false;

            }
        immunityCounter++;
    }
    else if(!knightIsImmune)
    {
        bool hit =false;
        int knightx=0;
        int knighty=0;

        tie(knightx,knighty) = knightAlias->GetEntityPosition();
        dragKnightCheck = true;
        hit = DragonSegmentsCollision(knightx,knighty,knightSize);
        if(hit)
        {
            knightIsImmune=true;
            immunityCounter=0;
            knightAlias->LoseLife();
        }
        dragKnightCheck = false;
    }
}

void Collision::BombCollision(int x, int y, int entSize)
{
    pieces_=gameBoard.getGrid();
    int entXR = x+entSize;
    int entYB = y+entSize;
    for(int a = 0; a<bombPositions.size(); a++)
    {

        int bXL = bombPositions[a][0];
        int bYT = bombPositions[a][1];
        int bXR = bXL+bomb_vec[a]->GetEntitySize();
        int bYB = bYT+bomb_vec[a]->GetEntitySize();

        if(((x>=bXL&&x<=bXR)||(entXR>=bXL&&entXR<=bXR))&&(y<=bYB))
        {

            swordBomb = true;
            exploding = true;
            boomPosition = {bXL-25,bYT-25};
            entityHandler_.DeleteBomb(a);

            for(int i=(((bYT-1)/25)-1); i<=((bYT-1)/25)+1; i++)
            {
                auto rowIt = pieces_[i].begin();
                for(int j =(((bXL-1)/25)-1); j<=(((bXL-1)/25)+1); j++)
                {
                    auto xIt = rowIt+j;
                    if(xIt->first==3)
                    {
                        entityHandler_.DeleteMushroom((xIt->second));
                    }
                }
            }
        }
    }
}

void Collision::CollisionDragMush()
{
    for (int i=0; i < mushroom_vec.size(); i++)
    {

        int mushSize = 25;
        int mushleft = mushroomPositions[i][0];
        int mushright = mushroomPositions[i][0]+mushSize;
        int mushtop = mushroomPositions[i][1];
        for(int j= 0; j < dragon_vec.size(); j++)
        {

            auto drag = *dragon_vec[j];//drag now is a dragon object
            auto d_x = 0;
            auto d_y = 0;
            tie(d_x, d_y) = drag.GetEntityPosition();//x and y of the dragon head

            auto dSize = drag.GetEntitySize();//size of each segment
            auto dir = drag.GetDirection();
            auto hitB = drag.HitBot();
            int dragleft = d_x;

            int dragright = d_x + dSize;

            auto m_x =0;
            auto m_y =0;
            tie(m_x, m_y) = dragon_vec[j]->getLastMushroom();
            if(m_x != mushleft && m_y !=mushtop)
                {
                if (mushtop<=810)//to avoid problems with bottom and top of screen
                {
                    if (mushtop<=d_y+3 && mushtop>=d_y-3)//if this mushroom is around the same height as the dragon
                    {
                        if(!hitB)
                        {
                            DragDirection(hitB,dir,mushleft,mushright,dragleft,dragright,mushtop,j);
                        }
                        else if(hitB&&mushtop>=601)
                        {
                            DragDirection(hitB,dir,mushleft,mushright,dragleft,dragright,mushtop,j);
                        }
                    }
                }

            }
        }
    }
}
void Collision::DragDirection(bool hitBot,EntityOperation dir,int mushleft,int mushright,int dragleft,int dragright,int mushtop,int position)
{
    auto UpOrDown = EntityOperation::moveDown;
    if(hitBot)
        UpOrDown = EntityOperation::moveUp;

    if(dir == EntityOperation::moveLeft)
    {
        if (dragleft<=mushright)
        {
            dragon_vec[position]->SetDirection(UpOrDown);
            dragon_vec[position]->Action();
            dragon_vec[position]->SetDirection(EntityOperation::moveRight);
            dragon_vec[position]->setLastMushroom(mushleft, mushtop);
        }
    }
    if (dir == EntityOperation::moveRight)
    {
        if (dragright>=mushleft)
        {
            dragon_vec[position]->SetDirection(UpOrDown);
            dragon_vec[position]->Action();
            dragon_vec[position]->SetDirection(EntityOperation::moveLeft);
            dragon_vec[position]->setLastMushroom(mushleft, mushtop);
        }
    }
}

void Collision::CollisionMushSword()
{


    //bool checkMushCollision = false
    for(int i = 0; i<mushroom_vec.size(); i++)
    {
        int mushbot = mushroomPositions[i][1]+25;
        int mushleft = mushroomPositions[i][0];
        int mushright = mushroomPositions[i][0]+25;
        for(int j = 0; j<sword_vec.size(); j++)
        {
            int swordright = swordPositions[j][0]+10;
            int swordleft = swordPositions[j][0];
            if((swordPositions[j][1]<=mushbot&&(swordPositions[j][1]+15)>=mushroomPositions[i][1])&&((swordright<=mushright&&swordright>=mushleft)||(swordleft>=mushleft&&swordleft<=mushright)))
            {

                entityHandler_.DeleteSword(j);
                if(mushroom_vec[i]->GetLives() ==0)
                {

                    entityHandler_.DeleteMushroom(i);
                    //i--;
                }
                else
                {
                    mushroom_vec[i]->LoseLife();
                }
            }
        }

    }
}

void Collision::CollisionSwordFlea(int s_x, int s_y,int swordNum)
{
    int fleaxr = fleax+25;
    int fleayb = fleay+25;
    if(s_x>=fleax&&s_x<=fleaxr&&s_y<=fleayb&&s_y>=fleay)
    {
        fleax =0;
        fleay = 0;
        entityHandler_.DeleteSword(swordNum);
        entityHandler_.DeleteFlea();
    }
}
void Collision::CollisionSword()
{
    if (sword_vec.empty()){return;}
    swordBomb = false;
    bool collided = false;

    for(int i= 0; i < sword_vec.size(); i++)//iterating through vector of shared sword pointers of type entity
    {

        dragSwordCheck = true;
        int s_x = swordPositions[i][0];

        int s_y = swordPositions[i][1];

        collided = DragonSegmentsCollision(s_x+7,s_y,2);
        if(collided)
        {

            entityHandler_.DeleteSword(i);
        }
        BombCollision(s_x,s_y,15);
        if(swordBomb)
        {

            entityHandler_.DeleteSword(i);
            swordBomb=false;
        }

        CollisionSwordFlea(s_x+8,s_y,i);

    }
    dragSwordCheck = false;

}

bool Collision::DragonSegmentsCollision(int s_x,int s_y,int creaSize)
{
    bool collided = false;
    int s_xr = s_x +creaSize;
    int s_yb = s_y +creaSize;
    for(int j= 0; j < dragon_vec.size(); j++)//iterating through vector of shared dragon pointers of type dragon
    {
        collided = false;
        auto drag = *dragon_vec[j];//drag now is a dragon object
        auto seg_vec = drag.getBody();//vector of dragon segments
        auto dSize = drag.GetEntitySize();//size of each segment

        dragCollisionx = 0;
        dragCollisiony = 0;

        auto dir = drag.GetDirection();

        for(int k= 0; k < seg_vec.size(); k++)//iterating through each segment of the current dragon
        {
            //these are the bounds of this segment of this dragon object at its current position
            int xlo = seg_vec[k].x_;        //left edge of square
            int xhi = xlo+dSize;            //right edge of square
            int yhi = seg_vec[k].y_;        //top of square
            int ylo = yhi+dSize;            //bottom of square

            if(((s_yb<=ylo && s_yb>=yhi)||(s_y<=ylo && s_y>=yhi)))
            {
                if((s_x>= xlo && s_x<=xhi)||(s_xr>= xlo && s_xr<=xhi))
                {
                    collided =true;
                    if(dragSwordCheck&&!(dir==EntityOperation::moveUp||dir==EntityOperation::moveDown))
                    {
                        dragCollisionx = xlo;
                        dragCollisiony = yhi;
                        collided = true;
                        entityHandler_.AddMushroom(xlo,yhi);
                        if (k == seg_vec.size()-1&&seg_vec.size()!=1)//if you hit the last segment
                        {

                            vector<DragonSegment> originalDragVec;
                            for (auto m = 0; m<seg_vec.size()-1; m++)//start from 1 to skip the head
                            {
                                originalDragVec.push_back(seg_vec[m]);
                            }
                            auto newDrag4 = shared_ptr<Dragon> {new Dragon(originalDragVec, drag.GetDirection(), drag.HitBot())};//create new dragon
                            entityHandler_.DragonAddition(newDrag4,j,dragCollisionx,dragCollisiony);

                            return collided;
                        }
                        if (k == 0)//handling the head being hit
                        {
                            if (seg_vec.size()==1)//if there is only a head segment
                            {
                                //vector<shared_ptr<Dragon>>::iterator nth = dragon_vec.begin() + j;
                                //dragon_vec.erase(nth);

                                entityHandler_.offWithHead(j);
                                j--;
                                return collided;
                            }
                            else{

                            //else there are multiple segments and we make a new dragon
                            vector<DragonSegment> originalDragVec;

                            for (auto m = 1; m<seg_vec.size(); m++)//start from 1 to skip the head
                            {
                                originalDragVec.push_back(seg_vec[m]);
                            }
                            auto newDrag3 = shared_ptr<Dragon> {new Dragon(originalDragVec, drag.GetDirection(),drag.HitBot())};//create new dragon
                            entityHandler_.DragonAddition(newDrag3,j,dragCollisionx,dragCollisiony);
                            //CollisionDragMush();
                            return collided;


                            }

                        }
                        //now we just collided somewhere inside the dragon body
                        vector<DragonSegment> newDragVec;

                        for (auto l =k+1; l<seg_vec.size(); l++)
                        {
                            newDragVec.push_back(seg_vec[l]);   //placing segments into new dragon body
                        }

                        vector<DragonSegment> originalDragVec;
                        for (auto m = 0; m<k; m++)
                        {
                            originalDragVec.push_back(seg_vec[m]);
                        }
                        auto newDrag1 = shared_ptr<Dragon> {new Dragon(originalDragVec, drag.GetDirection(),drag.HitBot())};//add old dragon
                        entityHandler_.DragonAddition(newDrag1,j,dragCollisionx,dragCollisiony);

                        auto newDrag2 = shared_ptr<Dragon> {new Dragon(newDragVec, drag.GetDirection(),drag.HitBot())};//create new dragon
                        entityHandler_.AddDragon(newDrag2);
                        CollisionDragMush();
                    }
                }
            }
            else
                collided = false;
        }
    }
    return collided;
}

void Collision::UpdateExplosion()
{
    if(!exploding)
        return;
    if(exploding&&explodeTime<35)
        explodeTime++;
    if(exploding&&explodeTime==35)
    {
        exploding = false;
        explodeTime = 0;
    }
}
