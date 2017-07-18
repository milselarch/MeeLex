import dynamo
import cAuth

import datetime
import calender

ID = 374204833 # your telegram ID
credential = cAuth.makeCredential(dynamo.readCredentials(ID)[0]["credential"])

start = datetime.datetime.utcnow()
end = start + datetime.timedelta(seconds=3600 * 24)
items = calender.cheakIfFree(credential, start, end)
print(items)