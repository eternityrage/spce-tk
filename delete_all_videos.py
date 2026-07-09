import os, requests, time

token = os.environ['FACEBOOK_TOKEN']
pid = os.environ['PAGE_ID']

print(f'Deleting videos from page {pid}...')
url = f'https://graph.facebook.com/v20.0/{pid}/videos'
params = {'fields': 'id', 'access_token': token, 'limit': 100}
all_vids = []
while url:
    r = requests.get(url, params=params if '?' not in url else None)
    data = r.json()
    all_vids.extend(data.get('data', []))
    url = data.get('paging', {}).get('next')
    params = None

print(f'Total videos: {len(all_vids)}')
success = 0
failed = 0
for v in all_vids:
    r = requests.delete(f'https://graph.facebook.com/v20.0/{v["id"]}', params={'access_token': token})
    if r.status_code == 200:
        success += 1
    else:
        failed += 1
    time.sleep(0.3)

print(f'Deleted: {success} | Failed: {failed}')
if failed > 0:
    exit(1)
