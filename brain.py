import requests
import random
import re
import json
import hashlib

def clean_xml(text='something <img>img_link</img>'):
    text_cleaned = re.sub("<.+>", "", text)
    return text_cleaned

class PandoraBot:

    def __init__(self, user_id='rnd', bot_name='David', is_male=True,
                 verbose=False):
        botkey = 'n0M6dW2XZacnOgCWTp0FRYUuMjSfCkJGgobNpgPv9060_72eKnu3Yl-o1v2nFGtSXqfwJBG2Ros~'

        if user_id == 'rnd':
            user_id = random.randint(0, 100000)

        user_hash = hashlib.sha1(str(user_id).encode()).hexdigest()[:6]

        self.client_name = 'kukilp-17307' + user_hash
        self.botkey = botkey
        self.bot_original_name = 'Kuki'
        self.verbose = verbose
        self.bot_name = bot_name
        self.sessionid = 'null'
        self.url = 'https://miapi.pandorabots.com/talk'
        self.chat_v = []
        self.re_v = [(self.bot_original_name, self.bot_name),
                     ('english', 'spanish'),
                     ]

        if is_male:
            self.re_v += [('female', 'male'),
                          ('woman', 'man'),
                          ('girl', 'boy')]
        self.send_post()

    def _text_replace(self, text):
        text_ = text
        for a, b in self.re_v:
            text_ = re.sub(r'\b' + a + r'\b', '&S' + b, text_, flags=re.IGNORECASE)
            text_ = re.sub(r'\b' + b + r'\b', '&S' + a, text_, flags=re.IGNORECASE)

        text_ = text_.replace('&S', '')
        return text_

    def send_post(self, text='xintro'):
        r = requests.post(
            self.url,
            data={
                'input': text,
                'sessionid': self.sessionid,
                'channel': '6',
                'botkey': self.botkey,
                'client_name': self.client_name},

            headers={'Referer': 'https://www.pandorabots.com/mitsuku/'})

        r_d = json.loads(r.content.decode(errors='ignore'))

        self.sessionid = str(r_d['sessionid'])
        resp_v = r_d['responses']

        return resp_v

    def get_response(self, q):
        text = q
        text = self._text_replace(text)
        resp_v = self.send_post(text)

        if len(resp_v) > 0 and resp_v[0] != '':
            ret_text = resp_v[0]
            ret_text = clean_xml(ret_text)

        else:
            ret_text = "I am sorry, I don't have an answer"
        ret_text = self._text_replace(ret_text)
        self.chat_v.append((q, ret_text))
        return ret_text

def brain(query):
    try:
        return PandoraBot(bot_name="Jarvis", is_male=True, verbose=True).get_response(query)
    except ConnectionError:
        return "Sir, I think we lost the connection to the Internet"