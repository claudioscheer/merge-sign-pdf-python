from endesive import pdf


def is_file_signed(file):
    try:
        file_data = open(file, "rb").read()
        (hash_ok, signature_ok, cert_ok) = pdf.verify(file_data)
        return signature_ok or hash_ok or cert_ok
    except:
        return False
