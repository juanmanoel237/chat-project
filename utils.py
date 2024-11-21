# utils.py
import os
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Authentification et accès aux fichiers Google Drive
def authenticate_google_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

# Recherche des documents dans Google Drive
def get_drive_documents(query):
    service = authenticate_google_drive()
    query = query.replace("'", "\\'")  # Échappe les apostrophes
    results = service.files().list(q=f"name contains '{query}'", fields="files(name, id)").execute()
    files = results.get('files', [])
    return [file['name'] for file in files]

# Recherche web via Google Custom Search
def search_google(query):
    API_KEY = "AIzaSyACo927KZ6zkUZn2zbMJNd1mEHvFFAUFxQ"  # Remplacez par votre clé API
    SEARCH_ENGINE_ID = "669cb7720de434b79"  # Remplacez par votre ID moteur
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
    response = requests.get(url)
    results = response.json().get('items', [])
    return [item['snippet'] for item in results[:3]]

# Récupération du contexte en fonction du type de recherche
def retrieve_context(query, search_type='drive'):
    contexts = []
    
    if search_type in ['drive', 'all']:
        drive_docs = get_drive_documents(query)
        contexts.extend(drive_docs)
    
    if search_type in ['web', 'all']:
        web_results = search_google(query)
        contexts.extend(web_results)
    
    return contexts[:5]  # Limiter à 5 résultats
