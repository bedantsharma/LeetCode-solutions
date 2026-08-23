import requests
from bs4 import BeautifulSoup


def print_secret_message(doc_url):
    """
    Fetches a published Google Doc containing a table of (x, character, y)
    grid data and prints the grid, revealing a hidden uppercase-letter message.
    """
    # Fetch the published HTML page
    response = requests.get(doc_url)
    response.raise_for_status()

    # Parse the HTML table
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    grid = {}
    max_x = 0
    max_y = 0

    # Skip the header row, read each data row
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) < 3:
            continue
        x = int(cells[0].get_text(strip=True))
        char = cells[1].get_text(strip=True)
        y = int(cells[2].get_text(strip=True))

        grid[(x, y)] = char
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    # Build and print the grid, row by row (y=0 at top, x=0 at left)
    for y in range(max_y + 1):
        line = ''.join(grid.get((x, y), ' ') for x in range(max_x + 1))
        print(line)


if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
    print_secret_message(url)
