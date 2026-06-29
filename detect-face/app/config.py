"""
config.py — Central Configuration
===================================
Single source of truth for all constants shared across both pipelines.

TRAINING pipeline  (train.py)  imports: IMAGE_SIZE, MAX_IMAGES_PER_STUDENT,
                                         FRAME_INTERVAL, MIN_FRAME_DIFFERENCE,
                                         BASE_THRESHOLD
INFERENCE pipeline (main.py)   imports: IMAGE_SIZE, BASE_THRESHOLD,
                                         AMBIGUITY_MARGIN
"""

# ---------------------------------------------------------------------------
# Image dimensions
# ---------------------------------------------------------------------------
# Size of the normalised face crop fed into F3 (detection output) and
# F4 (recognition vectors).  Both pipelines MUST use the same value,
# otherwise model vectors and live predictions will be incompatible.
IMAGE_SIZE: tuple[int, int] = (112, 112)

# ---------------------------------------------------------------------------
# Training pipeline — dataset collection (Function 2)
# ---------------------------------------------------------------------------
# Maximum number of face frames saved per student from a source video.
MAX_IMAGES_PER_STUDENT: int = 30

# Extract one frame every FRAME_INTERVAL frames from the source video.
# Higher = fewer, more varied frames; lower = denser sampling.
FRAME_INTERVAL: int = 15

# Skip a frame if its mean pixel difference from the previous saved frame
# is below this value (avoids storing near-identical frames).
MIN_FRAME_DIFFERENCE: float = 8.0

# ---------------------------------------------------------------------------
# Recognition classifier (Function 4)
# ---------------------------------------------------------------------------
# Upper bound for the Euclidean distance in feature space.
# The auto-calibrated threshold during training may be lower than this.
BASE_THRESHOLD: float = 16.0

# Reject a prediction if the gap between the best and second-best
# distance is smaller than this margin (ambiguous match → Unknown).
AMBIGUITY_MARGIN: float = 1.2
