#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    //Check if program has one command line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        //Check if command line argument is only digits
        for (int i = 0; argv[1][i] != '\0'; i++)
        {
            int a = isdigit(argv[1][i]);

            if (a == 0)
            {
                printf("Only numbers\n");
                return 1;
            }
        }

        //Convert key(argv[]) string into integers
        int key = atoi(argv[1]);

        //Prompt user for plaintext
        string pt = get_string("plaintext: ");

        //Shift plaintext by key
        printf("ciphertext: ");
        for (int i = 0; pt[i] != '\0'; i++)
        {
            //To preserve uppercase
            if ('A' <= pt[i] && pt[i] <= 'Z')
            {
                //Change ASCII index to alphabetical index
                int apt = pt[i] - 65;
                //Find cipher text in alpha index
                int act = (apt + key) % 26;
                //Go back to ASCII index
                int ct = act + 65;
                printf("%c", ct);
            }
            //To preserve lowercase
            else if ('a' <= pt[i] && pt[i] <= 'z')
            {
                int apt = pt[i] - 97;
                int act = (apt + key) % 26;
                int ct = act + 97;
                printf("%c", ct);
            }
            //To preserve spaces, #s and symbols
            else
            {
                printf("%c", pt[i]);
            }
        }
        printf("\n");
    }
}
