import dropbox
import os

dbx = dropbox.Dropbox(os.getenv('DROPBOX_ACCESS_TOKEN'))

def download_file(filename, savehere):
  testenv = int(os.getenv('testenv'))
  if(testenv == 1):
    filename= filename[1:]
    filename = "/slashy" + filename
  
  
  
  dbx.files_download_to_file(savehere, filename)
 

  


def upload_file(filename, localfile):
  testenv = int(os.getenv('testenv'))
  if(testenv == 1):
    filename= filename[1:]
    filename = "/slashy" + filename

  
  with open(localfile, "rb") as f:
    dbx.files_upload(f.read(), filename, mode=dropbox.files.WriteMode.overwrite)
  os.remove(localfile)
