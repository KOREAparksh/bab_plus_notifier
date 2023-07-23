import slack_sdk
import datetime as dt
from datetime import timedelta
import os

weekday = {
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
    now = dt.datetime.now()
    today = now.strftime("%y년 %m월 %d일 " + weekday[0])

    title = "🤩  `" + today + "` 오늘의 점심 메뉴는???"
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
    now = dt.datetime.now()
    today = now.strftime("%y년 %m월 %d일 " + weekday[0])
    tomorrow = (now + timedelta(days=1)).strftime("%y년 %m월 %d일 " + weekday[0])

    title = "`" + today + "` 오늘의 저녁 메뉴와\n`" + tomorrow + "` 내일 점심 메뉴는???"
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
            "image_url": dinnerImageUrl,
            "alt_text": ""
        },
        {
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": tomorrow,
                "emoji": True
            },
            "image_url": nextLaunchImageUrl,
            "alt_text": ""
        },
        {
            "type": "divider"
        },
    ]
    

    


def slackErrorMessageFormat(msg):
    now = dt.datetime.now()
    today = now.strftime("%y년 %m월 %d일")

    return [
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":alert: `Error` 메뉴를 불러오지 못했습니다.\n```" + today + "\n" + msg + "```"
			}
		},
    ]

def sendSlackLaunchMessage(imageUrl) :
    slackToken = os.getenv("TEST_TOKEN")
    channel = os.getenv("TEST_CHANNEL")
    client = slack_sdk.WebClient(token = slackToken)
    client.chat_postMessage(channel = channel, blocks = slackMessageLaunchFormat(imageUrl))


def sendSlackDinnerMessage(dinnerImageUrl, nextLaunchImageUrl) :
    slackToken = os.getenv("TEST_TOKEN")
    channel = os.getenv("TEST_CHANNEL")
    client = slack_sdk.WebClient(token = slackToken)
    client.chat_postMessage(channel = channel, blocks = slackMessageDinnerFormat(dinnerImageUrl, nextLaunchImageUrl))

def sendSlackErrorMessage(msg) :
    slackToken = os.getenv("TEST_TOKEN")
    channel = os.getenv("TEST_CHANNEL")
    client = slack_sdk.WebClient(token = slackToken)
    client.chat_postMessage(channel = channel, blocks = slackErrorMessageFormat(msg))

