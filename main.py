import argparse
import csv
import requests
from bs4 import BeautifulSoup
import sys

def fetch_results(profile_url):
    try:
        response = requests.get(profile_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching profile page: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')
    # This will need to be adapted based on actual page structure.
    # Example assumes results are in a table with class 'results-table'
    results_table = soup.find('table', {'class': 'results-table'})

    if not results_table:
        print("Could not find results table on the page.")
        sys.exit(1)

    headers = [th.get_text(strip=True) for th in results_table.find_all('th')]
    rows = []
    for tr in results_table.find_all('tr')[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all('td')]
        if cells:
            rows.append(cells)

    return headers, rows

def save_to_csv(headers, rows, filename='results.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Scrape Athlinks profile results to CSV.')
    parser.add_argument('--profile-url', required=True, help='URL of your Athlinks profile results page')
    args = parser.parse_args()

    headers, rows = fetch_results(args.profile_url)
    save_to_csv(headers, rows)

if __name__ == "__main__":
    main()
