import bs4
import logging
import requests


def main():
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    # TODO: scrape https://www.thisamericanlife.org/archive


if __name__ == '__main__':
    main()
