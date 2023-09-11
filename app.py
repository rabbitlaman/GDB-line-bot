from flask import Flask, request, abort
from linebot import (
    LineBotApi
    )
from linebot.models import *
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
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

line_bot_api = LineBotApi('042PpRCHOlObHG0lxX19iW08EBYLPXBKLe0Vbs4cMZeA2vvhA8sZFPTB3F7RzMl9ixpMb/v5VFJkEVMsI9U2M6Wa+8xq0xZtH4fQieO/qCCLVe+RmWtJ+Gy4fwxkxBzDKJqXFIAI4Q3M0q2sPuupPgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('eb625d3da1dc4e1ebacf288919e5234f')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    
        message_text = str(event.message.text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(message_text))
        if message_text == "cool" :
            line_bot_api.reply_message(event.reply_token,TextSendMessage('fdjifji'))
    
        if message_text == '安排表' :
            image_message = ImageSendMessage(
                original_content_url='https://github.com/rabbitlaman/GDB-line-bot/blob/main/156240.jpg',
            )
            line_bot_api.reply_message(event.reply_token, image_message)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(message_text))
            

if __name__ == "__main__":
    app.run()
