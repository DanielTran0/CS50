#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string key[])
{   
    // Checks to see if program has 1 command line argument
    if (argc != 2)
    {
        printf("Only 1 argument\n");
        return 1;
    }
    else
    {   
        // Finds string length of command line argument
        int len = strlen(key[1]);
        
        // Checks to see if there are 26 characters in argument
        if (len != 26)
        {
            printf("Key must have 26 characters.\n");
            return 1;
        }
        else
        { 
            for (int i = 0; i < len; i++)
            {
                // Checks to see if they are all letters
                int alph = isalpha(key[1][i]);
                
                if (alph == 0)
                {
                    printf("Letters only\n");
                    return 1;
                }
                
                // Checks for repeating letters (case insensitive)
                for (int j = i + 1; j < len; j++)
                {
                    if (key[1][i] == key[1][j] || key[1][i] == key[1][j] + 32)
                    {
                        printf("No duplicates\n");
                        return 1;
                    }
                }
            }
            
            // Prompt user for plaintext
            string pt = get_string("plaintext:  ");
            int len2 = strlen(pt);
            int ct[len2];
            
            // Change plaintext with key
            printf("ciphertext: ");
            for (int i = 0; i < len2; i++)
            {   
                string alpha = "abcdefghijklmnopqrstuvwxyz";
                
                // Preserve lowercase
                if (islower(pt[i]) != 0)
                {
                    for (int j = 0; j < len; j++)
                    {
                        if (pt[i] == alpha[j])
                        {
                            ct[i] = tolower(key[1][j]);
                            printf("%c", ct[i]);
                        }
                    }
                }
                // Preserve uppercase
                else if (isupper(pt[i]))
                {
                    for (int j = 0; j < len; j++)
                    {
                        if (pt[i] == toupper(alpha[j]))
                        {
                            ct[i] = toupper(key[1][j]);
                            printf("%c", ct[i]);
                        }
                    }
                }
                // Preserve numbers, symbols and spaces
                else
                {
                    ct[i] = pt[i];
                    printf("%c", ct[i]);
                }
            }
            printf("\n");
        }
    }
}

