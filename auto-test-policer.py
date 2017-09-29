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

#when say "dpdp" start to work
#when say "help" repaly what is the usage
#when say "stop" stop fxxking
#fun mode(2):when say "have fun" to change fun mode
#linux shell mode(3):when say "work a moment" 
#replay
#

SWITCH = 0;

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
    global SWITCH
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
        if(info.msg == "dpdp"):
            SWITCH = 1
            return "I had an zhong see you a long time!"
        elif(info.msg == "stop"):
            SWITCH = 0
            return "I miss you very much!"
        elif(info.msg == "help"):
            return """#when say "dpdp" start to work
#when say "help" repaly what is the usage
#when say "stop" stop fxxking
#fun mode(1):when say "have fun" to change to fun mode
#linux shell mode(2):when say "work a moment" to change to shell mode 
"""
        elif(SWITCH == 1 or SWITCH == 2 or SWITCH == 3):
            #choose mode
            if(info.msg == "have fun"): #funmode return
                SWITCH = 2
                return "fxxking"
            elif(info.msg == "work a moment"):
                SWITCH = 3
                return "woking"

        #default cmd
        if(info.msg == u'I need some color see see!'):
            return "@img@./Image/yellow.png"
        if(SWITCH == 2):
            return
        elif(SWITCH == 3):
            cmd = info.msg + ">.tmp"
            os.system(cmd)
            remsg = parserfile(".tmp")
            return remsg
            #return info.msg; #workmode return
            
    #info.msg

#working mode
@bot.register(bot.file_helper,None,False)
def print_messages(msg):
    global SWITCH
    print(msg)
    newmsg = parsermsg(msg)
    if (newmsg == None):
        return
    bot.file_helper.send(newmsg)
    return

#fun mode
@bot.register(my_group,None,False)
def cmdParser(msg):
    global SWITCH
    print msg
    newmsg = parsermsg(msg)
    if (newmsg == None):
        return
    return newmsg
    

#embed()
listen(bot)

