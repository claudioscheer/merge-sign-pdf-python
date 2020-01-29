from OpenSSL.crypto import load_pkcs12
from endesive import pdf
from edit_pdf import get_cache_file_path, remove_files


def is_file_signed(file):
    try:
        file_data = open(file, "rb").read()
        (hash_ok, signature_ok, cert_ok) = pdf.verify(file_data)
        return signature_ok or hash_ok or cert_ok
    except:
        return False


def sign_file(file, sign_infos, certificates, passwords, current_index=0):
    if current_index >= len(certificates):
        return file

    certificate = certificates[current_index]
    password = passwords[current_index]

    p12 = load_pkcs12(open(certificate, "rb").read(), password)
    if not sign_infos.get(b"location"):
        p12_subject = p12.get_certificate().get_subject()
        location = p12_subject.C if p12_subject.C else "Unknown"
    else:
        location = sign_infos.get(b"location")
    out_file_path = get_cache_file_path()

    pdf_data = open(file, "rb").read()
    pdf_signature_data = pdf.cms.sign(
        pdf_data,
        {**sign_infos, **{b"location": location.encode()}},
        p12.get_privatekey().to_cryptography_key(),
        p12.get_certificate().to_cryptography(),
        [],
        "sha256",
        timestampurl="http://timestamp.globalsign.com/scripts/timstamp.dll",
    )

    with open(out_file_path, "wb") as out_file:
        out_file.write(pdf_data)
        out_file.write(pdf_signature_data)

    remove_files([file])
    return sign_file(
        out_file_path,
        sign_infos,
        certificates,
        passwords,
        current_index=current_index + 1,
    )
