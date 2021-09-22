#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <cs50.h>
// #include "cs50/cs50.h"

char convertLetterToCipher(char plainLetter, string key);

int main(int argc, string argv[])
{
    // Check input key
    if (argv[1] == NULL || argv[2] != NULL) // if not input key
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else if (strlen(argv[1]) != 26) // if not input 26 character only
    {
        printf("Key must contain 26 characters.");
        return 1;
    }
    else
    {
        for (int i = 0, length = strlen(argv[1]); i < length; i++)
        {
            // Check invalid characters in key
            string k = argv[1];
            if (!(k[i] >= 97 && k[i] <= 122) && !(k[i] >= 65 && k[i] <= 90))
            {
                printf("Key must contain 26 characters.1");
                return 1;
            }

            // Check duplicate characters
            for (int j = i + 1; j < length; j++)
            {
                if (k[i] == k[j])
                {
                    printf("Key must contain 26 characters.2");
                    return 1;
                }
            }
        }
    }

    string key = argv[1];
    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");

    //get ciphertext for loop letter
    for (int i = 0, length = strlen(plaintext); i < length; i++)
    {
        char chipherLetter = convertLetterToCipher(plaintext[i], key);
        printf("%c", chipherLetter);
    }

    printf("\n");

    return 0;
}

char convertLetterToCipher(char plainLetter, string key)
{
    char letterCipher;
    int startAa;
    int endAa;

    // Check upper or lower or other => a~z: 97~122 || A~Z: 65~90
    if (plainLetter >= 97 && plainLetter <= 122)
    {
        startAa =  97;
        endAa = 122;
    }
    else if (plainLetter >= 65 && plainLetter <= 90)
    {
        startAa =  65;
        endAa = 90;
    }
    else
    {
        return plainLetter;
    }

    // Conver char to number range 0~25 (26 number)
    letterCipher = 26 - (endAa - plainLetter + 1);

    // Conver cipherLetter
    if (startAa == 97)
    {
        letterCipher =  tolower(key[(int) letterCipher]);
    }
    else
    {
        letterCipher =  toupper(key[(int) letterCipher]);
    }

    return letterCipher;
}