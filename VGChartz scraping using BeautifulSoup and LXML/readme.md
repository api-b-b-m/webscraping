# VGChartz scraping using BeautifulSoup and LXML

## Overview
VGChartz is a website that tracks video game sales data. It provides weekly sales figures for console hardware and software by region. The site also includes news, reviews, forums, and a database of games.

VGChartz is known for its detailed tracking of sales data, which is often used by industry analysts and gamers alike. However, it's important to note that the data provided by VGChartz is not always official and can sometimes be inaccurate. This is because the site relies on a variety of sources, including retailer reports and estimates, to compile its data.   

Despite this, VGChartz remains a popular resource for those who are interested in tracking video game sales trends.

This project is a Python-based web scraper designed to extract detailed video game sales data from VGChartz. The script automates the process of navigating through multiple pages, collecting relevant data and exporting it to a CSV file for analysis.

## Requirements

- Python 3.11.5
- Bs4 (version 0.0.2)
- Lxml (version 5.3.0)
- Requests (version 2.32.3)
- Tqdm (version 4.67.0)
- Pandas (version 2.2.2)

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/api-b-b-m/webscraping.git
    ```

2. Navigate to the project directory:

    ```bash
    cd "webscraping/VGChartz scraping using BeautifulSoup and LXML"
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the main script:

    ```bash
    python vgchartz_scrape.py
    ```

## Result

- The scraped data will be saved to a CSV file named vgchartz_scrape_output.csv in the current directory.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.en.html).
