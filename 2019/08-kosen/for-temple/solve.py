import pandas as pd
import urllib.parse
import re
df = pd.read_csv('data.csv')
data = df[df['Protocol'] == 'HTTP']
data.reset_index(inplace=True)


time, source, destination, info = data['Time'], data['Source'], data['Destination'], data['Info']
r = re.compile(r"\d+")

flag = ''
for i in range(1, len(data)):
    for j in range(i+1, len(data)):
        if source.iloc[j] == destination.iloc[i] and destination.iloc[j] == source.iloc[i]:
            if time.iloc[j]-time.iloc[i] >= 0.1:
                s = urllib.parse.unquote(info[i])
                if s.startswith('GET /index.php'):
                    flag += chr(int(re.findall(r, s)[2]))
                    print(f'\r[+] Flag: {flag}', end='')
            i += j-i+1
            break
print()
