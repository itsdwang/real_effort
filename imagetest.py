 
from PIL import Image, ImageDraw, ImageFont
import math


# create Image object with the input image
def writeText(text, fileName): 
    image = Image.open('background.png')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('Roboto-Regular.ttf', size=12)
    imageChars = 50
    numLines = len(text) / imageChars
    numLines = int(math.ceil(numLines))
    lines = []
    for i in range(numLines):
        if(imageChars * (i + 1) < len(text)):
            lines.append(text[imageChars * i : imageChars * (i+1)])
        else:
            lines.append(text[imageChars * i : len(text)])

            

    for i in range(numLines):
        (x, y) = (10, 20 * i)
        message = lines[i]
        color = 'rgb(0, 0, 0)' # black color
        draw.text((x, y), message, fill=color, font=font)

    image.save(fileName + '.png')

