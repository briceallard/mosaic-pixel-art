## Image Mosaic
#### Purpose
This program has 2 functionallities.  
- First: Given a YouTube video ID, downloads the highest quality and frame rate available to the desired directory, then takes a screen capture of the current frame at the given interval (default: 1 second)
- Second: Using the dataset of images collected from screen capturing (or any other large dataset of images) we import an image using PIL and replace each pixel with the most "SIMILIAR" image from the dataset creating a Image Mosaic.

#### Description
In the example, I used the trailers to every Marvel Avengers movie for my dataset of images and the upcoming release poster for Avengers: Endgame as my Image Mosaic backdrop image. Each pixel is replaced with an image from one of the Avengers trailers, creating a Avengers mosaic of Avengers ;)

**Files**
* /dominant_data/
    * a folder where the .json dataset is stored with dominant color
* /frame_captures/
    * a folder where all the screen shots from downloaded YouTube clips are stored
* /input_images/
    * my testing images used for processing into mosaic images
* /videos/
    * a folder where each YouTube video is stored locally
* frame_captures_to_json.py
    * Gathers dominant color data and stores into .json
* image_mosaic.py
    * Processes input image and converts to mosaic form
* images_from_yt.py
    * Downloads YouTube videos and captures frames in given interval

## Instructions
**Requirements**
* FFmpeg - A complete, cross-platform solution to record, convert and stream audio and video.
    * Install with `sudo apt install ffmpeg`  
* Pillow - Python imaging library that adds support for opening, manipulating, and saving many different image file formats.  
    * Install with `pip3 install Pillow`  

### Step One -
**Get images from YouTube clips**
`images_from_yt.py` specifically handles the download requests as well as the image capture in 1 second intervals. The YouTube video and the Frame Captures are stored locally on the hard drive for use in future steps. The frame captures are also automatically resized and cropped to equal aspect ratio to better represent a single pixel for the mosaic effect.  

**Instructions**
`python3 images_from_yt.py -i YouTubeIDHere -d /output_folder/ -s 1` to execute the program.
* `-i` - YouTube ID
    * The last sequence on letters/numbers in the YouTube video link in browser  
    * `https://www.youtube.com/watch?v=eOrNdBpGMv8`: ID would be eOrNdBpGMv8  
* `-d` - Destination Output
    * The output directory where you want to save the videos  
    * The Frame Captures are automatically saved to the `./frame_captures/` directory  
* `-s` - Seconds (Interval)
    * How frequently you would like to have the frames saved locally. 
    * 1 = 1 Second, 1/60 = 1 Minute, 5/60 = 5 Minutes 

### Step Two -
**Dominant Color .json**
`frame_captures_to_json.py` will take a directory of images and find the dominant color for each image. These are stored into a .json file in a `filename : color` representation to be used for processing each pixel and finding the best representation of that pixels color.

**Instructions**
`python3 frame_captures_to_json.py -i ./input_folder/ -o output_name` to execute the program.
* `-i` Input Directory
    * A directory in which all of your images are being stored for processing
* `-o` Filename
    * The output name you would like the .json saved as 
    * The compelted .json will always be stored inside the `./dominant_data/` directory  

### Step Three -
**Create Mosaic**
`image_mosaic.py` utelizes the previous steps results and converts an original image, into another image made up of many smaller images, giving the **mosaic** look.

**Instructions**
`python3 image_mosaic.py -i ./input_images/filename.jpg -o ./mosaic.jpeg` to execute the program.
* `-i` Input image
    * This is the image used for processing.
    * Should support .jpg, .jpeg, .bmp, .png and others. But just incase stick with .jpg
* `-o` Filename
    * The output name you would like the final mosaic image to be saved as  

**WARNING:** Processing images may take a long time. For quick results use very small images. The larger the image, the longer it will take.


## Results

#### Original
![Original Iron Man](examples/ironman_original.jpg?raw=true "Original Iron Man")  

https://www.briceallard.com/images/ironman_original.jpg  

#### Output
![Mosaic Iron Man](examples/ironman_mosaic_example.png?raw=true "Mosaic Iron Man")  

For best quality open in browser, or download.  
https://www.briceallard.com/images/ironman_mosaic.jpg

#### Original
![Original Avengers](examples/avengers_original.jpg?raw=true "Original Avengers")  

https://www.briceallard.com/images/avengers_original.jpg

#### Output
![Mosaic Avengers](examples/avengers_mosaic_example.png?raw=true "Mosaic Avengers")  

For best quality open in browser, or download.  
https://www.briceallard.com/images/avengers_mosaic.jpg