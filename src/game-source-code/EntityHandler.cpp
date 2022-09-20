#include "EntityHandler.h"

vector<shared_ptr<Entity>> EntityHandler::sword_vec;
vector<array<int,2>> EntityHandler::swordPositions;
int EntityHandler::swordCounter;
EntityOperation EntityHandler::operation;
Grid game;
Grid EntityHandler::gameBoard=game;
int EntityHandler::throwRate=8;

int EntityHandler::initialMushroomAmount = 15;

int EntityHandler::yWindowLength = 850;
int EntityHandler::xWindowLength = 1550;

bool EntityHandler::mushDragon;
//bool EntityHandler::dragSwordCheck;
//bool EntityHandler::dragKnightCheck;

int EntityHandler::tempBombx;
int EntityHandler::tempBomby;
bool EntityHandler::swordBomb;
//bool EntityHandler::shortTime = true;
int EntityHandler::previousMushroom = 0;
//int EntityHandler::dragCollisionx = 0;
//int EntityHandler::dragCollisiony = 0;
int EntityHandler::timeBomb = 0;
int EntityHandler::randFlea =0;
bool EntityHandler::exploding = false;
int EntityHandler::explodeTime = 0;
bool EntityHandler::knightIsImmune = false;
//int EntityHandler::immunityCounter = 0;
//int EntityHandler::knightSize=26;
bool EntityHandler::hitKnight=false;
vector<shared_ptr<Entity>> EntityHandler::flea_vec;
//vector<vector<pair<int,int>>> EntityHandler::pieces_;

array<int,2> EntityHandler::boomPosition;
int EntityHandler::fleax = 0;
int EntityHandler::fleay = 0;
bool EntityHandler::mushCheck_x;
bool EntityHandler::mushCheck_y;
Mushroom EntityHandler::checkMushroom;
int EntityHandler::maxMushrooms = 21;
shared_ptr<Entity> EntityHandler::newMushroom;
float EntityHandler::mushroomBox;
vector<shared_ptr<Dragon>> EntityHandler::dragon_vec;
vector<shared_ptr<Entity>> EntityHandler::mushroom_vec;
vector<array<int,2>> EntityHandler::mushroomPositions;
vector<shared_ptr<Entity>> EntityHandler::bomb_vec;
vector<array<int,2>> EntityHandler::bombPositions;
bool EntityHandler::isFlea;
int EntityHandler::waitFlea;
bool EntityHandler::fleaIsHit;
int EntityHandler::waitBomb;
int EntityHandler::tempMushx;
int EntityHandler::tempMushy;

EntityHandler::EntityHandler()
{
    //ctor
    srand(time(0));
    waitBomb = GetRandomNumber(20);
    waitFlea = GetRandomNumber(20);
    //auto gameBoard = unique_ptr<Grid>(new Grid());

}

EntityHandler::~EntityHandler()
{
    //dtor
}

void EntityHandler::DeleteSword(int swordNum)
{
    if (sword_vec.empty())
        {
            return;
        }

    auto swordIt = sword_vec.begin()+swordNum;

    sword_vec.erase(swordIt);

}

void EntityHandler::DeleteMushroom(int mushNum)
{
    auto mushIt = mushroom_vec.begin()+mushNum;
    int x;
    int y;
    tie(x,y)=mushroom_vec[mushNum]->GetEntityPosition();
    mushroom_vec.erase(mushIt);
    gameBoard.UpdateGrid(((x+1)/25)-1,((y+1)/25)-1,0,0);
    mushroomPositions.clear();
    for(int i = 0;i<mushroom_vec.size();i++)
    {
            tie(tempMushx,tempMushy) = mushroom_vec[i]->GetEntityPosition();
            mushroomPositions.push_back({tempMushx,tempMushy});
    }
}
void EntityHandler::AddMushroom(int mush_x,int mush_y)
{
    newMushroom = shared_ptr<Entity> {new Mushroom{mush_x,mush_y}};
    mushroom_vec.push_back(newMushroom);
    mushroomPositions.push_back({mush_x,mush_y});
    gameBoard.UpdateGrid(((mush_x+1)/25)-1,((mush_y+1)/25)-1,3,(mushroom_vec.size()-1));
}

void EntityHandler::DeleteBomb(int bombNum)
{
    auto bombIt = bomb_vec.begin()+bombNum;
    int x;
    int y;
    tie(x,y)=bomb_vec[bombNum]->GetEntityPosition();
    bomb_vec.erase(bombIt);
    gameBoard.UpdateGrid(((x+1)/25)-1,((y+1)/25)-1,0,0);
    bombPositions.clear();

    for(int i = 0;i<bomb_vec.size();i++)
    {
            tie(tempBombx,tempBomby) = bomb_vec[i]->GetEntityPosition();
            bombPositions.push_back({tempBombx,tempBomby});
    }
}

void EntityHandler::DeleteFlea()
{
    flea_vec.clear();
    isFlea = false;
    randFlea = 0;
    waitFlea = GetRandomNumber(200);
}
void EntityHandler::UpdateSwords(EntityOperation shoot,unique_ptr<Knight>& knightAliasInSword)
{
    auto x = 0;
    auto y = 0;
    swordPositions.clear();
    for(int i= 0; i < sword_vec.size(); i++)
    {
        sword_vec[i]->Action();//moving each sword in the vector of swords
        tie(x,y) = sword_vec[i]->GetEntityPosition();
        if (y<0)
        {
            DeleteSword(i);
        }
        else{swordPositions.push_back({x,y});}
        //entering the new positions of each sword into the swordPositions vector
    }
    swordCounter++;
    if (operation == EntityOperation::throwSword && swordCounter >= throwRate)
    {
        swordCounter = 0;
        tie(x,y) = knightAliasInSword->GetEntityPosition();//getting knight current position
        auto tempSword = shared_ptr<Entity> {new Sword{x,y-25}};
        sword_vec.push_back(tempSword);
        tie(x,y) = tempSword->GetEntityPosition();
        swordPositions.push_back({x,y});
    }
}

bool EntityHandler::CoinFlip()
{
    if(((rand()%101+1)-1)>88)
        return true;
    else
        return false;
}
void EntityHandler::FleaMushrooms()
{
    if (mushroom_vec.size()<maxMushrooms&&CoinFlip())
    {
        int tempMushy = ((round(fleay/25))*25-1);
        AddMushroom(fleax,tempMushy);
    }
    else return;
}

void EntityHandler::UpdateFleas()
{
    if(!isFlea && randFlea == waitFlea)
    {
        isFlea = true;
        int tempx = GetRandomNumber(xWindowLength)+24;
        auto flea = shared_ptr<Entity> {new Flea{tempx,24}};
        flea_vec.push_back(flea);
    }
    if(isFlea)
    {
        for(int fleacounter = 0; fleacounter<flea_vec.size(); fleacounter++)
        {
            flea_vec[fleacounter]->Action();
            int tempx;
            int tempy;
            tie(tempx,tempy)=flea_vec[0]->GetEntityPosition();

            if(tempy>yWindowLength+24)
            {
                DeleteFlea();
            }
            FleaMushrooms();
        }
    }
    randFlea++;
}


void EntityHandler::UpdateEntities(unique_ptr<Knight>& knightAlias)
{
    operation = userInput.GetKeys();
    knightAlias->Action(operation);
    timeBomb++;
    AddBomb();
    //UpdateExplosion();

    UpdateSwords(operation,knightAlias);
    UpdateFleas();

    for (auto d: dragon_vec)//get dragon to move
    {
        d->Action();
    }
}

int EntityHandler::GetRandomNumber(int xOrY)
{
    int coordinate =rand() % xOrY + 25;
    mushroomBox = coordinate/25;//realised too late we should have been using a grid this whole time
    coordinate = (round(mushroomBox)*25)-1;
    return coordinate;
}

bool EntityHandler::CheckValidMushroom(int coordinate,int currentMushroom,int vecSize)
{
    for(int j=0; j<vecSize; j++)
    {
        if(mushroomPositions[j][coordinate]==currentMushroom)
            return false;
        if(abs(mushroomPositions[j][coordinate]-currentMushroom)<=checkMushroom.GetEntitySize())
            return false;
    }
    return true;
}

void EntityHandler::MakeMushroomField()
{
    int temp_mush_x;
    int temp_mush_y;

    mushCheck_x = true;
    mushCheck_y = true;

    for(int i = 0; i<initialMushroomAmount; i++)
    {
        temp_mush_x = GetRandomNumber(xWindowLength-50);
        temp_mush_y = GetRandomNumber(yWindowLength-325);

        if(i>0)
        {
            mushCheck_x = CheckValidMushroom(0,temp_mush_x,mushroom_vec.size());
            mushCheck_y = CheckValidMushroom(1,temp_mush_y,mushroom_vec.size());

            if(mushCheck_x||mushCheck_y)
                AddMushroom(temp_mush_x,temp_mush_y);
            else
                i--;
        }
        else if (i==0)
            {AddMushroom(temp_mush_x,temp_mush_y);
            auto tempBomb = shared_ptr<Entity>{new Bomb(temp_mush_x,temp_mush_y)};
            bomb_vec.push_back(tempBomb);
            bombPositions.push_back({temp_mush_x-25,temp_mush_y+25});}
    }

}
bool EntityHandler::CheckValidBomb(int tempx,int tempy)
{
    if (bomb_vec.size()>=4){return false;}
    if(!CheckValidMushroom(0,tempx,mushroomPositions.size())||!CheckValidMushroom(1,tempy,mushroomPositions.size())){return false;}
    return true;
}

void EntityHandler::AddBomb()
{
    if (timeBomb==waitBomb)
    {
        waitBomb = GetRandomNumber(50);
        tempBombx = GetRandomNumber(xWindowLength-50);
        tempBomby = GetRandomNumber(yWindowLength-50);
        if(CheckValidBomb(tempBombx,tempBomby))
        {
            auto tempBomb = shared_ptr<Entity>{new Bomb(tempBombx,tempBomby)};
            bomb_vec.push_back(tempBomb);
            bombPositions.push_back({tempBombx,tempBomby});
            timeBomb = 0;
            gameBoard.UpdateGrid(((tempBombx+1)/25)-1,((tempBomby+1)/25)-1,4,bomb_vec.size()-1);
        }
        else
            timeBomb = 0;
    }
}



vector<array<int,2>>& EntityHandler::BombPositions()
{
    return bombPositions;
}
vector<shared_ptr<Entity>>& EntityHandler::GetBombVec()
{
    return bomb_vec;
}

vector<array<int,2>>& EntityHandler::MushroomPositions()
{
    return mushroomPositions;
}

vector<array<int,2>>& EntityHandler::SwordPositions()
{
    return swordPositions;
}

void EntityHandler::NewSword (int h_x, int h_y, shared_ptr<Entity> h_ptr )
{
    array<int,2> tempArr = {h_x, h_y};
    swordPositions.push_back(tempArr);
    sword_vec.push_back(h_ptr);
}

vector<shared_ptr<Entity>>& EntityHandler::GetSwordVec()
{
    return sword_vec;
}
vector<shared_ptr<Dragon>>& EntityHandler::GetDragonVec()
{
    return dragon_vec;
}
void EntityHandler::InitialiseDragon()
{
     vector<int> vect {1500, 24};//starting position
     dragon_vec.push_back(shared_ptr<Dragon>{new Dragon(12, vect)});
}

void EntityHandler::DragonAddition(shared_ptr<Dragon>& drag,int dragDelete,int lastMushx,int lastMushy)
{
    vector<shared_ptr<Dragon>>::iterator nth = dragon_vec.begin() + dragDelete;
    dragon_vec.erase(nth);
    dragon_vec.push_back(drag);
    dragon_vec[dragDelete]->setLastMushroom(lastMushx,lastMushy);
}


vector<shared_ptr<Entity>>& EntityHandler::GetMushroomVec()
{
    return mushroom_vec;
}

bool EntityHandler::isExploding()
{
    return exploding;
}

tuple<int,int> EntityHandler::BoomPosition()
{
    return{boomPosition[0],boomPosition[1]};
}
bool EntityHandler::IsKnightImmune()
{
    return knightIsImmune;
}

tuple<int,int> EntityHandler::GetFleaPosition()
{
    tie(fleax,fleay)=flea_vec[0]->GetEntityPosition();
    return{fleax,fleay};
}
vector<shared_ptr<Entity>>& EntityHandler::GetFleaVec()
{
    return flea_vec;
}
bool EntityHandler::IsFlea()
{
    return isFlea;
}

void EntityHandler::SetHit(bool immunity,bool explode,bool sBomb,bool fHit)
{
    knightIsImmune = immunity;
    swordBomb = sBomb;
    exploding = explode;
    fleaIsHit =fHit;
}

void EntityHandler::SetCollision(int boomx,int boomy)
{
    boomPosition[0]=boomx;
    boomPosition[1]=boomy;
}

void EntityHandler::AddDragon(shared_ptr<Dragon> drag)
{
    dragon_vec.push_back(drag);
}
void EntityHandler::offWithHead(int num)
{
    vector<shared_ptr<Dragon>>::iterator nth = dragon_vec.begin() + num;
    dragon_vec.erase(nth);
}
