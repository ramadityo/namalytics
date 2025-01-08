import cv2
import os
import random

INPUT_FOLDER = "C:\\BUAT_BELAJAR_KULIAH\\Visi Komputer\\namalytics\\input"
OUTPUT_FOLDER = "C:\\BUAT_BELAJAR_KULIAH\\Visi Komputer\\namalytics\\output"

def rotate(image, angle, center=None, scale=1.0):
    (h, w) = image.shape[:2]
    if center is None:
        center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def flip(image, flipCode=1):
    return cv2.flip(image, flipCode)

def adjust_brightness(image, factor=1.0):
    return cv2.convertScaleAbs(image, alpha=factor, beta=0)

def crop(image, x_start, y_start, width, height):
    return image[y_start:y_start+height, x_start:x_start+width]

def random_augment(image):
    augmentations = []

    if random.random() < 0.5:
        angle = random.choice([90, 180, 270])
        image = rotate(image, angle)
        augmentations.append(f"rotate_{angle}")

    if random.random() < 0.5:
        flipCode = random.choice([-1, 0, 1])
        image = flip(image, flipCode)
        augmentations.append(f"flip_{flipCode}")

    if random.random() < 0.5:
        brightness_factor = random.uniform(0.5, 1.5)
        image = adjust_brightness(image, brightness_factor)
        augmentations.append(f"brightness_{brightness_factor:.2f}")

    if random.random() < 0.5:
        h, w = image.shape[:2]
        crop_w = random.randint(int(w * 0.5), w)
        crop_h = random.randint(int(h * 0.5), h)
        x_start = random.randint(0, w - crop_w)
        y_start = random.randint(0, h - crop_h)
        image = crop(image, x_start, y_start, crop_w, crop_h)
        augmentations.append(f"crop_{crop_w}x{crop_h}")

    return image, augmentations

def resize_batch(folder, output_folder, size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        if not filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            continue

        image = cv2.imread(file_path)
        if image is None:
            print(f"Warning: Cannot read {filename}. Skipping.")
            continue

        resized_image = cv2.resize(image, (image.shape[1] // size, image.shape[0] // size))
        output_filename = os.path.join(output_folder, filename)
        cv2.imwrite(output_filename, resized_image)

def batch_augment():
    NUM_GENERATE = 1

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    for idx, filename in enumerate(os.listdir(INPUT_FOLDER)):
        file_path = os.path.join(INPUT_FOLDER, filename)

        if not filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            continue

        image = cv2.imread(file_path)
        if image is None:
            print(f"Warning: Cannot read {filename}. Skipping.")
            continue

        for i in range(NUM_GENERATE):
            augmented_image, augmentations = random_augment(image)
            name, ext = os.path.splitext(filename)
            output_filename = f"gambar{idx + 1}_output_{i + 1}_{'_'.join(augmentations)}{ext}"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)

            cv2.imwrite(output_path, augmented_image)
            print(f"Saved: {output_filename} with augmentations: {augmentations}")

if __name__ == "__main__":
    batch_augment()
    # resize_batch(INPUT_FOLDER, OUTPUT_FOLDER, 2)