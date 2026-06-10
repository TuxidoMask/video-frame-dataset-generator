import cv2
import os
import random

# 📂 Carpeta donde están los videos
video_folder = "videos"

# 📂 Carpeta base del dataset
dataset_path = "dataset/images"

train_path = os.path.join(dataset_path, "train")
val_path = os.path.join(dataset_path, "val")

os.makedirs(train_path, exist_ok=True)
os.makedirs(val_path, exist_ok=True)

# ⏱️ Intervalo en segundos
interval_seconds = 5

# 📊 Contadores
total_saved = 0

# 🎥 Obtener todos los videos automáticamente
video_paths = [
    os.path.join(video_folder, f)
    for f in os.listdir(video_folder)
    if f.lower().endswith((".mp4", ".avi", ".mov"))
]

print(f"Videos encontrados: {len(video_paths)}")

# 🔁 Procesar cada video
for video_path in video_paths:

    print(f"\nProcesando: {video_path}")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"No se pudo abrir {video_path}")
        continue

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        print(f"FPS inválido en {video_path}")
        continue

    frame_interval = int(fps * interval_seconds)

    frame_count = 0
    saved_count = 0

    video_name = os.path.splitext(os.path.basename(video_path))[0]

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % frame_interval == 0:

            timestamp = int(frame_count / fps)

            # 🎯 Split train / val (80/20)
            if random.random() < 0.8:
                output_dir = train_path
            else:
                output_dir = val_path

            frame_name = os.path.join(
                output_dir,
                f"{video_name}_f{saved_count:04d}_t{timestamp}s.jpg"
            )

            cv2.imwrite(frame_name, frame)

            print(f"Guardado: {frame_name}")

            saved_count += 1
            total_saved += 1

        frame_count += 1

    cap.release()

    print(f"Frames guardados de {video_name}: {saved_count}")

print(f"\nTOTAL GENERAL: {total_saved} frames")
