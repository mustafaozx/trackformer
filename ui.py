import streamlit as st
import os
import subprocess
import uuid
import threading

# Streamlit uygulamasını başlat
st.title("Trackfomer: UI")

# Video dosyasını seçme
video_file = st.file_uploader(
    "Lütfen bir video dosyası seçin", type=["mp4", "avi", "mov"]
)

if video_file is not None:
    # Videoyu geçici bir klasöre kaydetme
    temp_folder = str(uuid.uuid4())
    os.makedirs(temp_folder)

    video_path = os.path.join(temp_folder, video_file.name)

    with open(video_path, "wb") as f:
        f.write(video_file.read())

    # Videoyu Streamlit ile gösterme
    st.video(video_path)

    # ffmpeg kullanarak videoyu çerçevelere ayırma
    # cmd = [
    #     "ffmpeg",
    #     "-i", video_path,
    #     "-vf", "fps=30",  # Çerçeve hızı (örnekte 30 FPS olarak ayarlanmıştır)
    #     os.path.join(temp_folder, "%06d.png"),  # Çerçeve dosya adı formatı
    # ]

    # ffmpeg -y -i 'rtsp://localhost:8081/mystream2' -vf "fps=1" -q:v 2 %06d.jpg

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-vf",
        "fps=30",  # Çerçeve hızı (örnekte 30 FPS olarak ayarlanmıştır)
        os.path.join(temp_folder, "%06d.png"),  # Çerçeve dosya adı formatı
    ]

    thread = threading.Thread(target=subprocess.run, args=(cmd,))
    thread.start()

    # python src/track.py with \
    #     dataset_name=DEMO \
    #     data_root_dir=data/snakeboard \
    #     output_dir=data/snakeboard \
    #     write_images=pretty

    cmd = [
        "python",
        "src/track.py",
        "with",
        "dataset_name=DEMO",
        "reid",
        "data_root_dir={}".format(temp_folder),
        "output_dir={}".format(temp_folder),
        "write_images=pretty",
    ]

    subprocess.run(cmd)

    # ffmpeg -framerate 1 -re -stream_loop -1 -i %06d.jpg -c:v libx264 -preset veryfast -tune zerolatency -vf "fps=1" -f rtsp rtsp://localhost:8081/mystream3


# Uygulama sonu
st.write("Muhammet Mustafa ÖZ")
