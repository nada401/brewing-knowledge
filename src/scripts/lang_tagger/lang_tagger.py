import gzip
import csv
import re
from fast_langdetect import detect, detect_multilingual

def lang_tagger(text):
    text = text.replace("\n", "")
    res = ""

    for couple in detect_multilingual(text):
       if couple['score'] > 0.2:
          res = res + ('' if res=='' else ", ") + couple['lang']
    return res

# Step 1: Read and process the file line by line from the .gz file
def parse_and_write_to_csv(input_gz_file, output_csv_file):
    # Regular expression for matching 'field: value' format
    field_regex = re.compile(r'(\w+):\s*(.*)')

    with gzip.open(input_gz_file, 'rt', encoding='utf-8') as f, open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
        # Initialize CSV writer
        writer = None
        current_entry = {}

        keys = ['beer_id','date', 'user_id']

        for line in f:
            line = line.strip()  # Remove leading/trailing whitespaces
            match = field_regex.match(line)

            if match:
                key, value = match.groups()
                if key in keys:
                    current_entry[key] = value
                elif key == 'text':
                    current_entry['lang_tag'] = lang_tagger(value)
            else:
                if current_entry:
                    if writer is None:
                        headers = current_entry.keys()
                        writer = csv.DictWriter(csv_file, fieldnames=headers)
                        writer.writeheader()

                    # Write the current entry
                    writer.writerow(current_entry)
                    current_entry = {}  

        # Write the last entry (if any)
        if current_entry:
            writer.writerow(current_entry)

# Main function to execute the language tagging process
def tag_datasets():
    # the files "./data/RateBeer/reviews.txt.gz" and "./data/BeerAdvocate/reviews.txt.gz" must be present for the pipeline to work
    dirs = ["./data/RateBeer/", "./data/BeerAdvocate/"]

    input_gz_file = 'reviews.txt.gz'  
    output_csv_file = 'reviews_tagged.csv'   

    for d in dirs:
        parse_and_write_to_csv(d+input_gz_file, d+output_csv_file)