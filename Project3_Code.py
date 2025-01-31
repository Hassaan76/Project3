
#PART 1
import cv2
import numpy as np
import os


INPUT_IMAGE_PATH = "C:/Users/hassa/Documents/GitHub/Projects/Project3/motherboard_image.JPEG"
OUTPUT_DIR = "C:/Users/hassa/Documents/GitHub/Projects/Project3/processed"
EDGE_IMAGE_PATH = f"{OUTPUT_DIR}/edge_detected_image.JPEG"
MASKED_IMAGE_PATH = f"{OUTPUT_DIR}/masked_image.JPEG"
EXTRACTED_IMAGE_PATH = f"{OUTPUT_DIR}/extracted_motherboard.JPEG"

os.makedirs(OUTPUT_DIR, exist_ok=True)

original_image = cv2.imread(INPUT_IMAGE_PATH)
if original_image is None:
    raise FileNotFoundError(f"Image not found at {INPUT_IMAGE_PATH}")

rotated_image = cv2.rotate(original_image, cv2.ROTATE_90_CLOCKWISE)
grayscale_image = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)
blurred_image = cv2.GaussianBlur(grayscale_image, (45, 45), 5)
_, binary_image = cv2.threshold(blurred_image, 110, 255, cv2.THRESH_BINARY)

edges = cv2.Canny(binary_image, threshold1=120, threshold2=250)
edges_dilated = cv2.dilate(edges, kernel=np.ones((5, 5), np.uint8), iterations=8)

cv2.imwrite(EDGE_IMAGE_PATH, edges_dilated)
print(f"Edge-detected image saved at: {EDGE_IMAGE_PATH}")

contours, _ = cv2.findContours(edges_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if not contours:
    raise Exception("No contours detected.")
largest_contour = max(contours, key=cv2.contourArea)
mask = np.zeros_like(grayscale_image)
cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED)

isolated_motherboard = cv2.bitwise_and(rotated_image, rotated_image, mask=mask)

cv2.imwrite(MASKED_IMAGE_PATH, isolated_motherboard)
print(f"Masked image saved at: {MASKED_IMAGE_PATH}")
final_extracted_image = isolated_motherboard
cv2.imwrite(EXTRACTED_IMAGE_PATH, final_extracted_image)
print(f"Final extracted motherboard image saved at: {EXTRACTED_IMAGE_PATH}")






#Part 2

"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1agdEJmShzpmrwaanB_VviaD9S-zEJ4Vg
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install ultralytics

from ultralytics import YOLO
import shutil

model = YOLO('yolov8n.pt')


model.train(
    data='/content/drive/MyDrive/Project3/data.yaml',
    epochs=175,
    lr0=0.001,
    batch=8,
    imgsz=900,
    name='pcb_detector_refined',
    project='/content/drive/MyDrive/Project3/runs',
    augment=True,
    patience=10
)

print("Refinement training complete!")


results_dir = '/content/drive/MyDrive/Project3/runs/detect/pcb_detector_refined'
best_weights = f'{results_dir}/weights/best.pt'
last_weights = f'{results_dir}/weights/last.pt'

try:
    shutil.copy(best_weights, '/content/drive/MyDrive/Project3/best.pt')
    shutil.copy(last_weights, '/content/drive/MyDrive/Project3/last.pt')
    print(f"Best weights saved at: /content/drive/MyDrive/Project3/best.pt")
    print(f"Last weights saved at: /content/drive/MyDrive/Project3/last.pt")
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Model weights not found.")

from ultralytics import YOLO

model = YOLO('/content/drive/MyDrive/Project3/runs/pcb_detector_refined2/weights/best.pt')

results = model.predict(source='/content/drive/MyDrive/Project3/evaluation', save=True)

print("Testing completed.")

import shutil

best_weights = '/content/drive/MyDrive/Project3/runs/pcb_detector_refined2/weights/best.pt'
last_weights = '/content/drive/MyDrive/Project3/runs/pcb_detector_refined2/weights/last.pt'

backup_path = '/content/drive/MyDrive/Project3'

try:
    shutil.copy(best_weights, f'{backup_path}/best.pt')
    shutil.copy(last_weights, f'{backup_path}/last.pt')
    print(f"Backups created at: {backup_path}/best.pt and {backup_path}/last.pt")
except Exception as e:
    print(f"Error during backup: {e}")
