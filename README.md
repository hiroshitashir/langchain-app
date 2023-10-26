# langchain-app

## Credentials
For integration, you would need the following environment variables:

```
# For github_repo_*.py
export GITHUB_TOKEN=<github token>
export OPENAI_API_KEY=<openai key>

# For spotify_*.py
export SPOTIPY_CLIENT_ID='<client id>'
export SPOTIPY_CLIENT_SECRET='<client secret>'
export SPOTIPY_REDIRECT_URI='<direct uri>'
```

For Google (Gmail, Calendar and Youtube) integration, you need `credential.json`. See [here](https://developers.google.com/workspace/guides/create-credentials) for more info.


## To run
1. Run `poetry shell`
2. Run `poetry install`
3. Run `python <script name>.py`

