# pyllustrate
Text-based command-line image creation for quick pixel-art via python.

## Background
I've always loved using applications such as asesprite for quick pixel-art while working on various projects. However, after the jump to Ubuntu I have grown tired of switching back to Mac OS to make a simple sprite. Pyllustrate hopes to solve this issue.

## Dependencies
* Works with ```Python 3.6```
* For conversions to png and jpg, ```ImageMagick``` is required for Linux and the ```PIL``` library is required for Python

## Example
Navigate to the pyllustrate folder and type ```python3.6 pyllustrate.py paladin.txt paladinimage -m 100 -t png``` to convert paladin.txt into a ppm and png.


Warning: The ppm created from the image is P3 style, and therefore takes up a large amount of space. Be careful when using magnify as you may get an image much larger than you desired. For this reason, magnify is cut off at 1000, but should probably not be used at over 100.
