# USAGE
# python ocr.py --image images/example_01.png 
# python ocr.py --image images/example_02.png  --preprocess blur

# import the necessary packages
from PIL import Image #not quite shure why this is greyed out
import pytesseract
import argparse
import cv2
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Image, PageBreak

# parse the arguments for images through terminal (no args right now, should be handled by the for loop)
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image to be OCR'd")
# ap.add_argument("-p", "--preprocess", type=str, default="thresh",
# 	help="type of preprocessing to be done")
# args = vars(ap.parse_args())
#CREATES THE CANVAS THAT I CAN WRITE TO
canvas = canvas.Canvas("EnterFilenameHere.pdf",pagesize=landscape(letter))
canvas.setLineWidth(.3)
canvas.setFont('Helvetica', 12)
for file in os.listdir('/home/ping/.PyCharmCE2018.2/config/scratches/images'): #add dirname and images; should pass back the
    # load the example image and convert it to grayscale
    image = cv2.imread(file)
    #image = cv2.imread(args["image"]) #should be now loaded by the for loop
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Image", gray) #comment out; for testing

    # check to see if we should apply thresholding to preprocess the image can uncomment/rework if pictures are too grainy (should not be the case)
    # if args["preprocess"] == "thresh":
    #     gray = cv2.threshold(gray, 0, 255,
    #         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #
    # # make a check to see if median blurring should be done to remove
    # # noise
    # elif args["preprocess"] == "blur":
    #     gray = cv2.medianBlur(gray, 3)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    #TODO: .jpg format, currently all images in that directory are .png
    filename = "{}.png".format(os.getpid()) #switch to file format of the images that are passed through
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    print(text)

    # show the output images for testing
    # cv2.imshow("Image", image)
    cv2.imshow("Output", gray) #TODO: comment out
    cv2.waitKey(0) #TODO: comment out

    #writes the images to pdf
    canvas.drawImage(image,30,750, width=None, height=None) #draws image to odd page
    canvas.showPage() #next page
    canvas.drawString(100,750, text) #writes the ocr'd text ot even page
    canvas.showPage() #next page
    #end of loop



canvas.save()
#end