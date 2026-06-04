import cv2

from detector import detect_number_plate
from ocr_reader import read_plate_text
from utils import draw_plate_box

IMAGE_PATH = "../images/car1.jpg"

# Test image loading
test_image = cv2.imread(IMAGE_PATH)

if test_image is None:
    print("[ERROR] Image not loading")
    exit()

cv2.imshow("Loaded Image", test_image)
cv2.waitKey(2000)

try:

    # Detect number plate
    image, plate, coordinates = detect_number_plate(
        IMAGE_PATH
    )

    # Show detected plate
    cv2.imshow("Detected Plate", plate)
    cv2.waitKey(2000)

    # Convert to grayscale
    gray_plate = cv2.cvtColor(
        plate,
        cv2.COLOR_BGR2GRAY
    )

    # Noise removal
    gray_plate = cv2.bilateralFilter(
        gray_plate,
        11,
        17,
        17
    )

    # Improve contrast
    gray_plate = cv2.equalizeHist(
        gray_plate
    )

    # Adaptive threshold
    gray_plate = cv2.adaptiveThreshold(
        gray_plate,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # OCR text extraction
    plate_text, confidence = read_plate_text(
        gray_plate
    )

    print("\n===== ANPR RESULT =====")
    print("Detected Plate:", plate_text)
    print("Confidence:", confidence)

    # Draw box around plate
    output_image = draw_plate_box(
        image,
        coordinates,
        plate_text
    )

    # Show final output
    cv2.imshow("ANPR Result", output_image)

    cv2.waitKey(2000)

    cv2.destroyAllWindows()

except Exception as e:

    print("[ERROR]", e)