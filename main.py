import cv2
import numpy as np
import os

# Global variables
drawing = False
ix, iy = -1, -1
photo_boxes = []
sign_boxes = []
current_box = None
image = None
display_image = None
scale_factor = 1.0

def create_folders():
    for folder in ['photos', 'sign']:
        if not os.path.exists(folder):
            os.makedirs(folder)

def scale_coordinates(x, y, factor):
    return int(x / factor), int(y / factor)

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, photo_boxes, sign_boxes, current_box, image, display_image, scale_factor

    x, y = scale_coordinates(x, y, scale_factor)

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        current_box = []

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = display_image.copy()
            cv2.rectangle(img_copy, (int(ix*scale_factor), int(iy*scale_factor)), 
                          (int(x*scale_factor), int(y*scale_factor)), (0, 255, 0), 2)
            for box in photo_boxes:
                cv2.rectangle(img_copy, (int(box[0]*scale_factor), int(box[1]*scale_factor)), 
                              (int(box[2]*scale_factor), int(box[3]*scale_factor)), (255, 0, 0), 2)
            for box in sign_boxes:
                cv2.rectangle(img_copy, (int(box[0]*scale_factor), int(box[1]*scale_factor)), 
                              (int(box[2]*scale_factor), int(box[3]*scale_factor)), (0, 0, 255), 2)
            cv2.imshow('image', img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(display_image, (int(ix*scale_factor), int(iy*scale_factor)), 
                      (int(x*scale_factor), int(y*scale_factor)), (0, 255, 0), 2)
        current_box = [min(ix, x), min(iy, y), max(ix, x), max(iy, y)]

def process_image(image_path, image_index):
    global image, display_image, photo_boxes, sign_boxes, scale_factor, current_box

    # Reset global variables for each image
    photo_boxes = []
    sign_boxes = []
    current_box = None

    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Unable to read the image file at '{image_path}'")
        return

    # Scale the image to fit the screen
    screen_res = 1920, 700  # Adjust this to your screen resolution
    scale_width = screen_res[0] / image.shape[1]
    scale_height = screen_res[1] / image.shape[0]
    scale_factor = min(scale_width, scale_height)

    if scale_factor < 1:
        display_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)
    else:
        display_image = image.copy()
        scale_factor = 1.0

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_rectangle)

    while True:
        cv2.imshow('image', display_image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('p'):  # Press 'p' to add a photo box
            if current_box:
                photo_boxes.append(current_box)
                current_box = None
        elif key == ord('s'):  # Press 's' to add a signature box
            if current_box:
                sign_boxes.append(current_box)
                current_box = None
        elif key == ord('c'):  # Press 'c' to clear all boxes
            photo_boxes = []
            sign_boxes = []
            current_box = None
            display_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)
        elif key == ord('q'):  # Press 'q' to quit and process
            break

    cv2.destroyAllWindows()

    # Save the cropped areas immediately with unique filenames
    for i, box in enumerate(photo_boxes):
        photo = image[box[1]:box[3], box[0]:box[2]]
        save_compressed_image(f'photos/photo_{image_index+1}_{i+1}.jpg', photo)

    for i, box in enumerate(sign_boxes):
        signature = image[box[1]:box[3], box[0]:box[2]]
        save_compressed_image(f'sign/sign_{image_index+1}_{i+1}.jpg', signature)

    print(f"Processing complete for image: {os.path.basename(image_path)}")

def save_compressed_image(file_path, image, target_size_kb=20, quality_step=5):
    """
    Saves the image to the specified path with a size less than or equal to the target size in KB.
    """
    quality = 95  # Start with high quality
    while True:
        # Save the image with the current quality setting
        cv2.imwrite(file_path, image, [cv2.IMWRITE_JPEG_QUALITY, quality])
        
        # Check the file size
        file_size_kb = os.path.getsize(file_path) / 1024  # Convert to KB
        
        # If the file size is within the target size or quality is too low, stop
        if file_size_kb <= target_size_kb or quality <= 10:
            break
        
        # Reduce the quality for the next iteration
        quality -= quality_step

def process_sheet_folder():
    sheet_folder = 'Sheet'
    if not os.path.exists(sheet_folder):
        print(f"Error: The '{sheet_folder}' folder does not exist.")
        return

    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = [f for f in os.listdir(sheet_folder) if os.path.splitext(f)[1].lower() in image_extensions]

    if not image_files:
        print(f"No image files found in the '{sheet_folder}' folder.")
        return

    create_folders()

    for image_index, image_file in enumerate(image_files):
        image_path = os.path.join(sheet_folder, image_file)
        print(f"Processing image: {image_file}")
        process_image(image_path, image_index)

    print("All images processed. Check 'photos' and 'sign' folders for results.")

if __name__ == "__main__":
    process_sheet_folder()
