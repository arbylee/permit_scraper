# import ipdb
import os
import random
import sys
import time
import urllib2

from bs4 import BeautifulSoup


def csvify(tag):
    return '"' + tag.get_text().strip() + '"' + SEPARATOR

SEPARATOR = ','
URL_PREFIX = ('https://www.austintexas.gov/devreview/'
              'b_showpublicpermitfolderdetails.jsp?FolderRSN=')
OUTPUT_DIR = 'output'
START = 99997
END = 2800000


for claim in range(START, END):
    claim_dir = os.path.join(OUTPUT_DIR, str(claim))
    if os.path.exists(claim_dir):
        continue

    os.makedirs(claim_dir)
    req = urllib2.Request(URL_PREFIX + str(claim))

    response = urllib2.urlopen(req)

    data = response.read()

    formatted_data = BeautifulSoup(data)

    form_table = formatted_data.find(id='form_table')
    sub_tables = form_table.find_all(class_='sub_table')
    if not sub_tables:
        sys.stdout.write('.')
        os.rmdir(claim_dir)
        continue

    print "Processing claim: %d" % claim

    for idx, sub_table in enumerate(sub_tables):
        output_file = open(os.path.join(claim_dir, 'table' + str(idx)), 'w')
        trs = sub_table.find_all('tr')

        title_table = trs.pop(0)
        headers = title_table.find_all(['th', 'td'])

        for header in headers:
            output_file.write(csvify(header))

        output_file.write('\r\n')

        for tr in trs:
            tds = tr.find_all('td')
            for td in tds:
                if td.has_attr('colspan'):
                    continue
                output_file.write(csvify(td))

            output_file.write('\r\n')

        output_file.close()

    time.sleep(random.random())
    if claim % 10 == 0:
        time.sleep(random.randrange(3, 5))
