# %%
import os
import requests
import json
import csv
import logging

# %%
logging.basicConfig(filename='api-to-csv.log', encoding='utf-8', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)


output_filename = 'data.csv'


with open(output_filename, 'w', newline='') as csv_file:

    limit = 500
    offset = 0

    while(1):

        try:

            url = 'https://connection.keboola.com/v2/storage/files?limit='+ str(limit) +'&offset=' + str(offset) + '&showExpired=true'

            r = requests.get(url, headers={"X-StorageApi-Token":os.environ['X-Storage-Token']})

            data = json.loads(r.text)

            logging.info(offset)


            if len(data) > 0:
                offset += limit


                if not csv_file.tell():
                    csv_writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
                    csv_writer.writeheader()
                    

                for row in data:
                    csv_writer.writerow(row)

                
            else:
                break

        except Exception as e:
            logging.error('Loop:\t' + str(e))



