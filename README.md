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


### Virtual environment (venv) — recommended
Create and activate an isolated environment to avoid dependency conflicts.

Unix / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

To exit the environment:
```bash
deactivate
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
From the project root (with the venv activated):
```bash
python prepare_data.py
```
Confirm data preparation completed and required files were created before running the main pipeline.

- Verify train/test lists and label files exist at the project root (or update paths in config.py):
```bash
ls -l 2025_Karyogram_CV_Camp train.txt test.txt
```

- If you need to change dataset or training settings, edit config.py now.

Then run the main pipeline:
```bash
python main.py
```

Finally, generate/visualize consolidated metrics:
```bash
python show_metrics.py
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

- `show_metrics.py`  
    Post-processing/visualization script that loads saved metrics and generates consolidated plots and summaries (e.g., combined PR curves, class-wise metrics) in `runs/final_submission_run/`.

## Outputs
Saved to `runs/final_submission_run/`:
- `weights/best.pt` — best model weights
- `PR_curve.png` — precision–recall curve
- `results.csv` — evaluation metrics per class and overall
- additional plots/summaries produced by `show_metrics.py`

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
├── prepare_data.py  
└── show_metrics.py

## Notes & Tips
- Ensure `train.txt` and `test.txt` contain correct absolute or project-relative image paths.
- For faster training, use a CUDA-capable GPU and appropriate batch size in `config.py`.
- Inspect `runs/final_submission_run/` after execution to review metrics and plots.

## Data credits:
 Tseng et al., 2023 — https://pmc.ncbi.nlm.nih.gov/articles/PMC9950090/; KCDH, IIT Bombay

## Citation

If you use this work in a publication or project, please cite the repository and author.

Recommended BibTeX:
```bibtex
@misc{aryan2025chromosome,
    author = {Aryan},
    title = {Chromosome Detection and Classification for Karyotyping},
    year = {2025},
    note = {https://github.com/TheDarKnight50/CV_Camp-InterIIT25}
}
```

Plain citation (APA):
Aryan. (2025). Chromosome Detection and Classification for Karyotyping. GitHub. https://github.com/TheDarKnight50/CV_Camp-InterIIT25

Please include the author name (Aryan) and the repository link in acknowledgements or references when citing this work.

## License

This project is licensed under the MIT License — see the full text below.

MIT License

Copyright (c) 2025 Aryan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.