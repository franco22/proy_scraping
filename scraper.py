from urllib import response
import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.redgol.cl/'

XPATH_LINK_TO_ARTICLE = '//h2[@class="jsx-1119537696 card-title thumbnail-title"]/a/@href'
XPATH_TITLE = '//h1[@class="jsx-2954190014 article-title"]/text()'
XPATH_SUMMARY = '//h2[@class="jsx-1270612896 article-excerpt"]/p/text()'
XPATH_BODY = '//div[@class="jsx-1945861266 article-body"]/p/text()'

#pasa los elementos de una noticia a un archivo
def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
              
            try:           
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                #summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
   
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                #f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')   
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime('%d-%m-%Y')
            #print(links_to_notices)
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notices:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()
