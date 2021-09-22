// #include "../../cs50/cs50.h"
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

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
void print_winner();

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }

    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }

    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes++;
            return true;
        }
    }

    return false;
}

// Print the winner (or winners) of the election
void print_winner()
{
    int votes_total = 0;
    while (true)
    {

        // sort votes (bubble Sort)
        int tmp =  -1;
        string tmp_name;
        for (int i = 0; i < candidate_count - 1 ; i++)
        {
            if (candidates[i].votes > candidates[i + 1].votes)
            {
                // change number
                tmp = candidates[i].votes;
                candidates[i].votes = candidates[i + 1].votes;
                candidates[i + 1].votes = tmp;

                //change name
                tmp_name = candidates[i].name;
                candidates[i].name = candidates[i + 1].name;
                candidates[i + 1].name = tmp_name;
            }
        }

        // if votes nubmer sorted
        if (tmp == -1)
        {
            // get Total votes
            for (int i = 0; i < candidate_count; i++)
            {
                votes_total += candidates[i].votes;
            }

            break;
        }

    }


    // get winner/s and print name/s
    int last_index = candidate_count - 1; // get last index (large number votes)

    if (candidates[last_index].votes > candidates[last_index - 1].votes)
    {
        // if one winner only
        printf("%s\n", candidates[last_index].name);

    }
    else if (candidates[last_index].votes == candidates[last_index - 1].votes)
    {
        // if multiple winners
        int winner_count = 0;
        string name[candidate_count]; // save list name winners

        for (int i = last_index; i >= 0; i--)
        {
            if (i != 0 && candidates[i].votes == candidates[i - 1].votes)
            {
                name[winner_count++] = candidates[i].name;
            }
            else if (winner_count != 0)
            {
                if (candidates[i].votes == candidates[i + 1].votes)
                {
                    name[winner_count++] = candidates[i].name;
                }

                break;
            }
        }


        // Print Winner sort
        for (int i = winner_count - 1; i >= 0 ; i--)
        {
            printf("%s\n", name[i]);
        }

    }

}
