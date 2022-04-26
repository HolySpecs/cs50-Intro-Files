//header files
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

//defining standards
#define JAR 512
typedef unsigned char BYTE;

int main(int argc, char *argv[]){
    //check for invalid usage
    if (argc != 2){
        printf("Usage: .recover image\n");
        return 1;
    }

    //input pointer
    char* card = argv[1];
    FILE *file = fopen(card, "r");
    //check if the file can be opened or not
    if (!file){
        printf("Could not open %s.\n", card);
        return 1;
    }

    //important ponters and variables
    BYTE buffer[JAR];                   //buffer for data
    int counter = 0;                    //counter for the amount of images seen
    char frontName[4];                  //the new image file name
    char newName[8];                    //the new image file name with the extension
    FILE *newImg;                       //new file pointer
    
    //while there is still data
    while (fread(buffer, sizeof(buffer), 1, file)){
        //if a new image is found
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0){
            //check if the counter is a specific value or not
            if (counter < 10){
                //single digit
                sprintf(frontName, "00%i", counter);
            }
            else if (counter < 100){
                //double digit
                sprintf(frontName, "0%i", counter);
            }
            else{
                //triple digit
                sprintf(frontName, "%i", counter);
            }
            
            //goes to do a specific thing depending on the counter value
            switch (counter){
                case 0:                                             //starting point
                    sprintf(newName, "%s.jpg", frontName);          //makes new file name
                    counter ++;                                     //adds to counter to prep for a new file
                    newImg = fopen(newName, "w");                   //makes the new image (is blank at first)
                    fwrite(buffer, sizeof(buffer), 1, newImg);      //writes the data
                    break;                                          //exits the swtich case statement
                default:
                    fclose(newImg);                                 //closes previous file
                    sprintf(newName, "%s.jpg", frontName);          
                    counter ++;                                     
                    newImg = fopen(newName, "w");                   
                    fwrite(buffer, sizeof(buffer), 1, newImg);      
                    break;  
            }
        }
        //go to the next buffer
        else if (counter > 0){
            fwrite(buffer, sizeof(buffer), 1, newImg);
        }
    }
    
    //close files
    fclose(file);
    fclose(newImg);
    return 0;
}
