import os
import shutil
from ultralytics import YOLO
import config

def create_full_path_list(original_list_path, image_dir):
    """
    Reads a file with image IDs (e.g., '103064'), finds the corresponding .jpg image,
    and writes a new file with the full, absolute paths to those images.
    Returns the path to the new temporary file.
    """
    print(f"--- Generating full path list for {os.path.basename(original_list_path)} ---")
    
    # Create a path for the new temporary file
    temp_file_path = original_list_path.replace('.txt', '_full_paths.txt')

    with open(original_list_path, 'r') as f:
        image_ids = [line.strip() for line in f.readlines()]

    found_paths = []
    for img_id in image_ids:
        # Assumes the image file has a .jpg extension
        img_filename = f"{img_id}.jpg"
        
        # Check in both 'train' and 'val' subdirectories to be safe
        potential_path_train = os.path.join(image_dir, 'train', img_filename)
        potential_path_val = os.path.join(image_dir, 'val', img_filename)
        
        if os.path.exists(potential_path_train):
            found_paths.append(potential_path_train)
        elif os.path.exists(potential_path_val):
            found_paths.append(potential_path_val)
        else:
            print(f"  - WARNING: Could not find image for ID: {img_id}")

    # Write the full paths to the new temporary file
    with open(temp_file_path, 'w') as f:
        f.write('\n'.join(found_paths))
    
    print(f"--- Created temporary list at {temp_file_path} with {len(found_paths)} entries. ---\n")
    return temp_file_path


def main():
    """
    Main execution script.
    """
    # Step 1: Create temporary list files with full paths for YOLO
    train_list_path = create_full_path_list(config.ORIGINAL_TRAIN_LIST, config.IMAGE_DIR)
    val_list_path = create_full_path_list(config.ORIGINAL_TEST_LIST, config.IMAGE_DIR)

    # Step 2: Create a temporary dataset.yaml that points to these new lists
    with open(config.YOLO_DATA_YAML, 'r') as f:
        yaml_content = f.read()
    
    # Replace the train/val lines with our new temporary lists
    temp_yaml_path = 'temp_dataset.yaml'
    with open(temp_yaml_path, 'w') as f:
        for line in yaml_content.splitlines():
            if line.strip().startswith('train:'):
                f.write(f"train: {os.path.abspath(train_list_path)}\n")
            elif line.strip().startswith('val:'):
                f.write(f"val: {os.path.abspath(val_list_path)}\n")
            else:
                f.write(f"{line}\n")

    # The rest of the script now uses the temporary files
    try:
        # Step 3: Check for model or train
        if os.path.exists(config.FINAL_MODEL_PATH):
            print(f"--- Found existing model at {config.FINAL_MODEL_PATH}. Skipping training. ---")
        else:
            print(f"--- Model not found. Starting training... ---")
            model = YOLO(config.BASE_MODEL)
            model.train(
                data=temp_yaml_path,  # Use the temporary YAML
                epochs=config.EPOCHS,
                imgsz=config.IMG_SIZE,
                project=config.RUNS_DIR,
                name=config.DETECTOR_RUN_NAME
            )

        # Step 4: Load and validate the model
        print("\n--- Loading the best trained model for validation ---")
        model = YOLO(config.FINAL_MODEL_PATH)
        model.val(
            data=temp_yaml_path,  # Use the temporary YAML
            save_json=True,
            conf=config.CONF_THRESHOLD,
            iou=config.IOU_THRESHOLD,
            project=config.RUNS_DIR,
            name=config.DETECTOR_RUN_NAME,
            exist_ok=True
        )

        print("\n--- Script finished successfully! ---")

    finally:
        # Clean up temporary files
        print("\n--- Cleaning up temporary files ---")
        os.remove(train_list_path)
        os.remove(val_list_path)
        os.remove(temp_yaml_path)

if __name__ == '__main__':
    main()
