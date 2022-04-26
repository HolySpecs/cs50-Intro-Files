#include <cs50.h>
#include <stdio.h>
#include <string.h>

//additional header files
#include <ctype.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

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
    for (int i = 0; i < candidate_count; i ++){
        if (strcmp(candidates[i].name, name) == 0){
            candidates[i].votes ++;
            return true;
        }   
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    //to store the locations of those that have the same votes
    int winnerLocations[MAX];
    //makes the winnerLocations array 'blank' (have values of -1)
    for (int i = 0; i < MAX; i ++){
        winnerLocations[i] = -1;
    }
    int largest = 0;
    //Search the vote arrays for the largest number
    for (int i = 0; i < candidate_count; i ++){
        if (candidates[i].votes > largest){
            largest = candidates[i].votes;

            //make the rest of the items in winnerLocations -1
            for (int j = 1; j < MAX; j ++){
                winnerLocations[j] = -1;
            }
            //place the location in winnerLocations
            winnerLocations[0] = i;
        }
        //if there is a candidate with the same amount of votes
        else if (candidates[i].votes == largest){
            //finds an empty spot to then place the location
            for (int j = 1; j < MAX; j ++){
                if (winnerLocations[j] == -1){
                    winnerLocations[j] = i;
                    break;
                }
            }
        }
    }
    
    //print the winners
    for (int i = 0; i < MAX; i ++){
        //ensures that a valid location is printed
        if (winnerLocations[i] > -1){
            printf("%s\n", candidates[winnerLocations[i]].name);
        }
    }
    return;
}