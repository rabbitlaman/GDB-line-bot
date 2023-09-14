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
    ImageMessage
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
        if event.message.text == "cool":
            image_message = ImageMessage(
                original_content_url='https://www.bing.com/images/search?view=detailV2&ccid=u4%2fnrN%2f3&id=5392735A19DB7652243782F7BA18C5B7953B9C68&thid=OIP.u4_nrN_3Mg-n8NBGTtYsAAHaNK&mediaurl=http%3a%2f%2fpuui.qpic.cn%2fvpic_cover%2fe0964z1l4bc%2fe0964z1l4bc_vt.jpg%2f720&exph=1280&expw=720&FORM=imgfdp&ck=61A4A4E6B74B4C4A5C4E41243E1FB76F&reqid=A9DF8EC79412430790096EF70A94DA2F&selectedIndex=1&idpp=insfeed&ajaxhist=0&ajaxserp=0',
                preview_image_url='https://www.bing.com/images/search?view=detailV2&ccid=w0%2FITiU0&id=AD7A6579F4796B6E8CC0826BFA753A7A21923D1B&thid=OIP.w0_ITiU01iXpg3qlWVEEogAAAA&mediaurl=https%3A%2F%2Fkk-cloudserver.de%2Fkk_logo_quadratisch.png&cdnurl=https%3A%2F%2Fth.bing.com%2Fth%2Fid%2FR.c34fc84e2534d625e9837aa5595104a2%3Frik%3DGz2SIXo6dfprgg%26pid%3DImgRaw%26r%3D0&exph=150&expw=150&q=kk&simid=607994458596116583&form=IRPRST&ck=DF7B90F500BC164FA329A3B7C23AFF2C&selectedindex=2&qft=+filterui%3aimagesize-small&ajaxhist=0&ajaxserp=0&vt=0&sim=11'
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[image_message]
                    )
                )

        else:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='fuck')]
                    )
                )

if __name__ == "__main__":
    app.run()
