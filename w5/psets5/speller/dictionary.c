// Implements a dictionary's functionality

#include <stdbool.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table
// https://stackoverflow.com/questions/22741966/how-to-choose-size-of-hash-table
const unsigned int N = 190788; // 75%=> N = input/0.75

// Hash table
node *table[N];

// Number of word in hash table (dictionary)
unsigned int count_word = -1;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // int index_hash = hash(word);
    node *n = table[hash(word)];

    while (n != NULL)
    {
        // if found word is in dictionary
        if (strcasecmp(n->word, word) == 0)
        {
            return true;
        }

        // check next node
        n = n->next;
    }

    // if not found word is in dictionary
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    //  https://stackoverflow.com/questions/7666509/hash-function-for-string/7666577#7666577

    unsigned int hash = 5381; // 5381;
    int c;
    while ((c = *word++))
    {
        hash = ((hash << 5) + hash) + tolower(c); /* hash * 33 + c */
    }

    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // open file
    FILE *input = fopen(dictionary, "r");
    if (input == NULL)
    {
        printf("Error: not open file\n");
        return false;
    }

    char word[LENGTH + 1];
    // file reading and create hash table
    do
    {
        // read word
        fscanf(input, "%s", word);

        // get hash word
        int index_hash = hash(word);

        // if index hash not data saved
        if (table[index_hash] == NULL)
        {
            node *n = malloc(sizeof(node));
            if (n == NULL)
            {
                printf("Erorr load(): not found more RAM");
                return false;
            }

            strcpy(n->word, word);

            n->next = NULL;
            table[index_hash] = n;
        }

        // if index hash data saved
        else
        {
            node *temp = table[index_hash];

            node *p = malloc(sizeof(node));
            if (p == NULL)
            {
                printf("Erorr load(): not found more RAM");
                return false;
            }

            strcpy(p->word, word);
            p->next = temp->next;
            temp->next = p;
        }

        // count Number word
        count_word++;

    }
    while (!feof(input));

    fclose(input);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if (count_word > 0)
    {
        return count_word;
    }

    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] == NULL)
        {
            continue;
        }

        node *j = table[i];

        while (j->next != NULL)
        {
            node *temp = j->next;
            free(j);
            j = temp;
        }
        free(j);
    }

    return true;
}
