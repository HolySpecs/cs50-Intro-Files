#include <stdio.h>
#include <cs50.h>

//luhn algorithm
bool luhn(long number)
{
    bool result = false;
    char num[16];
    
    long long int num1 = number;
    sprintf(num, "%lld", num1);
    int sum = 0;
    for (int i = 0; i < 16 ; i ++ )
    {
        int memory = num[i];
        printf("%i",memory);
        printf("\n");
        if (i % 2 == 0 )
        {
            sum = sum + (2 * memory);
        }
        else
        {
            sum = sum + memory;
        }
    }
    printf("%i",sum);
    printf("\n");
    if (sum % 10 == 0)
    {
        result = true;
    }
    return result;
}

int main(void)
{
    long number = get_long("Number:");
    if (luhn(number))
    {
        printf("VALID");
    }
    else
    {
        printf("INVLALID");
    }
}