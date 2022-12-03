import json
import datetime


def decoration(function):
    def box(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except Exception as e:
            print(function.__name__, "函数发生异常")
            print("错误发生时间：", str(datetime.datetime.now()))
            print("错误的详细情况：", repr(e))

    return box


class Message(object):
    def __init__(self):
        """
        content json消息文件
        """
        self.content = {"content": []}
        self.content_data = self.content["content"]
        self.Number = 1001

    @decoration
    def 生成消息文件(self, number):
        """

        :param number: 生成的文件名称
        :return:
        """
        with open(f"content{number}.json", "w", encoding="utf-8")as f:
            f.write(json.dumps(self.content, ensure_ascii=False, indent=4))


class NMessageCommon(Message):
    """
    子类继承，Message
    """

    @decoration
    def 选择同桌(self):
        """
        选择同桌
        :return:
        """
        self.content_data.append({"id": self.Number, "type": "MatchUser", "data": {}})
        self.Number += 1

    @decoration
    def 文本消息(self, Text: str, Time=-1):
        """

        :param Time: 单位是秒默认不用填或者填 -1 ， 0 的话立即弹下一条。
        :param Text: 文本内容
        :return:
        """
        self.content_data.append({"id": self.Number, "type": "Text", "data": {"time": Time, "text": f"{Text}"}})
        self.Number += 1

    @decoration
    def 视频消息(self, video_url: str):
        """

        :param video_url: 视频地址
        :return:
        """
        self.content_data.append({"id": self.Number, "type": "Video", "data": {"src": f"{video_url}"}})
        self.Number += 1

    @decoration
    def 图片消息(self, img_url: str):
        """

        :param img_url: 图片地址
        :return:
        """
        self.content_data.append({"id": self.Number, "type": "Image", "data": {"src": f"{img_url}"}})
        self.Number += 1

    @decoration
    def 课后快速选择题(self, choices: int):
        """

        :param choices: 题库题号
        :return:
        """
        self.content_data.append({"id": self.Number, "type": "QuickSelect", "data": {"limit": 20, "choice": choices}})
        self.Number += 1

    @decoration
    def 课后单选题(self, choices: list, limit):
        """

        :param limit: 答题时间
        :param choices: 题号-列表传入
        :return:
        """
        self.content_data.append(
            {"id": self.Number, "type": "QuickChoices", "data": {"limit": limit, "choices": choices}})
        self.Number += 1

    @decoration
    def 程序设计题(self, problem: int):
        """

        :param problem: 题号
        :return:
        """
        self.content_data.append({"id": self.Number, "type": "Programming", "data": {"problem": problem}})
        self.Number += 1

    @decoration
    def pk(self, universityName: str, iamge_url: str):
        """

        :param cookbook: 菜谱.txt
        :param universityName: 学校名称
        :param iamge_url: 学校图片
        :return:
        """
        with open(f"菜谱/{universityName}.txt", "r", encoding="utf-8") as f:
            cookbook = f.read()
        universityName = universityName.split(".")[1]
        for i in range(100):
            universityName = universityName.replace(f"{i}", "")
        self.content_data.append({"id": self.Number, "type": "Pk",
                                  "data": {"type": "set",
                                           "name": universityName,
                                           "image": iamge_url,
                                           "cookbook": cookbook,
                                           "winNoty": f"解锁积木「菜谱」：{universityName}",
                                           "failNoty": ""}})
        self.Number += 1

    @decoration
    def 代码消息NumPy(self, desc, fileName, ):
        """

        :param desc: 描述信息
        :param fileName: 读取的文件名称
        :return:
        """
        with open(f"配套代码/{fileName}", "r", encoding="utf-8") as f:
            code_txt = f.read()
        self.content_data.append(
            {"id": self.Number, "type": "Code", "data": {"desc": f"{desc}", "code": f"{code_txt}", "type": "oj"}})
        self.Number += 1

    @decoration
    def 弹出知识卡(self, Text_list: list):
        """

        :param Text_list:获得「知识卡」：数组
        :return:
        """
        if len(Text_list) > 5:
            print(f"知识卡片数量超过不能超过5个,现在添加卡片数量{len(Text_list)}。")
        else:
            self.content_data.append({"id": self.Number, "type": "Notice", "data": {"text": Text_list, "type": "info"}})
            self.Number += 1

    @decoration
    def 代码消息NumPy_需添加附件(self, desc, fileName, attachements_name):
        """

        :param attachements_name: 附件名称
        :param desc: 描述信息
        :param fileName: 读取的文件名称
        :return:
        """
        with open(f"配套代码/{fileName}", "r", encoding="utf-8") as f:
            code_txt = f.read()
        attachments = [{
            "name": attachements_name,
            "path": f"/data/files/numpy/{attachements_name}"
        }]
        self.content_data.append(
            {"id": self.Number, "type": "Code", "data": {"desc": f"{desc}",
                                                         "code": f"{code_txt}",
                                                         "type": "oj",
                                                         "attachments": attachments
                                                         }})
        self.Number += 1

    @decoration
    def 文本消息跳转站外(self, Text: str, keyword, keyword_url, Time=-1):
        """

        :param keyword_url: 关键词url
        :param Time: 单位是秒默认不用填或者填 -1 ， 0 的话立即弹下一条。
        :param Text: 文本内容
        :param keyword: 关键词替换HTML代码
        :return:
        """
        Text = Text.replace(keyword, f"<a href=\"{keyword_url}\" target=\"_blank\" >{keyword}</a>")
        self.content_data.append({"id": self.Number, "type": "Text", "data": {"time": Time, "text": f"{Text}"}})
        self.Number += 1
    def 代码消息(self, desc, fileName, code_type="oj", image="", fill=""):
        """代码消息

        :param fill: fill="manual" 就会显示手动敲，如果不填，则默认敲好不想给代码，则 code 留空
        :param image: 图片url地址
        :param code_type: CodeMessage 两种类型，oj 和 code_type="browser"浏览器模式turtle题型使用
        :param desc: 描述信息
        :param fileName: 读取的文件名称
        :return:
        """

        with open(f"配套代码/{fileName}", "r", encoding="utf-8") as f:
            code_txt = f.read()
        message = {
            "id": self.Number,
            "type": "Code",
            "data": {"desc": f"{desc}",
                     "code": f"{code_txt}",
                     "type": code_type,
                     "image": image,
                     "fill": fill}}
        self.content_data.append(message)
        self.Number += 1
