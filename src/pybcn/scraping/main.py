import bs4
import logging
import requests



HTTP_TIMEOUT = 15  # seconds


def get_mp3_link(article_url: str) -> str:
    try:
        page = requests.get(
            article_url,
            timeout=HTTP_TIMEOUT,
            allow_redirects=True,
        )

        soup = bs4.BeautifulSoup(page.content, 'html.parser')

        link_elem = soup.select_one("li.download > a")

        return link_elem['href'] if link_elem else ""

    except requests.RequestException:
        return ""


def scrape_this_american_life(year: int):

    root_url = f"https://www.thisamericanlife.org"
    year_url = f"{root_url}/archive?year={year}"

    try:
        page = requests.get(
            year_url,
            timeout=HTTP_TIMEOUT,
            allow_redirects=True,
        )

        soup = bs4.BeautifulSoup(page.content, 'html.parser')

        nodes_panel = soup.find('div', class_='nodes')
        if not nodes_panel:
            logging.warning("No nodes panel found")
            return

        articles = nodes_panel.find_all('article')
        if not articles:
            logging.warning("No articles found")
            return

        for article in articles:
            title_elem = article.find('h2')
            title = title_elem.text.strip() if title_elem else "[no-title]"
            summary_elem = article.find('div', class_='field-type-text-with-summary')
            summary = summary_elem.text.strip() if summary_elem else "[no-summary]"
            link_elem = title_elem.find('a') if title_elem else None
            article_link = (root_url + link_elem['href']) if link_elem else None
            mp3_link = get_mp3_link(article_link)
            print(f"Article:\n- Title: {title}\n- Summary: {summary}\n- Link: {article_link}\n- mp3: {mp3_link}")

    except requests.exceptions.RequestException:
        logging.exception("Unable to retrieve main web page")

def main():
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    scrape_this_american_life(2018)


if __name__ == '__main__':
    main()
