# import the necessary packages
import PIL.Image
import pytesseract
import cv2
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Image, PageBreak
import time

#CREATES THE CANVAS THAT I CAN WRITE TO
save_name = "Precalculus-Axler.pdf" #name of the pdf
canvas = canvas.Canvas(save_name,pagesize=landscape(letter))
canvas.setLineWidth(.3)
canvas.setFont('Helvetica', 12)
for file in sorted(os.listdir('/home/ping/.PyCharmCE2018.2/config/scratches/images')): #add dirname and images; should pass back the
    # load the example image and convert it to grayscale
    fname = ("/home/ping/.PyCharmCE2018.2/config/scratches/images/"+file) #opencv requires the entire filepath to the image
    print("reached " + fname) #testing
    image = cv2.imread(fname)
    #image = cv2.imread(args["image"]) #should be now loaded by the for loop
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("created gray image") #testing
    cv2.imshow("Image", gray) #testing
    # check to see if we should apply thresholding to preprocess the image can uncomment/rework if pictures are too grainy (should not be the case)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "Test_{}.png".format(os.getpid()) #creates a temporary bmp image file for pytesseract
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(PIL.Image.open(filename))
    os.remove(filename)
    print(text)

    # show the output images for testing
    # cv2.imshow("Image", image)
    cv2.imshow("Output", gray) #TODO: comment out
    cv2.waitKey(500) #testing; pops up the greyscale image that was ocr'd for half a second

    #writes the images to pdf
    canvas.drawImage(image,30,750) #draws image to odd page
    canvas.showPage() #next page
    canvas.drawString(100,750, text) #writes the ocr'd text ot even page
    canvas.showPage() #next page
    #end of loop



#canvas.save() #uncomment to save final pdf
#end