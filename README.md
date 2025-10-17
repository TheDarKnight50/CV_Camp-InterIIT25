Chromosome Detection and Classification for Karyotyping
This project automates the identification and classification of human chromosomes from metaphase images using an object detection model. The goal is to create an efficient alternative to the traditional, labor-intensive manual methods of karyotyping.

Project Goal
The primary objective is to train a model that can take a metaphase image containing scattered chromosomes and output the identity for each one (1-22, X, Y), similar to a manually created karyogram.

Methodology
This project utilizes the YOLOv8 object detection model, a state-of-the-art architecture known for its speed and accuracy.

The workflow is managed by two main scripts:

prepare_data.py: This script processes the raw dataset, which contains XML annotations, and generates train.txt and test.txt files. These files contain lists of images that are used to train and evaluate the model, respectively.

main.py: This is the primary execution script. It handles the end-to-end process:

It checks if a trained model already exists.

If not, it trains a new YOLOv8 model on the chromosome dataset.

It then runs the validation step on the test set to evaluate performance.

Finally, it generates the output metrics and plots, saving them to the runs/ directory.

Results
The model achieved excellent performance on the test set. The primary evaluation metric is the mean Average Precision (mAP) at an IoU threshold of 0.5, which is equivalent to the Area Under the Precision-Recall Curve (auPRC).

Final Performance:

mAP@50 (auPRC): 0.9724

The detailed Precision-Recall curve, along with other evaluation plots, can be found in the output directory: runs/final_submission_run/.

How to Run
1. Setup
First, ensure all dependencies are installed.

Bash

pip install ultralytics pandas numpy Pillow scikit-learn
The project expects the dataset to be structured as provided, with the 2025_Karyogram_CV_Camp directory at the root of the project.

2. Run the Main Script
Execute the main script from the terminal to start the training and validation process.

Bash

python main.py
The script will automatically handle all steps. The final trained model, performance metrics (results.csv), and output plots will be saved in the runs/final_submission_run/ directory.

Project Structure
.
├── 2025_Karyogram_CV_Camp/
│   ├── 24_chromosomes_object/
│   ├── single_chromosomes_object/
│   ├── test.txt
│   └── train.txt
├── runs/
│   └── final_submission_run/
│       ├── weights/
│       │   └── best.pt
│       ├── PR_curve.png
│       └── results.csv
├── config.py
├── main.py
└── prepare_data.py
