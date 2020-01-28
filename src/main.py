import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--files", nargs="+", help="PDF files to merge and sign")
parser.add_argument(
    "--rotate-pages-matrix",
    help="Degrees to rotate PDF pages. The values for each PDF file must be separated by semicolons. Ex: 0 0; 90",
)
parser.add_argument("--keys", nargs="+", help="Keys to sign the PDF files")
parser.add_argument("-o", "--output", help="Output file name")
args = parser.parse_args()

files_len = len(args.files)
rotate_pages_matrix = [
    z.split() for z in [x.strip() for x in args.rotate_page_matrix.split(";")]
]
rotate_pages_matrix_len = len(rotate_pages_matrix)

if files_len != rotate_pages_matrix_len:
    sys.exit("Files and rotate pages matrix must have the same lenght.")

print(rotate_pages_matrix)
