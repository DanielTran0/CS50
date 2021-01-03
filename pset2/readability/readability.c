#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
float grade_level(int letters, int words, int sentences);

int main(void)
{
    //Prompt user for text
    string t = get_string("Text:\n");
    
    //Uses funcs to count letters, words and sentences
    int l = count_letters(t);
    int w = count_words(t);
    int s = count_sentences(t);
    float g = grade_level(l, w, s);
    
    //Print amount amount of each type
    printf("%i Letter(s)\n", l);
    printf("%i Word(s)\n", w);
    printf("%i Sentence(s)\n", s);
    
    //Checks grade level to display correct message
    if (g < 1)
    {
        printf("Before Grade 1\n");
    }
    if (1 <= g && g < 16)
    {
        printf("Grade %.0f\n", round(g));
    }
    if (g >= 16)
    {
        printf("Grade 16+\n");
    }
}

//Count # of letters
int count_letters(string text)
{
    int letters = 0;
    
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

//Count # of words
int count_words(string text)
{
    int words = 1;
    
    for (int i = 0; text[i] != '\0' ; i++)
    {
        if (text[i] == 32)
        {
            words++;
        }
    }
    return words;
}

//Count # of sentences
int count_sentences(string text)
{
    int sentences = 0;
    
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (text[i] == 33 || text[i] == 46 || text[i] == 63)
        {
            sentences++;
        }
    }
    return sentences;
}

//Calculates reading grade
float grade_level(int letters, int words, int sentences)
{
    float l = (float) letters / words * 100;
    float s = (float) sentences / words * 100;
    float index = (0.0588 * l) - (0.296 * s) - 15.8;
    
    return index;
}