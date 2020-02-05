import wikipedia # pip install wikipedia for this to work
from googleapiclient.discovery import build # pip instal google-api-python-client
from google_auth_oauthlib.flow import InstalledAppFlow # pip instal google-auth-httplib2 google-auth-oauthlib

def init():
    query = get_user_input()
    text = search_in_wikipedia(query)
    service = authenticate()
    doc_id = create_document(service, query)
    add_text_to_doc(service, doc_id, query, text)
    style_text(service, doc_id, query, text)
    print('Done!')


def get_user_input():
    return input('Query: ')

def search_in_wikipedia(query):
    return wikipedia.summary(query)

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(
        './credentials.json',
        scopes='https://www.googleapis.com/auth/documents'
    )

    flow.run_local_server()
    credentials = flow.credentials

    return build('docs', 'v1', credentials=credentials)

def create_document(service, query):
    response = service.documents().create(body={'title': query}).execute()
    return response.get('documentId')

def add_text_to_doc(service, doc_id, query, text):
    requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1
                    },
                    'text': text
                },
            },
            {
                'insertText': {
                    'location': {
                        'index': 1
                    },
                    'text': f'{query}\n'
                }
            }
    ]

    service.documents().batchUpdate(
        documentId = doc_id, body={'requests': requests}
    ).execute()

def style_text(service, doc_id, query, text):
    requests = [
        {
            'updateParagraphStyle': {
                'paragraphStyle': {
                    'namedStyleType': 'NORMAL_TEXT',
                    'alignment': 'JUSTIFIED',
                    'indentFirstLine': {
                        'magnitude': 36,
                        'unit': 'PT'
                    },
                    'lineSpacing': 150
                },
                'fields': '*',
                'range': {
                    'startIndex': len(query) + 1,
                    'endIndex': len(query) + len(text) + 2
                }
            }
        },
        {
            'updateParagraphStyle': {
                'paragraphStyle': {
                    'namedStyleType': 'TITLE',
                    'alignment': 'CENTER'
                },
                'fields': '*',
                'range': {
                    'startIndex': 1,
                    'endIndex': len(query) + 1
                }
            }
        },
        {
            'updateTextStyle': {
                'textStyle': {
                    'fontSize': {
                        'magnitude': 12,
                        'unit': 'PT'
                    }
                },
                'fields': '*',
                'range': {
                    'startIndex': len(query) + 1,
                    'endIndex': len(query) + len(text) + 2
                }
            }
        }
    ]

    service.documents().batchUpdate(
        documentId = doc_id, body={'requests': requests}
    ).execute()

init()
