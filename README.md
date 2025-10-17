# Chromosome Detection and Classification for Karyotyping

Automated pipeline to detect and classify human chromosomes in metaphase images using a YOLOv8 object detection model. The system outputs chromosome identities (1–22, X, Y) for each detected instance, providing an efficient alternative to manual karyotyping.

## Key Features
- End-to-end pipeline: data preparation, training, validation, and result visualization
- State-of-the-art detection using YOLOv8
- Reproducible outputs: model weights, precision–recall curves, and CSV metrics

## Results
- Primary metric: mean Average Precision at IoU 0.5 (mAP@50 / auPRC)
- Final performance on test set: **mAP@50 = 0.9724**
- Detailed plots and CSV metrics: `runs/final_submission_run/`

## Quick Start

### Requirements
- Python 3.8+

```bash
pip install ultralytics pandas numpy Pillow scikit-learn
```

### Dataset layout
Place the provided dataset directory at the project root as shown below:
```
2025_Karyogram_CV_Camp/
├── 24_chromosomes_object/
├── single_chromosomes_object/
├── test.txt
└── train.txt
```
The repository expects the dataset directory `2025_Karyogram_CV_Camp` to be present at the project root.

### Run the pipeline
From the project root:
```bash
python main.py
```
Behavior:
- If a trained model exists, it will be used for evaluation.
- Otherwise, the script trains a new YOLOv8 model, performs validation on `test.txt`, and saves outputs to `runs/final_submission_run/`.

## Scripts

- `prepare_data.py`  
    Converts raw XML annotations into the train/test lists (`train.txt`, `test.txt`) and prepares any required label files.

- `main.py`  
    Orchestrates training, validation, and result generation:
    - checks for existing weights
    - trains the model (if needed)
    - runs validation on the test set
    - saves metrics, plots, and weights

## Outputs
Saved to `runs/final_submission_run/`:
- `weights/best.pt` — best model weights
- `PR_curve.png` — precision–recall curve
- `results.csv` — evaluation metrics per class and overall

## Project structure
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

## Notes & Tips
- Ensure `train.txt` and `test.txt` contain correct absolute or project-relative image paths.
- For faster training, use a CUDA-capable GPU and appropriate batch size in `config.py`.
- Inspect `runs/final_submission_run/` after execution to review metrics and plots.

## Data credits:
 Tseng et al., 2023 — https://pmc.ncbi.nlm.nih.gov/articles/PMC9950090/; KCDH, IIT Bombay