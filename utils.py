import os
import glob
from PIL import Image
import face_recognition


def preprocess_images(folder_path):
    for file_path in glob.glob(os.path.join(folder_path, "*")):
        if not file_path.lower().endswith(
            (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")
        ):
            os.remove(file_path)
            print(f"Not a supported image format: {file_path}")
            continue

        image = face_recognition.load_image_file(file_path)
        face_locations = face_recognition.face_locations(image)

        if len(face_locations) == 1:
            top, right, bottom, left = face_locations[0]
            padding = left // 4
            top = max(0, top - padding)
            right = min(image.shape[1], right + padding)
            bottom = min(image.shape[0], bottom + padding)
            left = max(0, left - padding)

            face_image = Image.open(file_path)
            face_image = face_image.crop((left, top, right, bottom))
            face_image.save(file_path)
            print(f"Face cropped and saved: {file_path}")
        elif len(face_locations) > 1:
            os.remove(file_path)
            print(f"More than one face detected: {file_path}")
        else:
            os.remove(file_path)
            print(f"No face detected: {file_path}")
