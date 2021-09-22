// #include "../../cs50/cs50.h"
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
} candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{

    // Loop over all voters
    for (int i = 0; i < 2; i++) {
        string name = (string) get_string("Vote: ");
        // Check for invalid vote

        if (name  == "ss"){
            printf("%d\n", true);
        } else {
            printf("%d\n", false);
        }

    }

}

// Update vote totals given a new vote
bool vote(string name)
{

}
