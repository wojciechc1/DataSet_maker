from downloader.runner import run_downloader
from config import DATASETS, BASE_DIR, HEADLESS

if __name__ == "__main__":
    for dataset in DATASETS:
        run_downloader(
            dataset["queries"],
            BASE_DIR,
            folder_name=dataset["folder_name"],
            num_images=dataset["num_images"],
            headless=HEADLESS,
            reset_folder=dataset["reset_folder"]
        )
