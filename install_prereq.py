# -*- coding: utf-8 -*-

import sys, subprocess

prereqs = [
    'discord',
    'pillow',
    'pymysql',
    'aiohttp',
    'py-fumen',
    'python-dotenv'
]

for p in prereqs:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', p])