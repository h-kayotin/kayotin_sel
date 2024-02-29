# 通过Selenium批量填写问卷

### 起因

为啥要做这个呢。因为某天老婆让我帮她填问卷，而且是填几十份一模一样的，点的我鼠标都要冒烟了。所以研究下自动化工具，咱肯定不能一个个手工去点呀。

### 如何使用

请安装所需的库：requests、numpy、Selenium

1. 在config.py中设定问卷答案：
    
    ```python
    # 设置每个问题的填写情况，按照每个选项的概率填写。例如ABCD对应1111的话，就是各25%
    # ！！！ 注意：选项长度一定要和实际一样，否则会报错
    answers = {
        1: [1, 0],
        2: [1, 0, 0, 1],
        3: [1, 1, 0, 0, 0],
    }
    
    # 简答题，需要设置好文本;如没有请无视即可
    answer_list = {
        6: ["文本1", "文本2"]
    }
    ```
    
    以上的问题代表了这个问卷的填写情况：[问卷链接](https://www.wjx.cn/vm/rJoCZrn.aspx)
    
2. 在config.py中填写代理IP（选填：如果不使用代理IP，这个api里保持如下就行，但不能为空
    
    ```python
    # 实际上不使用代理也可以，无非就是做的多了会有验证
    api = "https://service.ipzan.com/core-extract"
    ```
    
3. 运行主程序auto_wjx.py，选择做多少份
    
    ```python
        my_url = "https://www.wjx.cn/vm/rJoCZrn.aspx"
        my_wjx = MyWjx(my_url, 10)
        my_wjx.fill_in()  # 做1份
    	  my_wjx.do_works()  # 做10份
    ```
    

### 参考链接：

该工具很大程度上参考了如下链接：

https://github.com/zzmvp-1/wjx-auto-fill

# 京东图片滑块验证码登录

用Selenium来模拟京东的登录。为什么是京东，因为我常用京东，而且它刚好是滑块验证码。

### 如何使用

1. 安装图片识别库：ddddocr、pillow
2. 在selenium_jd.py程序中填写账号密码：
    
    ```python
        # 模拟输入
        username_input.send_keys('18xxxxxxx93')
        pw_input.send_keys('1234567')
    ```
    
3. 运行selenium_jd.py

> 验证码图片会保存在同级的文件images中，请确保该文件夹存在
>
