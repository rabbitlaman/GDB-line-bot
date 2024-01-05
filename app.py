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
    PostbackEvent,
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

#Message 事件
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        profile = event.source.user_id
        #addful = profile.user_id +"\n"+ profile.display_name+"\n"+profile.picture_url
        
        if event.message.text == "a":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text = '成功')]
                    )
                )

            
#postback 事件
@handler.add(PostbackEvent)
def handle_postback(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
    postback = event.postback.data
    
    profile = line_bot_api.get_profile(event.source.user_id)
    addful = profile.user_id
    
    picture1 = ImageMessage(
         originalContentUrl='https://drive.google.com/file/d/19XR4tnlYv8naxVPBc29iYKQIWkQ27bug/view?usp=drive_link',
         previewImageUrl='https://drive.google.com/file/d/19XR4tnlYv8naxVPBc29iYKQIWkQ27bug/view?usp=drive_link'
         
    )
    
    
    if postback == '每日經節':
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[picture1]
                )
            )
    #與database做
    if postback == '功能使用':
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text = addful)]
                )
            )

if __name__ == "__main__":
    app.run()
