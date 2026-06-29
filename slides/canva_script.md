# Canva Presentation Script
## Face Attendance System — Computer Vision Assignment

> **How to use this file:** Each slide section gives you:
> - `HEADLINE` — the main title text for that slide
> - `CONTENT` — all text, bullet points, and labels to type in Canva
> - `VISUALIZATION` — exactly what to draw/design in the visual area
> - `SPEAKER NOTES` — what to say during the presentation

**Suggested Canva style:** Dark background (#0a0f1e or #1a1a2e), accent color blue (#3b82f6) and cyan (#06b6d4), white/light text. Use a modern sans-serif font (Inter, Poppins, or Raleway).

---

## SLIDE 1 — Title

**HEADLINE:**
> Face Attendance System

**SUBHEADLINE:**
> Real-time student recognition using IP Camera, Face Detection & Face Recognition

**CONTENT (bottom area — 3 info tags side by side):**
- 🎓 Subject: CPV301 — Computer Vision
- 🏫 University: FPT University
- 👥 Team: Nguyen Quang Minh & 5 members

**VISUALIZATION:**
Draw a centered circular graphic on the right half of the slide:
- Large outer ring (thin stroke, blue glow)
- Inside: a stylized face silhouette outline (simple oval head + shoulders)
- Small green checkmark badge in the bottom-right of the face circle
- Around the ring: 3 small floating pill labels pointing outward:
  - 📡 "RTSP Camera" (top-left)
  - 👁️ "Face Detect" (top-right)
  - 🧠 "AI Recognize" (bottom)
- Subtle grid dots in the background

**SPEAKER NOTES:**
> "Today we'll present our Face Attendance System. The idea is simple: a student stands in front of a camera, the system detects their face, recognizes who they are, and logs their attendance automatically. No manual check-in needed."

---

## SLIDE 2 — Agenda

**HEADLINE:**
> What We'll Cover Today

**CONTENT (numbered list, 2 columns):**

Left column:
1. System Overview
2. Function 1 — RTSP Stream
3. Function 2 — Frame Extraction
4. Pre-processing

Right column:

5. Function 3 — Face Detection
6. Function 4 — Face Recognition
7. Training Pipeline
8. Inference Pipeline & Demo

**VISUALIZATION:**
Draw a horizontal progress bar with 8 segments. Each segment is a colored rounded rectangle with a number (1–8) inside. Color the segments in gradient: F1 = blue, F2 = cyan, Pre = orange, F3 = purple, F4-train = green, F4-infer = green, demo = teal. Below each segment, a small label matching the list items above.

**SPEAKER NOTES:**
> "Here's our agenda. We built 4 main functions as required by the assignment, plus the optional pre-processing step. We'll also show you how we organized the code into two separate pipelines — training and inference."

---

## SLIDE 3 — Team & Evaluation Criteria

**HEADLINE:**
> Our Team & Grading Criteria

**CONTENT — LEFT COLUMN (Team table):**

| Student ID | Full Name |
|---|---|
| HE190019 | Tran Van Truong |
| HE191357 | Nguyen Huy Son |
| HE200457 | Le Trung Kien |
| HE200629 | Le Trung Hieu |
| HE204132 | Hoang Trung Hieu |
| HE204913 | Nguyen Quang Minh |

**CONTENT — RIGHT COLUMN (Scoring table):**

| Criteria | Mark |
|---|---|
| Function 1 — RTSP Stream | 1 |
| Function 2 — Frame Cropping | 1 |
| Function 3 — Face Detection | 2 |
| Function 4 — Face Recognition | 2 |
| Pre-processing *(optional)* | 1 |
| PowerPoint Presentation | 3 |
| **Total** | **10** |

**VISUALIZATION:**
- Left half: 6 team member cards in a 2×3 grid. Each card: rounded rectangle, student ID in small blue monospace font at top, full name in white bold below, small icon (person silhouette) in corner.
- Right half: scoring table styled as a clean dark table with a green highlighted "Total = 10" row at the bottom. Add a small donut chart next to it showing the mark breakdown by color (F3+F4 = biggest slice, Presentation = medium, F1+F2 = small).

**SPEAKER NOTES:**
> "Our team has 6 members. The assignment is graded out of 10 marks. The biggest weightings are the presentation (3 marks) and functions 3 and 4 which are the core AI components (2 marks each)."

---

## SLIDE 4 — System Architecture Overview

**HEADLINE:**
> How The System Works

**SUBHEADLINE:**
> A complete pipeline from IP Camera to Attendance Record

**VISUALIZATION (MAIN — full-width horizontal pipeline diagram):**

Draw 5 boxes connected by arrows left to right:

```
[📡 IP Camera]  →→  [F1 Stream]  →→  [F2 Frames]  →→  [F3 Detect]  →→  [F4 Recognize]  →→  [📋 attendance.csv]
```

Details for each box:
- **IP Camera**: camera icon, label "RTSP / Webcam"
- **F1 Stream** (blue): label "Threaded Video Reader", subtext "continuous frame buffer"
- **F2 Frames** (cyan): label "Frame Extraction", subtext "mirror + resize + deduplicate"
- **F3 Detect** (purple): label "Haar Cascade", subtext "112×112 face crop"
- **F4 Recognize** (green): label "Centroid Classifier", subtext "Euclidean distance"
- **attendance.csv** (green file icon): label "student_id, name, timestamp"

Below the pipeline, add two separated swimlane labels:
- Top swimlane label: 🏋️ **TRAINING** — covers F2 + F3 + F4 boxes
- Bottom swimlane label: 🎯 **INFERENCE** — covers F1 + F3 + F4 boxes

Add a small "data/model.pkl" cylinder icon between F4 training output and F4 inference input with a dashed arrow.

**SPEAKER NOTES:**
> "The system has two distinct pipelines. Training: we extract frames from videos, detect faces, and build a model. Inference: the live camera stream feeds into detection and recognition in real time, and attendance is logged automatically."

---

## SLIDE 5 — Function 1: RTSP Stream

**HEADLINE:**
> Function 1 — Stream Video from IP Camera

**CHIP/TAG (top right):** `1 mark`

**CONTENT — KEY POINTS (left side, 4 bullet points):**

- **Connect to source**
  Supports webcam (`index 0`) and IP camera via RTSP protocol (`rtsp://192.168.x.x/stream`).
  OpenCV backend: `CAP_DSHOW` for webcam, `CAP_FFMPEG` for RTSP.

- **Minimize buffer delay**
  Buffer size set to `1` → always reads the latest frame, no stale frames accumulate.

- **Background thread**
  A daemon thread continuously reads frames into a shared memory buffer.
  Main UI thread calls `.read()` and gets the latest frame **instantly** — zero I/O wait.

- **Context Manager**
  Supports `with CameraStream() as cam:` — auto-disconnects on exit, no resource leaks.

**VISUALIZATION (right side):**
Draw a threading diagram:

```
IP Camera / Webcam
        ↓ (RTSP / USB)
  ┌─────────────────────┐
  │   Background Thread │  ← runs _update() loop
  │   reads frame       │
  │   stores in buffer  │
  └────────┬────────────┘
           │  threading.Lock
           ↓
  ┌─────────────────────┐
  │    Main UI Thread   │  ← calls .read() every 30ms
  │    renders display  │
  └─────────────────────┘
```

Use two parallel vertical lanes with a lock icon between them. Left lane = background thread (blue), right lane = main thread (white). Connected by a small shared "frame buffer" rectangle in the middle.

**SPEAKER NOTES:**
> "Function 1 handles streaming. The key design choice is threading: one thread reads from the camera constantly, another handles the UI. Without this, every time we call read(), the UI would freeze waiting for the network. With threading, the UI always gets the latest frame instantly."

---

## SLIDE 6 — Function 2: Frame Extraction

**HEADLINE:**
> Function 2 — Crop Video into Image Frames

**CHIP/TAG (top right):** `1 mark`

**CONTENT — TWO MODES (left side):**

**Mode A — Live Capture (webcam/RTSP)**
- Saves 1 frame every 0.5 seconds
- Skips frames too similar to the previous
- Stops when 30 images saved or user presses ESC

**Mode B — Extract from .MOV File**
- Reads source video recordings (`.MOV` files)
- Samples 1 frame every **15 frames**
- Applies same deduplication logic
- Used to build the dataset from student recordings

**Deduplication algorithm:**
> 1. Convert frame → 100×100 grayscale thumbnail
> 2. Compute mean pixel difference vs last saved frame
> 3. If diff **< 8.0** → skip (too similar)
> 4. Otherwise → save as `frame_NNN.jpg`

**CONTENT — Bottom stats bar (3 numbers):**
- **6** Students
- **554** Total images saved
- **~92** Average images per student

**VISUALIZATION (right side):**
Draw a filmstrip graphic (horizontal strip of 5 film frames). Above each frame, label:
- Frame 1 (saved ✅)
- Frame 2 (saved ✅)
- Frame 3 (too similar ❌)
- Frame 4 (too similar ❌)
- Frame 5 (saved ✅)

Below the filmstrip, draw a folder tree:
```
dataset/
├── HE190019_Tran_Van_Truong/   (117 images)
├── HE191357_Nguyen_Huy_Son/    (24 images)
├── HE200457_Le_Trung_Kien/     (100 images)
├── HE200629_Le_Trung_Hieu/     (100 images)
├── HE204132_Hoang_Trung_Hieu/  (119 images)
└── HE204913_Nguyen_Quang_Minh/ (94 images)
```

**SPEAKER NOTES:**
> "Function 2 builds our training dataset. We recorded a short video for each student, then automatically extracted diverse face frames. The deduplication step is important — without it, we'd save nearly identical frames in sequence, giving the model very little variety."

---

## SLIDE 7 — Pre-processing

**HEADLINE:**
> Pre-processing — Light Balance & Noise Filtering

**CHIP/TAG (top right):** `+1 mark (optional)`

**CONTENT — 3 steps side by side:**

**① Grayscale Conversion**
- `cv2.cvtColor(frame, BGR2GRAY)`
- Removes colour information — face structure lives in luminance
- Reduces computation: 3 channels → 1 channel
- Haar Cascade detects on luminance only

**② CLAHE — Adaptive Histogram Equalisation**
- `cv2.createCLAHE(clipLimit=2.0, tileGrid=(8,8))`
- **Problem it solves:** faces under uneven classroom lighting (bright window on one side, shadow on other) are missed by plain detection
- **How it works:** splits image into 8×8 tiles, equalises each tile independently, clips extreme contrast to avoid noise amplification
- Result: face features become clearly visible regardless of lighting

**③ Gaussian Blur**
- `cv2.GaussianBlur(kernel=(3,3))`
- Smooths sensor noise and JPEG compression artefacts
- Prevents the cascade from triggering on high-frequency noise patterns
- ⚠️ Applied only for **detection** — not saved to dataset

**VISUALIZATION:**
Draw a 3-stage image transformation row:

```
[Original BGR photo]  →  [Grayscale]  →  [After CLAHE]  →  [After Blur]
     (dark corners)        (flat)         (bright face)     (smooth)
```

Use simple face placeholder rectangles with shading:
- Image 1: Rectangle with dark gradient on one side (poor lighting)
- Image 2: Same but grey, flat
- Image 3: Grey but with clearly visible features (higher contrast)
- Image 4: Same but slightly softer edges

Below the images, show a simple histogram chart for each — flat/skewed for image 1, tall/spread for image 3.

**SPEAKER NOTES:**
> "Pre-processing significantly improves detection accuracy under realistic classroom conditions. CLAHE is the most impactful step — it boosts contrast locally, so a student's face near a bright window is just as detectable as one in a dim corner. The Gaussian blur reduces false positives from noisy image textures."

---

## SLIDE 8 — Function 3: Face Detection

**HEADLINE:**
> Function 3 — Face Detection

**SUBHEADLINE:**
> Haar Cascade Classifier — `haarcascade_frontalface_default.xml`

**CHIP/TAG (top right):** `2 marks`

**CONTENT — 4 steps (left side):**

**① Pre-process frame** *(from previous slide)*
Grayscale → CLAHE → Gaussian Blur → used for detection only

**② Run detectMultiScale**
| Parameter | Value | Meaning |
|---|---|---|
| `scaleFactor` | 1.2 | Shrink image by 20% per pyramid level |
| `minNeighbors` | 5 | Min overlapping detections to confirm a face |
| `minSize` | (70,70) | Ignore faces smaller than 70×70 px |

**③ Select Largest Face**
- If multiple faces detected → select the one with maximum area (`w × h`)
- Reason: student stands closest to camera = largest face = the one attending

**④ Crop & Normalise**
- Crop region from original **colour** frame (not pre-processed)
- Convert crop → grayscale
- Resize to **112 × 112 pixels** using `INTER_AREA`
- Output: `FaceBox(x, y, w, h)` + face image numpy array

**VISUALIZATION (right side — diagram):**
Draw a camera frame with a person inside. Show:
1. A large green rectangle around the primary face (labeled "Largest face selected ✅")
2. A smaller dashed red rectangle around a secondary face in background (labeled "Ignored ❌ — smaller area")
3. An arrow from the green rectangle pointing right to:
   - A small 112×112 grey square (the output face crop)
   - Label: "112×112 grayscale crop"

Below: a small Haar feature illustration — two rectangles (white + dark) side by side labeled "Haar-like feature: detects eye-cheek contrast"

**SPEAKER NOTES:**
> "Function 3 uses the Haar Cascade — a classical computer vision method. It works by sliding a window across the image at multiple scales, checking each region against a series of trained classifiers. If a region passes all stages, a face is detected. We then take only the largest face — that's our student."

---

## SLIDE 9 — Function 4: Training Phase

**HEADLINE:**
> Function 4 — Training the Recognition Model

**SUBHEADLINE:**
> Building one "template" (centroid) per student from face images

**CHIP/TAG (top right):** `2 marks`

**CONTENT (left side — numbered steps):**

**Step 1 — Load each dataset image**
- For each image: try to re-detect face with Haar Cascade (F3)
- If detection fails → fall back to raw greyscale read
- Result: tight 112×112 face crop per image

**Step 2 — Vectorize the face**
1. `equalizeHist(face)` — global histogram equalisation (makes lighting consistent)
2. `flatten()` → convert 112×112 grid into a long 1D list
3. `÷ 255` → scale all values to `[0.0, 1.0]`
4. Result: a **12,544-dimensional vector** representing that face

**Step 3 — Compute centroid per student**
```
centroid = average of all image vectors for that student
```
- Each student has ~90–120 images → ~90–120 vectors → 1 centroid
- The centroid is that student's "average face" in vector space

**Step 4 — Auto-calibrate the threshold**
- Measure how far each student's own images are from their centroid *(own distances)*
- Measure how far from the wrong centroid *(impostor distances)*
- Set threshold = `min(16.0, p95_own × 1.15, p5_impostor × 0.85)`
- Guarantees the model accepts real matches and rejects strangers

**Step 5 — Save model**
- `data/model.pkl` contains:
  - `centroids` → (6 × 12,544) matrix — one row per student
  - `labels` → list of folder names aligned with centroids
  - `people` → folder name → (student_id, display_name)
  - `threshold` → the calibrated rejection distance

**VISUALIZATION (right side):**
Draw a 2D scatter plot (simplified, conceptual):
- 6 clusters of dots, each cluster a different color
- Each cluster has ~8–10 dots (representing image vectors)
- A larger star/diamond marker at the center of each cluster labeled "centroid"
- Label each cluster with a student ID (HE190019, etc.)
- A dashed circle around one cluster labeled "threshold radius"
- A red X marker outside the circle labeled "Unknown face rejected"

Below the chart: label "Feature Space (12,544 dimensions → shown in 2D)"

**SPEAKER NOTES:**
> "Training is simple: we convert every face image into a 12,544-dimensional vector, then compute the average vector — the centroid — for each student. That centroid is the student's 'signature'. The threshold defines how far from the centroid a live face can be before we say 'I don't recognize this person'."

---

## SLIDE 10 — Function 4: Inference / Prediction Phase

**HEADLINE:**
> Function 4 — Real-time Face Recognition

**SUBHEADLINE:**
> Nearest centroid lookup in milliseconds

**CHIP/TAG (top right):** `2 marks`

**CONTENT (step by step):**

**Input:** 112×112 grayscale face image from live camera (F3 output)

**Step 1 — Vectorize live face**
Same process as training:
`equalizeHist → flatten → ÷255 → 12,544-dim vector`

**Step 2 — Compute distances**
Calculate Euclidean distance to every student centroid:
```
distance_i = sqrt( Σ (vector[j] - centroid_i[j])² )
```
→ 6 distances computed (one per student)

**Step 3 — Find best match**
```
best = student with minimum distance
```

**Step 4 — Apply two rejection rules:**

| Rule | Condition | Result |
|---|---|---|
| Threshold check | `best_distance > threshold` | ❌ Unknown — too different |
| Ambiguity check | `2nd_best - best < 1.2` | ❌ Unknown — too ambiguous |
| Accepted | Both checks pass | ✅ Recognized → log attendance |

**Step 5 — Log attendance**
```
student_id, name, timestamp → attendance.csv
Each student logged only once per session
```

**VISUALIZATION (right side):**
Draw a bar chart — horizontal bars showing distance to each student centroid:

```
HE190019 ████████████████████████  dist = 24.1  ❌ too far
HE191357 ██████████████████         dist = 18.3  ❌ too far
HE200457 ████                       dist = 6.2   ✅ MATCH
HE200629 █████████████              dist = 15.8  ❌ too far
HE204132 ████████████               dist = 13.1  ❌ too far
HE204913 █████████                  dist = 10.4  ❌ too far
         ─────────────────────────────────────────────
         Threshold = 12.0
```

The bar for HE200457 is colored green (shortest), all others are grey/red. A vertical dashed red line marks the threshold. Label the winning bar: "✅ Le Trung Kien — logged to attendance.csv"

**SPEAKER NOTES:**
> "At inference time, we take the live face from the camera, convert it to the same vector format as training, then measure how far it is from each student's centroid. The nearest centroid wins — but only if it's close enough. If it's too far, or if two students are equally likely, we reject it as unknown."

---

## SLIDE 11 — Demo & Results

**HEADLINE:**
> Application Demo

**CONTENT (left side — how to run):**

**Setup:**
```
source .venv/bin/activate
pip install -r requirements.txt
```

**Training Pipeline:**
```
python train.py
```
Output:
> `=== STEP 1: Extract frames ===`
> `  Saved 30 images for Nguyen Quang Minh`
> `=== STEP 2: Train model ===`
> `  Trained on 554 images — model.pkl saved`

**Inference Pipeline:**
```
python main.py
```
Output (in UI log):
> `✅ Webcam opened (1280×720)`
> `✅ Điểm danh: HE204913 — Nguyen Quang Minh`
> `✅ Điểm danh: HE200629 — Le Trung Hieu`
> `❌ Unknown face — skipped`

**CONTENT (right side — stats):**

Four metric boxes:
- **6** — Students enrolled
- **554** — Training images
- **< 1s** — Training time
- **~4 FPS** — Detection rate (every 4th frame)

**attendance.csv output format:**
```
student_id  | name               | timestamp
HE204913    | Nguyen Quang Minh  | 2025-07-01 08:32:11
HE200629    | Le Trung Hieu      | 2025-07-01 08:33:05
HE204132    | Hoang Trung Hieu   | 2025-07-01 08:33:47
```

**VISUALIZATION:**
Draw a mock desktop app window:
- Dark window chrome at top: "Face Attendance — Điểm danh khuôn mặt"
- Left: a camera feed rectangle (grey with a simplified face silhouette + green bounding box drawn around the face region)
- Label above box in green: "HE204913 — Nguyen Quang Minh"
- Right panel: "Bảng điều khiển" with two mode buttons: "Đăng ký" and "Điểm danh" (second one selected/highlighted)
- Below: a log box showing 3 green ✅ attendance entries

**SPEAKER NOTES:**
> "Here's the application running. After training on our 554 dataset images, the model is ready in under a second. In the live app, students just stand in front of the camera. The system detects the face, runs recognition, and writes their ID to the attendance file. The whole process takes about 4 frame cycles — roughly real-time."

---

## SLIDE 12 — Conclusion

**HEADLINE:**
> What We Accomplished

**CONTENT (6 achievement cards in a 2×3 grid):**

**Card 1 — F1 ✅**
📡 RTSP Stream
> Threaded architecture streams webcam or IP camera. Zero-latency frame delivery via shared memory buffer.

**Card 2 — F2 ✅**
🎞️ Frame Extraction
> Extracted 554 diverse training images from 6 student videos with smart deduplication and mirror correction.

**Card 3 — Pre-processing ✅**
🌤️ Light Balance + Noise Filter
> CLAHE + Gaussian Blur applied before every detection. Handles uneven classroom lighting reliably.

**Card 4 — F3 ✅**
👁️ Haar Cascade Detection
> Detects and crops the largest frontal face per frame. Output: clean 112×112 grayscale crop.

**Card 5 — F4 ✅**
🧠 Centroid Recognition
> No neural network needed. Trains in < 1 second. Auto-calibrated rejection threshold. Two-level Unknown filtering.

**Card 6 — System ✅**
📋 Attendance Logging
> CSV output with student ID, name, and timestamp. Clean two-pipeline architecture: `train.py` + `main.py`.

**Bottom — Final line:**
> "Simple approach. Real results. Built entirely with OpenCV and NumPy."

**VISUALIZATION:**
Arrange the 6 cards in 2 columns × 3 rows. Each card:
- Rounded rectangle with subtle dark background
- Large emoji icon at top
- Bold title
- 2-line description below
- Small green checkmark badge in top-right corner

Below all cards, add a single horizontal line with icons:
`📹 → 🎞️ → 🌤️ → 👁️ → 🧠 → 📋`
(mini pipeline reminder)

**Last line (centered, larger):**
Thank you — Q&A

**SPEAKER NOTES:**
> "To summarize: we successfully implemented all 4 required functions plus the optional pre-processing step. The system works end-to-end — from streaming a live camera to automatically logging attendance in a CSV file. The approach is deliberately simple — no deep learning, no GPU — but it works reliably for a controlled classroom setting. Thank you."

---

## Design Notes for Canva

**Color palette:**
- Background: `#0a0f1e` (very dark navy) or `#1a1a2e`
- Primary accent: `#3b82f6` (blue)
- Secondary accent: `#06b6d4` (cyan)
- Success: `#22c55e` (green)
- Warning: `#f97316` (orange)
- Highlight: `#a855f7` (purple)
- Text: `#e2e8f0` (off-white)
- Muted text: `#64748b` (grey)

**Typography:**
- Title: **Poppins Bold** or **Raleway ExtraBold**, size 40–52pt
- Body: **Inter Regular/Medium**, size 16–22pt
- Code snippets: **Courier New** or **JetBrains Mono**, size 14pt, in a dark rounded box

**Consistent slide layout:**
- Top-left: small colored tag/chip (e.g. "Function 1", "Pre-processing")
- Top-right: mark chip (e.g. "1 mark", "2 marks", "+1 mark")
- Left 50%: text content
- Right 50%: visualization / diagram
- Bottom: thin horizontal accent line or progress dots
