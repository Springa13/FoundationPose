import os
import cv2
import numpy as np
from segment_anything import SamPredictor, sam_model_registry
import sys

# Initialize SAM model
def initialize_sam(model_type="vit_b", checkpoint_path="weights/SAM/sam_vit_b.pth"):
    sam = sam_model_registry[model_type](checkpoint=checkpoint_path)
    return SamPredictor(sam)

# Mouse callback function
def click_event(event, x, y, flags, param):
    global predictor, input_points, input_labels, clicked_event
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get input point and label (1 for foreground)
        input_points.append([x, y])
        input_labels.append(1)
        
        clicked_event = True
        
def display_mask(image, mask):
    # Create a color mask
    color_mask = np.zeros_like(image)
    color_mask[mask > 0] = [0, 0, 255]  # Green mask

    # Blend with original image
    blended = cv2.addWeighted(image, 0.8, color_mask, 0.4, 0)
    
    # Show the result
    cv2.imshow("frame000000", blended)

def save_mask(mask_path, image, mask):
    # Create white mask on black background
    binary_mask = np.zeros_like(image, dtype=np.uint8)
    binary_mask[mask > 0] = 255  # White where mask is True
    
    # Optionally save the mask
    cv2.imwrite(mask_path, binary_mask)

# Main code
def create_mask(data_folder):
    global predictor, input_points, input_labels, clicked_event
    clicked_event = False
    
    # Load image
    rgb_path = f'data/{data_folder}/rgb/frame000000.png'
    mask_path = f'data/{data_folder}/masks/frame000000.png'
    
    image = cv2.imread(rgb_path)
    if image is None:
        print("Error: Could not load image")
        exit()
    
    # Initialize SAM predictor
    predictor = initialize_sam()
    
    # Set the image for SAM
    predictor.set_image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    # Display image and set mouse callback
    cv2.imshow("frame000000", image)
    cv2.setMouseCallback("frame000000", click_event)
    
    print("Click on an object to segment it. Press 'r' to reset. Press 's' to save. Press 'q' to save and quit.")
    
    input_points = []
    input_labels = []

    while True:
        if (clicked_event):
            points = np.array(input_points)
            labels = np.array(input_labels)

            masks, scores, logits = predictor.predict(
                point_coords=points,
                point_labels=labels,
                multimask_output=False,
            )

            display_mask(image, masks[0])
            # Predict masks
            
            
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            save_mask(mask_path, image, masks[0])
        elif key == ord('r'):
            input_points = []
            input_labels = []
            clicked_event = False
            cv2.imshow("frame000000", image)
            
        
    cv2.destroyAllWindows()
        
      
create_mask(sys.argv[1])
