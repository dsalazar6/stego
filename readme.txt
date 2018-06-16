                         .       .
                        / `.   .' \
                .---.  <    > <    >  .---.
                |    \  \ - ~ ~ - /  /    |
                 ~-..-~             ~-..-~
             \~~~\.'                    `./~~~/
   .-~~^-.    \__/                        \__/
 .'  O    \     /               /       \  \
(_____,    `._.'               |         }  \/~~~/
 `----.          /       }     |        /    \__/
       `-.      |       /      |       /      `. ,~~|
           ~-.__|      /_ - ~ ^|      /- _      `..-'   f: f:
                |     /        |     /     ~-.     `-. _||_||_
                |_____|        |_____|         ~ - . _ _ _ _ _>

Stego the Steganograsaurus - A python utility by Daniel Salazar

DESCRIPTION:

The included python file includes two functions to use steganography to hides messages: 
one to extract messages from image files and one to inject messages into image files.
This is accomplished using the pillow library to access images and image maps as well as
access color bands pixel-bypixel, and standard bit manipulation to find/hide data on a
binary level. Data is found starting in the bottom right of images going to the upper
left, starting with message length and then the message itself.

INSTRUCTIONS:

1. Open a python shell in the command line by typing 'python' (without single quotes).
2. Compile the python functions by typing 'import stego'.

To inject a message into an image:
3. Call the inject function by typing 'stego.inject("image", "message")' (double quotes are required),
   where image is the name of the .jpg file used as a source image and message is the text you want
   to hide.
	a. The source file SHOULD be a .jpg file.
	b. Be sure to include the path if the file is not in the same directory as stego.py.
4. The program will inform you that the modified file was saved as a .png file, which can be found
   in the same directory as stego.py.

To extract a message from an image:
3. Call the extract function by typing 'stego.extract("image")' (double quotes are required),
   where image is the name of the .png file used as a source image.
	a. The source file SHOULD be a .png file.
	b. Be sure to include the path if the file is not in the same directory as stego.py.
4. The program will write the message out to the command line.