import json


class Message(object):
    def __init__(self):
        """content json消息文件"""
        self.content = {"content": []}
        self.content_data = self.content["content"]

    def 生成消息文件(self, number):
        """生成消息文件

        :param number: 生成的文件名称
        :return:
        """
        with open(f"content{number}.json", "w", encoding="utf-8")as f:
            f.write(json.dumps(self.content, ensure_ascii=False, indent=4))


class MessageCommon(Message):
    """子类继承，Message"""

    def 选择同桌(self, number):
        """选择同桌

        :param number: 消息ID
        :return:
        """
        message = {
            "id": number,
            "type": "MatchUser",
            "data": {}
        }
        self.content_data.append(message)

    def 文本消息(self, number, Next, Text: str, Time=-1):
        """文本消息

        :param Next: 分支DI
        :param number: 消息ID
        :param Time: 单位是秒默认不用填或者填 -1 ， 0 的话立即弹下一条。
        :param Text: 文本内容
        :return:
        """
        message = {
            "id": number,
            "type": "Text",
            "data": {"time": Time,
                     "text": f"{Text}"},
            "next": Next}
        self.content_data.append(message)

    def 视频消息(self, number, Next, video_url: str):
        """视频消息

        :param Next: 分支ID
        :param number: 消息ID
        :param video_url: 视频地址
        :return:
        """
        message = {
            "id": number,
            "type": "Video",
            "data": {"src": f"{video_url}"},
            "next": Next}
        self.content_data.append(message)

    def 图片消息(self, number, Next, img_url: str):
        """图片消息

        :param Next: 分支ID
        :param number: 消息ID
        :param img_url: 图片地址
        :return:
        """
        message = {
            "id": number,
            "type": "Image",
            "data": {"src": f"{img_url}"},
            "next": Next}
        self.content_data.append(message)

    def 课后快速选择题(self, number, Next, choices: int):
        """课后快速选择题

        :param Next: 分支ID
        :param number: 消息ID
        :param choices: 题库题号
        :return:
        """
        message = {
            "id": number,
            "type": "QuickSelect",
            "data": {"limit": 20,
                     "choice": choices},
            "next": Next}
        self.content_data.append(message)

    def 课后单选题(self, number, Next, choices: list, limit):
        """课后单选题

        :param Next: 分支ID
        :param number: 消息ID
        :param limit: 答题时间
        :param choices: 题号-列表传入
        :return:
        """
        message = {
            "id": number,
            "type": "QuickChoices",
            "data": {"limit": limit,
                     "choices": choices},
            "next": Next}
        self.content_data.append(message)

    def 程序设计题(self, number, Next, problem: int):
        """程序设计题

        :param Next: 分支ID
        :param number: 消息ID
        :param problem: 题号
        :return:
        """
        message = {
            "id": number,
            "type": "Programming",
            "data": {"problem": problem},
            "next": Next}
        self.content_data.append(message)

    def pk(self, number, Next, universityName: str, image_url: str):
        """pk消息

        :param Next: 分支ID
        :param number: 消息ID
        :param universityName: 学校名称
        :param image_url: 学校图片
        :return:
        """
        with open(f"菜谱/{universityName}.txt", "r", encoding="utf-8") as f:
            cookbook = f.read()
        universityName = universityName.split(".")[1]
        for i in range(100):
            universityName = universityName.replace(f"{i}", "")
        message = {"id": number,
                   "type": "Pk",
                   "data": {"type": "set",
                            "name": universityName,
                            "image": image_url,
                            "cookbook": cookbook,
                            "winNoty": f"解锁积木「菜谱」：{universityName}",
                            "failNoty": ""},
                   "next": Next}
        self.content_data.append(message)

    def 代码消息(self, number, Next, desc, fileName, code_type="oj", image="", fill=""):
        """代码消息

        :param fill: fill="manual" 就会显示手动敲，如果不填，则默认敲好不想给代码，则 code 留空
        :param image: 图片url地址
        :param code_type: CodeMessage 两种类型，oj 和 code_type="browser"浏览器模式turtle题型使用
        :param Next: 分支ID
        :param number: 消息ID
        :param desc: 描述信息
        :param fileName: 读取的文件名称
        :return:
        """

        with open(f"配套代码/{fileName}", "r", encoding="utf-8") as f:
            code_txt = f.read()
        message = {
            "id": number,
            "type": "Code",
            "data": {"desc": f"{desc}",
                     "code": f"{code_txt}",
                     "type": code_type,
                     "image": image,
                     "fill": fill},
            "next": Next}
        self.content_data.append(message)

    def 弹出知识卡(self, number, Next, Text_list: list):
        """弹出知识卡

        :param Next: 分支ID
        :param number: 消息ID
        :param Text_list: 获得「知识卡」：数组
        :return:
        """
        if len(Text_list) > 5:
            print(f"知识卡片数量超过不能超过5个,现在添加卡片数量{len(Text_list)}。")
        else:
            message = {
                "id": number,
                "type": "Notice",
                "data": {"text": Text_list,
                         "type": "info"},
                "next": Next}
            self.content_data.append(message)

    def 代码消息附件(self, number, Next, desc, fileName, attachements_name, code_type="oj", image="", fill=""):
        """代码消息附件

        :param fill: fill="manual" 就会显示手动敲，如果不填，则默认敲好不想给代码，则 code 留空
        :param image: 图片url地址
        :param code_type: CodeMessage 两种类型，oj 和 code_type="browser"
        :param Next: 分支ID
        :param number: 消息ID
        :param attachements_name: 附件名称
        :param desc: 描述信息
        :param fileName: 读取的文件名称
        :return:
        """
        with open(f"配套代码/{fileName}", "r", encoding="utf-8") as f:
            code_txt = f.read()
        attachments = [{
            "name": attachements_name,
            "path": f"/data/files/course/{attachements_name}"
        }]
        message = {"id": number,
                   "type": "Code",
                   "data": {"desc": f"{desc}",
                            "code": f"{code_txt}",
                            "type": code_type,
                            "image": image,
                            "fill": fill,
                            "attachments": attachments},
                   "next": Next}
        self.content_data.append(message)

    def 文本消息跳转站外(self, number, Next, Text: str, keyword, keyword_url, Time=-1):
        """文本消息跳转站外

        :param Next: 分支ID
        :param number: 消息ID
        :param keyword_url: 关键词url
        :param Time: 单位是秒默认不用填或者填 -1 ， 0 的话立即弹下一条。
        :param Text: 文本内容
        :param keyword: 关键词替换HTML代码
        :return:
        """
        Text = Text.replace(keyword, f"<a href=\"{keyword_url}\" target=\"_blank\" >{keyword}</a>")
        message = {
            "id": number,
            "type": "Text",
            "data": {"time": Time,
                     "text": f"{Text}"},
            "next": Next}
        self.content_data.append(message)

    def 分支消息(self, number, Text, branches_dict: dict):
        """

        :param number: 消息ID
        :param Text: 分支问题
        :param branches_dict: 分支选项和跳转ID
        :return:
        """
        message = {
            "id": number,
            "type": "Branch",
            "data": {
                "text": Text,
                "branches": []}}
        branches = []
        for i in branches_dict:
            zd = {"text": i, "next": branches_dict[i]}
            branches.append(zd)
        message["data"]["branches"] = branches
        self.content_data.append(message)

    def 一级标题(self, number, text):
        message = {
            "id": number,
            "type": "Checkpoint",
            "data": {"text": text}}
        self.content_data.append(message)

    def 检查点(self, number, text):
        """断点

        :param number: 消息ID
        :param text: 断点描述信息
        :return:
        """
        message = {
            "id": number,
            "type": "Checkpoint",
            "data": {"text": text}}
        self.content_data.append(message)
