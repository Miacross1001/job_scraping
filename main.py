import pprint
from scraper import Parser

HOST = 'https://spb.hh.ru/search/vacancy/'

if '__main__' == __name__:
    parser = Parser(HOST)
    parser.print_vacancy()