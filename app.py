# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 02:15:23 2023

@author: z1014
"""

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
    ImageMessage,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token='042PpRCHOlObHG0lxX19iW08EBYLPXBKLe0Vbs4cMZeA2vvhA8sZFPTB3F7RzMl9ixpMb/v5VFJkEVMsI9U2M6Wa+8xq0xZtH4fQieO/qCCLVe+RmWtJ+Gy4fwxkxBzDKJqXFIAI4Q3M0q2sPuupPgdB04t89/1O/w1cDnyilFU=')
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
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        profile = line_bot_api.get_profile(event.source.user_id)
        
        if event.message.text == "cool":
            image_message = ImageMessage(
                original_content_url='156240.jpg',
                preview_image_url='156240.jpg'
            )
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[image_message]
                    )
                )

        else:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text = profile.user_id)]
                    )
                )

if __name__ == "__main__":
    app.run()
