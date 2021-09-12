#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Notes
    // sepiaRed = .393 * originalRed + .769 * originalGreen + .189 * originalBlue
    // sepiaGreen = .349 * originalRed + .686 * originalGreen + .168 * originalBlue
    // sepiaBlue = .272 * originalRed + .534 * originalGreen + .131 * originalBlue
    // 200, 210, 220
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int originalRed = round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue);
            int originalGreen = round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue);
            int originalBlue = round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue);

            image[i][j].rgbtRed = (originalRed > 255) ? 255 : originalRed;
            image[i][j].rgbtGreen = (originalGreen > 255) ? 255 : originalGreen;
            image[i][j].rgbtBlue = (originalBlue > 255) ? 255 : originalBlue;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int half = width / 2.0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < half; j++)
        {
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = tmp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // output saved
    RGBTRIPLE temp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // One pxiel
            int sumRgbtRed = 0;
            int sumRgbtGreen = 0;
            int sumRgbtBlue = 0;
            float count = 0.0;

            for (int k = i - 1, len = i + 1; k <= len; k++)
            {
                if (!(k < height) || k < 0)
                {
                    continue;
                }

                for (int p = j - 1, lenIn = j + 1; p <= lenIn; p++)
                {
                    if (!(p < width) || p < 0)
                    {
                        continue;
                    }
                    sumRgbtRed += image[k][p].rgbtRed;
                    sumRgbtGreen += image[k][p].rgbtGreen;
                    sumRgbtBlue += image[k][p].rgbtBlue;
                    count++;
                }
            }

            if (count == 0.0)
            {
                count++;
            }

            temp[i][j].rgbtRed = round(sumRgbtRed / count);
            temp[i][j].rgbtGreen = round(sumRgbtGreen / count);
            temp[i][j].rgbtBlue = round(sumRgbtBlue / count);
        }
    }

    // puch output on origin
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    // Gx and Gy
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // one pixel
            int gxOutput[3] = {0, 0, 0}; // X: 0:Read - 1:Green - 2:Blue
            int gyOutput[3] = {0, 0, 0}; // Y: 0:Read - 1:Green - 2:Blue
            int count[2] = {0, 0};       // 0:Row-index - 1:Column-index

            for (int k = i - 1, len = i + 1; k <= len; k++)
            {
                if (k < 0 || !(k < height))
                {
                    count[0]++;
                    continue;
                }

                for (int p = j - 1, lenIn = j + 1; p <= lenIn; p++)
                {
                    if (p < 0 || !(p < width))
                    {
                        count[1]++;
                        continue;
                    }

                    // GX
                    gxOutput[0] += image[k][p].rgbtRed * gx[count[0]][count[1]];
                    gxOutput[1] += image[k][p].rgbtGreen * gx[count[0]][count[1]];
                    gxOutput[2] += image[k][p].rgbtBlue * gx[count[0]][count[1]];

                    // GY
                    gyOutput[0] += image[k][p].rgbtRed * gy[count[0]][count[1]];
                    gyOutput[1] += image[k][p].rgbtGreen * gy[count[0]][count[1]];
                    gyOutput[2] += image[k][p].rgbtBlue * gy[count[0]][count[1]];
                    count[1]++;
                }
                count[1] = 0;
                count[0]++;
            }

            // change paxil temp
            int rgbtRed = round(sqrt(pow(gxOutput[0], 2) + pow(gyOutput[0], 2)));
            int rgbtGreen = round(sqrt(pow(gxOutput[1], 2) + pow(gyOutput[1], 2)));
            int rgbtBlue = round(sqrt(pow(gxOutput[2], 2) + pow(gyOutput[2], 2)));

            temp[i][j].rgbtRed = (rgbtRed > 255) ? 255 : rgbtRed;
            temp[i][j].rgbtGreen = (rgbtGreen > 255) ? 255 : rgbtGreen;
            temp[i][j].rgbtBlue = (rgbtBlue > 255) ? 255 : rgbtBlue;
        }
    }

    // copy output to origin
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
}
