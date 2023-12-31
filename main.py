import time
import requests
from bs4 import BeautifulSoup
import csv

def get_links_from_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a", href=True)
        return [link["href"] for link in links]
    else:
        print("Nie udało się pobrać strony.")
        return []

def check_links_status(links):
    with open('links_status.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['link', 'response_code']  # Poprawione nazwy pól
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  #zapisanie headerów

        for link in links:
            time.sleep(3) #uśpij zeby nie zabić serwera
            print(link)
            if link.startswith("http") or link.startswith("https"): #dodanie warunku, że link ma zaczynać się na http albo https
                response = requests.head(link)
                print(f"Link: {link}, Status kod: {response.status_code}") #wydrukowanie logu
                writer.writerow({'link': link, 'response_code': response.status_code}) #zapisanie wiersza
def read_links(path):
    results = []
    with open(path, newline='') as csvFile:
        reader = csv.reader(csvFile, delimiter=' ')
        for row in reader:
            cell_content_without_brackets = ''.join(c for c in row if c not in '[]')
            results.append(cell_content_without_brackets)
    return results


if __name__ == "__main__":
    urls_to_check = read_links("./links.csv")

    for url_to_check in urls_to_check:
        extracted_links = get_links_from_page(url_to_check)
        if extracted_links:
            check_links_status(extracted_links)
        else:
            print("Brak linków do sprawdzenia.")
