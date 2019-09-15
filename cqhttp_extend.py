import cqhttp_helper as _cqhttp

Error = _cqhttp.Error



class CQHttp(_cqhttp.CQHttp):
    """
    **CQhttp_extend**

    :作者: Nuctori
    :参考: HTTP API v3.4 & CoolQ HTTP API Python SDK封装类
    :版本: v0.0.3

    本类在CoolQ HTTP API Python SDK封装类的基础上，添加了额外的装饰器
    @self.MsgRoutes.route
    @self.MsgRoutes.groupRoute
    @self.MsgRoutes.privateRoute
    @self.MsgRoutes.discussRoute


    感谢 **richardchien** 为我们提供了如此简便酷Q应用开发方式。
    感谢 **SuperMarioSF** 为我们提供了详尽的中文文档

    本文件使用 WTFPL 2.0 许可证发布。

    要查看HTTP API的完整在线文档，请访问：

    | https://richardchien.github.io/coolq-http-api/
    | http://richardchien.gitee.io/coolq-http-api/docs/

    ------------

    **使用本文件**

    你可以将本文件作为导入 cqhttp 包的替代来使用。
    但需要注意，本文件需要你的 Python 环境中能够导入原 cqhttp 包，因为本文件只是对 cqhttp_helper 包的封装。
    将原先导入 cqhttp 包的写法:

    >>> from cqhttp import CQHttp, Error
    或
    >>> from cqhttp_helper import CQHttp, Error

    更换成:

    >>> from cqhttp_extend import CQHttp, Error

    即可使用额外功能

    ------------
    """

    _on_message = None

    def __init__(self, api_root=None, access_token=None, secret=None):
        super().__init__(api_root=api_root, access_token=access_token, secret=secret)
        self._handlers['message']['*'] = self.msg_handel
        self.MsgRoutes = MsgRoutes


    @classmethod
    def on_message(self):
        def decorate(func):
            self._on_message = func
            print(func)
            return func
        return decorate

    def msg_handel(self,context):
        self.MsgRoutes.Instruction(context)
        if self._on_message:
            self._on_message()



class MsgRoutes():
    privateRoutes = {}
    groupRoutes = {}
    discussRoutes = {}
    Routes = {}

    @classmethod
    def route(cls,key:str):
        '''
        路由装饰器，通过装饰器定义指令
        '''
        def decorate(func):
            if key:
                cls.Routes[key] = func
            return func
        return decorate

    @classmethod
    def groupRoute(cls,key:str):
        def decorate(func):
            if key:
                cls.groupRoutes[key] = func
            return func
        return decorate

    @classmethod
    def privateRoute(cls,key:str):
        def decorate(func):
            if key:
                cls.privateRoutes[key] = func
            return func
        return decorate

    @classmethod
    def discussRoute(cls,key:str):
        def decorate(func):
            if key:
                cls.discussRoutes[key] = func
            return func
        return decorate

    @classmethod
    def Instruction(cls,context):
        '''
        指令判断及执行程序
        '''
        message_type = context['message_type']
        raw_message = context['raw_message']
        def matching(routes):
            for route in routes.keys():
                if route in raw_message:
                    func = routes[route]
                    return func(context)

            if "*" in cls.Routes:
                return cls.Routes["*"](context)
            else:
                return None

        routes = cls.Routes.copy()
        if message_type == 'private':
            routes.update(cls.privateRoutes)
        elif message_type == 'group':
            routes.update(cls.groupRoutes)
        elif message_type == 'discuss':
            routes.update(cls.discussRoutes)
        
        return matching(routes)
