#include <iostream>
using namespace std;

class Numbers
{
    public:
        int a;
        int b;
};

int main()
{
    //declaring object to the class
    Numbers Num;
    //assign values to a and b 
    Num.a = 100;
    Num.b = 200;
    //print the values
    cout<<"Value of Num.a: "<<Num.a<<endl;
    cout<<"Value of Num.b: "<<Num.b<<endl;
    
    return 0;
}