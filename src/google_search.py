import os
from googleapiclient.discovery import build

api_key = os.environ['GOOGLE_API_KEY']
cse_id = os.environ['GOOGLE_CSE_ID']


def google_search(search_term, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

