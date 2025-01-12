import logging
import os
import requests
import tomllib

with open("pyproject.toml", "rb") as f:
    config = tomllib.load(f)
    pat_file = config["client"]["personal_access_token_file"]
    with open(pat_file, "r") as f:
        github_token = f.read().strip()


def get_headers() -> dict:
    headers = {"Authorization": f"Bearer {github_token}"}
    return headers


def get_pdf_files() -> dict:
    remote_dir = "https://api.github.com/repos/ftrojan/songbook/contents/pdf"
    files_response = requests.get(url=remote_dir, headers=get_headers())
    if files_response.ok:
        files_json = files_response.json()
        files_url = {x["name"]: x["download_url"] for x in files_json}
        return files_url
    else:
        logging.error(f"{files_response.text}")
        raise ConnectionError()


def download_pdf(download_url: str, target_path: str) -> None:
    r = requests.get(download_url)
    open(target_path, "wb").write(r.content)
    logging.info(f"downloaded {download_url} to {target_path}")


def prepare_dir(local_dir: str) -> None:
    os.makedirs(local_dir, exist_ok=True)


def clean_dir(local_dir: str) -> None:
    files = os.listdir(local_dir)
    logging.info(files)
    for f in files:
        file_path = os.path.join(local_dir, f)
        logging.info(f"removing {file_path}")
        os.remove(file_path)


def sync(local_dir: str | None = None) -> None:
    if local_dir is None:
        local_dir = config["client"]["target_dir"]
    logging.info(f"{local_dir=}")
    prepare_dir(local_dir)
    files_url = get_pdf_files()
    logging.info(f"{len(files_url)}:")
    clean_dir(local_dir)
    for name, url in files_url.items():
        download_pdf(url, target_path=f"{local_dir}/{name}")
