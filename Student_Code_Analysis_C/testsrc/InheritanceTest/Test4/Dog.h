#include "animal.h"

class Dog : private animal
{
    public:
        void bark();
        int b;

    private:
        int c;
};