from bs4 import BeautifulSoup
import requests
from config import headers, params
from time import sleep

class Parser:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url, headers=headers, params=params)
        self.obj = BeautifulSoup(self.response.text, features='lxml')

    def _get_city(self, link):
        response = requests.get(link, headers=headers)
        obj = BeautifulSoup(response.text, features='lxml')
        if obj.find('span', {'data-qa': 'vacancy-view-raw-address'}) != None:
            city = obj.find('span', {'data-qa': 'vacancy-view-raw-address'})
        else:
            city = obj.find('p', {'data-qa': 'vacancy-view-location'})
        return city.text

    def _get_salary(self, link):
        response = requests.get(link, headers=headers)
        obj = BeautifulSoup(response.text, features='lxml')
        if obj.find('span', {'data-qa': 'vacancy-salary-compensation-type-undefined', 'class': 'bloko-header-section-2 bloko-header-section-2_lite'}) != None:
            salary = obj.find('span', {'data-qa': 'vacancy-salary-compensation-type-undefined', 'class': 'bloko-header-section-2 bloko-header-section-2_lite'})
        else:
            salary = obj.find('span', {'data-qa': 'vacancy-salary-compensation-type-net', 'class': 'bloko-header-section-2 bloko-header-section-2_lite'})
        return salary.text

    def _get_name(self, link):
        response = requests.get(link, headers=headers)
        obj = BeautifulSoup(response.text, features='lxml')
        name = obj.find('span', {'data-qa': 'bloko-header-2', 'class': 'bloko-header-section-2 bloko-header-section-2_lite'})
        return name.text

    def linkVacancy(self):
        linkVacancy = self.obj.findAll('a', {'class': 'serp-item__title', 'data-qa': 'serp-item__title', 'target': '_blank'})
        result = []
        count = 0
        for link in linkVacancy:
            sleep(0.5)
            count += 1
            url: str = link.attrs['href']
            city: str = self._get_city(url)
            salary: str = self._get_salary(url)
            name: str = self._get_name(url)
            result.append(
                {'№': count, 'info': {'link': url, 'name': name, 'city': city, 'salary': salary}}
            )
        return result

    def print_vacancy(self):
        vacancy = self.linkVacancy()
        for var in vacancy:
            print(var)
