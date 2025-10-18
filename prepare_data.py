import os
import shutil
import re
import xml.etree.ElementTree as ET
from tqdm import tqdm
import config

def _parse_xml_for_yolo(xml_file):
    """
    Parses a single XML file and converts annotations to YOLO format.
    Uses the robust mapping from the config file.
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        size = root.find('size')
        if size is None: return None, None # Skip if size tag is missing
        w = int(size.find('width').text)
        h = int(size.find('height').text)
    except (ET.ParseError, AttributeError, ValueError):
        # Handle broken or malformed XML files
        return None, None

    annotations = []
    for obj in root.findall('object'):
        try:
            raw_label = obj.find('name').text.upper()
            if raw_label in config.XML_LABEL_TO_IDX:
                label_idx = config.XML_LABEL_TO_IDX[raw_label]
                
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)

                # Convert to YOLO format (center_x, center_y, width, height) normalized
                x_center = (xmin + xmax) / (2 * w)
                y_center = (ymin + ymax) / (2 * h)
                width = (xmax - xmin) / w
                height = (ymax - ymin) / h
                
                annotations.append(f"{label_idx} {x_center} {y_center} {width} {height}")
        except (AttributeError, ValueError):
            # Handle malformed object tags
            continue
            
    return annotations

def create_yolo_dataset():
    """
    Creates the complete YOLO dataset structure, including images, labels,
    and the train/val text files.
    """
    print("--- Step 1: Preparing YOLO dataset ---")
    
    # Clean up previous attempts
    if os.path.exists(config.YOLO_DATA_DIR):
        shutil.rmtree(config.YOLO_DATA_DIR)
        
    # Create directories
    images_train_dir = os.path.join(config.YOLO_DATA_DIR, "images", "train")
    images_val_dir = os.path.join(config.YOLO_DATA_DIR, "images", "val")
    labels_train_dir = os.path.join(config.YOLO_DATA_DIR, "labels", "train")
    labels_val_dir = os.path.join(config.YOLO_DATA_DIR, "labels", "val")
    
    os.makedirs(images_train_dir, exist_ok=True)
    os.makedirs(images_val_dir, exist_ok=True)
    os.makedirs(labels_train_dir, exist_ok=True)
    os.makedirs(labels_val_dir, exist_ok=True)

    # Process train and test lists
    for split, file_path, img_dest, lbl_dest in [
        ('train', config.TRAIN_TXT, images_train_dir, labels_train_dir),
        ('val', config.TEST_TXT, images_val_dir, labels_val_dir)
    ]:
        print(f"Processing {split} files...")
        with open(file_path, 'r') as f:
            file_ids = [line.strip() for line in f.readlines()]
        
        for file_id in tqdm(file_ids):
            xml_path = os.path.join(config.MULTI_ANNOTATIONS_DIR, f"{file_id}.xml")
            img_path = os.path.join(config.MULTI_IMAGES_DIR, f"{file_id}.jpg")

            if os.path.exists(xml_path) and os.path.exists(img_path):
                annotations = _parse_xml_for_yolo(xml_path)
                if annotations:
                    # Save label file
                    with open(os.path.join(lbl_dest, f"{file_id}.txt"), 'w') as label_file:
                        label_file.write("\n".join(annotations))
                    # Copy image file
                    shutil.copy(img_path, os.path.join(img_dest, f"{file_id}.jpg"))
    
    # --- CRITICAL FIX: Copy train/val lists into the YOLO directory ---
    print("Copying train/val file lists...")
    shutil.copy(config.TRAIN_TXT, os.path.join(config.YOLO_DATA_DIR, 'train.txt'))
    shutil.copy(config.TEST_TXT, os.path.join(config.YOLO_DATA_DIR, 'val.txt'))

    # Create the dataset.yaml file
    yaml_content = f"""
path: {os.path.abspath(config.YOLO_DATA_DIR)}
train: images/train
val: images/val

names:
"""
    for i in range(config.NUM_CLASSES):
        yaml_content += f"  {i}: '{config.IDX_TO_CLASS[i]}'\n"

    yaml_path = config.YOLO_YAML_PATH
    # Ensure parent directory exists
    yaml_dir = os.path.dirname(yaml_path)
    if yaml_dir:
        os.makedirs(yaml_dir, exist_ok=True)
    # Ensure file exists (create if missing), then write YAML content (overwrite)
    open(yaml_path, 'a').close()
    with open(yaml_path, 'w') as f:
        f.write(yaml_content)
        
    print("YOLO dataset preparation complete.")

if __name__ == '__main__':
    create_yolo_dataset()