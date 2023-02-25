#!/usr/bin/env python3
# Generate globals.json for all MachXO2 devices
import json, subprocess, pathlib

if __name__ == '__main__':
    devices = json.load(open('devices.json', 'r'))
    for family, family_data in devices['families'].items():
        if family != 'MachXO2':
            continue

        print(family)

        for device in family_data['devices'].keys():
            print(f'  {device}')
            pathlib.Path(f'database/{family}/{device}').mkdir(parents=True, exist_ok=True)
            subprocess.run(['tools/gen_globals.py', device, f'database/{family}/{device}/globals.json'], check=True)
