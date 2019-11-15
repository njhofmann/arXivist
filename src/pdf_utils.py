import requests as r
import pathlib as pl
import uuid
import subprocess as sbp
from utility import search_result as u

FOLDER_PATH = pl.Path(__file__).parent.parent.joinpath('pdfs')


def fetch_and_save_pdf(pdf_url: u.SearchResult) -> pl.Path:
    file_name = str(uuid.uuid4()) + '.pdf'
    pdf_url = 'http://arxiv.org/pdf/' + pdf_url.id + '.pdf'
    response = r.get(pdf_url, stream=True)
    response.raw.decode_content = True
    full_path = FOLDER_PATH.joinpath(file_name).resolve()
    with open(full_path, 'wb') as file:
        file.write(response.content)
    return full_path


def open_pdf(pdf_path: str) -> None:
    process = sbp.Popen(args=['evince', pdf_path], stderr=sbp.PIPE, stdout=sbp.PIPE)
    process.wait()
    if process.returncode != 0:
        out, err = process.communicate()
        raise RuntimeError(str(err))


if __name__ == '__main__':
    #fetch_and_save_pdf('https://arxiv.org/pdf/1509.06461')
    open_pdf('/home/natejh/PycharmProjects/arXivist/pdfs/9f887a72-a1e9-4d18-9865-d73718496dda.pdf')
