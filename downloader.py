import argparse
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading
import config
print(dir(config))
from config import COOKIE_BROWSER, GALLERY_DL, LOG_FILE
from logger_util import AppLogger


logger = AppLogger(LOG_FILE)


def build_gallery_dl_command(url):
    return [
        GALLERY_DL,
        "--cookies-from-browser",
        COOKIE_BROWSER,
        url,
    ]


def download_url(url, output_callback=None):
    cmd = build_gallery_dl_command(url)

    logger.info(f"Downloading: {url}")

    if output_callback:
        output_callback(f"Running: {' '.join(cmd)}\n")

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    for line in process.stdout:
        logger.info(line.rstrip())

        if output_callback:
            output_callback(line)

    process.wait()

    logger.info(f"Finished: {url}")


def run_downloads(urls, output_callback=None):
    for url in urls:
        if url.strip():
            download_url(url.strip(), output_callback)


def load_urls_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return [
            line.strip()
            for line in f.readlines()
            if line.strip()
        ]


class DownloadGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gallery-DL Downloader")
        self.root.geometry("900x600")

        self.urls = ScrolledText(self.root, height=10)
        self.urls.pack(fill="x", padx=10, pady=10)

        self.button = ttk.Button(
            self.root,
            text="Start Download",
            command=self.start_download
        )
        self.button.pack(pady=5)

        self.log_text = ScrolledText(self.root)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

    def append_log(self, text):
        self.log_text.insert("end", text)
        self.log_text.see("end")

    def start_download(self):
        urls = self.urls.get("1.0", "end").splitlines()

        thread = threading.Thread(
            target=run_downloads,
            args=(urls, self.append_log),
            daemon=True
        )
        thread.start()

    def run(self):
        self.root.mainloop()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "urls",
        nargs="*",
        help="URLs to download"
    )

    parser.add_argument(
        "--url-file",
        help="Text file containing URLs"
    )

    parser.add_argument(
        "--externalapp",
        action="store_true",
        help="Run without prompts/UI"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    urls = []

    if args.urls:
        urls.extend(args.urls)

    if args.url_file:
        urls.extend(load_urls_file(args.url_file))

    if args.externalapp:
        logger.info("External App Mode Enabled")
        run_downloads(urls)
        return

    if urls:
        run_downloads(urls)
        return

    gui = DownloadGUI()
    gui.run()


if __name__ == "__main__":
    main()