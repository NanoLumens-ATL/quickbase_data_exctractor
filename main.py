import requests
from dotenv import load_dotenv
from xlsxwriter import Workbook
import pandas as pd
import json
import os

load_dotenv()

headers = {
    'QB-Realm-Hostname': os.getenv('domain'),
    'Authorization': os.getenv('token')
}
print(headers)


def main(app, fields, start, end):
    body = {
        'from': 'bmb347gyc',
        'where': '{1.BF.\'1/1/2023\'}AND{1.AF.\'1/1/2022\'}',
        'select': [1, 2, 3, 4, 5, 6]
    }

    response = requests.post(
        "https://api.quickbase.com/v1/records/query",
        headers=headers,
        json=body
    )

    rjson = response.json()
    data = {}

    for i in range(len(rjson['data'])):
        for field in iter(rjson['fields']):
            if data.get(i) is None:
                data[i] = dict()
                data[i][field['label']] = rjson['data'][i][str(field['id'])]['value']
            else:
                data[i][field['label']] = rjson['data'][i][str(field['id'])]['value']

    df = pd.DataFrame(data)
    df = df.transpose()

    writer = pd.ExcelWriter("./test.xlsx", engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet 1')
    writer.close()


if __name__ == '__main__':
    # find_field_id('')
    main('bmb347gyc', [1, 2, 3, 4, 5], '1/1/2023', '1/1/2022')
