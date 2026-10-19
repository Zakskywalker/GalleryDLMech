# Gallery-DL Downloader

 ## System Design
Single downloader engine that can operate as a GUI, CLI or External Application.

User
 │
 ▼
downloader.py
 │
 ├── GUI Mode
 ├── CLI Mode
 └── External Mode
      │
      ▼
  Gallery-DL
      │
      ▼
 Browser Cookies
      │
      ▼
   Downloads


## Features

- GUI Mode
- CLI Mode
- URL File Support
- Browser Cookies
- External App Mode
- Logging

## Usage

python downloader.py

python downloader.py URL

python downloader.py --url-file urls.txt

python downloader.py --externalapp --url-file jobs.txt

## Files

config.py
logger_util.py
downloader.py
