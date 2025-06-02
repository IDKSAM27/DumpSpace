import cv2
import easyocr
import matplotlib.pyplot as plt
import os

# Preprocess image: grayscale, blur, threshold, resize
def preprocess_image(image, scale_factor=2):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    resized = cv2.resize(thresh, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
    return resized, scale_factor

# Get script directory and image path
script_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(script_dir, 'images')
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp')

# Collect image files
try:
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(image_extensions)]
    if not image_files:
        print("No image files found in the 'images' directory.")
        exit()
except FileNotFoundError:
    print(f"Image directory not found: {image_dir}")
    exit()

# Initialize EasyOCR
reader = easyocr.Reader(['en'], gpu=False)

# Process each image
for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    image = cv2.imread(image_path)

    if image is None:
        print(f"Could not load image: {image_path}")
        continue

    # Preprocess image and get resized version
    processed_image, scale_factor = preprocess_image(image)

    # Perform OCR on processed (resized) image
    results = reader.readtext(processed_image, detail=1, allowlist='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

    print(f'\nResults for: {image_file}')
    for (bbox, text, confidence) in results:
        print(f'Detected: "{text}" with confidence {confidence:.2f}')

        # Scale bounding box back to original image coordinates
        scaled_bbox = [(int(x / scale_factor), int(y / scale_factor)) for (x, y) in bbox]
        (top_left, top_right, bottom_right, bottom_left) = scaled_bbox

        # Draw boxes and text on original image
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(image, text, (top_left[0], top_left[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # Display the result
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title(f'OCR Results: {image_file}')
    plt.show()
    plt.close()
