# Extract PDF metadata
exiftool document.pdf

pdfinfo document.pdf

# Extract PDF text
pdftotext document.pdf

# Search for keywords
pdfgrep -i "IP address\|PLC\|SCADA" document.pdf
