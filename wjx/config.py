"""
answer_temp - 问卷具体填写

Author: hanayo
Date： 2024/2/29
"""

# 设置每个问题的填写情况，按照每个选项的概率填写。例如ABCD对应1111的话，就是各25%
# ！！！ 注意：选项长度一定要和实际一样，否则会报错
answers = {
    1: [1, 0],
    2: [1, 0, 0, 1],
    3: [1, 1, 0, 0, 0],
}

# 简答题，需要设置好文本
answer_list = {
    6: ["文本1", "文本2"]
}

# 代理IP API提取链接 https://xip.ipzan.com/
# 实际上不使用代理也可以，
api = "https://service.ipzan.com/core-extract?num=1&no=20240228220128183994&minute=10&repeat=1&pool=quality&secret=lqeop7k8is0l12"
# User-Agent库， 分别是网页、手机、微信
UA = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
      "Mozilla/5.0 (Linux; Android 10; SEA-AL10 Build/HUAWEISEA-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/9538 MicroMessenger/8.0.27.2220(0x28001B53) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
      "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/045913 Mobile Safari/537.36 V1_AND_SQ_8.8.68_2538_YYB_D A_8086800 QQ/8.8.68.7265 NetType/WIFI WebP/0.3.0 Pixel/1080 StatusBarHeight/76 SimpleUISwitch/1 QQTheme/2971 InMagicWin/0 StudyMode/0 CurrentMode/1 CurrentFontScale/1.0 GlobalDensityScale/0.9818182 AppId/537112567 Edg/98.0.4758.102",
      ]
