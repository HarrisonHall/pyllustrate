'''Program Logic:
parse through code:
1. Parse first line to get writeName1
2. Check if write name 1 and 2 are taken, if not write to ~
3. Parse "use *"  and "* (*,*,*)" and replace
4. Start at {
5. Write pixels for characters
   a. Write black or translucent
   b. 
6. Finish file at EOF or }

Note: I need a lot of try or excepts to help with bug fixing

Command line: pyllustrate filename [-tools*, -name, -magnify, -type (png, jpg, etc.)] writeName2
'''

import sys

tools = 0 # 0 is no tools
fileName = "" # 0 is no new name
magnify = 1
imageType = ""
writeName = ""
#myiterator = 1

##Read command line arguments
def checkArguments():
    global tools
    global fileName
    global magnify
    global imageType
    global writeName
    commands = sys.argv
    fileName = commands[1]
    writeName = commands[2]
    for i in range(len(commands)):
        if commands[i] == "-n" or sys.argv[i] == "-name":
            writeName = commands[i+1]
        if commands[i] == "-t" or commands[i] == "-type":
            if commands[i+1] == "png":
                try:
                    #import image as image
                    imageType = "png"
                except:
                    print("Please install PIL")
            elif commands[i+1] == "jpeg" or commands[i+1] == "jpg":
                try:
                    #import image as image
                    imageType = "jpeg"
                except:
                    print("Please install PIL")
            else:
                print("Unspecified type.")
        if commands[i] == "-m" or commands[i] == "-magnify":
            try:
                import math
                magnify = math.floor(int(commands[i+1]))
                if magnify > 1000 or magnify < 1:
                    magnify = 1
            except:
                print("Error with magnify")
                magnify = 1

##Check if file name is taken, if not return file to be written, if so, change ~, if taken, add iterator until not
def checkFile():
    fileName = sys.argv[1]
    return fileName

##Writes to file
def writeFile(writeString,writeFile):
    writefile = open(writeFile+".ppm","w+")
    for line in writeString:
        writefile.write(line+"\n")
    global imageType
    if imageType == "jpeg":
        try:
            import os
            os.system("convert "+writeFile+".ppm "+writeFile+".ppm")
            from PIL import Image
            ppm = Image.open(writeFile+".ppm")
            newjpeg = ppm.convert("RGB")
            newjpeg.save(writeFile+".jpg")
        except:
            print("Please install PIL and ImageMagick.")
    if imageType == "png":
        try:
            import os
            os.system("convert "+writeFile+".ppm "+writeFile+".ppm")
            from PIL import Image
            ppm = Image.open(writeFile+".ppm")
            newpng = ppm.convert("RGB")
            newpng.save(writeFile+".png")
        except:
            print("Please install PIL and ImageMagick.")

def replaceExistingPalette(paletteList,line):
    i = 0
    while (i < len(paletteList)):
        if line[0] == paletteList[i]:
            paletteList[i+1] = line[2:len(line)-1]
    return paletteList
            
##Searches through and writes palette
def definePalette(filename):
    paletteList = []
    checkFile = open(filename)
    attempt = ""
    x = 0
    for line in checkFile:
        if x == 0:
            x += 1
            continue
        if "{" in line:
            break
        if line[:3].lower() == "use":
            attempt = line[4:]
            attempt = attempt[:len(attempt)-1] #remove newline
            try:
                palette = "palettes/" + attempt + ".txt"
                palette = open(palette)
                iterator = 1
                for line in palette:
                    if iterator != 1:
                        try:
                            if line[0] not in paletteList:
                                paletteList.append(line[0])
                                rgbVals = line[2:len(line)-1]
                                paletteList.append(rgbVals)
                            else:
                                paletteList = replaceExistingPalette(paletteList,line)
                        except:
                            print("Issue with palette.")
                    iterator += 1
                palette.close()
            except:
                try:
                    palette = attempt + ".txt"
                    palette = open(attempt+"txt")
                except:
                    pass
        else:
            if line[0] not in paletteList:
                paletteList.append(line[0])
                paletteList.append(line[2:len(line)-1])
            else:
                paletteList = replaceExistingPalette(paletteList,line)
        x += 1
    print(paletteList)
    checkFile.close()
    return paletteList
                
##Finds numbers to write
def getWriteString(filename,palette,multiplier):
    checkFile = open(filename)
    writeList = ["P3","","255"]
    write = False
    writeListPart = 3
    rows = 0
    columns = 0
    for line in checkFile:
        if write == True:
            if columns == 0:
                columns = len(line) - 1
            if "}" in line:
                writeList[1] = str(columns*multiplier) + " " + str(rows*multiplier) #width height
                return writeList
            writeList.append("")
            for character in line:
                i = 0
                written = False
                while (i < len(palette)):
                    if character == palette[i]:
                        for x in range(multiplier):
                            writeList[writeListPart] += palette[i+1] + "\t"
                        written = True
                    i += 1
                if written == False:
                    if character != "\n" and character != " " and character != "\t":
                        for x in range(multiplier):
                            writeList[writeListPart] += "0 0 0\t"
            for x in range(multiplier-1):
                writeList.append(writeList[len(writeList)-1])
                writeListPart += 1
            writeListPart += 1
            rows += 1
        if write == False:
            if "{" in line:
                write = True
                
##Begin
checkArguments()
palette = definePalette(fileName)
writeString = getWriteString(fileName,palette,magnify)
writeFile(writeString, writeName)
