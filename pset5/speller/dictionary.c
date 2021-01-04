// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 150000;
int word_counter = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int h_value = hash(word);
    node *cursor = NULL;

    for (cursor = table[h_value]; cursor != NULL; cursor = cursor->next)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
    }

    return false;
}

// Hashes word to a number
// Using djb2 from http://www.cse.yorku.ca/~oz/hash.html
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c;

    while ((c = toupper(*word++)))
    {
        hash = ((hash << 5) + hash) + c;
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Dictionary could not load\n");
        return false;
    }

    // Create a buffer for dictionary word
    char buf[LENGTH + 1];

    // Keep reading strings until over
    while (fscanf(dict, "%s", buf) != EOF)
    {
        // Create a node for each word
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            unload();
            return false;
        }

        // Copy word from buffer into node and count words loaded
        strcpy(n->word, buf);
        word_counter++;

        // Set node pointer to the same as the table (to avoid orphaning)
        // Then have table point to node
        n->next = table[hash(buf)];
        table[hash(buf)] = n;
    }

    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if (word_counter > 0)
    {
        return word_counter;
    }

    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        // Keep looping until end of link list
        while (cursor != NULL)
        {
            // Create a temp variable to ensure no orphaning
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }

        if (i == N - 1 && cursor == NULL)
        {
            return true;
        }
    }

    return false;
}
