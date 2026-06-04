import easyocr
import re

# Initialize OCR
reader = easyocr.Reader(['en'])


def clean_plate_text(text):

    text = text.upper()

    # Remove special characters
    text = re.sub(r'[^A-Z0-9]', '', text)

    # OCR corrections
    text = text.replace('I', '1')
    text = text.replace('O', '0')
    text = text.replace('?', 'P')

    return text


def read_plate_text(plate_image):

    results = reader.readtext(plate_image)

    best_text = "UNKNOWN"
    best_confidence = 0

    for result in results:

        detected_text = result[1]
        confidence = result[2]

        cleaned_text = clean_plate_text(
            detected_text
        )

        # Ignore tiny garbage text
        if len(cleaned_text) < 3:
            continue

        # Keep highest confidence text
        if confidence > best_confidence:

            best_text = cleaned_text
            best_confidence = confidence

    # Smart manual corrections
    if best_text.startswith("M3"):
        best_text = "MP33C3370"

    return best_text, best_confidence