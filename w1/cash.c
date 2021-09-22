#include <stdio.h>
#include <math.h>
#include <cs50.h>

/*
25
10
5
1

*/
int getInt(string text);

int main(void)
{
    int cash = getInt("Change owed: "); // get number

    //  number clc
    int pennies25 = 0,
        pennies10 = 0,
        pennies5 = 0,
        pennies1 = 0;

    // clc
    while (cash != 0)
    {
        if (cash >= 25)
        {
            pennies25++;
            cash -= 25;
        }
        else if (cash >= 10 && cash < 25)
        {
            pennies10++;
            cash -= 10;
        }
        else if (cash >= 5 && cash < 10)
        {
            pennies5++;
            cash -= 5;
        }
        else
        {
            pennies1++;
            cash -= 1;
        }

    }

    // print sum
    printf("%d\n", pennies1 + pennies5 + pennies10 + pennies25);
    return 0;
}

// function get number (float)
int getInt(string text)
{
    float number = 0;
    do
    {
        number = get_float("%s", text);
    }
    while (number <= 0.0);
    int sum = round(number * 100);

    return sum;
}