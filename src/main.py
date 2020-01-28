import datetime
import argparse
import sys
from edit_pdf import merge_rotate_pdf_files
from sign_pdf import is_file_signed, sign_file

parser = argparse.ArgumentParser()
parser.add_argument(
    "--files", nargs="+", help="PDF files to merge and sign", required=True
)
parser.add_argument(
    "--pages-rotation-matrix",
    help='Degrees to rotate PDF pages. The values for each PDF file must be separated by semicolons. Ex: "0 0; 90"',
    required=True,
)
parser.add_argument(
    "--certificates",
    nargs="+",
    help="Certificates to sign the PDF files",
    required=True,
)
parser.add_argument(
    "--passwords", nargs="+", help="Passwords to open the certificates", required=True
)
parser.add_argument("-o", "--output", help="Output file name", required=True)
args = parser.parse_args()

files_len = len(args.files)
# region Verify is some file is already signed.
for file in args.files:
    if is_file_signed(file):
        raise Exception(f"The file {file} is already signed.")
# endregion
# region Convert --pages-rotation-matrix argument to a matrix of int.
pages_rotation_matrix = []
for file_array in [x.strip() for x in args.pages_rotation_matrix.split(";")]:
    values_each_page = file_array.split()
    pages_rotation_matrix.append([int(x) for x in values_each_page])
# endregion
pages_rotation_matrix_len = len(pages_rotation_matrix)

if files_len != pages_rotation_matrix_len:
    raise Exception("Files and pages rotation matrix must have the same length.")

if len(args.certificates) != len(args.passwords):
    raise Exception("Certificates and passwords must have the same length.")

file_merged = merge_rotate_pdf_files(args.files, pages_rotation_matrix)

date = datetime.datetime.utcnow()
date = date.strftime("%Y%m%d%H%M%S+00'00'")
sign_infos = {
    b"sigflags": 3,
    b"contact": b"example@example.com",
    b"location": b"Unknown",
    b"signingdate": date.encode(),
    b"reason": b"Just a document",
}
file_signed = sign_file(file_merged, sign_infos, args.certificates, args.passwords)
print(file_signed)
