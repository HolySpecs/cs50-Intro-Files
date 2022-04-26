#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

string caesarShift(int key, string plainText){
    int length = strlen(plainText);
    char cipherText[length];
    int memory = 0;
    string result;
    for (int i = 0, n = length; i < n; i ++){
        char ch = plainText[i];
        if (ch >= 'A' && ch <= 'Z'){ //uppercase
            memory = (int) ch + key;
            if (memory >= 91){
                memory = memory - 26;
            }
        }
        else if (ch >= 'a' && ch <= 'z'){ //lowercase
            memory = (int) ch + key;
            if (memory >= 123){
                memory = memory - 26;
            }
        }
        else{
            memory = (int) ch;
        }
        cipherText[i] = (char) memory;
    }
    cipherText[length] = '\0';
    result = cipherText;
    return result;
}

bool isNumber(string num){
    bool result = false;
    int length = strlen(num);
    for (int i = 0, n = length; i < n; i ++){
        if (isdigit(num[i])){
            result = true;
        }
        else{
            result = false;
        }
    }
    return result;
}

int main(int argc, string argv[]){
    int shift;
    int result;
    if (argc == 2 && (isNumber(argv[1]) == true)){
        shift = atoi(argv[1]) % 26;
        string plainText = get_string("plaintext: ");
        printf("ciphertext: %s\n", caesarShift(shift, plainText));
        result = 0;
    }
    else{
        printf("Usage: ./caesar key\n");
        result = 1;
    }
    return result;
}