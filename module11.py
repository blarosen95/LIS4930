import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import re


def get_frame():
    return pd.read_excel('COVID19_03242020_ByCounty.xlsx', index_col=None)


df = get_frame()

max_cases_all = df.loc[df['CasesAll'].idxmax()]
print(max_cases_all[['COUNTYNAME', 'CasesAll']].head())
print()

top_3_cases = df.nlargest(3, 'CasesAll')
with plt.xkcd():
    plt.bar(top_3_cases['COUNTYNAME'], top_3_cases['CasesAll'], color='dimgray')
    plt.title('Top 3 Florida Counties for COVID-19 (March 24th, 2020)')
    plt.xlabel('County Name')
    plt.ylabel('Confirmed Cases')
    plt.show()
    pass
plt.close()

no_cases = df.loc[df['CasesAll'] == 0]
print(f'As of March 24th, 2020, there were {len(no_cases)} counties with 0 confirmed cases of COVID-19')
print()


def get_paragraph(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup.findAll('p')[2]


paragraph = get_paragraph('https://en.wikipedia.org/wiki/Coronavirus_disease_2019')
pattern = r'As of .+ recovered\.'
paragraph = str(paragraph.get_text())
match = re.search(pattern, paragraph)
figure = match.group(0)
figure = re.sub(r'\[\d+\]', '', figure)
figure = re.sub(r'\. ', '.\n', figure)
print(figure)
