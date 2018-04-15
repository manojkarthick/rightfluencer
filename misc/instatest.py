
from InstagramAPI import InstagramAPI

api = InstagramAPI("aringhosh", "Asansol@123")
if (api.login()):
    result = api.SendRequest('users/madhubanimotifs/media/recent/')
    # api.getSelfUserFeed()  # get self user feed
    # print(api.LastJson)  # print last response JSON
    print(result)
else:
    print("Can't login!")