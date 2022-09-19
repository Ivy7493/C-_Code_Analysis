#include "Grid.h"


int Grid::boardx=62;
int Grid::boardy = 34;
vector<vector<pair<int,int>>> Grid::gameBoard;
Grid::Grid()
{
    vector<vector<pair<int,int>>> board(boardy,vector<pair<int,int>>(boardx,make_pair(0,0)));
    gameBoard = board;
}

vector<vector<pair<int,int>>>& Grid::getGrid()
{
    return gameBoard;
}

void Grid::UpdateGrid(int x, int y, int remap,int vecNum)
{
    auto iter = gameBoard[y].begin();

    iter=iter+x;

    iter->first=remap;
    iter->second = vecNum;
}

Grid::~Grid()
{
    //dtor
}
