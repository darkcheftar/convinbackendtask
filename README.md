## Google Calendar Integration with Django RestFramework

Install Dependecies

- Endpoints:
```
/rest/v1/calendar/init/ -> GoogleCalendarInitView()
```
Redirects to Google OAUTH2 Page


```
/rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView()
```
- Gets access code
- Uses it to display calendar events

## Important
``` 
Credentials.json file has to be populated before executing the project from client secret from Google Developer Console
```