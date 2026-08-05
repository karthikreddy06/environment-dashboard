from django.test import Client
import time, traceback
from django.conf import settings

# Remove optional middleware that may not be available in this environment (eg. whitenoise)
mw = list(getattr(settings, 'MIDDLEWARE', []))
filtered = [m for m in mw if not m.startswith('whitenoise.')]
settings.MIDDLEWARE = filtered

client = Client()

urls = ['/', '/analytics/', '/countries/', '/map/', '/map/data/', '/reports/']
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

# Exports
for ex in ['/export-csv/', '/export-excel/', '/export-pdf/']:
    try:
        start = time.time()
        r = client.get(ex)
        print(ex, r.status_code, round(time.time()-start,3))
    except Exception as e:
        print(ex, 'exception', e)
