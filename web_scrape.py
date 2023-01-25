import pandas as pd
import numpy as np

import requests
import bs4 as BeautifulSoup



state_url_dict = {
    "DC" : "https://mychildcare.dc.gov/Home/SearchFacilities"
}
facility_url = "https://mychildcare.dc.gov/MychildCare/FacilityProfile?FacilityId="


def generate_soup(url):
    response = requests.get(url)
    url_content = response.content
    soup = BeautifulSoup.BeautifulSoup(url_content, 'html.parser')
    return soup

if __name__ == '__main__':
    print("Start scraping...")

    # get employed persons data url_csv
    response = requests.get(state_url_dict['DC'])
    # add headers
    # response = requests.get(url, headers=headers)
    url_content = response.content
    # get state county data url_geo
    soup = BeautifulSoup.BeautifulSoup(url_content, 'html.parser')

    # get all facility names
    all_a = list(
        soup
        .body
        .div
        .find_next_sibling('div')
        .find_all('a', {"class" : "ProximaSoft-Semibold"})
    )

    daycare_names = [list(a.children)[0]for a in all_a]
    daycare_ids = [a['id'][5:] for a in all_a]
    daycare_capacity = []


    for idx, daycare_id in enumerate(daycare_ids):
        print(f'scraping capacity for {daycare_id}, {idx+1} / {len(daycare_ids)}')

        soup = generate_soup(facility_url + daycare_id)

        capacity = list(
            soup
            .body
            .div
            .find_next_sibling('div')
            .div
            .div
            .find_next_sibling('div')
            .table
            .tr
            .find_next_sibling('tr')
            .find_next_sibling('tr')
            .td
            .find_next_sibling('td')
            .find_next_sibling('td')
            .find_next_sibling('td')
            .span
            .find_next_sibling('span')
            .children)[0]
        daycare_capacity.append(capacity)


    # create pandas dataframe and sae
    d = {
        'facility_name' : daycare_names,
        'facility_id' : daycare_id, 
        'facility_capacity' : daycare_capacity
    }
    df = pd.DataFrame(data=d).set_index('facility_id')

    df.to_csv('dc_daycare_facility.csv')
