from csv import writer
from bs4 import BeautifulSoup
import requests

url = 'https://www.icliniq.com/search/online-doctors-directory'
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
docList = soup.findAll('div', 'ic-card-shadow mb-4')

with open('docinfo.csv', 'w', encoding='utf8', newline='') as f:
    thewriter = writer(f)
    header = ['Name', 'profile Link', 'Image', 'Degree', 'Experience', 'Specialization',
              'Price: Query', 'Price: Phone/Video', 'Consulting Languages', 'Experience']
    thewriter.writerow(header)

    for doc in docList:
        name = doc.find('h3', 'case-study').text.replace('\n',
                                                         '').replace('.,', '')
        profileURL = doc.find('h3', 'case-study').find('a')['href']
        imageSrc = doc.find(
            'div', 'media-left mr-3').find('a').find('img')['src']
        degree = doc.find(
            'div', 'media-body').find('p').text.split('Experience')[0].strip()
        experience = doc.find('div', 'media-body').find('p',
                                                        'm-0').find('span', 'font-weight-bold').text.replace('\n', '')
        spec = doc.find('div', 'mb-2').text.replace('\n', '')
        query = doc.find('div', 'media-right').find('div',
                                                    'align-center').findAll('p')[1].find('span', 'font-weight-bold').text
        phoneVideo = doc.find('div', 'media-right').find('div',
                                                         'align-center').findAll('p')[2].find('span', 'font-weight-bold').text
        languages = doc.find('div', 'media-right').find('div',
                                                        'align-center').findAll('p')[3].find('span', 'font-weight-bold').text
        rating = 'N/A' if doc.find('div', 'overall-rating') == None else doc.find(
            'div', 'overall-rating').text.replace('\n', '')

        info = [name, profileURL, imageSrc, degree, experience,
                spec, query, phoneVideo, languages, rating]
        thewriter.writerow(info)
