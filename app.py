from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    TemplateMessage,
    ButtonsTemplate,
    PostbackAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    FollowEvent,
    PostbackEvent,
    TextMessageContent
)
import os

app = Flask(__name__)

configuration = Configuration(access_token = os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'
#加入好友事件
@line_handler.add(FollowEvent)
def handle_follow(event):
    print(f'Got {event.type} event')

#訊息事件
@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)



        if event.message.text =='postback':
            buttoms_template = ButtonsTemplate(
                title = 'Postback Sample',
                text = 'Postback Action',
                actions = [
                    PostbackAction(label = 'Postback Action', text = 'Postback Action Buttom Clicked!', data = 'postback'),
                ]
            )
            template_message = TemplateMessage(
                altText = 'Postback Sample',
                template=buttoms_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[template_message]
                )
            )
                    #line_bot_api.reply_message_with_http_info(
         #   ReplyMessageRequest(
          #      reply_token=event.reply_token,
           #     messages=[TextMessage(text=event.message.text)]

          #  )
        #)
@line_handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'postback':
        print('Postback event is triggered')

if __name__ == "__main__":
    app.run()