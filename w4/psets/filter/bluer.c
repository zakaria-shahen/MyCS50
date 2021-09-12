            // 0[0  1  2]  1[3  4  5] 2[6  7  8]
            // 3[0  1  2]  4[3  4  5] 5[6  7  8]
            // 6[0  1  2]  7[3  4  5] 8[6  7  8]
            int mapX[] = {i-1, i, i+1};
            int mapY[] = {j-1, j, j+1};

            for (int k = 0; k <= 3; k++){
                if (!(mapX[k] < height) || mapX[k] < 0){
                    continue;
                }
                
                for (int p = 0; p <= 3; p++){
                    if (!(mapY[p] < width)|| mapY[p] < 0){
                        continue;
                    }
                    sumRgbtRed += image[mapX[k]][mapY[p]].rgbtRed;
                    sumRgbtGreen += image[mapX[k]][mapY[p]].rgbtGreen;
                    sumRgbtBlue += image[mapX[k]][mapY[p]].rgbtBlue;
                    count++;
                }
            }