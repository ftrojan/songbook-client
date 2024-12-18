import logging
import os
import requests
import tomllib

with open("pyproject.toml", "rb") as f:
    config = tomllib.load(f)


def get_headers() -> dict:
    varname = config["client"]["personal_access_token_variable"]
    github_token = os.getenv(varname)
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
    files_url = get_pdf_files()
    logging.info(f"{len(files_url)}:")
    clean_dir(local_dir)
    for name, url in files_url.items():
        download_pdf(url, target_path=f"{local_dir}/{name}")
