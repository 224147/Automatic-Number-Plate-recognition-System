import cv2
import imutils

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_russian_plate_number.xml"

plate_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def detect_number_plate(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise Exception(f"Image not found: {image_path}")

    image = imutils.resize(image, width=700)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(25, 25)
    )

    if len(plates) == 0:
        raise Exception("Number plate not detected")

    x, y, w, h = plates[0]

    plate = image[y:y+h, x:x+w]

    return image, plate, (x, y, w, h)