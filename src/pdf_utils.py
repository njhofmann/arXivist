import requests as r
import pathlib as pl
import uuid
import subprocess as sbp
from utility import search_result as u
from typing import Union
import sys

FOLDER_PATH = pl.Path(__file__).parent.parent.joinpath('pdfs')
BASE_ARXIV_PDF_URL = 'http://arxiv.org/pdf/'


def fetch_and_save_pdf(pdf_url: u.SearchResult) -> pl.Path:
    file_name = str(uuid.uuid4()) + '.pdf'
    pdf_url = BASE_ARXIV_PDF_URL + pdf_url.id + '.pdf'
    full_path = FOLDER_PATH.joinpath(file_name).resolve()

    response = r.get(pdf_url, stream=True)
    response.raw.decode_content = True
    with open(full_path, 'wb') as file:
        file.write(response.content)

    return full_path


def open_pdf(pdf_path: Union[str, pl.Path]) -> None:
    cur_os = sys.platform  # TODO finish implementing for other oses
    if cur_os == 'linux':
        pdf_exe_cmd = ['evince']
    elif cur_os == 'win32':
        pass  # adobe
    elif cur_os == ' darwin':
        pass  # ??
    else:
        raise RuntimeError(f'{cur_os} is an unsupported OS for opening PDFs')

    process = sbp.Popen(args=[pdf_exe_cmd, pdf_path], stderr=sbp.PIPE, stdout=sbp.PIPE)
    process.wait()
    if process.returncode != 0:
        out, err = process.communicate()
        raise RuntimeError(str(err))


if __name__ == '__main__':
    #fetch_and_save_pdf('https://arxiv.org/pdf/1509.06461')
    open_pdf('/home/natejh/PycharmProjects/arXivist/pdfs/9f887a72-a1e9-4d18-9865-d73718496dda.pdf')