import cv2
import numpy as np

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    return thresh

def split_lines(block, line_gap=5):
    horizontal_sum = np.sum(block, axis=1)
    in_line = False
    line_boxes = []
    for i, val in enumerate(horizontal_sum):
        if val > 0 and not in_line:
            in_line = True
            y0 = i
        elif val == 0 and in_line:
            in_line = False
            y1 = i
            if y1 - y0 > line_gap:
                line_boxes.append((y0, y1))
    if in_line:
        line_boxes.append((y0, block.shape[0]-1))
    return line_boxes

def split_characters(line_roi, min_gap=2):
    vertical_sum = np.sum(line_roi, axis=0)
    in_char = False
    char_boxes = []
    for i, val in enumerate(vertical_sum):
        if val > 0 and not in_char:
            in_char = True
            x0 = i
        elif val == 0 and in_char:
            in_char = False
            x1 = i
            if x1 - x0 > min_gap:
                char_boxes.append((x0, x1))
    if in_char:
        char_boxes.append((x0, line_roi.shape[1]-1))
    return char_boxes

def normalize_character(char_roi, target_size=(32,32)):
    rows = np.any(char_roi, axis=1)
    if not np.any(rows):
        return None
    y_start, y_end = np.where(rows)[0][[0,-1]]
    char_roi = char_roi[y_start:y_end+1, :]
    
    h, w = char_roi.shape
    max_side = max(h,w)
    if max_side == 0:
        return None
    scale = (target_size[0]-4)/max_side
    new_w, new_h = max(1,int(w*scale)), max(1,int(h*scale))
    char_resized = cv2.resize(char_roi, (new_w,new_h), interpolation=cv2.INTER_AREA)
    
    pad_top = (target_size[0]-new_h)//2
    pad_bottom = target_size[0]-new_h-pad_top
    pad_left = (target_size[1]-new_w)//2
    pad_right = target_size[1]-new_w-pad_left
    char_padded = np.pad(char_resized, ((pad_top,pad_bottom),(pad_left,pad_right)),
                         mode='constant', constant_values=0)
    return char_padded

def extract_characters_from_image_handwriting(image_path, target_size=(32,32), min_gap=2, line_gap=5, block_height=1000):
    thresh = preprocess_image(image_path)
    chars = []
    height = thresh.shape[0]
    
    for start_row in range(0, height, block_height):
        end_row = min(start_row + block_height, height)
        block = thresh[start_row:end_row, :]
        lines = split_lines(block, line_gap)
        
        for y0, y1 in lines:
            line_roi = block[y0:y1, :]
            char_boxes = split_characters(line_roi, min_gap)
            
            for x0, x1 in char_boxes:
                char_roi = line_roi[:, x0:x1]
                char_norm = normalize_character(char_roi, target_size)
                if char_norm is not None:
                    chars.append(char_norm)
    
    return chars