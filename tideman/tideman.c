#include <cs50.h>
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
} pair;

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
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for(int i = 0; i < candidate_count; i++)
    {
        for(int j = i + 1; j < candidate_count; j++)
        {
            if(preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count ++;
            }
            else if(preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count ++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // compare the amount of people that prefer the winner to the loser
    // sort by the biggest numbers first
    for(int i = pair_count - 1; i >= 0; i--)
    {
        for(int j = 0; j <= i; j++)
        {
            if((preferences[pairs[j].winner][pairs[j].loser])
               <
               (preferences[pairs[j + 1].winner][pairs[j+1].loser]))
            {
                pair temp = pairs[j];
                pairs[j] = pairs[j+1];
                pairs[j+1] = temp;
            }
        }
    }
    return;
}

// Lock pairs into the candidate graph in decreasing order of victory strength
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        // Check if adding this pair creates a cycle
        if (!creates_cycle(pairs[i].winner, pairs[i].loser))
        {
            // Lock the pair
            preferences[pairs[i].winner][pairs[i].loser] = true;
        }
    }
}

// Check if adding the pair (winner, loser) would create a cycle
bool creates_cycle(int winner, int loser)
{
    bool visited[candidate_count];
    for (int i = 0; i < candidate_count; i++)
    {
        visited[i] = false;
    }

    return has_cycle(winner, loser, visited);
}

// Recursive function to check for a cycle
bool has_cycle(int current, int original_loser, bool visited[])
{
    // Base case 1: No preferences for the current candidate
    if (preferences[current][0] == original_loser)
    {
        return false;
    }

    // Base case 2: Cycle detected (current candidate already visited)
    if (visited[current])
    {
        return true;
    }

    // Mark the current candidate as visited
    visited[current] = true;

    // Check preferences recursively
    for (int i = 0; i < candidate_count; i++)
    {
        if (preferences[current][i] == original_loser)
        {
            // We've looped back to the original loser, indicating a cycle
            return true;
        }
        else if (!visited[preferences[current][i]])
        {
            // Recursively check preferences of the preferred candidate
            if (has_cycle(preferences[current][i], original_loser, visited))
            {
                return true;
            }
        }
    }

    // Reset the visited status for the current candidate (backtrack)
    visited[current] = false;

    // No cycle detected
    return false;
}

// Print the winner of the election
void print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        bool is_source = true;
        for (int j = 0; j < candidate_count; j++)
        {
            if (preferences[j][i])
            {
                is_source = false;
                break;
            }
        }
        if (is_source)
        {
            printf("%s\n", candidates[i]);
            return;
        }
    }
}
