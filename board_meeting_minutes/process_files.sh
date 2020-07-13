
# Convert PDF to PNG
# This will create one PNG document per page (no more than 999 pages)

declare -a DOCS
DOCS=(
"https://www1.nyc.gov/assets/nycha/downloads/pdf/board_meeting_minutes_07312019.pdf"
"https://www1.nyc.gov/assets/nycha/downloads/pdf/board_meeting_minutes_09252019.pdf"
"https://www1.nyc.gov/assets/nycha/downloads/pdf/board_meeting_minutes_10302019.pdf"
"https://www1.nyc.gov/assets/nycha/downloads/pdf/board_meeting_minutes_12182019.pdf"
"https://www1.nyc.gov/assets/nycha/downloads/pdf/board_meeting_minutes_02262020-corrected.pdf"
"https://www1.nyc.gov/assets/nycha/downloads/pdf/board_meeting_minutes_04292020.pdf"
)declare -r DOCS

# We download the files.
for doc in $DOCS; do curl $doc -o ${doc##*/}; done 


for file in *.pdf
do
  echo convert -density 300  $file  -depth 8 -strip -background white -alpha off ${file%.pdf}-%03d.tiff
done


file=board_meeting_minutes_04292020
# Do OCR on all the pages
for page in $file-???.tiff; do tesseract $page ${page%.tiff}; done

cat $file-*.txt > $file.txt