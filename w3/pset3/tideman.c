#include <cs50.h>
// #include "../../cs50/cs50.h"
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int check_loop_out();

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
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
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++){
        if (strcmp(candidates[i], name) == 0){
            ranks[rank] = i;
            return true;
        }
    }

    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count - 1; i++){
            int winner = ranks[i]; // 0 1 2
            for (int j = i + 1; j < candidate_count; j++){
                preferences[winner][ranks[j]]++;
            }
    }





}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    pair_count = 0; // candidate_count * (candidate_count - 1) / 2;

    // int count_pair_test = 0; // testing
    // 0 1 2

    for (int i = 0; i < candidate_count - 1; i++){
        // 0 1 2
        for (int j = i + 1; j < candidate_count; j++){
            if (preferences[i][j] > 0){
                pairs[i].winner = j; // 1
                pairs[i].loser = i; // 0
                pair_count++;
                // count_pair_test++; // testing
                // printf("\npair %d.... winner: %d, loser: %d\n", pair_count, pairs[i].winner, pairs[i].loser);
            }
        }
    }

    // printf("%d\n\n", pair_count); // testing
    // // testing
    // if (pair_count == count_pair_test){
    //     printf("add_pairs():Good....\n   pair_count%d\n   count_pair_test%d\n", pair_count, count_pair_test);
    // } else {
    //     printf("add_pairs():Error....\n   pair_count%d\n   count_pair_test%d\n", pair_count, count_pair_test);
    // }

}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void) // Error here
{
    bool tmp_status = true;
    while (true)
    {
         tmp_status = true;
        //  printf("\npair_count: %d\n", pair_count);
         for (int i = 0; i < pair_count - 1; i++){
            int j = i + 1;
            if (pairs[j].winner > pairs[i].winner){
                // printf("sort_pairs()Error Here:: \npair %d.... winner: %d, loser: %d\n", 0, pairs[i].winner, pairs[i].loser);
                // printf("\npair %d.... winner: %d, loser: %d\n", 0, pairs[j].winner, pairs[j].loser);

                pair tmp = pairs[i];
                if (i == 2){
                    printf("tmp%d", tmp.winner);
                }

                pairs[i] = pairs[j];
                pairs[j] = tmp;

                // printf("\npair %d.... winner: %d, loser: %d\n", 0, pairs[i].winner, pairs[i].loser);
                // printf("\npair %d.... winner: %d, loser: %d\n", 0, pairs[j].winner, pairs[j].loser);
                tmp_status = false;

            }


        }

        if (tmp_status)  {
            break;
        }
    }

    // testing
    for (int i = 0; i < pair_count; i++){
        // printf("\nsort_pairs(): pair %d.... winner: %d, loser: %d\n", i, pairs[i].winner, pairs[i].loser);
    }




}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count / 2; i++){
        for (int j = 0; j < pair_count / 2; j++){
            locked[i][j] = true;
            if (check_loop_out() == -1){
                locked[i][j] = false;
            }

        }
    }



}

// Print the winner of the election
void print_winner(void)
{

    // check
    bool out[pair_count];
    for (int i = 0; i < pair_count - 1;  i++){
        for (int j = i + 1; j < pair_count; j++){
            if (locked[i][j] == true){
                out[j] = true;
            }
        }
    }


    // print winner (no edge)
    for (int i = 0; i < pair_count; i++){
        if (out[i] == false){
            printf("%s\n", candidates[pairs[i].winner]);
            return;
        }
    }
}


// check graph adjacency matrix not loop
int check_loop_out(){

    bool out[pair_count];
    for (int i = 0; i < pair_count - 1;  i++){
        for (int j = i + 1; j < pair_count; j++){
            if (locked[i][j] == true){
                out[j] = true;
            }
        }
    }

    for (int i = 0; i < pair_count; i++){
        if (out[i] == false){
            return i;
        }
    }
    return -1;

}