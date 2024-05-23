import cv2
import csv
import os

# Function to extract pixel values from an image
def extract_pixels(image_path):
    # Read the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Resize the image to 20x20 pixels
    resized_img = cv2.resize(img, (20, 20))
    # Flatten the image array
    flattened_img = resized_img.flatten()
    return flattened_img

# Directory containing the JPEG images
image_dir = "numbers"

# List to store pixel values and labels of all images
data = []

# Loop through all images in the directory
for filename in os.listdir(image_dir):
    if filename.endswith(".jpg"):
        # Get the full path of the image
        image_path = os.path.join(image_dir, filename)
        # Extract pixel values
        pixels = extract_pixels(image_path)
        # Extract label from the filename (first character)
        label = filename[0]
        # Append label and pixel values to the data list
        data.append([label] + list(pixels))

# Write pixel values and labels to a CSV file
csv_file = "numbers.csv"
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["Label"] + ["Pixel" + str(i) for i in range(1, len(data[0]))])
    # Write label and pixel values for each image
    writer.writerows(data)

print("CSV file with labels saved successfully.")