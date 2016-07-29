"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request, response
import json
import math
import time
from random import randint

boto_memory = {"user_name":""}

@route('/', method='GET')
def index():
    response.set_cookie("user_name","")
    return template("chatbot.html")



def processUserMsgLevel5(msg):
    how_are_you = ['how are you', 'feel', 'feeling', 'how are you feeling', 'how you doin', 'doing']
    feel_response = ["im sooo bored today", "I feel just perfect!", "Im doing great", "I'm really tired!", "starving!!!" ]
    if msg.endswith('?'):
        msg = msg.replace(msg[len(msg) - 1], '')
    user_words = msg.split(" ")
    for word in user_words:
        if any(word in how_are_you for word in user_words):
            return {"animation": "confused", "msg": feel_response[randint(0, len(feel_response)-1)]}

def processUserMsgLevel4(msg):
    joke_requests = ['joke', 'laugh','funny']
    robot_jokes = ['A robot walks into a bar, orders a drink, and lays down some cash. Bartender says, "Hey, we dont serve robots."And the robot says, "Oh, but someday you will."',
                   'Jack: Why was the robot angry? Ben: Beats me. Jack: Because someone kept pushing his buttons!',
                   'Billy: What did the man say to his dead robot? Bob: What? Billy: “Rust in peace.”'
]
    if msg.endswith('?'):
        msg = msg.replace(msg[len(msg) - 1], '')
    user_words = msg.split(" ")
    for word in user_words:
        if any(word in joke_requests for word in user_words):
            return {"animation": "laughing", "msg": "ok..." + robot_jokes[randint(0, len(robot_jokes) -1)]}


def processUserMsgLevel3(msg):
    negative_list = ['no', 'dont', 'not']
    feelings_list = ["angry", "sad", "pissed", "stupid", "terrible"]
    if msg.endswith('?'):
        msg = msg.replace(msg[len(msg) - 1], '')
    user_words = msg.split(" ")
    for word in user_words:
        if any(word in negative_list for word in user_words):
            if word in feelings_list:
                word = word.replace(word + "?", "").replace("!", "")
                return {"animation": "dancing", "msg": "that is fantastic! I hate being " + word}


def processUserMsgLevel2(msg):

        fact_request = ["fact","fun","facts","news","learn","teach", "new"]
        fun_facts =["Banging your head against a wall burns 150 calories an hour.",
             "In the UK, it is illegal to eat mince pies on Christmas Day!",
             "Pteronophobia is the fear of being tickled by feathers!",
             "When hippos are upset, their sweat turns red.",
             "A flock of crows is known as a murder.",
            "'Facebook Addiction Disorder' is a mental disorder identified by Psychologists.",
             "The average woman uses her height in lipstick every 5 years.",
             "29th May is officially “Put a Pillow on Your Fridge Day“.",
             "Cherophobia is the fear of fun.",
             "Human saliva has a boiling point three times that of regular water.",
             "If you lift a kangaroo’s tail off the ground it can’t hop."
]
        if msg.endswith('?'):
            msg = msg.replace(msg[len(msg) - 1], '')
        user_words = msg.split(" ")
        for word in user_words:
            if any(word in fact_request for word in user_words):
                return {"animation": "laughing", "msg": "ok..." + fun_facts[randint(0, len(fun_facts) -1)]}
        return None

def processUserMsgLevel1(msg):
    botoLevel1 = {
        "hi": {"animation": "inlove", "msg": "hi " + boto_memory["user_name"]},
        "what is the time": {"animation": "waiting", "msg": "Dude, Im not your watch! alright...  "},
        "how do you feel?": {"animation": "bored", "msg": "like...soooo bored"},
        "dog": {"animation": "dog", "msg": "I love dogs"},
        "name": {"animation": "excited", "msg": "that is the most beautiful name I've ever heard!"},
        "time": {"animation": "waiting", "msg": "I am not your clock...  " + time.ctime()},
        "money": {"animation": "money", "msg": "I'm broke"}

    }
    if msg.endswith('?'):
        msg = msg.replace(msg[len(msg)-1], '')
    user_words = msg.split(" ")

    for word in user_words:
        if word in botoLevel1:
            # word = word.replace(word+"?","").replace("!","")
            return {"animation": botoLevel1[word]["animation"], "msg": botoLevel1[word]["msg"]}
    return None


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    boto_memory["user_name"] = request.get_cookie("user_name")
    if not boto_memory["user_name"]:
        boto_memory["user_name"] = user_message.split(" " )[0]
        response.set_cookie("user_name",boto_memory["user_name"])
        return {"animation": "inlove", "msg": "Nice to meet you " + boto_memory["user_name"]}



    result5 = processUserMsgLevel5(user_message)
    if result5:
        return json.dumps(result5)
    if not result5:
        result4 = processUserMsgLevel4(user_message)
        if result4:
            return json.dumps(result4)
        if not result4:
            result3 = processUserMsgLevel3(user_message)
            if result3:
                return json.dumps(result3)
            if not result3:
                result2 = processUserMsgLevel2(user_message)
                if result2:
                    return json.dumps(result2)
                if not result2:
                    result1 = processUserMsgLevel1(user_message)
                    if not result1:
                        return json.dumps({"animation": "crying", "msg": "Man, I don't get you today...."})

                    else:
                        return json.dumps(result1)



@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
