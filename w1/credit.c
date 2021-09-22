#include <stdio.h>
#include <math.h>
#include <cs50.h>


long long getLongLong(string text);

int main(void)
{
    long long number = getLongLong("Number: ");

    int ConditionNumber = log10(number) + 1; // check number == 16 digit
    if (ConditionNumber != 16 && ConditionNumber != 15 && ConditionNumber != 13)
    {
        printf("INVALID\n");
    }
    else
    {
        int sum = 0;
        int firstTwoNumber;
        int numberOne;

        for (int i = 0; i < 8; i++)
        {
            // 40 03 60 00 00 00 00 14 <-- number is testing...
            //     4 22 22 22 22 22 22
            //          61 76 29 29 29
            //  3 78 28 22 46 31 00 05  <-- number is testing...

            if (i == 7 && ConditionNumber == 15)
            {
                numberOne = number % 10;
                sum += numberOne;
                number /=  10;
                break;
            }
            else if (i == 6 && ConditionNumber == 13)
            {
                numberOne = number % 10;
                sum += numberOne;
                number /=  10;
                break;
            }


            numberOne = number % 10; // get last number
            number /= 10; // delete last number
            if (i == 6 && ConditionNumber == 15)
            {
                firstTwoNumber = number;
            }
            else if (i == 5 && ConditionNumber == 13)
            {
                firstTwoNumber = number;
            }


            int numberTwo = (number % 10) * 2; // get new last number

            if (numberTwo > 9) // if numberTwo -> "two digits" Ex: 99 or 11 or 10
            {
                int transfer = numberTwo % 10; // get last number
                numberTwo /= 10; // delete last number
                numberTwo += transfer; // total clc two number in numberTwo variable
            }

            sum += numberOne + numberTwo; // total cla
            number /= 10; // delete new last number


            // Saved first Two digit  in number
            if (i == 6 && ConditionNumber == 16)
            {
                firstTwoNumber = number;
            }
        }
        // if 15 digit (AmericanExpress)


        if (sum % 10 == 0)
        {
            // AmericanExpress : 34, 37 || MasterCard : 51, 52, 53, 54, 55 || Visa: 4

            if (firstTwoNumber == 34 || firstTwoNumber == 37)
            {
                printf("AMEX\n");
            }
            else if (firstTwoNumber >= 51 && firstTwoNumber <= 55)
            {
                printf("MASTERCARD\n");
            }
            else if (firstTwoNumber / 10 == 4)
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }


        }
        else
        {
            printf("INVALID\n");
        }

    }


    return 0;
}

long long getLongLong(string text)
{
    long long number = 0;
    do
    {
        number = get_long_long("%s", text);
    }
    while (number <= 0);
    return number;
}
