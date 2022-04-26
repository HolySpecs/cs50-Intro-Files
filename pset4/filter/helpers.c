#include "helpers.h"

//other header files
#include <string.h>
#include <math.h>
#include <stdlib.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int red;
    int green;
    int blue;
    int average;
    for (int y = 0; y < height; y ++){
        for (int x = 0; x < width; x ++){
            //get the values
            red = image[y][x].rgbtRed;
            green = image[y][x].rgbtGreen;
            blue = image[y][x].rgbtBlue;
            //gets average
            average = round(((float)(red + green + blue)/3));
            //applies it to the file
            image[y][x].rgbtRed = average;
            image[y][x].rgbtGreen = average;
            image[y][x].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float red;
    int newRed;
    float green;
    int newGreen;
    float blue;
    int newBlue;
    for (int y = 0; y < height; y ++){
        for (int x = 0; x < width; x ++){
            //get values
            red = image[y][x].rgbtRed;
            green = image[y][x].rgbtGreen;
            blue = image[y][x].rgbtBlue;
            //change and apply values
            newRed = round((0.393 * red) + (0.769 * green) + (0.189 * blue));
            if (newRed > 255){
                newRed = 255;
            }
            newGreen = round((0.349 * red) + (0.686 * green) + (0.168 * blue));
            if (newGreen > 255){
                newGreen = 255;
            }
            newBlue = round((0.272 * red) + (0.534 * green) + (0.131 * blue));
            if (newBlue > 255){
                newBlue = 255;
            }
            
            image[y][x].rgbtRed = newRed;
            image[y][x].rgbtGreen = newGreen;
            image[y][x].rgbtBlue = newBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE memory;
    int middle = floor(width/2);
    for (int y = 0; y < height; y ++){
        for (int x = 0 ; x < middle ; x ++){
            memory = image[y][x];
            int reflectLocation = width - x - 1;
            
            image[y][x] = image[y][reflectLocation];
            
            image[y][reflectLocation] = memory;

        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE result[height][width];
    //store the image in another location
    for (int y = 0; y < height; y++){
        for(int x = 0; x < width; x ++){
            result[y][x] = image[y][x];
        }
    }
    
    //applying the blur effect
    for (int y = 0; y < height; y++){
        for(int x = 0; x < width; x ++){
            //For counting the averages
            float redSum = 0;
            float greenSum = 0;
            float blueSum = 0;
            int pixelCount = 0;
            
            //checks if surrounding pixels are available or not
            for (int i = -1; i < 2; i ++){
                for (int j = -1; j < 2; j ++){
                    if (i + y >= 0  && j + x >= 0 && i + y <= height - 1 && j + x <= width - 1){
                        redSum += result[y + i][x + j].rgbtRed;
                        greenSum += result[y + i][x + j].rgbtGreen;
                        blueSum += result[y + i][x + j].rgbtBlue;
                        pixelCount ++;
                    }
                }
            }
            
            image[y][x].rgbtRed = round(redSum/pixelCount);
            image[y][x].rgbtGreen = round(greenSum/pixelCount);
            image[y][x].rgbtBlue = round(blueSum/pixelCount);
        }
    }
    
    return;
}
