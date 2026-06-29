# CPV — Face Attendance System
**Subject**: Computer Vision | **University**: FPT University

---

## Project Structure

```
cpv-minhnguyen/               ← Git repository root
├── detect-face/              ← Main project (deliverable)
│   ├── train.py              Training pipeline entry point
│   ├── main.py               Inference pipeline entry point
│   ├── self_check.py         Sanity test
│   ├── requirements.txt      Python dependencies
│   ├── README.md             Detailed project documentation
│   └── app/                  Source package
│       ├── config.py         Shared constants (IMAGE_SIZE, thresholds, …)
│       ├── storage.py        Path constants + I/O helpers
│       ├── function1_stream.py   F1: threaded RTSP / webcam stream
│       ├── function2_frames.py   F2: video → frame extraction
│       ├── function3_detection.py F3: Haar Cascade face detector
│       ├── function4_recognition.py F4: centroid classifier
│       ├── face.py           Facade combining F3 + F4
│       └── ui.py             Desktop UI (CustomTkinter)
│
└── .venv/                    Virtual environment (gitignored)
```

---

## Quick Start

```bash
# 1. Activate virtual environment
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 2. Install dependencies (first time only)
pip install -r detect-face/requirements.txt

# 3. Training pipeline — build the model
cd detect-face
python train.py                  # extract frames + train
python train.py --skip-extract   # retrain on existing dataset

# 4. Inference pipeline — attendance application
python main.py
```

---

## Two Pipelines

### Training (`python train.py`)
```
videos/*.MOV
  → [F2] extract frames → dataset/{ID}_{Name}/*.jpg
  → [F3+F4] re-detect + vectorize + compute centroids
  → data/model.pkl
```

### Inference (`python main.py`)
```
webcam / RTSP
  → [F1] threaded stream
  → [F3] detect face (every 4th frame)
  → [F4] nearest-centroid prediction
  → attendance.csv
```

See [`detect-face/README.md`](detect-face/README.md) for full details.
