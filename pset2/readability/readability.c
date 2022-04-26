#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void){
    string text = get_string("Text: ");
    int letters = 0;
    int sentences = 0;
    int words = 1;
    float index = 0;
    for (int i = 0, n = strlen(text); i < n ; i ++){
        //check if is a sentence
        if (text[i] == '.' || text[i] == '!' || text[i] =='?'){
            sentences += 1;
        }
        //check if it is a word
        if (isspace(text[i])){
            words += 1;
        }
        //count the amount of letters
        if (isalpha(text[i])){
            letters += 1;
        }
    }
    
    //Coleman-Liau index
    float L = ((float)letters / words) * 100;
    float S = ((float)sentences / words) * 100;
    index = (0.0588 * L) - (0.296 * S) - 15.8;
    
    if (index < 1){
        printf("Before Grade 1\n");
    }
    else if (index > 16){
        printf("Grade 16+\n");
    }
    else{
        printf("Grade %i\n", (int) round(index));
    }
}