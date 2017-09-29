#coding=utf-8
from wxpy import *
from wechat_sender import *
import os
import random

bot = Bot(cache_path=True)
my_friend = bot.friends().search(u'苏裕')[0]
my_group = bot.groups().search(u'万安')[0]
bot.file_helper.send('Hello WeChat!')
myself = bot.self


class MsgInfo:
    sender = u''
    group_sender = u''
    msg = u''
    def __init__(self,msg):
        print msg.text
        self.sender = msg.sender 
        self.group_sender = msg.member
        self.msg = msg.text

def parserfile(filename):
    fp=open(filename,"ro")
    lines = fp.readlines()
    remsg = u""
    for line in lines:
        words = line.split(' ')
        for word in words:
            remsg = remsg + word + "\n"
    print "here"
    return remsg

def parsermsg(msg):
    if(msg.type == RECORDING):
        msg.get_file("./Recoding/"+msg.file_name)
        return 
    if(msg.type == PICTURE):
        msg.get_file("./Image/"+msg.file_name)
        imagefile = os.listdir("./Image/")
        return "@img@./Image/"+random.choice(imagefile)
    elif(msg.type == SHARING):
        print msg.url.encode('utf8')
        return 
    elif(msg.type == TEXT):
        info = MsgInfo(msg)
        if(msg.member != None): #funmode return
            if(info.msg == u'I need some color see see!'):
                return "@img@./Image/yellow.png"
            else:
                return
        else:
            return info.msg; #workmode return
    #info.msg

#working mode
@bot.register(bot.file_helper,None,False)
def print_messages(msg):
       print(msg)
       newmsg = parsermsg(msg)
       if (newmsg == None):
           return
       #cmd = newmsg + ">.tmp"
       #os.system(cmd)
       #remsg = parserfile(".tmp")
       #bot.file_helper.send(remsg)
       bot.file_helper.send(newmsg)
       return

#fun mode
@bot.register(my_group,None,False)
def cmdParser(msg):
    #if not msg.is_at:
    #    return
    #else:       
        print msg
        newmsg = parsermsg(msg)
        if (newmsg == None):
            return
        print newmsg
        return newmsg

#embed()
listen(bot)

