from __future__ import print_function
from PIL import Image
import os, sys

# Function to extract a string from a png image.
def extract(image):
    # Open the file passed in as an argument
    infile = Image.open(image)
    
    # Make sure the image is in RBG mode
    rgb_file = infile.convert('RGB')
    
    # Get the maximum dimensions of the image (offest to be indexed)
    width = infile.width - 1
    height = infile.height - 1

    # Check the first 11 pixels for the string length
    bLen = ""
    for x in range(0,11):
        # Split the color bands of each pixel
        r, g, b = rgb_file.getpixel((width, height))
        
        # Add the least significant bit of each color band to a bit string
        bLen += str(r&1)
        bLen += str(g&1)
        # Skip the last blue bit, because length is a 32-bit integer
        if x < 10:
            bLen += str(b&1)
            
        # Jump up to the next row of pixels, in case the image is less than 11 pixels wide
        if width != 0:
            width -= 1
        else:
            width = infile.width - 1
            height -= 1
            
    # Convert the bit string to an integer
    numLen = int(bLen, 2)

    # Extract the bits from the image to get the message
    bMes = ""
    strMes = ""
    while numLen > 0:
        # Split the color band for each pixel
        r, g, b = rgb_file.getpixel((width, height))
        
        # Add the least significant bit of each color band to a bit string
        bMes += str(r&1)
        
        # extract the character after every 8th bit
        if len(bMes) == 8:
            strMes += chr(int(bMes, 2))
            bMes = ""
            
        bMes += str(g&1)
        
        if len(bMes) == 8:
            strMes += chr(int(bMes, 2))
            bMes = ""
            
        bMes += str(b&1)

        if len(bMes) == 8:
            strMes += chr(int(bMes, 2))
            bMes = ""
            
        # Jump up to the next row of pixels if needed
        if width != 0:
            width -= 1
        else:
            width = infile.width - 1
            height -= 1
        numLen -= 3
            
    # Output the message to console
    print(strMes)
    

# Function to inject a string into a jpeg image
def inject(image, message):
    # Open the input file
    infile = Image.open(image)

    # Make sure the image is in RBG mode
    rgb_file = infile.convert('RGB')

    # Load the pixel map
    pixels = infile.load()

    # Get the maximum dimensions of the image (offest to be indexed)
    width = infile.width - 1
    height = infile.height - 1

    # Convert the length of the message into a string of bits
    messLen = '{0:032b}'.format(len(message)*8)

    # Insert the bits of the length into the pixels
    for x in range(0, 11):
        # Split the color band for each pixel
        r, g, b = rgb_file.getpixel((width, height))

        # Get the bit to go into the red value
        rBit = int(messLen[0])
        messLen = messLen[1:]

        # Get the bit to go into the green value
        gBit = int(messLen[0])
        messLen = messLen[1:]

        if x < 10:
            # Get the bit go into the blue value
            bBit = int(messLen[0])
            messLen = messLen[1:]

            # Insert the 3 color bits into the pizel
            pixels[width, height] = ((r&~1)| rBit, (g&~1) | gBit, (b&~1) | bBit)
        else:
            # If the 11th pixel just insert the red and green bits
            pixels[width, height] = ((r&~1)| rBit, (g&~1) | gBit, b)

        # Jump up to the next row of pixels if needed
        if width != 0:
            width -= 1
        else:
            width = infile.width - 1
            height -= 1
            
    # Convert the message into a string of bits, character by character
    strBits = ""
    for char in message:
        strBits += '{0:08b}'.format(ord(char))

    # Insert the message bits into the image
    while len(strBits) > 0:
        # Split the color band for each pixel
        r, g, b = rgb_file.getpixel((width, height))

        rBit = int(strBits[0])
        strBits = strBits[1:]

        if len(strBits) > 0:
            gBit = int(strBits[0])
            strBits = strBits[1:]
        else:
            gBit = 2

        if len(strBits) > 0:
            bBit = int(strBits[0])
            strBits = strBits[1:]
        else:
            bBit = 2

        # Insert the bits into the color bands of the pixel, keeping tabs on the end of string
        if gBit > 1:
            pixels[width, height] = ((r&~1)| rBit, g, b)
        elif bBit > 1:
            pixels[width, height] = ((r&~1)| rBit, (g&~1) | gBit, b)
        else:
            pixels[width, height] = ((r&~1)| rBit, (g&~1) | gBit, (b&~1) | bBit)

        # Jump up to the next row of pixels if needed
        if width != 0:
            width -= 1
        else:
            width = infile.width - 1
            height -= 1

    # Save the image
    newFile = image[:-3] + "png"
    infile.save(newFile)
    print("Message has been hidden inside " % (newFile))

