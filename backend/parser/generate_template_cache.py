from processors.binary_threshold import binary_threshold
from processors.binary_threshold_red import binary_threshold_red
import cv2
import os
import pickle
from PIL import Image
import os
from pathlib import Path

template_dir = "templates"

# Initialize ORB inside the generator
orb = cv2.ORB_create(nfeatures=100)


def generate_cache():
    cache = {}

    # Ensure the cache directory exists
    os.makedirs("cache", exist_ok=True)

    for filename in os.listdir(template_dir):
        path = os.path.join(template_dir, filename)
        img = cv2.imread(path)
        #img = Image.open(path)

        binary_red = binary_threshold_red(img)
        preview = Image.fromarray(binary_red)

        name_without_ext = Path(filename).stem

        preview.save(f"processed_images/{name_without_ext}_red.png")
        binary = binary_threshold(img)
        preview = Image.fromarray(binary)
        preview.save(f"processed_images/{name_without_ext}.png")

        # if img is None:
        #     print(f"Failed to load {filename}")
        #     continue

        # processed = preprocess(img)
        # preview = Image.fromarray(processed)
        # preview.show()

        # # CRITICAL FIX: Compute and store the DESCRIPTORS, not the pixels
        # _, des = orb.detectAndCompute(processed, None)

        # if des is not None:
        #     cache[filename] = des
        #     print(f"Cached descriptors for {filename}")
        # else:
        #     print(f"Warning: No features found in {filename}, skipping.")

    with open("cache/template_cache.pkl", "wb") as f:
        pickle.dump(cache, f)

    print("\nTemplate cache generated successfully.")