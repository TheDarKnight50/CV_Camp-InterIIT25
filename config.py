import os
import torch

# --- Main Project Paths ---
ROOT_DIR = "./2025_Karyogram_CV_Camp"
YOLO_DATA_DIR = "./yolo_multiclass_dataset"
RUNS_DIR = "./runs"
DETECTOR_RUN_NAME = "final_submission_run" # A name for the final run
FINAL_MODEL_PATH = f"{RUNS_DIR}/{DETECTOR_RUN_NAME}/weights/best.pt"
AUPRC_PLOT_PATH = f"./auprc_plot_final.png" # Save plot in main directory
PREDICTIONS_JSON_PATH = f"./predictions.json" # Path for trusted YOLO predictions

# --- Source Data Paths ---
MULTI_CHROMO_DIR = f"{ROOT_DIR}/24_chromosomes_object"
MULTI_IMAGES_DIR = f"{MULTI_CHROMO_DIR}/images"
MULTI_ANNOTATIONS_DIR = f"{MULTI_CHROMO_DIR}/annotations"
TRAIN_TXT = f"{ROOT_DIR}/train.txt"
TEST_TXT = f"{ROOT_DIR}/test.txt"

# --- Class Definitions (Correct Mapping) ---
CLASSES = [str(i) for i in range(1, 23)] + ['X', 'Y']
NUM_CLASSES = len(CLASSES)
IDX_TO_CLASS = {i: name for i, name in enumerate(CLASSES)}
XML_LABEL_TO_IDX = {
    'A1': 0, 'A2': 1, 'A3': 2,
    'B4': 3, 'B5': 4,
    'C6': 5, 'C7': 6, 'C8': 7, 'C9': 8, 'C10': 9, 'C11': 10, 'C12': 11,
    'D13': 12, 'D14': 13, 'D15': 14,
    'E16': 15, 'E17': 16, 'E18': 17,
    'F19': 18, 'F20': 19,
    'G21': 20, 'G22': 21,
    'X': 22,
    'Y': 23
}

# --- Training Configuration ---
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
GPU_COUNT = torch.cuda.device_count()

# In config.py

# --- Model & Run Configuration ---
BASE_MODEL = 'yolov8n.pt'  # The base model to start training from
RUNS_DIR = './runs'
DETECTOR_RUN_NAME = 'final_submission_run'
FINAL_MODEL_PATH = f'{RUNS_DIR}/{DETECTOR_RUN_NAME}/weights/best.pt'

ORIGINAL_TRAIN_LIST = '2025_Karyogram_CV_Camp/train.txt'
ORIGINAL_TEST_LIST = '2025_Karyogram_CV_Camp/test.txt'
IMAGE_DIR = 'yolo_multiclass_dataset/images'
# --- Dataset Configuration ---
YOLO_DATA_YAML = 'yolo_multiclass_dataset/dataset.yaml'
YOLO_YAML_PATH = 'yolo_multiclass_dataset/dataset.yaml'

# --- Training Hyperparameters ---
EPOCHS = 50
IMG_SIZE = 640

# --- Validation Parameters ---
CONF_THRESHOLD = 0.001
IOU_THRESHOLD = 0.5