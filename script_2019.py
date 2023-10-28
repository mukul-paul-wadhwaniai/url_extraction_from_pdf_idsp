import requests
from bs4 import BeautifulSoup
import urllib.parse
import fitz
import pandas as pd
import csv
from urllib.parse import urlparse
import os

events = 0

def download_pdf(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        iframe = soup.find("iframe")

        if iframe:
            pdf_url = iframe.get("src")
            if not pdf_url.startswith("http"):
                base_url = urllib.parse.urlparse(url)
                pdf_url = urllib.parse.urljoin(base_url.geturl(), pdf_url)

            pdf_response = requests.get(pdf_url)

            if pdf_response.status_code == 200:
                with open(file_name, "wb") as pdf_file:
                    pdf_file.write(pdf_response.content)
                print("PDF file downloaded and saved as 'downloaded.pdf'.")
            else:
                print(f"Failed to download the PDF file. Status code: {pdf_response.status_code}")
            events += 1
        else:
            print("No PDF iframe found on the page.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


def url_extraction(pdf_file_path):
    pdf_document = fitz.open(pdf_file_path)
    first_page = pdf_document[0]
    first_page_text = first_page.get_text()
    first_page_text = first_page_text.split(" ")

    for text in first_page_text:
        if (
            (text.startswith("https://") or text.startswith("\nhttps://") or text.startswith("http://") or text.startswith("\nhttp://")) and
            ('facebook' not in text and 'twitter' not in text)
        ):
            print(text)
            parsed_url = urlparse(text)
            hostname = parsed_url.hostname
            print(hostname)
            return hostname
        

pdf_url = "https://idsp.mohfw.gov.in/showfile.php?lid="
start_param_lid = 4585
end_param_lid = 4614
urls = set()

start = 5
end = 10
count = 1
for param_lid in range(start_param_lid, end_param_lid + 1):
    pdf_link = pdf_url + str(param_lid)
    print(pdf_link)
    file_name = 'downlaoded.pdf'
    print(count, "       ", param_lid)
    count += 1
    download_pdf(pdf_link, file_name)
    if os.path.exists(file_name):
        url = url_extraction(file_name)
        if url:
            print("url ===================================: ", url)
            urls.add(url)
        if os.path.exists(file_name):
            os.remove(file_name)


def download_messages_as_csv(messages_array, csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['urls'])
        for message in messages_array:
            csv_writer.writerow([message])

csv_filename = 'urls.csv'

download_messages_as_csv(urls, csv_filename)

print(urls)
print(events)

