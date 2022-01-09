from zerionAPI import IFB
from pprint import pprint
import json
import os
import requests
import shutil
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def exportImages(api, profile_id, page_id, isRecursive=False, directory = '.'):
    print(
        'Getting page...',
        result := api.Pages('GET', profile_id, page_id)
    )

    if result.status_code == 200:
        count = 0

        page = result.response

        try:
            directory = f'{directory}/{page["name"]}'
            os.makedirs(directory, exist_ok=True)
        except FileExistsError as e:
            print(e)
            pass

        elements_field_grammar = 'name,data_type((="11")|(="18")|(="28")),data_size' if isRecursive else 'name,data_type((="11")|(="28"))'

        print(
            'Getting elements...',
            result := api.Elements('GET', profile_id, page['id'], params={'fields': elements_field_grammar})
        )

        if result.status_code == 200 and len(result.response) > 0:
            elements = result.response
            image_elements = [element for element in elements if element['data_type'] in (11, 28)]
            subform_elements = [element for element in elements if element['data_type'] == 18]

            # Image Element Loop
            if len(image_elements) > 0:
                print('Getting records...')
                result = api.Records('GET', profile_id, page['id'], params={'fields': ','.join([e['name'] for e in image_elements])})

                if result.status_code == 200 and len(result.response) > 0:
                    records = result.response
                    total = int(result.headers.get('Total-Count'))

                    print(f'Retrieved {len(records)}/{total} records...')
                    while len(records) < total:
                        result = api.Records('GET', profile_id, page['id'], params={'fields': ','.join([e['name'] for e in image_elements]), 'offset': len(records)})
                        if result.status_code == 200 and len(result.response) > 0:
                            records += result.response

                    for record in records:
                        record_id = record['id']
                        elements = {key: record[key] for key in record if key != 'id' and record[key] != None}
                        for element in elements:
                            r = requests.get(record[element], verify=False, stream=True)
                            r.raw.decode_content = True

                            filename = f'{record_id}_{element}.{record[element].split(".")[-1]}'
                            filepath = f'{directory}/{filename}' 
                            with open(filepath, 'wb') as f:
                                print(f'Exporting <{record[element]}> as "{filepath}"')
                                shutil.copyfileobj(r.raw, f)
                else:
                    print('No records found...')

            else:
                print('No image elements found...')

            # Subform Element Loop
            if isRecursive and len(subform_elements) > 0:
                for element in subform_elements:
                    print(f'Recursing into {element["name"]}...')
                    count += exportImages(api, profile_id, element['data_size'], isRecursive, directory=directory)
            
        else:
            print('No image elements found...')
            return 0
    else:
        print('Page not found...')
        return 0


if __name__ == "__main__":
    print('Not directly accessible')
    exit()