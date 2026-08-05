import os
import django
import time
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client

client = Client()

urls = [
    '/',
    '/analytics/',
    '/countries/',
    '/map/',
    '/map/data/',
    '/reports/',
]

results = []
for u in urls:
    try:
        start = time.time()
        resp = client.get(u)
        elapsed = time.time() - start
        results.append((u, resp.status_code, round(elapsed, 3)))
    except Exception:
        results.append((u, 'EXC', traceback.format_exc()))

print('SMOKE TEST RESULTS')
for r in results:
    print(r)

# Also test exports (without downloading large data)
try:
    start = time.time()
    r = client.get('/export-csv/')
    print('/export-csv/', r.status_code, round(time.time()-start,3))
except Exception as e:
    print('/export-csv/ exception', e)

try:
    start = time.time()
    r = client.get('/export-excel/')
    print('/export-excel/', r.status_code, round(time.time()-start,3))
except Exception as e:
    print('/export-excel/ exception', e)

try:
    start = time.time()
    r = client.get('/export-pdf/')
    print('/export-pdf/', r.status_code, round(time.time()-start,3))
except Exception as e:
    print('/export-pdf/ exception', e)
