# Youtube2spotify

This will create a new Spotify playlist based on the videos you like on Youtube. 

## Getting Started

Download youtube2spotify.py and client_secret.json in a directory. 
Grant access to your Youtube and Spotify accounts.
Install the requiremets
Run the program

### Prerequisites

1. Setup access to your Spotify Account
```
* To obtain your client_id and client_secret - goto https://developer.spotify.com/dashboard/applications and create a 'New App'.
* In the app setting - Set redirect URL to 'http://example.com'.
* spotify_user_id is your spotify username.Go here to check 'https://www.spotify.com/sg-en/account/overview/'
```

2. Setup access to your Youtube Account
```
* Goto https://console.developers.google.com/apis/credentials?project=opnsese and setup new OAuth 2.0 client ID. Select Application Type - other
* Save client_id and client_secret in client_secret.json file (provided in the package)
* You may need to setup a new OAuth Consent Screen

```

### Installing 

```
pip3 install -r requirements.txt
```

### Running

```
cd /<your folder>
python3 youtube2spotify.py <client_id client_secret> <spotify_user_id>

```



## Acknowledgments

* Orignal idea - https://github.com/TheComeUpCode
