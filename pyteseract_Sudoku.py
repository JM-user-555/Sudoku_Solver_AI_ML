import cv2
import pytesseract

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

def preprocess_image(image_path):
    image = cv2.imread(image_path) # Load the image

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to get a binary image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    denoised = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21) # Remove noise the image

    # Resize the image
    scale_percent = 150  # Percent of original size
    width = int(denoised.shape[1] * scale_percent / 100)
    height = int(denoised.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(denoised, dim, interpolation=cv2.INTER_LINEAR)

    return resized

def perform_ocr(image):
    # Define custom configuration
    custom_config = r'--oem 1 --psm 7 -c tessedit_char_whitelist=0123456789'
    #custom_config="--psm 7 -c tessedit_char_whitelist=0123456789"
    # Perform OCR on the processed image
    text = pytesseract.image_to_string(image, config=custom_config)
    

    return text




def main(image_path):
    processed_image = preprocess_image(image_path)
    ocr_result = perform_ocr(processed_image)
    return ocr_result

