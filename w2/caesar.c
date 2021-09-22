#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <cs50.h>

char cipher(int plain, int key, bool upperCase);

int main(int argc, string argv[])
{
    if (argv[1] == NULL || argv[2] != NULL) // if not input
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        for (int i = 0; argv[1][i] != '\0'; i++)
        {
            // 0~9 => 48~57
            if (!(argv[1][i] >= 48 && argv[1][i] <= 57)) // if not input number
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }


    int key =  atoi(argv[1]) ; // convert string number to intger
    string plaintext = get_string("plaintext: ");

    // Print ciphertext
    printf("ciphertext: ");

    for (int i = 0; plaintext[i] != '\0' ; i++)
    {
        char index;

        // Check char upper or lower or other => A~Z: 65~90  || a~b" 97~122
        if (plaintext[i] >= 65 && plaintext[i] <= 90)
        {
            index = cipher(plaintext[i], key, true);

        }
        else if (plaintext[i] >= 97 && plaintext[i] <= 122)
        {
            index = cipher(plaintext[i], key, false);

        }
        else
        {
            index = plaintext[i];
        }

        // print char cipher
        printf("%c", index);

    }

    printf("\n");

    return 0;
}


char cipher(int plain, int key, bool upperCase)
{
    int startAa, endAa;

    // Check upperCase char input => A~Z: 65~90  || a~b" 97~122
    if (upperCase == false)
    {
        startAa = 97;
        endAa = 122;
    }
    else if (upperCase == true)
    {
        startAa = 65;
        endAa = 90;
    }
    else
    {
        printf("\nError: UpperCase... cipher()\n");
        return 0;
    }

    plain = 26 - (endAa - plain + 1); // Convert to nubmer range 1~26
    plain = (plain + key) % 26; // cipherText (ci) = (plainText + key) % 26
    plain = startAa + plain;  // Convert number to range 97~122 Or 65~90

    return (char) plain;
}