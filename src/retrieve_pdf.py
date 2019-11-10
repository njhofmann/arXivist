import requests as r
import pathlib as pl
import uuid

FOLDER_PATH = pl.Path(__file__).parent.joinpath('pdfs')


def fetch_and_save_pdf(pdf_url: str) -> pl.Path:
    file_name = str(uuid.uuid4()) + '.pdf'
    response = r.get(pdf_url, stream=True)
    response.raw.decode_content = True
    full_path = FOLDER_PATH.joinpath(file_name).resolve()
    with open(full_path, 'wb') as file:
        file.write(response.content)
    return full_path


if __name__ == '__main__':
    fetch_and_save_pdf('https://arxiv.org/pdf/1509.06461')
