# Merge and Sign PDF files command line

This __alpha__ project uses Python to merge and sign PDF files with multiple certificates.

## How to install

Download the compiled file from [Releases](https://github.com/claudioscheer/merge-sign-pdf-python/releases) page.

## How to use

```console
foo@bar:~$ ./merge-sign-pdf --help
```

### Example

```console
foo@bar:~$ ./merge-sign-pdf --files ./test-files/pdfs/file1.pdf ./test-files/pdfs/file2.pdf ./test-files/pdfs/file4.pdf --pages-rotation-matrix "0; 90; 0 270" --certificates ./test-files/certificates/user1@example.com/cert.p12 ./test-files/certificates/user2@example.com/cert.p12 --passwords "user1@example.com" "user2@example.com" --output output.pdf --location BR --reason "Just sign it!" --contact "example@example.com"
```