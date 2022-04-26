#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int changeToReturn(float money){
    int coins = 0;
    int quarters = 0;
    int dimes = 0;
    int nickels = 0;
    div_t memory;
    int cents = round(money * 100);
    if (cents >= 25){                        //Quarters
        memory = div(cents, 25);
        quarters = memory.quot;
        cents = cents - (25 * quarters);
    }
    if (cents >= 10){                        //Dimes
        memory = div(cents, 10);
        dimes = memory.quot;
        cents = cents - (10 * dimes);
    }
    if (cents >= 5){                         //Nickels
        memory = div(cents, 5);
        nickels = memory.quot;
        cents = cents - (5 * nickels);
    }
    coins = quarters + dimes + nickels + cents;
    return coins;
}

int main(void){
    float cash = 0;
    do{
        cash = get_float("Change owed:");
    } while(cash < 0);
    printf("%i", changeToReturn(cash));
}