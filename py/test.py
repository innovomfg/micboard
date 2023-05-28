import sys

sys.path.append("/usr/local/lib/python3.9/site-packages")
sys.path.append('.')
import dropbox




access_token = 'sl.BfPh6aLX3iKe-uyZxhMBM0Aiy2bJkf3viDmO3K5sZ2pOYVS5qM5FVxshydrE2EBgc2oKb9VmRYWqWpS952hw6jAPEOEI6-KcCPctoq14xTR4cFPlm_4DrXIjQG8Dphi1t81j0-Y'
key = 'jcxx2rsffmpxws9'
secret = 'e2w2jnn30onq65i'
# Authenticate with Dropbox
print('Downloading images from Dropbox...')
dbx = dropbox.Dropbox(app_key = key, app_secret = secret, oauth2_refresh_token = access_token)

for entry in dbx.files_list_folder('').entries:
    print(entry)