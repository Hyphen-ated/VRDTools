# VRD Tools

These are some python 3 tools I wrote to help manage stuff related to running MTG Vintage Rotisserie drafts, as well as
calculating statistics for them. It's not written to really be usable by anyone but me, but if you would like to
look at my code, here it is.


## Setup:

```sh
pip3 install unidecode google-api-python-client google_auth_oauthlib requests
```

## Usage:

Run `update_scryfall_default_cards.py` before anything else to get the latest scryfall data and upload it to the [stats sheet](https://docs.google.com/spreadsheets/d/12LKNtBof-FTxO6Zyzrv8MN-2AEexw5aHV_YnlwD46WM/edit#gid=997264821).

Run `update_gsheets.py` to pull down new raw draft data, analyze it, and upload it back to the sheet.

If a card picked in a VRD is later banned in vintage, the name of that card should be put in `/cards-later-banned-in-vintage.txt`.


## Generating list of legal VRD cards

Save the `Default Cards` from [Scryfall's bulk data](https://scryfall.com/docs/api/bulk-data) as `/input/scryfall-default-cards.json`.

Run `python3 list_vintage_cards.py`

See the finished output in `/output/vintage_cards.txt`. If you want to use it in Google Sheets, copy-paste it into the `engine` tab and add `'` before `+2 Mace` to make Google Sheets happy.
