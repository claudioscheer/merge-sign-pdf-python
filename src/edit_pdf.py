import os
import uuid
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger


def get_cache_file_path():
    file_name = f"{uuid.uuid4().hex}.pdf"
    cache_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", ".cache-pdf")
    )
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)
    return os.path.join(cache_path, file_name)


def remove_files(files):
    for file in files:
        os.remove(file)


def merge_rotate_pdf_files(files, pages_rotation_matrix):
    rotated_files = []
    for (file, rotation) in zip(files, pages_rotation_matrix):
        out_file = rotate_pages(file, rotation)
        rotated_files.append(out_file)

    file_merged = merge_files(rotated_files)
    remove_files(rotated_files)
    return file_merged


def merge_files(files):
    out_file = get_cache_file_path()
    pdf_merger = PdfFileMerger()
    for pdf in files:
        pdf_merger.append(pdf)
    pdf_merger.write(out_file)
    pdf_merger.close()
    return out_file


def rotate_pages(file, pages_rotation):
    with open(file, "rb") as pdf_in:
        pdf_reader = PdfFileReader(pdf_in)
        if pdf_reader.numPages != len(pages_rotation):
            raise Exception(
                "The number of pages in PDF is different from the length os the rotation array."
            )
        pdf_writer = PdfFileWriter()
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            page.rotateClockwise(pages_rotation[page_num])
            pdf_writer.addPage(page)
        out_file = get_cache_file_path()
        with open(out_file, "wb") as pdf_out:
            pdf_writer.write(pdf_out)
            return out_file
