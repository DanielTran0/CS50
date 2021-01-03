#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float c;
    //Prompt user for change amount
    do
    {
        c = get_float("Change needed:\n");
    }
    while (c <= 0);

    //Convert dollar amount into cents
    int coins;
    int change;
    int cents = round(c * 100);
    printf("Change in cents: %i\n", cents);

    //Coin values
    int p = 1;
    int n = 5;
    int d = 10;
    int q = 25;

    //Find max amount of quaters to use
    while (cents >= q)
    {
        int qc = round(cents / q);
        change = cents - qc * q;
        coins = coins + qc;
        printf("Amount of quaters:%i\n", qc);
        cents = change;
    }

    //Find max amount of dimes to use
    while (cents >= d)
    {
        int dc = round(cents / d);
        change = cents - dc * d;
        coins = coins + dc;
        printf("Amount of dimes:%i\n", dc);
        cents = change;
    }

    //Find max amount of nickels to use
    while (cents >= n)
    {
        int nc = round(cents / n);
        change = cents - nc * n;
        coins = coins + nc;
        printf("Amount of nickels:%i\n", nc);
        cents = change;
    }

    //Find max amount of pennies to use
    while (cents >= p)
    {
        int pc = round(cents / p);
        change = cents - pc * p;
        coins = coins + pc;
        printf("Amount of pennies:%i\n", pc);
        cents = change;
    }

    //Show total coins needed for change
    printf("Total coins: %i\n", coins);
}
