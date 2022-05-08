# code folder
Root folder of the code. You can run the code by executing the `main.py` file, 
which is going to output individual frames to the `frames` folder. It is up to
you how you want to use the individual frames, but I am using `ffmpeg` to 
generate a usable `.mp4` file. Using the following command 
`ffmpeg -r 60 -i example%d.png -c:v libx264 -preset veryslow -crf 18 -pix_fmt yuv420p o.mp4 -y`.

## `main.py`
Main script that is executed, it will generate and render animation followed
by an upload to Instagram.

## `render.py`
Main script that generates and renders the animation. For rendering I am using
`ffmpeg` so make sure you have that installed

## `send_post.py`
Arguably the most fragile part of the entire project. I use `selenium` to login
to Instagram and post the final video. I am using a `chromedriver` with a 
user profile named `Person 1` which is already logged in to the correct 
Instagram account. This script also expect a login information, you can change
that logic, but at the moment I expect to to find a `.json` file located in the
code folder with the following structure: `[{"username":"username", "password":"password"}]`.
