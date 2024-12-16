import requests
from bs4 import BeautifulSoup

def scrape_website(session, url):
    try:
        print(f"Scraping: {url}")
        response = session.get(url, timeout=20)  # Increased timeout
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text(separator=' ', strip=True)
        return text_content
    except requests.exceptions.SSLError as ssl_err:
        print(f"SSL error occurred with {url}: {ssl_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred with {url}: {req_err}")
    except Exception as e:
        print(f"An unexpected error occurred while scraping {url}: {e}")
        return None  # Return None on scraping errors

def main():
    urls = [
        "https://www.uchicago.edu/",
        "https://www.washington.edu/",
        "https://www.stanford.edu/",
        "https://und.edu/"
    ]

    with requests.Session() as session:
        scraped_data = {}
        for url in urls:
            content = scrape_website(session, url)
            if content:  # Only save content if scraping was successful
                scraped_data[url] = content       

        if not scraped_data:
            print("No data scraped successfully from any website.")
            return

        # Prompt the user for a query
        query = input("Enter a query to search in the scraped content: ").strip().lower()

        # Search for the query in the scraped data
        found_results = {}
        for url, content in scraped_data.items():
            if query in content.lower():
                found_results[url] = content

        # Display the results
        if found_results:
            print("\nQuery found in the following websites:")
            for url, content in found_results.items():
                print(f"\n--- Results from {url} ---")
                # Displaying a snippet around the query
                start_index = content.lower().find(query)
                snippet = content[max(0, start_index - 100):start_index + 100]
                print(f"...{snippet}...")
        else:
            print("\nNo results found for your query.")

if __name__ == "__main__":
    main()
