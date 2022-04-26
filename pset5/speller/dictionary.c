// Implements a dictionary's functionality

#include <stdbool.h>

#include "dictionary.h"

//Additional header files
#include <string.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>

// Number of buckets in hash table
const unsigned int N = 13229;

//Global Variables
int wordCount = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    /*
    copy the word
    hash the copied word
    go to the hash address and check if the word is availale or not
    */
    
    //checks for the length of the word before copying it
    int length = strlen(word);
    char temp[length];
    strcpy(temp, word);
    //gets the hash value
    int index = hash(temp);
    //initialize pointer
    node *pointer = table[index];
    //while there is still data
    while (pointer != NULL){
        if (strcasecmp(pointer -> word, temp) == 0){
            return true;
        }
        //move on to the next pointer
        else{
            pointer = pointer -> next;
        }
    }
    return false;
}

// Hashes word to a number via the folding method
unsigned int hash(const char *word)
{
    /*
    Turn all characters in the word to lowercase
    Then get the total ascii values of all of the characters
    then return the remainder
    */
    
    //unsigned int only positive values
    unsigned int value = 0;
    int length = strlen(word);
    char temp[length + 1];
    for (int i = 0; i < length; i ++){
        temp[i] = tolower(word[i]);
        value += (int) temp[i];
    }
    return value % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    /*
    open dictionary file
    take out each word
    add it to the hash table
    */
    
    // open file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL){
        return false;
    }
    //initialize new word
    char newWord[LENGTH + 1];
    // Scans dictionary word by word
    while (fscanf(file, "%s", newWord) != EOF){
        // allocates memory for new nodes
        node *newNode = calloc(1,sizeof(node));
        // checks if it can allocate memory
        if (newNode == NULL){
            unload();
            fclose(file);
            return false;
        }
        // copies word into the new node
        strcpy(newNode->word, newWord);

        // gets the hash address
        int value = hash(newNode->word);

        // adds the loaction to the data node
        node *data = table[value];

        // if there is no data, go to the next node
        if (data != NULL){
            newNode->next = table[value];
        }
        //adds the data to the location
        table[value] = newNode;
        wordCount ++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return wordCount;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    /*
    go through all the buckets
    point all the pointers to NULL
    free them
    */
    
    //for all the values in the bucket
    for (int i = 0; i < N; i ++){
        //initialize pointers
        node *data = table[i];
        node *pointer = table[i];
        while (pointer != NULL){
            //redirects pointers to one address
            pointer = pointer -> next;
            //free the data
            free(data);
            //go to the next pointer
            data = pointer;
        }
    }
    return true;
}