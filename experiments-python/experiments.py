import os

import openai
from PIL import Image
import time
import numpy as np

#delete when submitting
openai.api_key = "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"

#opening test_data including all the objects that should be drawn
with open('test_data.txt') as f:
    objects_to_draw = f.read().splitlines()  
pixelMatrix = [ [ 0 for _ in range( 8 ) ] for _ in range( 8 ) ]


#enumerates all test data and makes one api call per test case
def main():
    for i, object in enumerate(objects_to_draw): 
        #used if the experiments failed in between test cases and I want to start at a certain test case
        if (i<0): continue

        response= openai.Completion.create(
            model="code-davinci-002",
            prompt=generate_prompt(object),
            temperature=0.3,
            max_tokens = 350,
            stop = "###"
        )
        f= open('raw_responses.txt', 'a')
        f.write("\n"+response.choices[0].text)
        f.close()
        response_split_filtered = filter_response(response.choices[0].text.splitlines())
        print(response_split_filtered)
        for i, line in enumerate(response_split_filtered): 
            for j, char in enumerate(line):
                pixelMatrix[i][j]=int(char)
        save_image(object)

        #sleep time needed to avoid api call restricions by openAI
        time.sleep(20)
        if(i%5 == 0): 
            print("sleeping ...")
            time.sleep(90)

#filter everything that is not one row of an image (needed for cot responses)
def filter_response(response_list):
    filtered_response = []
    for i in response_list:
        if i.isdigit() and i.count("0") + i.count("1") == len(i):
            filtered_response.append(i)
    return filtered_response

def save_image(object_to_draw):
    image = Image.new("RGB", (8, 8))
    for i in range(8):
        for j in range(8):
            if pixelMatrix[i][j] == 1:
                image.putpixel((j, i), (0, 0, 0))
            else:
                image.putpixel((j, i), (255, 255, 255))
    image.resize((400, 400), resample=0).save("generated_images/{}.png".format(object_to_draw.replace(" ", "_")))
    print("saved image {}".format(object_to_draw))


def generate_prompt(object_to_draw):
    return """Images displayed on a computer screen are actually a collection of dots of color, called pixels. If you look really closely at the screen, you will be able to see the individual pixels. The collection of pixels that make up an image are stored as a matrix.
We can represent different objects (e.g., numbers, letters, or shapes) by creating a pixel matrix which consists of 0s and 1s. The matrix should be of the size 8 by 8. Each entry represents a pixel of a black or a white pixel. That means the image has a display capable of 8 pixels in width and 8 pixels in height. Since there are only 64 pixels in total the objects to be displayed are significantly simplified. 
In the following examples, the images are created step-by-step from top to bottom. The examples are not complete, it is possible to use other structures. It is very important that each pixel matrix consisits of only 8 rows. 

Here is an example of creating a 8 by 8 grid of pixels step-by-step to form an image of the number three:
The number 3 was originally denoted by three lines. Overtime these lines have been curved, rotated and connected to form the current representation.
The top two rows of an 8 by 8 pixel matrix representing the number three show the first curved line and it looks like an arc or semicircle (2 pixel rows):
00111100
01000010
The next part of the image of a three represents the second horizontal line with two aditional slightly curved vertical strokes (3 pixel rows):
00000110
00111100
00000110
The bottom of the number three looks like the top but rotated by 180 degrees. It is a semicircle and the open part points upwards (2 pixel rows):
01000010
00111100
The last row of the 8 by 8 pixel matrix is not needed to form the number three and is therefore left white (1 pixel row):
00000000
This makes a total of 2+3+2+1=8 pixel rows.
###

Here is an example of generating a grid of pixels that form an image of the number 8. Each part of the image is described step-by-step:
Number 8 is represented by two loops on top of each other.
The first loop (4 pixel rows): 
00111100
01000010
01000010
00111100
The second loop without the top part which is also part of the first loop (4 pixel rows):
01000010
01000010
00111100
00000000
This makes a total of 4+4=8 pixel rows.
###

Here is an example of an 8 by 8 pixel matrix showing the capital letter F including the chain of thought:
Graphically the capital letter F consists of one large vertical line on the left and two horizontal lines: one at the top and one at in middle of the vertical line.
The first row of the grid of pixels forms the first horizontal line of the letter F (1 pixel row):
01111110
The following part of the pixel matrix shows part of the large vertical line that is in between the two horizontal lines (2 pixel rows):
01000000
01000000
The next part of the letter F is the second horizontal line (1 pixel row):
01111110
The bottom half of the image shows the remaining of the vertical line (4 pixel rows):
01000000
01000000
01000000
01000000
This makes a total of 1+2+1+4=8 pixel rows.
###

Here is an example of creating a 8 by 8 grid of pixels step-by-step to form an image of the letter Z:
The graphic representation of the capital letter Z consists of two horizontal lines that are connected with left slanted diagonal.
First, the horizontal line at the top (1 pixel row):
11111111
Second, the diagonal that connects the top and bottom lines (6 pixel rows):
00000011
00000110
00011000
00110000
01100000
11000000
Last, the horizontal line at the bottom of the letter Z (1 pixel row):
11111111
This makes a total of 1+6+1 = 8 pixel rows. 
###

Here is an example of generating a grid of pixels that form an image of a colon. Each part of the image is described step-by-step.
The colon is a punctuation mark consisting of two equally sized dots aligned vertically.
The first row of pixels is left white because the space is not needed to draw a colon (1 pixel row):
00000000
The first dot (2 pixel rows):
00001100
00001100
The space inbetween the dots (1 pixel row):
00000000
The second dot (2 pixels rows):
00001100
00001100
The remaining of the 8 by 8 pixel matrix is left white (2 pixel rows):
00000000
00000000
This makes a total of 1+2+1+2+2=8 pixel rows.
###

Here is an example of an 8 by 8 pixel matrix showing the equal sign including the chain of thought:
The equal sign is a mathematicl symbol which is represented by two equally sized horizontal lines with space inbetween.
The top row of the 8 by 8 pixel matrix is left white (1 pixel row):
00000000
The first horizontal line (2 pixel rows):
11111111
11111111
The whitespace inbetween the two lines (2 pixel rows):
00000000
00000000
00000000
The second horizontal line (2 pixel rows):
11111111
11111111
This makes a total of 1+2+3+2 = 8 pixel rows.
###

Here is an example which is not a 8 by 8 grid of pixel because it has more than 8 pixel rows:
The graphic representation of the number 7 consists of a large diagonal line that is connected to a vertical line.
The diagonal line (7 pixel rows):
00000011
00000110
00001100
00011000
00110000
01100000
11000000
The vertical line (7 pixel rows):
11000000
11000000
11000000
11000000
11000000
11000000
11000000
This makes a total of 7+7=14 pixel rows. This is too much!

Here is an example of creating a 8 by 8 grid of pixels step-by-step to form an image of {}:
""".format(object_to_draw)

main()