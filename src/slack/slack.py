import slack_sdk
import datetime as dt
from datetime import timedelta
import os

weekdays = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일",
    5: "토요일",
    6: "일요일",
}

#낮에 보내는 당일 점심 
def slackMessageLaunchFormat(imageUrl):
    url = os.getenv("CRAWLING_URL")
    today = dt.datetime.now()
    weekday = today.weekday()
    today = today.strftime("%y년 %m월 %d일 " + weekdays[weekday])

    title = "🤩  `" + today + "` 오늘의 점심 메뉴는???\n밥플러스 SKV1 메뉴블로그:\n" + url
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": title
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": today,
                "emoji": True
            },
            "image_url": imageUrl,
            "alt_text": ""
        },
        {
            "type": "divider"
        },
    ]

#밤에 보내는 당일 저녁과 다음날 점심 
def slackMessageDinnerFormat(dinnerImageUrl, nextLaunchImageUrl):
    url = os.getenv("CRAWLING_URL")
    temp = "test\n"
    temp += url + "\n"
    temp += "<" + dinnerImageUrl + "| >"
    temp += "<" + nextLaunchImageUrl + "| >"
    return temp
    
    # today = dt.datetime.now()
    # weekday = today.weekday()
    # tomorrow = today + timedelta(days=1)

    # today = today.strftime("%y년 %m월 %d일 " + weekdays[weekday])
    # tomorrow = tomorrow.strftime("%y년 %m월 %d일 " + weekdays[(weekday + 1) % 7])

    # title = "🤩  `" +"`" + today + "` 오늘의 저녁 메뉴와\n`" + tomorrow + "` 내일 점심 메뉴는???\n밥플러스 SKV1 메뉴블로그:\n" + url
    # return [
    #     {
    #         "type": "section",
    #         "text": {
    #             "type": "mrkdwn",
    #             "text": title
    #         }
    #     },
    #     {
    #         "type": "divider"
    #     },
    #     {
    #         "type": "image",
    #         "title": {
    #             "type": "plain_text",
    #             "text": today,
    #             "emoji": True
    #         },
    #         "image_url": dinnerImageUrl,
    #         "alt_text": ""
    #     },
    #     {
    #         "type": "image",
    #         "title": {
    #             "type": "plain_text",
    #             "text": tomorrow,
    #             "emoji": True
    #         },
    #         "image_url": nextLaunchImageUrl,
    #         "alt_text": ""
    #     },
    #     {
    #         "type": "divider"
    #     },
    # ]


#낮에 보내는 당일 점심 
def slackMessageFridayFormat(imageUrl):
    url = os.getenv("CRAWLING_URL")
    today = dt.datetime.now()
    friday = today + timedelta(days=3)
    friday = friday.strftime("%y년 %m월 %d일 " + weekdays[0])

    title = "🤩  `" + friday + "` 다음주 월요일의 점심 메뉴는???\n밥플러스 SKV1 메뉴블로그:\n" + url
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": title
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": friday,
                "emoji": True
            },
            "image_url": imageUrl,
            "alt_text": ""
        },
        {
            "type": "divider"
        },
    ]

    
def slackErrorMessageFormat(msg):
    today = dt.datetime.now()
    today = today.strftime("%y년 %m월 %d일")

    return [
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":alert: `Error` 메뉴를 불러오지 못했습니다.\n```" + today + "\n" + msg + "```"
			}
		},
    ]

def sendSlackLaunchMessageTEST(image, slackToken, channel) :
    client = slack_sdk.WebClient(token = slackToken)
    client.chat_postMessage(channel = channel, blocks = slackMessageLaunchFormat(image))
    
def sendSlackDinnerMessageTEST2(imageUrl1, imageUrl2, slackToken, channel) :
    client = slack_sdk.WebClient(token = slackToken)
    os.system("mkdir -p /home/ubuntu/image")
    os.system("curl " + imageUrl1 + " > " + "/home/ubuntu/image/image1.png")
    os.system("curl " + imageUrl2 + " > " + "/home/ubuntu/image/image2.png")
    
    image1 = open("/home/ubuntu/image/image1.png", 'rb')
    upload1 = client.files_upload(file=image1)
    image2 = open("/home/ubuntu/image/image2.png", 'rb')
    upload2 = client.files_upload_v2(file=image2)
    client.chat_postMessage(channel=channel, text=slackMessageDinnerFormat(upload1["file"]["permalink"], upload2["file"]["permalink"]), blocks=[{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "tttt"
            }
        }])

def sendSlackDinnerMessageTEST(imageUrl1, imageUrl2, slackToken, channel) :
    client = slack_sdk.WebClient(token = slackToken)
    client.chat_postMessage(channel = channel, blocks = slackMessageDinnerFormat(imageUrl1, imageUrl2))

def sendSlackFridayMessageTEST(imageUrl, slackToken, channel) :
    client = slack_sdk.WebClient(token = slackToken)
    client.chat_postMessage(channel = channel, blocks = slackMessageFridayFormat(imageUrl))

def sendSlackErrorMessageTEST(msg, slackToken, channel) :
    client = slack_sdk.WebClient(token = slackToken)
    client.chat_postMessage(channel = channel, blocks = slackErrorMessageFormat(msg))
