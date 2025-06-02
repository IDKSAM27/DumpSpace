import cv2
import easyocr
import matplotlib.pyplot as plt
import os

# Dynamically get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(script_dir, 'images')

# Supported image formats
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp')

# Get all image files in the directory
try:
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(image_extensions)]
except FileNotFoundError:
    print(f"Image directory not found: {image_dir}")
    exit(1)

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if you have a GPU

# Loop through all image files
for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    image = cv2.imread(image_path)

    if image is None:
        print(f"Could not load image: {image_path}")
        continue

    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform OCR
    results = reader.readtext(image_path, detail=1)

    # Display results
    print(f'\nResults for: {image_file}')
    for (bbox, text, confidence) in results:
        print(f'Detected: "{text}" with confidence {confidence:.2f}')
        # Draw bounding boxes
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(image, text, (top_left[0], top_left[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # Show the image with boxes
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title(f'OCR Results: {image_file}')
    plt.show()
