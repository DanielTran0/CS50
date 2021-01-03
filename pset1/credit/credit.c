#include <stdio.h>
#include <cs50.h>

int main(void)
{
    long n;
    //Prompt user for credit card #
    do
    {
        n = get_long("Enter credit card number.\n");
    }
    while (n < 0);

    //Finding every other digit from second last, x2, and add digits
    int f;
    for (long i = 100; i < n * 10; i = i * 100)
    {
        long a = n % i;
        int b = a / (i / 10);
        int c = b * 2;
        int d = c % 10;
        int e = c / 10;
        f = f + e + d;
    }

    //For adding up all other digits not multiplied and add together
    int j;
    for (long x = 10; x < n * 10; x = x * 100)
    {
        long g = n % x;
        int h = g / (x / 10);
        j = j + h;
    }

    //Find check sum
    int check = f + j;
    printf("Sum Check:%i\n", check);
    int k = check % 10;

    //Finding first 2 digits of credit card
    long m = n;
    long q = 2;
    while (m >= 100)
    {
        m = m / 10;
        q = q + 1;
    }

    //Checking the type of credit card, first with check sum
    if (k > 0)
    {
        printf("INVALID\n");
    }
    //Checking if American Express
    else if (q == 15)
    {
        if (m == 34 || m == 37)
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    //Checking if Visa
    else if (q == 13)
    {
        if (m >= 40 && m < 50)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    //Checking if Visa or Mastercard
    else if (q == 16)
    {
        if (m >= 40 && m < 50)
        {
            printf("VISA\n");
        }

        else if (m == 51 || m == 52 || m == 53 || m == 54 || m == 55)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    //If check sum is valid but doesn't belong to the 3 groups
    else if (q < 13 || q > 16)
    {
        printf("INVALID\n");
    }
}