import urllib.request, json, sys
base = 'http://127.0.0.1:5000'
# create test account
try:
    req = urllib.request.Request(base + '/auth/create-test-account', data=b'{}', headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read().decode())
except Exception as e:
    print('ERROR creating test account:', e)
    sys.exit(1)

if not resp.get('success'):
    print('Create test account failed:', resp)
    sys.exit(1)

token = resp.get('token')
print('TEST_ACCOUNT_TOKEN:', token)

# prepare profile payload
b64 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=='
payload = {
    'first_name': 'Auto',
    'last_name': 'Tester',
    'description': 'Profile test from automated script',
    'avatar': b64
}
body = json.dumps(payload).encode()
req2 = urllib.request.Request(base + '/api/user', data=body, headers={'Content-Type':'application/json', 'Authorization': f'Bearer {token}'}, method='POST')
try:
    with urllib.request.urlopen(req2, timeout=30) as r:
        resp2 = json.loads(r.read().decode())
        print('PROFILE RESPONSE:', json.dumps(resp2))
except urllib.error.HTTPError as e:
    print('HTTPError:', e.code, e.read().decode())
except Exception as e:
    print('ERROR posting profile:', e)
    sys.exit(1)
