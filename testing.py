import csv

input_file = "urls.csv"
output_file = "output.csv"

# Set to store unique URLs
unique_urls = set()

# Read the input CSV and collect unique URLs
with open(input_file, "r", newline="") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        url = row["urls"]
        unique_urls.add(url)

# Write the unique URLs to the output CSV
with open(output_file, "w", newline="") as outfile:
    fieldnames = ["url"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for url in unique_urls:
        writer.writerow({"url": url})

print(f"Unique URLs have been saved to '{output_file}'.")