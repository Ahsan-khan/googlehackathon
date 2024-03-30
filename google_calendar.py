from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
import os.path

# Scopes required by the Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(start_time_str, end_time_str, summary, description=''):
    service = get_calendar_service()
    event_result = service.events().insert(calendarId='primary',
        body={
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_time_str, "timeZone": 'Your/Timezone'},
            "end": {"dateTime": end_time_str, "timeZone": 'Your/Timezone'},
            "conferenceData": {
                "createRequest": {"requestId": "sample123", "conferenceSolutionKey": {"type": "hangoutsMeet"}}
            },
            "reminders": {
                "useDefault": False,
                "overrides": [{"method": "email", "minutes": 24 * 60}, {"method": "popup", "minutes": 10}],
            },
        },
        conferenceDataVersion=1
    ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])
    print("Google Meet link: ", event_result['hangoutLink'])

# Example usage
create_event('2024-05-30T09:00:00', '2024-05-30T10:00:00', 'Test Meeting', 'This is a test description.')
