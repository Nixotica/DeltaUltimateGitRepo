import requests

IDENTIFIER = "3a241c5daa981d2c8175"
SECRET = "f4d8c6f492cace60cabb6bbe3e7465e160712ceb"

if __name__ == "__main__":
    # Post a GET request using the TM OAuth credentials
    url = "https://api.trackmania.com/oauth/authorize" \
          "?response_type=code" \
          "&client_id=3a241c5daa981d2c8175" \
          "&redirect_uri=https://competition.trackmania.nadeo.club/api/competitions/LID-COMP-xqj4dbhjvt0ljml"

    r = requests.get(url=url)

    print(r.content)