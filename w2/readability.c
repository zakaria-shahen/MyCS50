#include <stdio.h>
#include <math.h>
#include <string.h>
#include <cs50.h>

void getL_S(string text, float *l, float *s);

int main(void)
{
    string text = get_string("Text: ");
    float l = 0, s = 0;
    getL_S(text, &l, &s);

    // printf("s: %2f\nl: %2f\n", s, l);

    float index = 0.0588 * l - 0.296 * s - 15.8;

    int level = round(index);

    if (level >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (level < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %d\n", level);
    }

    return 0;
}

void getL_S(string text, float *l, float *s)
{

    int countSentendces = 0;
    int countWord = 1;
    int countLetter = 0;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        // get word Count ->
        // It was a bright cold day in April,
        if (text[i] != ' ' && text[i + 1] == ' ')
        {
            ++countWord;
        }

        // get letter count  -> Hint: 65~90 || 97~122
        if ((text[i] >= 65 && text[i] <= 90) || ((text[i] >= 97 && text[i] <= 122)))
        {
            ++countLetter;

            //get count Sentendces
            char secondChar = text[i + 1];
            if (secondChar == '!' || secondChar == '.' || secondChar == '?')
            {
                ++countSentendces;
            }
        }

        if (countWord == 100)
        {
            countWord = 0;
            *s += (countSentendces / 100) * 100; // S - > average number of Sentendces per 100 words
            *l += (countLetter / 100) * 100;    // L -> average number of letters per 100 words
            countSentendces = 0;
            countLetter = 0;
        }
    }

    if (countWord > 0)
    {
        //printf("word: %d\nLetter: %d\nSentendces: %d\n", countWord, countLetter, countSentendces);
        *s += (countSentendces / (float) countWord) *  100; // S - > average number of Sentendces per 100 words
        *l += (countLetter / (float) countWord) * 100;   // L -> average number of letters per 100 words
    }


}
