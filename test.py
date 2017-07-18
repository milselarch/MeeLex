import dynamo
import cAuth

ID = 1 # your telegram ID
credential = cAuth.makeCredential(dynamo.readCredentials(ID))
