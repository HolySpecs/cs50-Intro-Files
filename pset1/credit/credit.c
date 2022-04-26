#include <stdio.h>
#include <cs50.h>

//Luhn's algorithm: Multiply every other digit by 2, add the remaining digits, get the sum of the two and must be a multiple of ten
bool luhn(string num)
{
    bool result = false;
    string num1 = num;
    int length = sizeof(num1);
    int sum1 = 0; // double sum
    int sum2 = 0; // normal sum
    for (int i = 0; i < length -1; i ++)
    {
        int mem = num1[i];
        if (i % 2 == 0)
        {
            sum1 = sum1 + ( 2 * mem);
        }
        else
        {
            sum2 = sum2 + mem;
        }
    }
    if ((sum1 + sum2) % 10 == 0)
    {
        result = true;
    }
    return result;
}

//Verify MasterCard: 16 digits, starts with 51, 52, 53, 54, or 55
bool verifMas(string num)
{
    bool result = false;
    char num1[] = num;
    if (sizeof(num1) == 16)
    {
        int first = num1[0];
        int second = num1[1];
        if (first == 5)
        {
            if (second <= 5 || second >= 1)
            {
                result = luhn(num);
            }
        }
    }
    return result;
}

//Verify Visa: 13 to 16 digits, starts with 4
bool verifVis(string num)
{
    bool result = false;
    
    return result;
}

//Verify American Express: 15 digits, starts with 34 or 37
bool verifAmer(string num)
{
    bool result = false;
    
    return result;
}

//main program
int main(void)
{
    long number = get_long("Number:");
    printf("\n");
    string num = number;
    if (verifMas(num))
    {
        printf("MASTERCARD");
    }
    else if (verifVis(num))
    {
        printf("VISA");
    }
    else if (verifAmer(num))
    {
        printf("AMERICAN EXPRESS");
    }
    else
    {
        printf("INVALID");
    }
}