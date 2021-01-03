#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Says hello to world and user
    string name = get_string("What is your name?\n");
    printf("hello, world.\n");
    printf("hello, %s.\n", name);
}