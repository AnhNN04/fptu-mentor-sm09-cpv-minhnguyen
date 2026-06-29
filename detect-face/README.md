# Face Attendance System
**Subject**: Computer Vision — FPT University

## Team Members

| Student ID | Full Name |
|---|---|
| HE190019 | Tran Van Truong |
| HE191357 | Nguyen Huy Son |
| HE200457 | Le Trung Kien |
| HE200629 | Le Trung Hieu |
| HE204132 | Hoang Trung Hieu |
| HE204913 | Nguyen Quang Minh |

---

## System Requirements

- Python ≥ 3.10
- Webcam **or** IP camera with RTSP support

## Setup

```bash
# 1. Clone the repo
cd detect-face

# 2. Install dependencies
pip install -r requirements.txt
```

---

## Pipeline 1 — Training

Converts raw `.MOV` video recordings into a trained recognition model.

```
videos/*.MOV  →  [F2] extract frames  →  dataset/
              →  [F3+F4] train centroids  →  data/model.pkl
```

```bash
# Full pipeline: extract frames from videos/ then train
python train.py

# Retrain on existing dataset (skip video extraction)
python train.py --skip-extract

# Options
python train.py --max-images 50 --interval 10
python train.py --video-dir /path/to/videos
```

### What happens:

**Step 1 — Frame Extraction** (`function2_frames.py`)
- Opens each `.MOV` with OpenCV (FFMPEG backend)
- Samples 1 frame every 15 frames, mirrors, resizes to 640 px wide
- Skips near-duplicate frames (mean pixel diff < 8.0)
- Saves ≤ 30 `.jpg` images per student into `dataset/{ID}_{Name}/`

**Step 2 — Model Training** (`function3_detection.py` + `function4_recognition.py`)
- Re-detects face in each dataset image (Haar Cascade + CLAHE pre-processing)
- Vectorizes each 112×112 face: `equalizeHist → flatten → float32 / 255`
- Computes one centroid (mean vector) per student
- Auto-calibrates rejection threshold from the training distance distribution
- Saves model to `data/model.pkl`

---

## Pipeline 2 — Inference (Attendance)

Runs real-time face recognition against the trained model.

```
webcam/RTSP  →  [F1] stream  →  [F3] detect  →  [F4] predict  →  attendance.csv
```

```bash
python main.py
```

### What happens:

**Function 1** (`function1_stream.py`) — Streams video using a background thread (no frame lag)  
**Function 3** (`function3_detection.py`) — Detects and crops the largest face every 4 frames  
**Function 4** (`function4_recognition.py`) — Predicts student identity via nearest-centroid lookup  
**Storage** (`storage.py`) — Logs `student_id, name, timestamp` to `attendance.csv`

### UI Modes

| Mode | What it does |
|---|---|
| **Đăng ký** (Register) | Capture face images for a new student + trigger training |
| **Điểm danh** (Attendance) | Live recognition; each student logged once per session |

---

## Project Structure

```
detect-face/
├── train.py                  Training pipeline entry point
├── main.py                   Inference pipeline entry point
├── self_check.py             Automated sanity test
├── requirements.txt
│
├── app/
│   ├── config.py             All shared constants (IMAGE_SIZE, thresholds, …)
│   ├── storage.py            Path constants + file I/O helpers
│   ├── function1_stream.py   F1: threaded camera / RTSP stream
│   ├── function2_frames.py   F2: frame extraction + dataset collection
│   ├── function3_detection.py F3: Haar Cascade face detector
│   ├── function4_recognition.py F4: centroid classifier
│   ├── face.py               Facade combining F3 + F4
│   └── ui.py                 CustomTkinter desktop UI
│
├── dataset/                  Face images per student (gitignored)
├── data/                     Trained model.pkl (gitignored)
├── videos/                   Source .MOV recordings (gitignored)
└── attendance.csv            Output attendance log (gitignored)
```
