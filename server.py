import web
import requests
import dropbox
import httplib2

from requests.auth import HTTPBasicAuth
from web.wsgiserver import CherryPyWSGIServer
from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build
from apiclient import errors
from functii import *
from apiclient.http import MediaFileUpload

CherryPyWSGIServer.ssl_certificate = "/etc/ssl/certs/ssl-cert-snakeoil.pem"
CherryPyWSGIServer.ssl_private_key = "/etc/ssl/private/ssl-cert-snakeoil.key"

urls = (
  '/googleauth', 'googleauth',
  '/googleauthcallback', 'googleauthcallback',
  '/listfiles', 'listfiles',
  '/testing', 'testing',
  '/setup', 'setup',
  '/allfiles', 'liststorage',
  '/download', 'download',
  '/upload', 'upload',
  '/(.*)', 'hello',
)

render = web.template.render('templates/')

web.config.debug = False

app = web.application(urls, globals())

app_key = "egdmfyi59f5o2hg";
app_secret = "jibv7nuqzuhd5aj";

session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={})

uploads = {}

class hello:        
  def GET(self, name):

    data = web.input(code=None)

    flow = dropbox.client.DropboxOAuth2Flow(app_key, app_secret, "https://mangocloud.me:80/", session, "dd")

    if not name:
      name = 'World'

    if data.code:
      url = "https://api.dropbox.com/1/oauth2/token"

      access_token, user_id, state_url = flow.finish({"state": session.dd, "code": data.code})

      session.access_token = access_token
      session.user_id = user_id

      web.seeother('/listfiles')
    else:
      return flow.start()

    return 'Hello, ' + name + '!'

class listfiles:
  def GET(self):
    client = dropbox.client.DropboxClient(session.access_token)
    return client.metadata('/')

class liststorage:
  def GET(self):
    return list_storage("testUser")

class googleauth:
  def GET(self):
    # Authorize server-to-server interactions from Google Compute Engine.

    flow = flow_from_clientsecrets('./client_secrets.json',
                               scope='https://www.googleapis.com/auth/drive',
                               redirect_uri='https://mangocloud.me:80/googleauthcallback')

    service = build('drive', 'v2')

    def retrieve_all_files(service):
      result = []
      page_token = None
      while True:
        try:
          param = {}
          if page_token:
            param['pageToken'] = page_token
            files = service.files().list(**param).execute()

            result.extend(files['items'])
            page_token = files.get('nextPageToken')

            break

        except errors.HttpError, error:
          print 'An error occurred: %s' % error
          break
      return result

      if 'authed' in session:
        http = httplib2.Http()
        credentials = session.credentials;
        http = credentials.authorize(http)
        service = build('drive', 'v2', http)

        return retrieve_all_files(service)
      else:
        uri = flow.step1_get_authorize_url()
        return uri

class googleauthcallback:
  def GET(self):
    flow = flow_from_clientsecrets('./client_secrets.json', scope='https://www.googleapis.com/auth/drive', redirect_uri='https://mangocloud.me:80/googleauthcallback')
    if 'code' in web.input():
      credentials = flow.step2_exchange(web.input()['code'])
      session.authed = True
      session.credentials = credentials
      web.seeother('/googleauth')


class dropbox_worker:
  def __init__(self, access_token):
    self.client = dropbox.client.DropboxClient(access_token)

  def upload(self, filename, array):
    f = open("tmp.dat", "w");
    f.write(array)
    f.close()
    f = open("tmp.dat", "r");
    self.client.put_file(filename, f)

  def download(self, filename):
    f, metadata = self.client.get_file_and_metadata(filename)
    return f.read()

  def get_free_space(self):
    pass

  def initial_setup(self):
    pass

class google_worker:
  def __init__(self, credentials):
    http = httplib2.Http()
    self.credentials = session.credentials;
    http = credentials.authorize(http)
    self.service = build('drive', 'v2', http)

  def upload(self, filename, array):

    def insert_file(service, title, description, parent_id, mime_type, filename):
      """Insert new file.

      Args:
        service: Drive API service instance.
        title: Title of the file to insert, including the extension.
        description: Description of the file to insert.
        parent_id: Parent folder's ID.
        mime_type: MIME type of the file to insert.
        filename: Filename of the file to insert.
      Returns:
        Inserted file metadata if successful, None otherwise.
      """
      media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
      body = {
        'title': title,
        'description': description,
        'mimeType': mime_type
      }
      # Set the parent folder.
      if parent_id:
        body['parents'] = [{'id': parent_id}]

      try:
        file = service.files().insert(
            body=body,
            media_body=media_body).execute()

        # Uncomment the following line to print the File ID
        # print 'File ID: %s' % file['id']

        return file
      except errors.HttpError, error:
        print 'An error occured: %s' % error
        return None

    about = service.about().get().execute()
    rootId = about['rootFolderId']
    f = open("tmp.dat", "w");
    f.write(array)
    f.close()
    f = open("tmp.dat", "r");
    insert_file(self.service, filename, None, rootId, "application/octet-stream", "tmp.dat")

  def download(self, filename):

    def retrieve_files(service, filename):
      result = []
      page_token = None
      while True:
        try:
          param = {}
          if page_token:
            param['pageToken'] = page_token
            param['q'] = "title=\"" + filename + "\""
            files = service.files().list(**param).execute()

            result.extend(files['items'])
            page_token = files.get('nextPageToken')

            break

        except errors.HttpError, error:
          print 'An error occurred: %s' % error
          break
      return result

    result = retrieve_files(self.service, filename)

    if len(result) == 0:
        return "Failed to find file"

    def download_file(service, drive_file):
      """Download a file's content.

      Args:
        service: Drive API service instance.
        drive_file: Drive File instance.

      Returns:
        File's content if successful, None otherwise.
      """
      download_url = drive_file.get('downloadUrl')
      if download_url:
        resp, content = service._http.request(download_url)
        if resp.status == 200:
          print 'Status: %s' % resp
          return content
        else:
          print 'An error occurred: %s' % resp
          return None
      else:
        # The file doesn't have any content stored on Drive.
        return None

    return download_file(self.service, result[0])

  def get_free_space(self):
    pass

  def initial_setup(self):
    pass

class testing:
  def GET(self):
    array = ''.join(chr(x) for x in [0x50, 0x51, 0x52] * 10)
    d = dropbox_worker(session.access_token)
    d.upload("00.dat", array)
    return str(d.download("00.dat"))

class setup:
  def GET(self):
    return render.index()

class upload:
  def GET(self):
    return "Upload successful!"

  def POST(self):
    update_form = web.input(file={})

    if 'file' in update_form:
      file_name = update_form.file.filename
      data = update_form.file.file.read()
      uploads[file_name] = data 

      #upload_req(data, file_name, len(data))

    return self.GET()

class download:
  def GET(self):
    get_parameters = web.input(file={})
    if 'file' in get_parameters:
      file_name = get_parameters.file.filename
      dld = uploads[file_name]#download_req(file_name, False)
      web.header("Content-Type", "application/octet-stream") # Set the Header
      return dld 

if __name__ == "__main__":
    app.run()
