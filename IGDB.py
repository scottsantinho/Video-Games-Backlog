import requests
import json

# Your client ID and secret from Twitch API
id = "4jz82v49yw96o08kffd53bqw53bl4s" # Enter your own client ID
secret = "elidvbr5mb0d76v4gfemmyfww4mhxw" # Enter your own client secret

# Authenticating with Twitch API
url = "https://id.twitch.tv/oauth2/token"
params = {
    "client_id": id,
    "client_secret": secret,
    "grant_type": "client_credentials"
}

response = requests.post(url, data=params)

if response.status_code == 200:
    print("Authentication successful")
    access_token = response.json().get("access_token")
    print(f"Access Token: {access_token}")
else:
    print(f"Failed to authenticate: {response.status_code}")
    print(response.json())

# Create a new IGDBWrapper object and give it your Client-ID and App Access Token
from igdb.wrapper import IGDBWrapper
wrapper = IGDBWrapper(id, access_token)

# Search for games with the some keywords
search_input = "Assassin's Creed"
query = f'fields *; offset 0; search "{search_input}"; limit 100;'
byte_array = wrapper.api_request('search', query)

# Parse the JSON response
json_response = json.loads(byte_array.decode('utf-8'))

# Print the parsed JSON response
for game_element in json_response:
    print(game_element)