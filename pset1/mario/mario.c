#include <cs50.h>
#include <stdio.h>

string layer(int height, char* result,int length)                    //The front blocks
{
    int i = height + 1;
    while ( i > 0){
        result[length - i] = '#';
        i --;
    }
    string final = result;                  //Turns it to string
    return final;
}

//The main code
int main(void)
{
    int height;                             //initiates the height variable
    do
    {
        height = get_int("Height:");
    } while((height > 8) || (height < 1));  //will repeat until the height given is between 1 and 8
    char result[height + 1];
    for (int num1 = 0; num1 < height; num1 ++){
        result[num1] = ' ';
    }
    result[height] = '\0';
    for (int j = 0; j <= height-1; j ++)      //print multiple floors
    {
        printf("%s", layer(j, result, height));
        printf("\n");
    }
}