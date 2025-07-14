import os
import cv2
import numpy as np

# 1. Configuration
INPUT_PATH = "image.png"
OUTPUT_DIR = "augmented"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Load source
img = cv2.imread(INPUT_PATH)
if img is None:
    raise FileNotFoundError(f"Could not load '{INPUT_PATH}'")

h, w = img.shape[:2]

# 3.  Define transforms

def stretch(img, fx, fy):
    return cv2.resize(img, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)

def blur(img, k):
    return cv2.GaussianBlur(img, (k, k), 0)

def to_grayscale(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)

def distort(img, max_shift=0.1):
    """Random perspective warp: each corner shifts by up to max_shift*dim."""
    pts1 = np.float32([[0,0], [w,0], [w,h], [0,h]])
    # apply a small random shift to each corner
    shift = lambda x: x + np.random.uniform(-max_shift, max_shift) * (w if x in [0,w] else h)
    pts2 = np.float32([
        [shift(0),       shift(0)],
        [shift(w),       shift(0)],
        [shift(w),       shift(h)],
        [shift(0),       shift(h)]
    ])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(img, M, (w, h))

# 4.  Apply & save
variants = []

# stretching: 80%, 120% horizontally & vertically
for fx, fy in [(1.2,1.0), (0.8,1.0), (1.0,1.2), (1.0,0.8)]:
    variants.append( (f"stretch_{int(fx*100)}x_{int(fy*100)}y", stretch(img, fx, fy)) )

# blurs: mild and strong
for k in (5, 15):
    variants.append( (f"blur_{k}", blur(img, k)) )

# grayscale
variants.append( ("grayscale", to_grayscale(img)) )

# random distortions (3 examples)
for i in range(1,4):
    variants.append( (f"distort_{i}", distort(img, max_shift=0.08)) )

# save them all
for name, im in variants:
    out_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(os.path.basename(INPUT_PATH))[0]}_{name}.png")
    cv2.imwrite(out_path, im)
    print(f"Saved {out_path}")

print("✅ All augmentations done.")

