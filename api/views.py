from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
import googleapiclient.discovery

CREDENTIALS_FILE = 'credentials.json'
REDIRECT_URL = 'https://convinbackendtask.malliditarun.repl.co/rest/v1/calendar/redirect'


@api_view(['GET'])
def GoogleCalendarInitView(request):
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri=REDIRECT_URL)
    auth_url, state = flow.authorization_url(prompt='consent')
    request.session['state'] = state

    return redirect(auth_url)


@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    scopes = ['https://www.googleapis.com/auth/calendar']
    state = request.session.get('state')

    flow = Flow.from_client_secrets_file(CREDENTIALS_FILE,
                                         scopes,
                                         state=state,
                                         redirect_uri=REDIRECT_URL)

    code = request.query_params.get('code')
    flow.fetch_token(code=code)

    credentials = flow.credentials
    service = googleapiclient.discovery.build('calendar',
                                              'v3',
                                              credentials=credentials,
                                              static_discovery=False)
    events_result = service.events().list(calendarId='primary',
                                          maxResults=10,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return Response(events)
