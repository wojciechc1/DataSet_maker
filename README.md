# Image Scraper Selenium

A Python project for downloading images from Google Images using Selenium. Supports multiple queries, dataset organization, metadata tracking, and error handling.

---

## Features

- Download images from Google Images based on a list of queries.
- Organize images in subfolders per dataset or user-defined folder.
- Avoid downloading duplicate images using JSON metadata.
- Resume interrupted downloads without re-downloading existing images.
- Reset folder option to start fresh for a new dataset.
- Logs actions for easier debugging and tracking.
- Handles failed downloads gracefully (SSL, connection errors, etc.).

---

## Project Structure
```bash
project/
│── main.py                # test
│── config.py              # configuration (limits, pahts, selenium options itd.)
│── requirements.txt       
│── README.md              
│
├── downloader/
│   ├── __init__.py
│   ├── selenium_driver.py  # launching and controlling Selenium
│   ├── scraper.py          # collecting image URLs
│   ├── runner.py           # running the download workflow
│   └── downloader.py       # downloading images to disk
│
├── utils/
│   ├── __init__.py
│   ├── file_utils.py       # folders, paths, metadata
│   ├── image_utils.py      # duplicate filtering, validation --- future
│   └── logger.py           # logging setup
│
└── tests/
    ├── test_scraper.py
    ├── test_downloader.py
    └── test_utils.py

```

---

## Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd Image_scraper_selenium
```
1. Clone the repository

```bash
pip install -r requirements.txt
```

3. Make sure you have Chrome installed, and optionally install chromedriver or use webdriver-manager

---

## Usage

1. Edit config.py to define your queries and folder settings:

```bash
DATASETS = [
    {
        "queries": ["cat", "tiger"],
        "folder_name": "cats",
        "num_images": 1,
        "reset_folder": True
    },
    {
        "queries": ["dog", "wolf"],
        "folder_name": "dogs",
        "num_images": 1,
        "reset_folder": False
    } #....
]
BASE_DIR = "downloads"
HEADLESS = True

```

2. Run the main script:

```bash
python main.py
```

3. Or call the runner directly:*

```bash
from downloader.runner import run_downloader

run_downloader(
    ["cat", "tiger"],
    "downloads",
    folder_name="cats",
    num_images=5,
    headless=True,
    reset_folder=True
)

```
--- 
## Configuration Options:
- queries: List of search queries.
- base_directory: Base folder to save datasets.
- folder_name: Name of the subfolder for current dataset.
- num_images: Number of images per query.
- headless: Boolean, whether to run Chrome in headless mode.
- reset_folder: Boolean, whether to clear the folder before downloading.

--- 
## Metadata

Each folder has a metadata.json file:
```json
{
  "downloaded": ["url1", "url2", ...],
  "queries": ["cat", "tiger"]
}
```
- Ensures no duplicate downloads.
- Tracks which queries have been processed.

--- 
## Logging

- All actions are logged, including:
- Clicked thumbnails
- Downloaded images
- Failed downloads (SSL or connection issues)
- Query processing summary

---

## Future Improvements
- Add type filters (e.g., jpg, png, gif) to limit downloads by file type.
- Support other image sources beyond Google Images.
- Parallel downloading for faster scraping.
- Command-line interface for easy usage

---

## License

MIT License – free to use and modify.