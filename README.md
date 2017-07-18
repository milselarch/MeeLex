# MeeLex

Meeting scheduler using Lex, dynamoDB, API gateway, Serverless framework and Lambda, Telegram, and google calender API
lambdas/authlambda contains lambda function to authenticate user using oauth, and lambdas/telegramLambda contains lambda function that runs telegram bot.

uses a single dynamoDB table caled cxausers to store user OAuth credentials needed to access google calender API: the dynamodb key is the telegram user ID, and the table maps telegram user IDs to their json encoded OAuth2 credentials

python files at root are neither serverless nor used as part of project - they exist only for personal reference on how to port code to serverless services. all functioning bot code is running on lambda functions.

Natural and intuitive communication is brought by feeding text data to a lex bot we created, and sceduling meetings based on what they say.

Commands
/start - start conversation
/b <meeting information> - book meeting
