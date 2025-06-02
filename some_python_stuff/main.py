import cv2
import easyocr
import matplotlib.pyplot as plt

image_path = r'C:\Users\Sampreet\Downloads\mu_boli_sex.png'

image = cv2.imread(image_path)

# Convert BGR to RGB (OpenCV loads images in BGR)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if you have a GPU

# Perform OCR
results = reader.readtext(image_path, detail=1)

# Display results
for (bbox, text, confidence) in results:
    print(f'Detected: "{text}" with confidence {confidence:.2f}')
    # Draw bounding boxes
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(image, text, (top_left[0], top_left[1] - 10), 
    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

# Show the image with boxes (optional)
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title('Handwritten Text Detection')
plt.show()
