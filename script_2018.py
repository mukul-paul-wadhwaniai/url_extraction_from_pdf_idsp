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
        with open(file_name, "wb") as pdf_file:
            pdf_file.write(response.content)

    else:
        print(f"Failed to download the PDF file. Status code: {response.status_code}")


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
        

pdf_url = "https://idsp.nic.in/WriteReadData/Media_Alert_Oct-2018/"
start_param_lid = 4935
end_param_lid = 4999
urls = set()

start = 5
end = 10
count = 1
for param_lid in range(start_param_lid, end_param_lid + 1):
    pdf_link = pdf_url + str(param_lid) + '.pdf'
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

