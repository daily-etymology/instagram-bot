# code folder
Root folder of the code. You can run the code by executing the `main.py` file, which is going to output individual frames to the `frames` folder. It is up to you how you want to use the individual frames, but I am using `ffmpeg` to generate a usable `.mp4` file. Using the following command `ffmpeg -r 60 -i example%d.png -c:v libx264 -preset veryslow -crf 18 -pix_fmt yuv420p o.mp4 -y`