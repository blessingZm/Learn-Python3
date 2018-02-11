"""
dumps是将dict转化成str格式，loads是将str转化成dict格式。————针对字符串和字典
dump和load也是类似的功能，只是与文件操作结合起来了。————针对读写文件
"""

import json

file = '.\\省级AJ ftp访问用户名、密码.json'
with open(file, 'r') as jrf:
    jsonData = json.load(jrf)

# with open('end_ftp访问用户名、密码.json', 'w') as wf:
#     json.dump(jsonData, wf, ensure_ascii=False, indent=0)

print(json.dumps(jsonData, ensure_ascii=False, indent=0))