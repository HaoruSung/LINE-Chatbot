from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
# 載入json處理套件
import json
# 將消息模型，文字收取消息與文字寄發消息，Follow事件引入
from linebot.models import (
    MessageEvent, FollowEvent, JoinEvent,
    TextSendMessage, TemplateSendMessage,
    TextMessage, ButtonsTemplate,
    PostbackTemplateAction, MessageTemplateAction,
    URITemplateAction,ImageSendMessage,CarouselTemplate,CarouselColumn,
    FlexSendMessage,BubbleContainer
)
# 載入requests套件
import requests

app = Flask(__name__,static_url_path = "/images" , static_folder = "./images/")

# 載入基礎設定檔，本機執行所以路徑可以相對位置
secretFile=json.load(open("./secret_key",'r'))
server_url = secretFile.get("server_url")
ChannelAccessToken = secretFile.get("server_url")
ChannelSecret = secretFile.get("server_url")

# Channel Access Token
line_bot_api = LineBotApi(ChannelAccessToken)
# Channel Secret
handler = WebhookHandler(ChannelSecret)

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'



#宣告並設定推播的 button_template_message (全域變數)
button_template_message = CarouselTemplate(
            columns=[
                CarouselColumn(
                    #置換成自己要用的照片
                    thumbnail_image_url="https://%s/images/S__16629765.jpg" %server_url,
                    title='宋浩茹  Hi ! I\'m Amber',
                    text='關於我',
                    actions=[
                        PostbackTemplateAction(
                            label='自我介紹 I\'m Amber',
                            data="type=introduce"
                        ),
                        PostbackTemplateAction(
                            label='工作經驗 Experience',
                            data="type=work"
                        )
                    ]
                ),
                CarouselColumn(
                    #置換成自己要用的照片
                    thumbnail_image_url="https://%s/images/com.jpg" %server_url,
                    title='我的亮點經驗與專案實作',
                    text='相關經驗',
                    actions=[
                        PostbackTemplateAction(
                            label='亮點經驗 Highlights',
                            data="type=highlights"
                        ),
                        PostbackTemplateAction(
                            label='專案實作 Project',
                            data="type=project"
                        )
                    ]
                )]
            )


button_template_message_highlights = CarouselTemplate(
            columns=[
                CarouselColumn(
                    title='AI CUP 2021 繁體中文場景文字辨識高階賽 - 前標獎',
                    text='使用OCR技術以及影像前處理訓練模型，進行複雜街景之文字定位與辨識 。',
                    actions=[
                        PostbackTemplateAction(
                            label=' ',
                            data="type= "
                        )
                    ]
                ),
                CarouselColumn(
                    title='NCCU Google Developer Student Club',
                    text='NCCU GDSC 是與 Google 一起推動的，為政大服務的學生開發者社群，打造一個技術交流的場域。',
                    actions=[
                        PostbackTemplateAction(
                            label=' ',
                            data="type= "
                        )
                    ]
                ),
                CarouselColumn(
                    title='日本東京創新天才國際發明展 - 金牌',
                    text='中華明國專利證書號 - M526355。',
                    actions=[
                        PostbackTemplateAction(
                            label=' ',
                            data="type= "
                        )
                    ]
                ),
                CarouselColumn(
                    title='OOP物件導向程式設計 - 優良助教獎',
                    text='擔任基礎程式設計與OOP程式設計助教，協助課程教授指導學生 。',
                    actions=[
                        PostbackTemplateAction(
                            label=' ',
                            data="type= "
                        )
                    ]
                ),
                CarouselColumn(
                    title='大學畢業專題研究競賽 - 優勝',
                    text='研究主題 : 運用臉部動態表情辨識個性。',
                    actions=[
                        PostbackTemplateAction(
                            label=' ',
                            data="type= "
                        )
                    ]
                ),
                CarouselColumn(
                    title='大學書卷獎畢業',
                    text='全系第一名畢業 ( GPA : 3.81 / 4.00 ) 。',
                    actions=[
                        PostbackTemplateAction(
                            label=' ',
                            data="type= "
                        )
                    ]
                ),
                CarouselColumn(
                    title='TANET 2017-臺灣網際網路研討會論文',
                    text='榮獲教育部數位學伴計畫-傑出數位學伴獎。',
                    actions=[
                        PostbackTemplateAction(
                            label=' ',
                            data="type= "
                        )
                    ]
                )]
            )


button_template_message_project = CarouselTemplate(
            columns=[
                CarouselColumn(
                    #置換成自己要用的照片
                    thumbnail_image_url="https://%s/images/chatbot.png" %server_url,
                    title='LINE Chatbot 客服機器人',
                    text='●顧客可以詢問庫存以及熱銷產品等。\n●透過LineBotSDK開發，並串接line api，完成客服聊天機器人。',
                    actions=[
                         URITemplateAction(
                            label='GitHub',
                            uri='https://github.com/BuildSchool-MVC/LineBot'
                        )
                    ]
                ),
                CarouselColumn(
                    #置換成自己要用的照片
                    thumbnail_image_url="https://%s/images/datoding.jpg" %server_url,
                    title='DaToDing 旅遊網站 - 聊天室開發(IM Dev)',
                    text='●實作 WebSocket，開發個人聊天室、群組聊天室。',
                    actions=[
                         URITemplateAction(
                            label='DaToDing旅遊網站',
                            uri='https://www.datoding.com/login'
                        )
                    ]
                ),
                CarouselColumn(
                    #置換成自己要用的照片
                    thumbnail_image_url="https://%s/images/news.png" %server_url,
                    title='新聞推薦系統',
                    text='●當使用者下關鍵字後，系統會推薦Top 10 相關性最高的新聞內容。',
                    actions=[
                         URITemplateAction(
                            label='GitHub',
                            uri='https://github.com/HaoruSung/News-Recommendation'
                        )
                    ]
                ),
                CarouselColumn(
                    #置換成自己要用的照片
                    thumbnail_image_url="https://%s/images/kingston.png" %server_url,
                    title='AI視覺辨識 - 產品良率檢測系統(金士頓實習)',
                    text='●協助AOI設備與減少人工檢測，降低人力成本。',
                    actions=[
                        PostbackTemplateAction(
                            label=' ',
                            data="type= "
                        )
                    ]
                ),
                CarouselColumn(
                    #置換成自己要用的照片
                    thumbnail_image_url="https://%s/images/OCR.jpg" %server_url,
                    title='複雜街景之文字定位與辨識',
                    text='●透過OCR技術，進行複雜街景之文字定位與辨識。',
                    actions=[
                         URITemplateAction(
                            label='GitHub',
                            uri='https://github.com/HaoruSung/AICUP_OCR'
                        )
                    ]
                ),
                CarouselColumn(
                    #置換成自己要用的照片
                    thumbnail_image_url="https://%s/images/Imlab.png" %server_url,
                    title='實驗室網站開發',
                    text='●協助實驗室網站開發與維護。',
                    actions=[
                         URITemplateAction(
                            label='實驗室網站',
                            uri='http://imlab.cs.nccu.edu.tw/'
                        )
                    ]
                ),
                CarouselColumn(
                    #置換成自己要用的照片
                    thumbnail_image_url="https://%s/images/gold.PNG" %server_url,
                    title='日本東京創新天才國際發明展-金牌',
                    text='●解決日常生活中的痛點，與團隊發明複合式砧板，榮獲金牌。\n●中華明國專利證書號-M526355。',
                    actions=[
                        PostbackTemplateAction(
                            label=' ',
                            data="type= "
                        )
                    ]
                ),
                CarouselColumn(
                    #置換成自己要用的照片
                    thumbnail_image_url="https://%s/images/person.png" %server_url,
                    title='運用臉部動態表情辨識個性',
                    text='●運⽤機器學習、網路爬蟲與數據分析進⾏研究。',
                    actions=[
                         URITemplateAction(
                            label='專案報告',
                            uri='https://facial-expressions.azurewebsites.net/facePage.html'
                        )
                    ]
                )]
            )

#宣告並設定推播的 flex bubble (全域變數)
#圖片的URL要置換成絕對路徑
#URI要改成想連結的URI
flexBubbleContainerJsonString_INTRO ="""
{
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "自我介紹 I\'m Amber",
        "align": "center"
      }
    ]
  },
  "hero": {
    "type": "image",
    "url": "https://chatbothello2.herokuapp.com/images/S__16629771.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "https://www.cakeresume.com/s--JGIdyisiRl8q4MdnUB73GA--/haoru-sung"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "宋浩茹",
        "weight": "bold",
        "size": "xl"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "就讀國立政治大學資訊科學系(資工組) 碩一，研究NLP自然語言處理以及推薦系統。對於學習新技術充滿熱忱，擁有Learn how to learn的能力，對於LINE Chatbot有許多開發經驗 ，開發電商網站客服機器人Chatbot。並運用SDK將自然語言模型串接Chatbot，實現智慧QA問答。積極參與競賽，在AI CUP 2021繁體中文場景文字辨識競賽-高階賽，獲得前標獎的肯定。在金士頓科技實習時，獨立開發AI視覺辨識-產品良率檢測系統。有顆創造力十足的腦袋，為了解決活中的痛點，在日本創新天才國際發明展，榮獲金牌。也是DaToDing旅遊網站創始成員之一，培養了系統開發以及問題解決能力。我喜歡創新、熱愛學習新技術與不怕挑戰，絕對會是您最佳的人選，期待成為LINE的一份子 !",
                "color": "#aaaaaa",
                "size": "sm",
                "wrap": true
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "我的履歷表Resume",
          "uri": "https://www.cakeresume.com/s--JGIdyisiRl8q4MdnUB73GA--/haoru-sung"
        }
      }
    ],
    "flex": 0
  }
}"""

flexBubbleContainerJsonString_Work1 ="""
{
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "DATODING CO, LTD.",
        "align": "center",
        "size": "lg",
        "weight": "bold"
      }
    ]
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Software Engineer(Founding Member) ",
        "weight": "bold",
        "size": "md",
        "contents": [],
        "wrap": true
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "Microsoft 新創加速器第二期初選",
            "wrap": true,
            "color": "#FE9200"
          },
          {
            "type": "text",
            "text": "1. 獨立開發 Instant Messaging(IM) 聊天室功能。 ",
            "wrap": true
          },
          {
            "type": "text",
            "text": "2. 後端與前端功能設計、開發與維運，前後端擁有完整分層架構。",
            "wrap": true
          },
          {
            "type": "text",
            "text": "3. Unit Testing 、 Integration Testing & Selenium Test Automation 。",
            "wrap": true
          },
          {
            "type": "text",
            "text": "4. 完成一場技術分享 - Clean code (聽眾約 30 人)。",
            "wrap": true
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "Go To DATODING !",
          "uri": "https://www.datoding.com/"
        }
      }
    ],
    "flex": 0
  }
}"""

flexBubbleContainerJsonString_Work2 ="""
{
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Kingston Technology",
        "align": "center",
        "size": "lg",
        "weight": "bold"
      }
    ]
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Software Engineer (Intern) ",
        "weight": "bold",
        "size": "md",
        "contents": [],
        "wrap": true
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "1. 獨立開發AI視覺辨識-產品良率檢測系統。",
            "wrap": true
          },
          {
            "type": "text",
            "text": "2. 將Computer Vision Model導入Chatbot。 ",
            "wrap": true
          },
          {
            "type": "text",
            "text": "3. 透過Git進行版本維護與協同開發。 ",
            "wrap": true
          },
          {
            "type": "text",
            "text": "4. 完成一場技術分享 - Power BI (聽眾 5人) 。",
            "wrap": true
          }
        ]
      }
    ]
  }
}"""



#INTRO樣板封裝
bubbleContainer_intro= BubbleContainer.new_from_json_dict(json.loads(flexBubbleContainerJsonString_INTRO))
flexBubbleSendMessage_INTRO =  FlexSendMessage(alt_text="自我介紹", contents=bubbleContainer_intro)
#WORK樣板封裝
bubbleContainer_work1= BubbleContainer.new_from_json_dict(json.loads(flexBubbleContainerJsonString_Work1))
bubbleContainer_work2= BubbleContainer.new_from_json_dict(json.loads(flexBubbleContainerJsonString_Work2))
flexBubbleSendMessage_WORK1 =  FlexSendMessage(alt_text="工作經驗1", contents=bubbleContainer_work1)
flexBubbleSendMessage_WORK2 =  FlexSendMessage(alt_text="工作經驗2", contents=bubbleContainer_work2)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)
    user_name_len = len(user_profile.display_name)
    emoji_index = user_name_len + 6
    message = TextSendMessage(text=event.message.text)
    
    # emoji
    emoji = [
        {
            "index": emoji_index,
            "productId": "5ac21e6c040ab15980c9b444",
            "emojiId": "005"
        },
        {
            "index": emoji_index+7,
            "productId": "5ac21ae3040ab15980c9b440",
            "emojiId": "001"
        },
        {
            "index":  emoji_index+8,
            "productId": "5ac21ae3040ab15980c9b440",
            "emojiId": "039"
        },
        {
            "index":  emoji_index+9,
            "productId": "5ac21ae3040ab15980c9b440",
            "emojiId": "028"
        },
         {
            "index":  emoji_index+10,
            "productId": "5ac21ae3040ab15980c9b440",
            "emojiId": "031"
        },
         {
            "index":  emoji_index+11,
            "productId": "5ac21ae3040ab15980c9b440",
            "emojiId": "044"
        }
    ] 

    #針對剛加入的用戶回覆文字消息、圖片、旋轉門選單
    reply_message_list = [
                    TextSendMessage(text="Hi!%s您好~$\n我是宋浩茹$$$$$\n就讀國立政治大學 資訊科學系\n想多了解我可以點選按下方按鈕\n希望有機會成為LINE FRESH\n開啟LINE奇幻旅程!"% (user_profile.display_name) , emojis=emoji ),     
                    TemplateSendMessage(alt_text="您好,我是宋浩茹",template=button_template_message),
                ] 
                
        # 當用戶輸入VMware時判斷成立
    if (event.message.text.find('自我介紹')!= -1):
        # 回覆訊息
        line_bot_api.reply_message(
            event.reply_token,
            flexBubbleSendMessage_INTRO
            )

        # 當用戶輸入Linux Server時判斷成立
    elif (event.message.text.find('工作經驗')!= -1):
        # 回覆訊息
        line_bot_api.reply_message(
            event.reply_token,
            [flexBubbleSendMessage_WORK1,flexBubbleSendMessage_WORK2]
            )

    # 當用戶輸入Linux Server時判斷成立
    elif (event.message.text.find('亮點經驗')!= -1):
        # 將上面的變數包裝起來
        reply_list = [
            TemplateSendMessage(alt_text="亮點經驗",template=button_template_message_highlights)
        ]
        # 回覆訊息
        line_bot_api.reply_message(
            event.reply_token,
            reply_list
            )

            # 當用戶輸入Linux Server時判斷成立
    elif (event.message.text.find('專案實作')!= -1):
        # 將上面的變數包裝起來
        reply_list = [
            TemplateSendMessage(alt_text="專案實作",template=button_template_message_project)
        ]
        # 回覆訊息
        line_bot_api.reply_message(
            event.reply_token,
            reply_list
            )

    # 收到不認識的訊息時，回覆原本的旋轉門菜單    
    else:         
        line_bot_api.reply_message(
            event.reply_token,
            reply_message_list
        ) 



    #line_bot_api.reply_message(event.reply_token, reply_message_list)



"""
    
    收到按鈕（postback）的封包後
        1. 先看是哪種按鈕（introduce(自我介紹)，work(工作經驗)highlights(亮點經驗)project(專案實作)）
        2. 執行所需動作（執行之後的哪一些函式）
        3. 回覆訊息

"""
from linebot.models import PostbackEvent

#parse_qs用於解析query string
from urllib.parse import urlparse,parse_qs

#用戶點擊button後，觸發postback event，對其回傳做相對應處理
@handler.add(PostbackEvent)
def handle_post_message(event):
    #抓取user資料
    user_profile = event.source.user_id
    
    #抓取postback action的data
    data = event.postback.data
    
    #用query string 解析data
    data=parse_qs(data)
               
    #給按下"yourName自我介紹"，"yourName工作經驗"，"yourName的專長"，推播對應的flexBubble
    if (data['type']==['introduce']):
            line_bot_api.reply_message(
                event.reply_token,
                flexBubbleSendMessage_INTRO
            )
    elif (data['type']==['work']):
            line_bot_api.reply_message(
                event.reply_token,
                [flexBubbleSendMessage_WORK1,flexBubbleSendMessage_WORK2]
            )
    elif (data['type']==['highlights']):
            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(alt_text="亮點經驗",template=button_template_message_highlights)
            )
    elif (data['type']==['project']):
            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(alt_text="專案實作",template=button_template_message_project)
            )
    #其他的pass
    else:
        pass


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
