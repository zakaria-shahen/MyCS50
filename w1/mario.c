#include <stdio.h>
#include <cs50.h>

int getInt(string text);


int main(void)
{
    int n = getInt("Hight: ");

    // new line for loop
    for (int i = 0; i < n; i++)
    {
        // space
        for (int s = 1 ; s < n - i; s++)
        {
            printf(" ");
        }

        // # : new letter for loop
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        printf("  "); // space

        // #: letter loop 2
        for (int k = 0; k <= i; k++)
        {
            printf("#");
        }

        printf("\n");

    }

    return 0;
}

// function check input and get input
int getInt(string text)
{
    int number = 0;
    do
    {
        number = get_int("%s", text);
    }
    while (number <= 0 || number > 8);

    return number;
}