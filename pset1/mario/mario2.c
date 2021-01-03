#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int h;
    //Prompt user for block size
    do
    {
        h = get_int("Enter the height of the blocks (1 to 8): ");
    }
    while (h < 1 || h > 8);

    //Creates block base on user input
    for (int i = 1 ; i <= h; i++)
    {
        for (int k = h - i ; k > 0 ; k--)
        {
            printf(" ");
        }
        for (int j = 0 ; j < i; j++)
        {
            printf("#");
        }
        //Makes the space between the two blocks
        for (int a = 0 ; a < 2; a++)
        {
            printf(" ");
        }
        //Makes the second block
        for (int b = 0 ; b < i; b++)
        {
            printf("#");
        }
        printf("\n");
    }
}