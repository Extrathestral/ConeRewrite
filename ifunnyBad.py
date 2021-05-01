import cv2
import numpy as np
from PIL import Image
image = cv2.imread('t.jpg')

pixelIsYellow = lambda pixel: 100 < pixel[2] < 250 and 90 < pixel[1] < 235 and 40 < pixel[0] < 135
pixelIsBlack = lambda pixel: pixel[2] < 50 and pixel[1] < 50 and pixel[0] < 50

def getRowColorPercentages(imageRange):
    blackCount = 0
    yellowCount = 0
    otherCount = 0
    for i in imageRange:
        if pixelIsYellow(i):
            yellowCount += 1
        elif pixelIsBlack(i):
            blackCount += 1
        else:
            otherCount += 1
    totalCount = blackCount + yellowCount + otherCount
    blackPercent = float(blackCount)/float(totalCount)
    yellowPercent = float(yellowCount)/float(totalCount)
    otherPercent = float(otherCount)/float(totalCount)
    return blackPercent, yellowPercent, otherPercent
def rowIsBlackAndYellow(imageRange):
    blackPercent, yellowPercent, otherPercent = getRowColorPercentages(imageRange)
    return blackPercent+yellowPercent > 0.75

def hasBlackBar(image):
    reversedImage = image[::-1]
    blackBarArr = [rowIsBlackAndYellow(i) for i in reversedImage[:19]]
    # print(blackBarArr)
    return False not in blackBarArr

def hasIFunnyWatermark(image):
    if hasBlackBar(image):
        reversedImage = image[::-1]
        hasWatermark = True
        counter = 1
        for i in reversedImage[7:17]:
            blackPercent, yellowPercent, otherPercent = getRowColorPercentages(i[-134:-9])
            print(counter, blackPercent, yellowPercent, otherPercent)
            counter += 1
            if yellowPercent > 0.3:
                print("Has")
                continue
            else:
                print("Hasn't")
                hasWatermark = False
                break
        return hasWatermark

def cropIFunnyWatermark(image):
    return image[:-20]

def iFunnyFilter(imageInput):
    pil_image = imageInput.convert('RGB')
    image = np.array(pil_image)
    image = image[:, :, ::-1].copy()
    if hasIFunnyWatermark(image):
        newImage = cropIFunnyWatermark(image)
        img = cv2.cvtColor(newImage, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        return im_pil
    else:
        return

def main():
    if not hasIFunnyWatermark(image):
        print("Does not have watermark.")
    else:
        newImage = cropIFunnyWatermark(image)
        cv2.imwrite("saved.png",newImage)


if __name__ == "__main__":
    main()
