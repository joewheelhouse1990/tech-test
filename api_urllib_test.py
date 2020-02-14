from urllib.request import Request, urlopen

request = Request('https://api.lyrics.ovh/v1/Coldplay/Yellow')

resp_ = urlopen(request).read()

print(resp_)