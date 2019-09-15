from cqhttp_extend import CQHttp, Error


bot = CQHttp(api_root='http://127.0.0.1:5700/',
             access_token='123',
             secret='114514')

@bot.on_message()
def handle_msg(context):
    # on_message 装饰器仍能正常使用
    '''
    try:
        bot.send(context, '你好呀，下面一条是你刚刚发的：')
    except Error:
        pass
    return {'reply': context['message'],
            'at_sender': False}  # 返回给 HTTP API 插件，走快速回复途径
    '''
    pass

@bot.MsgRoutes.route('hello')
def _(context):
    bot.send(context,'你好')

@bot.MsgRoutes.groupRoute('测试')
def _(context):
    bot.send(context,'群消息测试成功')

@bot.on_notice('group_increase')  # 如果插件版本是 3.x，这里需要使用 @bot.on_event
def handle_group_increase(context):
    info = bot.get_group_member_info(group_id=context.group_id,
                                     user_id=context.user_id)
    nickname = info['nickname']
    name = nickname if nickname else '新人'
    bot.send(context, message='欢迎{}～'.format(name))


@bot.on_request('group')
def handle_group_request(context):
    if context['comment'] != 'some-secret':
        # 如果插件版本是 3.x，这里需要使用 context.message
        # 验证信息不符，拒绝
        return {'approve': False, 'reason': '你填写的验证信息有误'}
    return {'approve': True}


bot.run(host='127.0.0.1', port=5000)
