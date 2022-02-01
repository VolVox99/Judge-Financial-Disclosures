try:
    with open('AUTH_TOKEN.txt') as f:
        token = f.read().strip()

except:
    print('ERROR: Auth Token must be placed into auth_token.txt')