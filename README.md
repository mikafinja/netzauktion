# Netzauktion

Visualization of the data of the 5G frequency auction

## Example video after bidding round 318

https://www.youtube.com/watch?v=0Mtd5GJSSps

## Setup

`pip install -r requirements.txt`

## Run scripts

There is no fully automatic setup, yet.

1. Run `scrape.py` to download the raw data.
1. Run `parse.py` to extract the data from raw xml and convert it into json, with significant less overhead and a simpler data structure.
1. Run `render.py` to generate charts for each bidding round.
1. `concat.py` generates a ffconcat file used by ffmpeg as input, containing the file names and the duration how long each frames will be shown in the final video.
1. Change into the export dir `cd export` and run the follwing ffmpeg command to generate a video from the images: `ffmpeg -i netzauktion.ffconcat -s 1920x1080 -i %03d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p 5gAuktion.mp4`
