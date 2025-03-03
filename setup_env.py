import os
import gdown
import venv

folders = ["weights", "weights/2023-10-28-18-33-37", "weights/2024-01-11-20-02-45", "video_data"]

for folder in folders:

    try:
        os.mkdir(folder)
    except OSError as error:
        print(folder, "already created.")        

gdown.download("https://drive.google.com/uc?id=1E9FPB5WFIBMLrOJqZLpoVOK4Mjzrrxhv", "weights/2023-10-28-18-33-37/model_best.pth")
gdown.download("https://drive.google.com/uc?id=1477-st1s1TxXN6oqfM5ZnsQwd8BCzVg1", "weights/2023-10-28-18-33-37/config.yml")
gdown.download("https://drive.google.com/uc?id=1Zdjnkn4EHOI5_k08apofwRgTjWpai4E4", "weights/2024-01-11-20-02-45/model_best.pth")
gdown.download("https://drive.google.com/uc?id=1kQkQG-q_VvLRozv30hyeLB7P_jiEEqiE", "weights/2024-01-11-20-02-45/config.yml")

