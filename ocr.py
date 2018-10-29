# import the necessary packages
import PIL.Image
import pytesseract
import cv2
import os
from textwrap import wrap
from reportlab import *
from reportlab.pdfgen import canvas
from datetime import datetime
from functools import reduce

#CREATES THE CANVAS THAT I CAN WRITE TO
save_name = "/home/ping/.PyCharmCE2018.2/config/scratches/Precalculus-Axler.pdf" #name + path of the pdf
canvas = canvas.Canvas(save_name,pagesize=(4032, 3024), bottomup=1)
totalTime = []
for file in sorted(os.listdir('/home/ping/.PyCharmCE2018.2/config/scratches/images')): #add dirname and images; should pass back the
    # load the example image and convert it to grayscale
    fname = ("/home/ping/.PyCharmCE2018.2/config/scratches/images/"+file) #opencv requires the entire filepath to the image
    print("reached " + fname) #testing
    image = cv2.imread(fname)
    #image = cv2.imread(args["image"]) #should be now loaded by the for loop
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("created gray image") #testing
    #cv2.imshow("Image", gray) #testing
    # check to see if we should apply thresholding to preprocess the image can uncomment/rework if pictures are too grainy (should not be the case)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "Test_{}.png".format(os.getpid()) #creates a temporary bmp image file for pytesseract
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    print("processing ocr filter...")
    time = datetime.now()
    text = pytesseract.image_to_string(PIL.Image.open(filename))
    os.remove(filename)
    #print(text) #commented for testing
    totalTime.append(datetime.now() - time)
    time = str(datetime.now() - time)
    print("time elapsed = " + time)
    print("total time taken so far = " + str(reduce(lambda x, y: x + y, totalTime)))
    print("avg time taken for each page so far = " + str(reduce(lambda x, y: x + y, totalTime) / len(totalTime)))

    #opencv prototyping code
    # cv2.imshow("Image", image)
    #cv2.imshow("Output", gray) #TODO: comment out
    #cv2.waitKey(500) #testing; pops up the greyscale image that was ocr'd for half a second

    #writes the images to pdf
    canvas.drawImage(fname, 0, 0) #draws image to odd page
    canvas.showPage() #next page
    y = 2900
    for line in wrap(text, 190): #text wraping so it doesn't go off the page
        canvas.setFont("Times-Roman", 45)
        canvas.drawString(100, y, line)  # writes the ocr'd text to even page
        y = y - 65
    canvas.showPage() #next page
    #end of loop

canvas.save() #uncomment to save final pdf

#metrics
print( "metrics")
print("total time taken = " + str(reduce(lambda x, y: x + y, totalTime)))
print("avg time taken for each page = " + str(reduce(lambda x, y: x + y, totalTime) / len(totalTime)))
#end