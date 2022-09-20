#ifndef GRID_H
#define GRID_H

#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include<utility>

using namespace std;
//! The Grid class.
/*!
  This class handles the grid vector.
*/
class Grid
{
    public:
        ///Grid Constructor
        ///Initialises the game board grid vector
        Grid();
        ///Gets the grid
        ///@return returns the vector of vectors containing grid coordinate pairs
        static vector<vector<pair<int,int>>>& getGrid();
        ///Grid Destructor
        virtual ~Grid();
        ///Updates the grid
        ///@param x
        ///@param y
        ///@param remap
        ///@param vecNum
        static void UpdateGrid(int ,int ,int ,int vecNum);

    protected:

    private:
        static int boardx;
        static int boardy;
        static vector<vector<pair<int,int>>> gameBoard;

};
#endif // GRID_H
