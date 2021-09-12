#include <ctype.h>

// Number of buckets in hash table
const unsigned int N = 50; // any number 

// Hashes word to a number
unsigned long hash(const char *word)
{
    // hash function: djb2
    //  https://stackoverflow.com/questions/7666509/hash-function-for-string/7666577#7666577
    //  https://github.com/hathix/cs50-section/blob/master/code/7/sample-hash-functions/good-hash-function.c


    unsigned long hash = 5381;
    int c;
    while ((c = *word++))
    {
        hash = ((hash << 5) + hash) + tolower(c); /* hash * 33 + c */
    }

    return hash % N;
}