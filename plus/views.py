from django.shortcuts import render

# Create your views here.
import os
import logging
import httplib2
from django.contrib.auth.models import User
from apiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from plus.models import CredentialsModel
from studentWebcamp import settings
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage
from django.core.context_processors import request

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json')

'''
Create a Flow from a clientsecrets file.

Will create the right kind of Flow based on the contents of the clientsecrets
file or will raise InvalidClientSecretsError for unknown types of Flows.

Args:
  filename: string, File name of client secrets.
  scope: string or iterable of strings, scope(s) to request.
  redirect_uri: string, Either the string 'urn:ietf:wg:oauth:2.0:oob' for
    a non-web-based application, or a URI that handles the callback from
    the authorization server.
  message: string, A friendly string to display to the user if the
    clientsecrets file is missing or invalid. If message is provided then
    sys.exit will be called in the case of an error. If message in not
    provided then clientsecrets.InvalidClientSecretsError will be raised.
  cache: An optional cache service client that implements get() and set()
    methods. See clientsecrets.loadfile() for details.

Returns:
  A Flow object.

Raises:
  UnknownClientSecretsFlowError if the file describes an unknown kind of Flow.
  clientsecrets.InvalidClientSecretsError if the clientsecrets file is
    invalid.
'''
FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope=['https://www.googleapis.com/auth/plus.me', 'https://www.googleapis.com/auth/calendar'],
    redirect_uri='http://localhost:8000/oauth2callback')


# @login_required
def index(request):
    lenka = User.objects.get(username='lenka')
    storage = Storage(CredentialsModel, 'id', lenka, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("plus", "v1", http=http)
        activities = service.activities()
        activitylist = activities.list(collection='public',
                                   userId='me').execute()
        logging.info(activitylist)
    '''
    render_to_response(template_name[, dictionary][, context_instance][, content_type])
    Renders a given template with a given context dictionary and returns an HttpResponse object with that rendered text.
    '''
    return render_to_response('plus/welcome.html', {
                'activitylist': activitylist, 'user':lenka
                })

def cal(request):
    lenka = User.objects.get(username='lenka')
    '''
    @storage - Storage class object
    Constructor for Storage __init__(self, model_class, key_name, key_value, property_name) 
    Store and retrieve a single credential to and from
    the datastore.
    
    This Storage helper presumes the Credentials
    have been stored as a CredenialsField
    on a db model class.
    http://google-api-python-client.googlecode.com/hg/docs/epy/oauth2client.django_orm.Storage-class.html#locked_get
    '''
    storage = Storage(CredentialsModel, 'id', lenka, 'credential')
    '''
    @credential - storage method 
    Retrieve credential.
    The Storage lock must *not* be held when this is called.
    Returns:
      oauth2client.client.Credentials
    '''
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   lenka)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        '''
        @service - apiclient.discovery.built function
        Construct a Resource for interacting with an API.
        Construct a Resource object for interacting with an API. The serviceName and
        version are the names from the Discovery service.
        Args:
          serviceName: string, name of the service.
          version: string, the version of the service.
          http: httplib2.Http, An instance of httplib2.Http or something that acts
            like it that HTTP requests will be made through.
          discoveryServiceUrl: string, a URI Template that points to the location of
            the discovery service. It should have two parameters {api} and
            {apiVersion} that when filled in produce an absolute URI to the discovery
            document for that service.
          developerKey: string, key obtained from
            https://code.google.com/apis/console.
          model: apiclient.Model, converts to and from the wire format.
          requestBuilder: apiclient.http.HttpRequest, encapsulator for an HTTP
            request.
        
        Returns:
          A Resource object with methods for interacting with the service.
        https://google-api-python-client.googlecode.com/hg/docs/epy/apiclient.discovery-module.html
        '''
        service = build("calendar", "v3", http=http)
        '''
        @events - Returns the events Resource.
        https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/
        '''
        events = service.events()
        '''
        @eventList - function list from events Obj
        list(calendarId=*, orderBy=None, showHiddenInvitations=None, timeMin=None, privateExtendedProperty=None, pageToken=None, updatedMin=None, singleEvents=None, alwaysIncludeEmail=None, showDeleted=None, sharedExtendedProperty=None, maxAttendees=None, syncToken=None, iCalUID=None, maxResults=None, timeMax=None, q=None, timeZone=None)
        Returns events on the specified calendar.
        https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/calendar_v3.events.html#list
        '''
        eventList = events.list(calendarId='primary').execute()
        logging.info(eventList)
    '''
    render_to_response(template_name[, dictionary][, context_instance][, content_type])
    Renders a given template with a given context dictionary and returns an HttpResponse object with that rendered text.
    '''
    return render_to_response('plus/cldr.html', {
                'eventList': eventList, 'user':lenka
                })

def cal2(request):
    api_key = 'AIzaSyDbNTPNlyOgZDUQCF2pfDQ1YOGnxNiWIWI'
    service = build("calendar", "v3", developerKey=api_key)
    events = service.events()
    eventList = events.list(calendarId='85obn2bj4hvdj0dsd2vim4ibv4@group.calendar.google.com').execute()
    logging.info(eventList)
    return render_to_response('plus/cldr.html', {
                'eventList': eventList
                })

def yt(request):
    api_key = 'AIzaSyDbNTPNlyOgZDUQCF2pfDQ1YOGnxNiWIWI'
    service = build("youtube", "v3", developerKey=api_key)
    
    pLists = service.playlistItems()
    
    pListItems = pLists.list(playlistId='PLO33wg5Q-Gf3ceQEC6HMAIMCOhhnxGzEE', part="snippet",
            maxResults=50).execute()
    print(pListItems)
    logging.info(pListItems)
    return render_to_response('plus/yt.html', {
                'pListItems': pListItems
                })
@login_required
def auth_return(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'],
                                 request.user):
        return  HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.REQUEST)
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/")