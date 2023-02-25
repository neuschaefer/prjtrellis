#!/usr/bin/env python3
# Download Lattice pinout CSV files and convert them to the corresponding iodb.json files.
import requests, subprocess, tempfile, pathlib

resources = [
        # TODO: Add ECP5 entries

        {
            "family": "MachXO2",
            "devices": [ "LCMXO2-256HC", "LCMXO2-256ZE" ],
            "url": "https://www.latticesemi.com/view_document?document_id=39443",
        },
        {
            "family": "MachXO2",
            "devices": [ "LCMXO2-640HC", "LCMXO2-640ZE" ],
            "url": "https://www.latticesemi.com/view_document?document_id=42528",
        },
        {
            "family": "MachXO2",
            "devices": [ ], #"LCMXO2-640UHC" ],
            "url": "https://www.latticesemi.com/view_document?document_id=39438",
        },
        {
            "family": "MachXO2",
            "devices": [ "LCMXO2-1200HC", "LCMXO2-1200ZE" ],
            "url": "https://www.latticesemi.com/view_document?document_id=39442",
        },
        {
            "family": "MachXO2",
            "devices": [ ], #"LCMXO2-1200UHC" ],
            "url": "https://www.latticesemi.com/view_document?document_id=42567",
        },
        {
            "family": "MachXO2",
            "devices": [ "LCMXO2-2000HC", "LCMXO2-2000ZE", ], # "LCMXO2-2000HE" ],
            "url": "https://www.latticesemi.com/view_document?document_id=42568",
        },
        {
            "family": "MachXO2",
            "devices": [ ], #"LCMXO2-2000UHC", "LCMXO2-2000UHE" ],
            "url": "https://www.latticesemi.com/view_document?document_id=42570",
        },
        {
            "family": "MachXO2",
            "devices": [ "LCMXO2-4000HC", "LCMXO2-4000ZE", ], # "LCMXO2-4000HE" ],
            "url": "https://www.latticesemi.com/view_document?document_id=42571",
        },
        {
            "family": "MachXO2",
            "devices": [ "LCMXO2-7000HC", "LCMXO2-7000ZE", ], #"LCMXO2-7000HE" ],
            "url": "https://www.latticesemi.com/view_document?document_id=42572",
        },
]

def fetch(url):
    #url = 'https://web.archive.org/' + url
    r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
    assert r.status_code == 200
    return r.text

def get_packages(text):
    for l in text.splitlines():
        if l.startswith('PAD'):
            return l.split(',')[8:]

if __name__ == '__main__':
    for res in resources:
        family = res['family']
        devices = res['devices']
        url = res['url']

        print(f'Downloading {url}...')
        text = fetch(url)
        print(f'  Packages: {get_packages(text)}')

        with tempfile.NamedTemporaryFile(mode='w', prefix='trellis-', suffix='.csv') as tmp:
            tmp.write(text)
            tmp.flush()

            for dev in devices:
                # Ignore some packages that we currently don't care about
                if 'UHC' in dev or 'HE' in dev:
                    continue

                print(f'  Converting pinout for {dev}')
                pathlib.Path(f'database/{family}/{dev}').mkdir(parents=True, exist_ok=True)
                subprocess.run(['tools/read_pinout.py', dev, tmp.name, f'database/{family}/{dev}/iodb.json'], check=True)
