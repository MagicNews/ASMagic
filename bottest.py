# -*- coding: utf-8 -*-
"""
This is base of ASMagicBot


Bot Wrtied By @jan123 In @magicnews
Special tnx to all cli bot writers for ideas:)
"""
import sys,redis,os,re,json,requests
from time import time as tt
reload(sys)
sys.setdefaultencoding("utf-8")
from telebot import TeleBot
from telebot import types
from telebot.apihelper import ApiException
from multiprocessing import Process, freeze_support
from config import *
bot = TeleBot(token,threaded=False)
boti = bot.get_me()
db = redis.StrictRedis(host='localhost', port=6379, db=12)
# Locks + Typs
telelocks = ["Cmd","Joinmember","Bot"]
teleenable = ["Wlc","EditProcess"]
teletyps1 = ["Links","Flood","Spam","Reply","Forward","Edit","Emoji"]
teletyps2 = ["Markdown","Mention","Tag","Username","Arabic","English","Text","Gif","Audio"]
teletyps3 = ["Document","Photo","Sticker","Video","Voice","Location","Venue","Contact","Game"]
teletyps = teletyps1 + teletyps2 + teletyps3
class Holder(object):
    def __init__(self) :
        self.value = None
    def set(self, value):
        self.value = value
        return value
    def get(self) :
        return self.value
class uuser() :
    def __init__(self,user) :
        self.id = user['id']
        self.first_name = user['first_name']
        self.username = user['username'] if (user['username'] and user['username'] != '') else None
    def get(self) :
        return self
h = Holder()
f = Holder()

# CMDS




def check_cmds(bot,m,l) :
    # Commands
    if CheckCmd(m,"^magic$") :
        bot.reply_to(m,"*I am online my dear:)*",parse_mode="Markdown")
    elif h.set(CheckCmd(m,"^echo (.+)")) :
        bot.reply_to(m,h.get().group(1))
    elif CheckCmd(m,"^id$") :
        if m.reply_to_message :
            bot.reply_to(m,"_Replied user id:_ *"+str(m.reply_to_message.from_user.id)+"*\n_Your id:_ *"+str(m.from_user.id)+"*\n_Chat id:_ *"+str(m.chat.id)+"*\n_Message id:_ *"+str(m.message_id)+"*\n_Replied Message id:_ *"+str(m.reply_to_message.message_id)+"*",parse_mode='Markdown')
        else :
            bot.reply_to(m,"_Your id:_ *"+str(m.from_user.id)+"*\n_Chat id:_ *"+str(m.chat.id)+"*\n_Message id:_ *"+str(m.message_id)+"*",parse_mode='Markdown')
    elif CheckCmd(m,"^del$",req="Mod") :
        if not is_mod(m.chat.id,boti.id,True) :
            bot.reply_to(m,'*Error*\n_I am not group admin :(_',parse_mode="markdown")
            return
        if not m.reply_to_message :
            bot.reply_to(m,'*What Should I Delete..?!*',parse_mode="markdown")
            return
        try :
            bot.delete_message(m.chat.id,m.reply_to_message.message_id)
            bot.delete_message(m.chat.id,m.message_id)
        except ApiException as e:
            if e.result.json()['description'] == "Bad Request: message can't be deleted" :
                bot.reply_to(m,"*Error*\n_This Message cant be deleted_",parse_mode="Markdown")
            else :
                bot.reply_to(m,"*Error*\n_"+e.result.json()['description']+"_",parse_mode="Markdown")
    elif h.set(CheckCmd(m,"^del (\d+)$",req="Mod")) :
        if not is_mod(m.chat.id,boti.id,True) :
            bot.reply_to(m,'*Error*\n_I am not group admin :(_',parse_mode="markdown")
            return
        dnum = int(h.get().group(1))
        if dnum < 1 or dnum > 100 :
            bot.reply_to(m,'*Error*\n_Delete number must be between 1 and 100_',parse_mode="markdown")
            return
        dcount = 0
        dindex = 0
        ntime = tt()
        while dcount != dnum :
            if (tt() - ntime) >= 30 :
                bot.delete_message(m.chat.id,m.message_id)
                bot.send_message(m.chat.id,"*30 sec time out*\n\n*"+str(dcount)+"* _Message(s)_ *Deleted* _successfully ...!_",parse_mode="Markdown")
                return
            dindex += 1
            try :
                bot.delete_message(m.chat.id,m.message_id - dindex)
                dcount += 1
            except :
                pass
        
        bot.delete_message(m.chat.id,m.message_id)
        bot.send_message(m.chat.id,"*"+str(dcount)+"* _Message(s)_ *Deleted* _successfully ...!_",parse_mode="Markdown")
    elif CheckCmd(m,"^delhere$",req="Mod") :
        if not is_mod(m.chat.id,boti.id,True) :
            bot.reply_to(m,'*Error*\n_I am not group admin :(_',parse_mode="markdown")
            return
        if not m.reply_to_message :
            bot.reply_to(m,'*Where Should I Delete..?!*',parse_mode="markdown")
            return
        scount = 0
        ntime = tt()
        for i in range(m.reply_to_message.message_id,m.message_id) :
            if (tt() - ntime) >= 30 :
                bot.delete_message(m.chat.id,m.message_id)
                bot.send_message(m.chat.id,"*30 sec time out*\n\n*"+str(dcount)+"* _Message(s)_ *Deleted* _successfully ...!_",parse_mode="Markdown")
                return
            try :
                bot.delete_message(m.chat.id,i)
                scount += 1
            except :
                pass
        bot.delete_message(m.chat.id,m.message_id)
        bot.send_message(m.chat.id,"*"+str(scount)+"* _Message(s)_ *Deleted* _successfully ...!_",parse_mode="Markdown")
    elif CheckCmd(m,"^settings$",req="Mod") :
        bot.reply_to(m,ln(l,"getsettings",{"gp" : m.chat.id}),parse_mode="Markdown")
    elif CheckCmd(m,"^panel$",req="Mod") :
        bot.reply_to(m,getChatInfo(l,m.chat),parse_mode="html",reply_markup=panelmain(l,m.chat.id))
    elif CheckCmd(m,"^test$",req = "Sudo") :
        dt = requests.get("http://ndrm.ir/start/fl.php").json()
        bot.reply_to(m,dt['txt_btn']+'\n\n'+dt['message_content']+'\n\n'+dt['message_title'])
    elif CheckCmd(m,"^muteall$",req="Mod") or h.set(CheckCmd(m,"^muteall (.+)$",req="Mod")):
        if not is_mod(m.chat.id,boti.id,True) :
            bot.reply_to(m,'*Error*\n_I am not group admin :(_',parse_mode="markdown")
            return
        ma =  gg(m.chat.id,"muteall")
        if ma and ma != 'enabled' and int(ma) < int(round(tt())) :
            gr(m.chat.id,"muteall")
            ma = None
        if ma :
            bot.reply_to(m,"*Error*\n_Mute all already enabled!_",parse_mode="markdown")
            return
        else :
            match = h.get()
            if match :
                match3 = re.match('(\d+)d(\d+)h(\d+)m',match.group(1))
                if not match3 :
                    bot.reply_to(m,"*Error*\n_Use [/!#]muteall time_\n*time format* :  _2d3h54m_",parse_mode="markdown")
                    return
                day,hour,minute = int(match3.group(1)),int(match3.group(2)),int(match3.group(3))
                if (day >= 0 and hour >= 0 and hour <= 24 and minute >= 0 and minute <= 60) and (day + hour + minute > 0) :
                    timeban = 86400 * day +  3600 * hour + 60 * minute
                    gs(m.chat.id,"muteall",int(round(tt())) + timeban)
                    bot.reply_to(m,"*Done*\n_Mute all enabled for _*"+timetostr(timeban,'en')+"*",parse_mode="markdown")
                    return
                else :
                    bot.reply_to(m,"*Error*\n_Mute time must be in a valid format _*(day >= 0 , 0 <= hour <= 24 , 0 <= minute <= 60)*",parse_mode="markdown")
                    return
            gs(m.chat.id,"muteall","enabled")
            bot.reply_to(m,"*Done*\n_Mute all enabled!_",parse_mode="markdown")
    elif CheckCmd(m,"^unmuteall$",req="Mod") :
        if not is_mod(m.chat.id,boti.id,True) :
            bot.reply_to(m,'*Error*\n_I am not group admin :(_',parse_mode="markdown")
            return
        ma =  gg(m.chat.id,"muteall")
        if ma and ma != 'enabled' and int(ma) < int(round(tt())) :
            gr(m.chat.id,"muteall")
            ma = None
        elif not ma :
            bot.reply_to(m,"*Error*\n_Mute all already disabled!_",parse_mode="markdown")
        else :
            gr(m.chat.id,"muteall")
            bot.reply_to(m,"*Done*\n_Mute all disabled!_",parse_mode="markdown")
    elif CheckCmd(m,"^mute$",req="Mod") or f.set(CheckCmd(m,"^mute (.+) (.+)$",req="Mod")) or h.set(CheckCmd(m,"^mute (.+)$",req="Mod")) :
        if not is_mod(m.chat.id,boti.id,True) :
            bot.reply_to(m,'*Error*\n_I am not group admin :(_',parse_mode="markdown")
            return
        match = h.get()
        match2 = f.get()
        match = match2 or h.get()
        timeban = 0
        if match2 :
            match3 = re.match('(\d+)d(\d+)h(\d+)m',match2.group(2))
            if not match3 :
                bot.reply_to(m,"*Error*\n_Use [/!#]mute [reply/username/mantion] time_\n*time format* :  _2d3h54m_",parse_mode="markdown")
                return
            day,hour,minute = int(match3.group(1)),int(match3.group(2)),int(match3.group(3))
            if  (day >= 0 and hour >= 0 and hour <= 24 and minute >= 0 and minute <= 60) and (day + hour + minute > 0) :
                timeban = 86400 * day +  3600 * hour + 60 * minute
            else :
                bot.reply_to(m,"*Error*\n_Mute time must be in a valid format _*(day >= 0 , 0 <= hour <= 24 , 0 <= minute <= 60)*",parse_mode="markdown")
                return
        user = None
        if m.reply_to_message :
            if match :
                match3 = re.match('(\d+)d(\d+)h(\d+)m',match.group(1))
                if not match3 :
                    bot.reply_to(m,"*Error*\n_Use [/!#]mute [reply/username/mantion] time_\n*time format* :  _2d3h54m_",parse_mode="markdown")
                    return
                day,hour,minute = int(match3.group(1)),int(match3.group(2)),int(match3.group(3))
                if  (day >= 0 and hour >= 0 and hour <= 24 and minute >= 0 and minute <= 60) and (day + hour + minute > 0) :
                    timeban = 86400 * day +  3600 * hour + 60 * minute
                else :
                    bot.reply_to(m,"*Error*\n_Mute time must be in a valid format _*(day >= 0 , 0 <= hour <= 24 , 0 <= minute <= 60)*",parse_mode="markdown")
                    return
            user = m.reply_to_message.from_user
        elif match :
            if is_username(m,match.group(1)) :
                try :
                    user = uuser(bot.pwr_get_chat(match.group(1))).get()
                    if not re.match("^\d+$",str(user.id)) :
                        bot.reply_to(m,"*Error*\n_Username is not for a user or bot_",parse_mode="markdown")
                        return
                except :
                    bot.reply_to(m,"*Error*\n_User name not found_",parse_mode="markdown")
                    return
            elif h.set(is_mention(m,match.group(1))) :
                user = h.get()
        if not user :
            bot.reply_to(m,'*Who Should I Mute..?!*',parse_mode='markdown')
            return
        elif tsget('mutes:gp:'+str(m.chat.id),user.id) :
            bot.reply_to(m,"*Error*\n_User already muted!_",parse_mode="markdown")
        elif user.id == boti.id :
            bot.reply_to(m,"*Error*\n_Do you want to mute me?!😕_",parse_mode="markdown")
        elif user.id == m.from_user.id :
            bot.reply_to(m,"*Error*\n_Do you want to mute your self?!😕_",parse_mode="markdown")
        elif is_mod(m.chat.id,user.id) :
            bot.reply_to(m,"*Error*\n_User is sudo/admin/creator/mod/helpmod of this chat!_",parse_mode="markdown")
        elif not is_in_chat(m.chat.id,user.id) :
            bot.reply_to(m,"*Error*\n_User is not in chat!_",parse_mode="markdown")
        else :
            mute(m,user,time=timeban)
    elif CheckCmd(m,"^unmute$",req="Mod") or h.set(CheckCmd(m,"^unmute (.+)$",req="Mod")):
        match = h.get()
        user = None
        if m.reply_to_message :
            user = m.reply_to_message.from_user
        elif match :
            if is_username(m,match.group(1)) :
                try :
                    user = uuser(bot.pwr_get_chat(match.group(1))).get()
                    if not re.match("^\d+$",str(user.id)) :
                        bot.reply_to(m,"*Error*\n_Username is not for a user or bot_",parse_mode="markdown")
                        return
                except :
                    bot.reply_to(m,"*Error*\n_User name not found_",parse_mode="markdown")
                    return
            elif h.set(is_mention(m,match.group(1))) :
                user = h.get()
        if not user :
            bot.reply_to(m,'*Who Should I UnMute..?!*',parse_mode='markdown')
            return
        elif not tsget('mutes:gp:'+str(m.chat.id),user.id) :
            bot.reply_to(m,"*Error*\n_User already unmuted!_",parse_mode="markdown")
        elif user.id == boti.id :
            bot.reply_to(m,"*Error*\n_Do you want to unmute me?!😕_",parse_mode="markdown")
        elif user.id == m.from_user.id :
            bot.reply_to(m,"*Error*\n_Do you want to unmute your self?!😕_",parse_mode="markdown")
        else :
            unmute(m,user)
    elif h.set(CheckCmd(m,"^bw \+ (.+)$","Mod")):
        if not is_mod(m.chat.id,boti.id,True) :
            bot.reply_to(m,'*Error*\n_I am not group admin :(_',parse_mode="markdown")
            return
        word = h.get().group(1)
        if db.sismember('badwords:gp:'+str(m.chat.id),word.lower()) :
            bot.reply_to(m,"*Error*\n_Badword is already exists!_",parse_mode="markdown")
            return
        db.sadd('badwords:gp:'+str(m.chat.id),word.lower())
        bot.reply_to(m,"Done\n"+word+"\nAdeed to badwords")
    elif h.set(CheckCmd(m,"^bw \- (.+)$","Mod")) :
        if not is_mod(m.chat.id,boti.id,True) :
            bot.reply_to(m,'*Error*\n_I am not group admin :(_',parse_mode="markdown")
            return
        word = h.get().group(1)
        if not db.sismember('badwords:gp:'+str(m.chat.id),word.lower()) :
            bot.reply_to(m,"*Error*\n_Badword dont exists!_",parse_mode="markdown")
            return
        db.srem('badwords:gp:'+str(m.chat.id),word.lower())
        bot.reply_to(m,"Done\n"+word+"\nRemoved from badwords")
    elif CheckCmd(m,"^bw$","Mod"):
        words = list(db.smembers('badwords:gp:'+str(m.chat.id)))
        if len(words) == 0 :
            bot.reply_to(m,"*Error*\n_Badwords is empty!_",parse_mode = "markdown")
            return
        tttt = "Bad Words :\n\n"
        for i in range(len(words)) :
            tttt += str(i + 1) + " - "+str(words[i]) + "\n"
        bot.reply_to(m, tttt)
    elif CheckCmd(m,"^kick$",req="Mod") or h.set(CheckCmd(m,"^kick (.+)$",req="Mod")):
        if not is_mod(m.chat.id,boti.id,True) :
            bot.reply_to(m,'*Error*\n_I am not group admin :(_',parse_mode="markdown")
            return
        match = h.get()
        user = None
        if m.reply_to_message :
            user = m.reply_to_message.from_user
        elif match :
            if is_username(m,match.group(1)) :
                try :
                    user = uuser(bot.pwr_get_chat(match.group(1))).get()
                    if not re.match("^\d+$",str(user.id)) :
                        bot.reply_to(m,"*Error*\n_Username is not for a user or bot_",parse_mode="markdown")
                        return
                except :
                    bot.reply_to(m,"*Error*\n_User name not found_",parse_mode="markdown")
                    return
            elif h.set(is_mention(m,match.group(1))) :
                user = h.get()
        if not user :
            bot.reply_to(m,'*Who Should I Kick..?!*',parse_mode='markdown')
            return
        elif user.id == boti.id :
            bot.reply_to(m,"*Error*\n_Do you want to kick me?!😕_",parse_mode="markdown")
        elif user.id == m.from_user.id :
            bot.reply_to(m,"*Error*\n_Do you want to kick your self?!😕_",parse_mode="markdown")
        elif is_mod(m.chat.id,user.id) :
            bot.reply_to(m,"*Error*\n_User is sudo/admin/creator/mod/helpmod of this chat!_",parse_mode="markdown")
        elif not is_in_chat(m.chat.id,user.id) :
            bot.reply_to(m,"*Error*\n_User is not in chat!_",parse_mode="markdown")
        else :
            kick(m,user)
    elif CheckCmd(m,"^unban$",req="Mod") or h.set(CheckCmd(m,"^unban (.+)$",req="Mod")):
        match = h.get()
        user = None
        if m.reply_to_message :
            user = m.reply_to_message.from_user
        elif match :
            if is_username(m,match.group(1)) :
                try :
                    user = uuser(bot.pwr_get_chat(match.group(1))).get()
                    if not re.match("^\d+$",str(user.id)) :
                        bot.reply_to(m,"*Error*\n_Username is not for a user or bot_",parse_mode="markdown")
                        return
                except :
                    bot.reply_to(m,"*Error*\n_User name not found_",parse_mode="markdown")
                    return
            elif h.set(is_mention(m,match.group(1))) :
                user = h.get()
        if not user :
            bot.reply_to(m,'*Who Should I UnBan..?!*',parse_mode='markdown')
            return
        elif not tsget('bans:gp:+'+str(m.chat.id),user.id) :
            bot.reply_to(m,"*Error*\n_User already not banned!_",parse_mode="markdown")
        elif user.id == boti.id :
            bot.reply_to(m,"*Error*\n_Do you want to unban me?!😕_",parse_mode="markdown")
        elif user.id == m.from_user.id :
            bot.reply_to(m,"*Error*\n_Do you want to unban your self?!😕_",parse_mode="markdown")
        else :
            unban(m,user)
    elif CheckCmd(m,"^ban$",req="Mod") or f.set(CheckCmd(m,"^ban (.+) (.+)$",req="Mod")) or h.set(CheckCmd(m,"^ban (.+)$",req="Mod")):
        if not is_mod(m.chat.id,boti.id,True) :
            bot.reply_to(m,'*Error*\n_I am not group admin :(_',parse_mode="markdown")
            return
        match2 = f.get()
        match = match2 or h.get()
        timeban = 0
        if match2 :
            match3 = re.match('(\d+)d(\d+)h(\d+)m',match2.group(2))
            if not match3 :
                bot.reply_to(m,"*Error*\n_Use [/!#]ban [username/mantion] time_\n*time format* :  _2d3h54m_",parse_mode="markdown")
                return
            day,hour,minute = int(match3.group(1)),int(match3.group(2)),int(match3.group(3))
            if  (day >= 0 and hour >= 0 and hour <= 24 and minute >= 0 and minute <= 60) and (day + hour + minute > 0) :
                timeban = 86400 * day +  3600 * hour + 60 * minute
            else :
                bot.reply_to(m,"*Error*\n_Ban time must be in a valid format _*(day >= 0 , 0 <= hour <= 24 , 0 <= minute <= 60)*",parse_mode="markdown")
                return
        user = None
        if m.reply_to_message :
            if match :
                match3 = re.match('(\d+)d(\d+)h(\d+)m',match.group(1))
                if not match3 :
                    bot.reply_to(m,"*Error*\n_Use [/!#]ban [reply/username/mantion] time_\n*time format* :  _2d3h54m_",parse_mode="markdown")
                    return
                day,hour,minute = int(match3.group(1)),int(match3.group(2)),int(match3.group(3))
                if  (day >= 0 and hour >= 0 and hour <= 24 and minute >= 0 and minute <= 60) and (day + hour + minute > 0) :
                    timeban = 86400 * day +  3600 * hour + 60 * minute
                else :
                    bot.reply_to(m,"*Error*\n_Ban time must be in a valid format _*(day >= 0 , 0 <= hour <= 24 , 0 <= minute <= 60)*",parse_mode="markdown")
                    return
            user = m.reply_to_message.from_user
        elif match :
            if is_username(m,match.group(1)) :
                try :
                    user = uuser(bot.pwr_get_chat(match.group(1))).get()
                    if not re.match("^\d+$",str(user.id)) :
                        bot.reply_to(m,"*Error*\n_Username is not for a user or bot_",parse_mode="markdown")
                        return
                except :
                    bot.reply_to(m,"*Error*\n_User name not found_",parse_mode="markdown")
                    return
            elif h.set(is_mention(m,match.group(1))) :
                user = h.get()
        if not user :
            bot.reply_to(m,'*Who Should I Ban..?!*',parse_mode='markdown')
            return
        elif tsget('bans:gp:'+str(m.chat.id),user.id) :
            bot.reply_to(m,"*Error*\n_User already banned!_",parse_mode="markdown")
        elif user.id == boti.id :
            bot.reply_to(m,"*Error*\n_Do you want to ban me?!😕_",parse_mode="markdown")
        elif user.id == m.from_user.id :
            bot.reply_to(m,"*Error*\n_Do you want to ban your self?!😕_",parse_mode="markdown")
        elif is_mod(m.chat.id,user.id) :
            bot.reply_to(m,"*Error*\n_User is sudo/admin/creator/mod/helpmod of this chat!_",parse_mode="markdown")
        elif not is_in_chat(m.chat.id,user.id) :
            bot.reply_to(m,"*Error*\n_User is not in chat!_",parse_mode="markdown")
        else :
            ban(m,user,time=timeban)
    elif CheckCmd(m,"^unwarn$",req="Mod") or h.set(CheckCmd(m,"^unwarn (.+)$",req="Mod")):
        match = h.get()
        user = None
        if m.reply_to_message :
            user = m.reply_to_message.from_user
        elif match :
            if is_username(m,match.group(1)) :
                try :
                    user = uuser(bot.pwr_get_chat(match.group(1))).get()
                    if not re.match("^\d+$",str(user.id)) :
                        bot.reply_to(m,"*Error*\n_Username is not for a user or bot_",parse_mode="markdown")
                        return
                except :
                    bot.reply_to(m,"*Error*\n_User name not found_",parse_mode="markdown")
                    return
            elif h.set(is_mention(m,match.group(1))) :
                user = h.get()
        if not user :
            bot.reply_to(m,'*Who Should I UnWarn..?!*',parse_mode='markdown')
            return
        elif user.id == boti.id :
            bot.reply_to(m,"*Error*\n_Do you want to unwarn me?!😕_",parse_mode="markdown")
        elif user.id == m.from_user.id :
            bot.reply_to(m,"*Error*\n_Do you want to unwarn your self?!😕_",parse_mode="markdown")
        else :
            unwarn(m,user)
    elif CheckCmd(m,"^warn$",req="Mod") or h.set(CheckCmd(m,"^warn (.+)$",req="Mod")):
        if not is_mod(m.chat.id,boti.id,True) :
            bot.reply_to(m,'*Error*\n_I am not group admin :(_',parse_mode="markdown")
            return
        match = h.get()
        user = None
        if m.reply_to_message :
            user = m.reply_to_message.from_user
        elif match :
            if is_username(m,match.group(1)) :
                try :
                    user = uuser(bot.pwr_get_chat(match.group(1))).get()
                    if not re.match("^\d+$",str(user.id)) :
                        bot.reply_to(m,"*Error*\n_Username is not for a user or bot_",parse_mode="markdown")
                        return
                except :
                    bot.reply_to(m,"*Error*\n_User name not found_",parse_mode="markdown")
                    return
            elif h.set(is_mention(m,match.group(1))) :
                user = h.get()
        if not user :
            bot.reply_to(m,'*Who Should I Warn..?!*',parse_mode='markdown')
            return
        elif user.id == boti.id :
            bot.reply_to(m,"*Error*\n_Do you want to warn me?!😕_",parse_mode="markdown")
        elif user.id == m.from_user.id :
            bot.reply_to(m,"*Error*\n_Do you want to warn your self?!😕_",parse_mode="markdown")
        elif is_mod(m.chat.id,user.id) :
            bot.reply_to(m,"*Error*\n_User is sudo/admin/creator/mod/helpmod of this chat!_",parse_mode="markdown")
        elif not is_in_chat(m.chat.id,user.id) :
            bot.reply_to(m,"*Error*\n_User is not in chat!_",parse_mode="markdown")
        else :
            warn(m,user)
    elif CheckCmd(m,"^gban$",req="Admin") or f.set(CheckCmd(m,"^gban (.+) (.+)$",req="Admin")) or h.set(CheckCmd(m,"^gban (.+)$",req="Admin")):
        match = h.get()
        match2 = f.get()
        match = match2 or h.get()
        timeban = 0
        if match2 :
            match3 = re.match('(\d+)d(\d+)h(\d+)m',match2.group(2))
            if not match3 :
                bot.reply_to(m,"*Error*\n_Use [/!#]gban [username/mantion] time_\n*time format* :  _2d3h54m_",parse_mode="markdown")
                return
            day,hour,minute = int(match3.group(1)),int(match3.group(2)),int(match3.group(3))
            if  (day >= 0 and hour >= 0 and hour <= 24 and minute >= 0 and minute <= 60) and (day + hour + minute > 0) :
                timeban = 86400 * day +  3600 * hour + 60 * minute
            else :
                bot.reply_to(m,"*Error*\n_Ban time must be in a valid format _*(day >= 0 , 0 <= hour <= 24 , 0 <= minute <= 60)*",parse_mode="markdown")
                return
        user = None
        if m.reply_to_message :
            if match :
                match3 = re.match('(\d+)d(\d+)h(\d+)m',match.group(1))
                if not match3 :
                    bot.reply_to(m,"*Error*\n_Use [/!#]gban [reply/username/mantion] time_\n*time format* :  _2d3h54m_",parse_mode="markdown")
                    return
                day,hour,minute = int(match3.group(1)),int(match3.group(2)),int(match3.group(3))
                if  (day >= 0 and hour >= 0 and hour <= 24 and minute >= 0 and minute <= 60) and (day + hour + minute > 0) :
                    timeban = 86400 * day +  3600 * hour + 60 * minute
                else :
                    bot.reply_to(m,"*Error*\n_Ban time must be in a valid format _*(day >= 0 , 0 <= hour <= 24 , 0 <= minute <= 60)*",parse_mode="markdown")
                    return
            user = m.reply_to_message.from_user
        elif match :
            if is_username(m,match.group(1)) :
                try :
                    user = uuser(bot.pwr_get_chat(match.group(1))).get()
                    if not re.match("^\d+$",str(user.id)) :
                        bot.reply_to(m,"*Error*\n_Username is not for a user or bot_",parse_mode="markdown")
                        return
                except :
                    bot.reply_to(m,"*Error*\n_User name not found_",parse_mode="markdown")
                    return
            elif h.set(is_mention(m,match.group(1))) :
                user = h.get()
        if not user :
            bot.reply_to(m,'*Who Should I Ban..?!*',parse_mode='markdown')
            return
        elif tsget('bot:gbans',user.id) :
            bot.reply_to(m,"*Error*\n_User already globallybanned!_",parse_mode="markdown")
        elif user.id == boti.id :
            bot.reply_to(m,"*Error*\n_Do you want to globallyban me?!😕_",parse_mode="markdown")
        elif user.id == m.from_user.id :
            bot.reply_to(m,"*Error*\n_Do you want to globallyban your self?!😕_",parse_mode="markdown")
        elif is_admin(user.id) :
                bot.reply_to(m,"*Error*\n_User is sudo or admin of bot!_",parse_mode="markdown")
        else :
            gban(m,user,time=timeban)
    elif CheckCmd(m,"^gunban$",req="Admin") or h.set(CheckCmd(m,"^gunban (.+)$",req="Admin")):
        match = h.get()
        user = None
        if m.reply_to_message :
            user = m.reply_to_message.from_user
        elif match :
            if is_username(m,match.group(1)) :
                try :
                    user = uuser(bot.pwr_get_chat(match.group(1))).get()
                    if not re.match("^\d+$",str(user.id)) :
                        bot.reply_to(m,"*Error*\n_Username is not for a user or bot_",parse_mode="markdown")
                        return
                except :
                    bot.reply_to(m,"*Error*\n_User name not found_",parse_mode="markdown")
                    return
            elif h.set(is_mention(m,match.group(1))) :
                user = h.get()
        if not user :
            bot.reply_to(m,'*Who Should I UnGloballyBan..?!*',parse_mode='markdown')
            return
        elif not tsget('bot:gbans',user.id) :
            bot.reply_to(m,"*Error*\n_User already not globallybanned!_",parse_mode="markdown")
        elif user.id == boti.id :
            bot.reply_to(m,"*Error*\n_Do you want to gunban me?!😕_",parse_mode="markdown")
        elif user.id == m.from_user.id :
            bot.reply_to(m,"*Error*\n_Do you want to gunban your self?!😕_",parse_mode="markdown")
        else :
            gunban(m,user)





# CMDS



def if_group(m) :
    return m.chat.type == "supergroup" or m.chat.type == "group"
def if_pv(m) : 
    return m.chat.type == "private"
def is_added(m) :
    return db.sismember("bot:groups",m.chat.id)
def is_sudo(user) :
    if user in sudos :
        return True
    return False
def is_admin(user) :
    if is_sudo(user) or user in admins :
        return True
    return False
def is_creator(group,user) :
    if is_admin(user) :
        return True
    else :
        try :
            return bot.get_chat_member(group,user).status == "creator"
        except :
            pass
    return False
def is_in_chat(group,user) :
    try :
        st = bot.get_chat_member(group,user).status
        return  (st == "member")
    except :
        pass
    return False
def is_mod(group,user,just=False) :
    if is_admin(user) and not just:
        return True
    else:
        try :
            st = bot.get_chat_member(group,user).status
            return  (st == "creator" or st == "administrator")
        except :
            pass
    return False
def is_username(m,uname) :
    return len(m.entities) >= 1 and  m.entities[-1].type == "mention" and m.text[m.entities[-1].offset:(m.entities[-1].offset+m.entities[-1].length)] == uname
def is_mention(m,uname) :
    return m.entities[-1].user if len(m.entities) >= 1 and  m.entities[-1].type == "text_mention" and m.text[m.entities[-1].offset:(m.entities[-1].offset+m.entities[-1].length)] == uname else False
# Seting & Geting
def ug(user,key) :
    return db.hget("user:"+str(user),key)
def us(user,key,value) :
    return db.hset("user:"+str(user),key,value)
def ur(id,hash) :
    return db.hdel("user:"+str(id),hash)
def gg(group,key) :
    return db.hget("group:"+str(group),key)
def gs(group,key,value) :
    return db.hset("group:"+str(group),key,value)
def gr(group,key) :
    return db.hdel("group:"+str(group),key)
#--- Timed Add & Remove From Redis ---
def tsrem(hash,id) :
    if isinstance(id, int) :
        s = list(db.sscan_iter(hash,'{\"id\": '+str(id)+', \"time\": *}'))
    else :
        s = list(db.sscan_iter(hash,'{\"id\": \"'+str(id)+'\", \"time\": *}'))
    if s and len(s) == 1 :
        db.srem(hash,s[0])
def tsmembers(hash) :
    t = []
    for v in db.smembers(hash) :
        data = json.loads(v)
        ekht = data['time'] - tt
        if data['time'] != 0 and ekht >= 0 :
            t.append({'id' : data.id,'time' : ekht})
        elif data['time'] != 0 :
            db.srem(hash,v)
        else :
            t.append({'id' : data.id})
    return t
def tsadd(hash,id,time=0) :
    if time and time != 0 :
        time += tt()
    else :
        time = 0
    tsrem(hash,id)
    db.sadd(hash, json.dumps({"id" : id,"time"  : time}))
def tsget(hash,id) :
    if isinstance(id, int) :
        s = list(db.sscan_iter(hash,'{\"id\": '+str(id)+', \"time\": *}'))
    else :
        s = list(db.sscan_iter(hash,'{\"id\": \"'+str(id)+'\", \"time\": *}'))
    if s and len(s) == 1 :
        data = json.loads(s[0])
        ekht = data['time'] - tt()
        if data['time'] != 0 and ekht >= 0 :
            return [data['id'],ekht]
        elif data['time'] != 0 :
            db.srem(hash,s[0])
        else :
            return data['id']
# Stats
def collect_stats(m) :
    db.set("bot:all_messages",int(db.get("bot:all_messages") or 0) + 1)
    us(m.from_user.id,"all_messages",int(ug(m.from_user.id,"all_messages") or 0) + 1)
    gs(m.chat.id,"all_messages",int(gg(m.chat.id,"all_messages") or 0) + 1)
    db.set("bot:"+m.content_type+"_messages",int(db.get("bot:"+m.content_type+"_messages") or 0) + 1)
    us(m.from_user.id,m.content_type+"_messages",int(ug(m.from_user.id,m.content_type+"_messages") or 0) + 1)
    gs(m.chat.id,m.content_type+"_messages",int(gg(m.chat.id,m.content_type+"_messages") or 0) + 1)
    gs(m.chat.id,"user:"+str(m.from_user.id)+":all_messages",int(gg(m.chat.id,"user:"+str(m.from_user.id)+":all_messages") or 0) + 1)
    gs(m.chat.id,"user:"+str(m.from_user.id)+":"+m.content_type+"_messages",int(gg(m.chat.id,"user:"+str(m.from_user.id)+":"+m.content_type+"_messages") or 0) + 1)
# Get Stringed Data Of A User 
def inf(user) :
    if isinstance(user, int): 
        try :
            chat = bot.get_chat(user)
        except :
            return str(user)
    else :
        chat = user
    if chat.username :
        chat.username= "[@"+chat.username+"] "
    else :
        chat.username = ""
    return str(chat.first_name)+" "+chat.username+"("+str(chat.id)+')'
def getChatInfo(l,gp) :
        return ln(l,"chatinfot",{"id":gp.id,"title":gp.title,"type":gp.type})
def getChatInfo_long(l,gp) :
    mcount = bot.get_chat_members_count(gp.id)
    acount = 0
    bots = "member"
    for admn in bot.get_chat_administrators(gp.id) :
        if admn.user.id == boti.id :
            bots = admn.status
        if admn.status == "creator" :
            creator = admn.user
        else :
            acount += 1
    alladmin = gp.all_members_are_administrators
    id = gp.id
    title = gp.title
    stats = {}
    for typ in ['all','text', 'audio', 'document', 'photo', 'sticker', 'video', 'voice', 'location', 'contact','game'] :
        stats[typ] = int(gg(gp.id,typ+"_messages") or 0)
    return ln(l,"gpinfo",{"type":gp.type,"mc":mcount,"ac":acount,"creator":creator,"id":id,"title":title,'bs':bots,'alladmin':alladmin,'stats' : stats})
# --- Select Lang Cb ---
def langkb() :
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(text='English',callback_data='chooselang:en'),types.InlineKeyboardButton(text='فارسی',callback_data='chooselang:fa'))
    return markup
# --- Multi Lang ---
def ln(l,s,arg = None) :
    if s == 'started' :
        if l == 'en' :
            return '💫 *Welcome to "Magic Anti Spam Bot" :)*\n⚜️ _Bot Created  in _ [MagicTeam](https://telegram.me/magicnews)_ with ❤️ by @jan123\nChoose One:_'
        else :
            return '💫 به ربات "آنتی اسپم مجیک " خوش امدید :)\n⚜️ ساخته شده در  [MagicTeam](https://telegram.me/magicnews) با ❤️ توسط @jan123\nیکی را انتخاب کنید: '
    if s == 'newsubset' :
        if l == 'en' :
            return '🚀 User \n'+inf(arg['user'])+'\nJoined to robot as your subset.'
        else :
            return '🚀 کاربر\n'+inf(arg['user'])+'\nبه عنوان زیر مجموعه شما وارد ربات شد.'
    elif s == 'backed' :
        if l == 'en' :
            return '🔙 *Backed to main menu*\n⭕️ _Choose One :_'
        else :
            return '🔙 به منو اصلی برگشتید\n⭕️ یکی را انتخاب کنید :'
    elif s == 'back' :
        if l == 'en' :
            return '🔙 Back'
        else :
            return "🔙 برگشت"
    elif s == 'getsettings' :
        chat_id = arg["gp"]
        #-- Flood
        floods = gg(chat_id,"flood:Lock")
        flood = str(gg(chat_id,"flood-spam"))
        time = str(gg(chat_id,"flood-time"))
        #-- Spam
        spam = gg(chat_id,"spam:lock")
        chare = str(gg(chat_id,"chare"))
        # -- Other
        ma =  gg(chat_id,"muteall")
        if ma :
            if ma != 'enabled' :
                if int(ma) < int(round(tt())) :
                    gr(chat_id,"muteall")
                    ma = "Disable"
                else :
                    ma = timetostr(int(ma) - int(round(tt())),'en')
            else :
                ma = "Enable"
        else :
            ma = "Disable"
        maxwarns = str(gg(chat_id,"warn-number"))
        warnaction = gg(chat_id,"warn-action")
        wlc = gg(chat_id,"wlc:Enable")
        settings = """⭕️*Flood Settings:*
        -----------------------
    🔹Process Flood => _"""+(floods or "Offed")+"""_"""
        if floods :
            settings += """
    🔹Flood Sensitivity => _"""+(flood or '5')+"""_
    🔹Flood Time => _"""+(time or '3')+"""_"""
        settings += """
        -----------------------
⭕️*Spam Settings:*
        -----------------------
    🔸Process Spam => _"""+(spam or "Offed")+"""_"""
        if spam :
            settings += """
    🔸Char Sensitivity => _"""+(chare or '500')+"""_"""
        settings += """
        -----------------------
⭕️*Lock Settings:*
        -----------------------
"""
        for v in telelocks :
            settings += """    🔸Lock """+v+""" => _"""+(gg(chat_id,v.lower()+':Lock') or 'Unlock')+"""_
"""
        settings += """         -----------------------
⭕️*Process Settings:*
        -----------------------
"""
        for v in teletyps :
            if v.lower() != "spam" and v.lower() != "flood" :
                settings += """    🔹Process """+v+""" => _"""+(gg(chat_id,v.lower()+':Lock') or 'Offed')+"""_
"""
        settings += """         -----------------------
⭕️*More Settings:*
         -----------------------
    🔸Mute All => _"""+ma+"""_
    🔸Max Warns => _"""+(maxwarns or 3)+"""_
    🔸Warn Action => _"""+(warnaction or 'kick')+"""_
    🔸Welcome Status: _"""+(wlc or 'Disable')+"""_
         -----------------------
Channel:@MagicNews"""
        return settings
    elif s == 'chatinfot' :
        if l == 'en' :
            if arg['type'] == "supergroupsupergroup" :
                type = "Supergroup"
            else :
                type = "Group"
            return '<b>Title</b> : <i>'+arg['title'][:40].replace("<","&lt;").replace(">","&gt;").replace("&","&amp;")+'</i>\n<b>ID</b> : <i>'+str(arg['id'])+'</i>\n<b>Type</b> : <i>'+type+'</i>'
        else :
            if arg['type'] == "title" :
                type = "سوپر گروه"
            else :
                type = "گروه"
            return '<code>عنوان</code> : <i>'+arg['title'][:40].replace("<","&lt;").replace(">","&gt;").replace("&","&amp;")+'</i>\n<code>آیدی</code> : <i>'+str(arg['id'])+'</i>\n<code>نوع</code> : <i>'+type+'</i>'
    elif s == 'aboutus' :
        if l == 'en' :
            return '❗️ About Us'
        else :
            return '❗️ درباره ما'
    elif s == "fblocked" :
        if l == 'en' :
            return "‼️ *Sorry You Are Blocked For 5 minute!(flooding)*"
        else :
            return "‼️ با عرض معذرت شما برای 5 دقیقه بلاک شدید!(پیام پشت سر هم)"
    elif s == 'unblocked' :
        if l == 'en' :
            return '*You are unblocked!*'
        else :
            return '`شما آنبلاک شدید!`'
    elif s == 'contactust' :
        if l == 'en' :
            return '*Send your feedback*'
        else :
            return '`نظر خود را ارسال کنید`'
    elif s == 'dontfwd' :
        if l == 'en' :
            return "*Please dont forward!*"
        else :
            return '`لطفا فروارد نکنید!`'
    elif s == 'justtext' :
        if l == 'en' :
            return "*Please juust send text message!*"
        else :
            return '`لطفا فقط پیام متنی بفرستید!`'
    elif s == 'contactuss' :
        if l == 'en' :
            return '#feedback\n*Sent!*'
        else :
            return '#feedback\n`ارسال شد!`'
    elif s == 'contactus' :
        if l == 'en' :
            return '📮 Contact Us'
        else :
            return '📮 ارتباط با ما'
    elif s == 'nadmin' :
        if l == 'en' :
            return 'Group not found or bot is not admin in this group or you are not moderetor of this group!'
        else :
            return 'گروه یافت نشد یا ربات در گروه ادمین  نیست یا شما مدیر گروه نیستید!'
    elif s == 'locked' :
        if l == 'en' :
            return arg+' Locked!'
        else :
            return arg+' بسته شد!'
    elif s == 'unlocked' :
        if l == 'en' :
            return arg+' Unlocked!'
        else :
            return arg+' باز شد!'
    elif s == 'setto' :
        if l == 'en' :
            return arg['lock']+' is set to "'+arg['proc']+'"!'
        else :
            return arg['lock']+' روی "'+arg['proc']+'" تنظیم شد!'
    elif s == 'chatinfo' :
        if l == 'en' :
            return 'Chat info'
        else :
            return 'اطلاعات گروه'
    elif s == 'nmutelist' :
        if l == 'en' :
            return "Could't finy any mute user in this chat!"
        else :
            return 'هیچ کاربر موتی در این گروه پیدا نشد!'
    elif s == 'nbanlist' :
        if l == 'en' :
            return "Could't finy any ban user in this chat!"
        else :
            return 'هیچ کاربر مسدودی در این گروه پیدا نشد!'
    elif s == 'settings' :
        if l == 'en' :
            return 'Settings'
        else :
            return 'تنظیمات'
    elif s == 'locksettings' :
        if l == 'en' :
            return 'Lock Settings'
        else :
            return 'تنظیمات قفلی'
    elif s == 'mainsettings' :
        if l == 'en' :
            return 'Other settings'
        else :
            return 'تنظیمات متفرقه'
    elif s == 'enablesettings' :
        if l == 'en' :
            return 'Enabled items'
        else :
            return 'آیتم های فعال'
    elif s == 'floodsettings' :
        if l == 'en' :
            return 'Flood Settings'
        else :
            return 'تنظیمات پیام پشت سر هم'
    elif s == 'charesettings' :
        if l == 'en' :
            return 'Chare Settings'
        else :
            return 'تنظیمات اسپم'
    elif s == 'warnsettings' :
        if l == 'en' :
            return 'Warn Settings'
        else :
            return 'تنظیمات اخطار'
    elif s == 'floodhelp' :
        if l == 'en' :
            return 'When user sends messages upper than "Max allowed msgs" in a time lower than "Min allowed time" it called "Flood".'
        else :
            return 'زمانی که کاربر پیام هایی بیش از "بیشترین پیام های مجاز" در زمانی کمتر از "کمترین زمان مجاز" می فرستد آن را "فلوود" می نامیم.'
    elif s == 'warnhelp' :
        if l == 'en' :
            return 'When user sends messages that not allowed probably he/she got warned if user warns is upper than "Max allowed warns" he/she will be "Kicked/Banned" (depends to warn action)'
        else :
            return 'زمانی که کاربر پیام های غیر مجاز میفرستد احتمالا او اخطار میگیرد اگر اخطارهای کاربر بالاتر از "بیشترین اخطار های مجاز" باشد او "کیک یا بن" خواهد شد (بسته به عملکرد وارن)'
    elif s == 'charehelp' :
        if l == 'en' :
            return 'When user messages character count upper than "Max allowed character" it called "Spam".'
        else :
            return 'زمانی که تعداد کاراکتر های پیام های کاربر بیش از "بیشترین کاراکتر های مجاز" باشد آن را "اسپم" می نامیم.'
    elif s == "phelp" :
        if l == 'en' :
            return 'Just click on right cloumn and see what happened!'
        else :
            return 'فقط روی ستون سمت راست کلیک کن و ببین چی میشه!'
    elif s == 'Floodnum' :
        if l == 'en' :
            return 'Msgs num : '+str(arg)
        else :
            return 'تعداد پیام : '+str(arg)
    elif s == 'Charenum' :
        if l == 'en' :
            return 'Character num : '+str(arg)
        else :
            return 'تعداد کاراکتر : '+str(arg)
    elif s == 'Warnnum' :
        if l == 'en' :
            return 'Warn num : '+str(arg)
        else :
            return 'تعداد اخطار : '+str(arg)
    elif s == 'Floodtime' :
        if l == 'en' :
            return 'time : '+str(arg)
        else :
            return 'زمان : '+str(arg)
    elif s == 'Warnaction' :
        if l == 'en' :
            return 'Warn Action : '+str(arg)
        else :
            return 'عملکرد اخطار : '+str(arg)
    elif s == 'invalidrange' :
        if l == 'en' :
            return 'Wrong Number ,Range Is ['+str(arg["r1"])+'-'+str(arg["r2"])+']'
        else :
            return 'عدد نادرست ,عددی در محدوده ['+str(arg["r1"])+'-'+str(arg["r2"])+'] قابل قبول است'
    elif s == 'processsettings' :
        if l == 'en' :
            return 'Process Settings'
        else :
            return 'تنظیمات عملیاتی'
    elif s == 'page1' :
        if l == 'en' :
            return 'Page 1'
        else :
            return 'صفحه اول'
    elif s == 'page2' :
        if l == 'en' :
            return 'Page 2'
        else :
            return 'صفحه دوم'
    elif s == 'page3' :
        if l == 'en' :
            return 'Page 3'
        else :
            return 'صفحه سوم'
    elif s == 'mutelist' :
        if l == 'en' :
            return 'Mutelist'
        else :
            return 'موت لیست'
    elif s == 'mutelistbase' :
        if l == 'en' :
            return "Mute List for group : "+str(arg)
        else :
            return 'موت لیست گروه : '+str(arg)
    elif s == 'mutelistforever' :
        if l == 'en' :
            return "For ever"
        else :
            return "برای همیشه"
    elif s == 'mutelisttime' :
        if l == 'en' :
            return str(arg)+' seconds ('+timetostr(arg,"fa")+')'
        else :
            return str(arg)+' ثانیه ('+timetostr(arg,"fa")+')'
    elif s == 'mutelistt' :
        if l == 'en' :
            return "\n"+str(arg['count'])+" - ID : "+str(arg['id'])+" Time : "+arg['time']
        else :
            return "\n"+str(arg['count'])+" - آیدی : "+str(arg['id'])+" زمان : "+arg['time']
    elif s == 'banlist' :
        if l == 'en' :
            return 'Banlist'
        else :
            return 'بن لیست'
    elif s == 'banlistbase' :
        if l == 'en' :
            return "Ban List for group : "+str(arg)
        else :
            return 'بن لیست گروه : '+str(arg)
    elif s == 'banlistforever' :
        if l == 'en' :
            return "For ever"
        else :
            return "برای همیشه"
    elif s == 'banlisttime' :
        if l == 'en' :
            return str(arg)+' seconds ('+timetostr(arg,"en")+')'
        else :
            return str(arg)+' ثانیه ('+timetostr(arg,"fa")+')'
    elif s == 'banlistt' :
        if l == 'en' :
            return "\n"+str(arg['count'])+" - ID : "+str(arg['id'])+" Time : "+arg['time']
        else :
            return "\n"+str(arg['count'])+" - آیدی : "+str(arg['id'])+" زمان : "+arg['time']
    elif s == 'gpinfo' :
        #{"type":gp.type,"mc":mcount,"ac":acount,"creator":creator,"id":id,"title":title,'bs':bs,'alladmin':alladmin,'stats' : stats}
        if l == 'en' :
            if arg['alladmin'] :
                arg['alladmin'] = "Yes"
            else :
                arg['alladmin'] = "No"
            typ = "Supergroup" if arg["type"] == "supergroup" else "Group"
            ttt = "<b>Type</b> : <i>"+typ+"</i>\n<b>Title</b> : <i>"+arg['title'][:40].replace("<","&lt;").replace(">","&gt;").replace("&","&amp;")+"</i>\n<b>Id</b> : <i>"+str(arg['id'])+"</i>\n<b>Creator </b> : <i>"+inf(arg["creator"])+"</i>\n<b>Magic role</b> : <i>"+arg["bs"]+"</i>\n<b>Members Count</b> : <i>"+str(arg['mc'])+"</i>\n<b>Admins count</b> : <i>"+str(arg['ac'])+"</i>"+(("\n<b>Any one is admin?</b> <i>"+arg['alladmin']+"</i>")  if arg["type"] == "Group" else "")+"\n\n<b>Message stats</b> : \n"
            for i,v in arg["stats"].iteritems() : 
                ttt += "<i>"+i + "</i> : <b>"+str(v)+"</b>\n"
            return ttt
        else :
            if arg['alladmin'] :
                arg['alladmin'] = "بله"
            else :
                arg['alladmin'] = "خیر"
            typ = "سوپر گروه" if arg["type"] == "supergroup" else "گره"
            ttt = "<code>نوع</code> : <i>"+arg["type"]+"</i>\n<code>عنوان</code> : <i>"+arg['title'][:40].replace("<","&lt;").replace(">","&gt;").replace("&","&amp;")+"</i>\n<code>آیدی</code> : <i>"+str(arg['id'])+"</i>\n<code>سازنده </code> : <i>"+inf(arg["creator"])+"</i>\n<code>نقش مجیک</code> : <i>"+arg["bs"]+"</i>\n<code>شمار کاربران</code> : <i>"+str(arg['mc'])+"</i>\n<code>شمار مدیران</code> : <i>"+str(arg['ac'])+"</i>"+(("\n<code>همه مدیر هستند؟?</code> <i>"+arg['alladmin']+"</i>")  if arg["type"] == "Group" else "")+"\n\n<code>آمار پیام ها</code> : \n"
            for i,v in arg["stats"].iteritems() : 
                ttt += "<i>"+i + "</i> : <b>"+str(v)+"</b>\n"
            return ttt
#lock langs
    elif s == "Lock" :
        if arg['res'] :
            return arg['lock']+" 🔒"
        else :
            return arg['lock']+" 🔓"
    elif s == "Enable" :
        if arg['res'] :
            return arg['lock'] + " 🌕"
        else :
            return arg['lock'] + " 🌑"
    elif s == "Poff" :
        if l == 'en' :
            return "Off ✅"
        else :
            return "خاموش ✅"
    elif s == "Pdelete" :
        if l == 'en' :
            return "Delete 🗑"
        else :
            return "حذف 🗑"
    elif s == "Pwarn" :
        if l == 'en' :
            return "Warn ⚠️"
        else :
            return "اخطار ⚠️"
    elif s == "Pkick" :
        if l == 'en' :
            return "Kick 👞️"
        else :
            return "اخراج 👞️"
    elif s == "Pban" :
        if l == 'en' :
            return "Ban ⚔"
        else :
            return "مسدودیت ⚔"  
    elif s == "Pgban" :
        if l == 'en' :
            return "Gban 🌐"
        else :
            return "مسدودیت جهانی 🌐"
# Get Str Time
def timetostr(time,ln) :
    day = 0
    hour = 0
    minute = 0
    sec = 0
    if time > (24 * 60 * 60) :
        day = int(time/(24 * 60 * 60))
        time = time - (day * 24 * 60 * 60)
    if time > (60 * 60) :
        hour = int(time / (60 * 60))
        time = time - (hour * 60 * 60)
    if time > (60) :
        minute = int(time / (60))
        time = time - (minute * 60)
    sec = int(time)
    stri = ''
    if ln == "en" :
        if day > 0 :
            stri = stri + str(day) + 'days '
        if hour > 0 :
            stri = stri +str(hour) + ' hour '
        if minute > 0 :
            stri = stri +str(minute) + ' minute '
        if sec > 0  :
            stri = stri+str(sec)+' sec'
    else :
        if day > 0 :
            stri = stri + str(day) + 'روز '
        if hour > 0 :
            stri = stri +str(hour) + ' ساعت '
        if minute > 0 :
            stri = stri +str(minute) + ' دقیقه '
        if sec > 0  :
            stri = stri+str(sec)+' ثانیه'
    return stri
# --- Main cb ---
def mainkb(l) :
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(ln(l,'aboutus'),ln(l,'contactus'))
    markup.row("🔄 تغییر زبان\Change Language")
    return markup
# --- back cb ---
def bkb(l) :
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(ln(l,'back'))
    return markup
# --- inline back keyboards needs in callback_query:| ---
def ibkb1(l,gp) :
    gp = str(gp)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(ln(l,"back")+" 🔙",callback_data="gpinfo:"+gp))
    return markup
def panelmain(l,gp) :
    gp = str(gp)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(ln(l,"chatinfo")+" 📝",callback_data="chatinfo:"+gp),types.InlineKeyboardButton(ln(l,"chatusers")+" 👥",callback_data="chatusers:"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"mutelist")+" 🔇",callback_data="mutelist:"+gp),types.InlineKeyboardButton(ln(l,"settings")+" ⚙",callback_data="settings:"+gp),types.InlineKeyboardButton(ln(l,"banlist")+" ☠",callback_data="banlist:"+gp))
    return markup
def settingkbmain(l,gp) :
    gp = str(gp)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(ln(l,"locksettings")+" 🔐",callback_data="locksettings:"+gp),types.InlineKeyboardButton(ln(l,"enablesettings")+" 🔅",callback_data="enablesettings:"+gp),types.InlineKeyboardButton(ln(l,"processsettings")+" ⛓",callback_data="processsettings:"+gp))
    markup.add(types.InlineKeyboardButton("📍 "+ln(l,"mainsettings")+" 📍",callback_data="mainsettings:"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"back")+" 🔙",callback_data="gpinfo:"+gp))
    return markup
def settingkbother(l,gp) :
    gp = str(gp)
    markup = types.InlineKeyboardMarkup()
    #Flood
    if gg(gp,'flood:Lock') :
        floodtime = gg(gp,'flood-time') or 3
        floodnum = gg(gp,'flood-spam') or 3
        markup.add(types.InlineKeyboardButton("⚡️ "+ln(l,"floodsettings")+" ⚡️",callback_data="floodhelp:"+gp))
        markup.add(types.InlineKeyboardButton("➕",callback_data="floodnum:up:"+gp),types.InlineKeyboardButton(ln(l,"Floodnum",floodnum),callback_data="floodhelp:"+gp),types.InlineKeyboardButton("➖",callback_data="floodnum:down:"+gp))
        markup.add(types.InlineKeyboardButton("➕",callback_data="floodtime:up:"+gp),types.InlineKeyboardButton(ln(l,"Floodtime",floodtime),callback_data="floodhelp:"+gp),types.InlineKeyboardButton("➖",callback_data="floodtime:down:"+gp))
    #Char
    floodnum = gg(gp,'chare') or 500
    markup.add(types.InlineKeyboardButton("🎐 "+ln(l,"charesettings")+" 🎐",callback_data="charehelp:"+gp))
    markup.add(types.InlineKeyboardButton("➕",callback_data="chare:up:"+gp),types.InlineKeyboardButton(ln(l,"Charenum",floodnum),callback_data="charehelp:"+gp),types.InlineKeyboardButton("➖",callback_data="chare:down:"+gp))
    #Warn
    floodnum = gg(gp,'warn-number') or 3
    warnaction = gg(gp,'warn-action') or "kick"
    markup.add(types.InlineKeyboardButton("⚠️ "+ln(l,"warnsettings")+" ⚠️",callback_data="warnhelp:"+gp))
    markup.add(types.InlineKeyboardButton("➕",callback_data="warn:up:"+gp),types.InlineKeyboardButton(ln(l,"Warnnum",floodnum),callback_data="warnhelp:"+gp),types.InlineKeyboardButton("➖",callback_data="warn:down:"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"Warnaction",ln(l,"P"+warnaction)),callback_data="warn:action:"+gp))
    #Mutelist
    markup.add(types.InlineKeyboardButton(ln(l,"Lock",{"lock":"Mute All","res":gg(gp,'muteall')}),callback_data="muteall:"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"settings")+" ⚙",callback_data="settings:"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"back")+" 🔙",callback_data="gpinfo:"+gp))
    return markup
def settingkbenable(l,gp) :
    gp = str(gp)
    markup = types.InlineKeyboardMarkup()
    argt = []
    for lock in teleenable :
        argt.append(types.InlineKeyboardButton(ln(l,"Enable",{"lock":lock,"res":gg(gp,lock.lower()+':Enable')}),callback_data="Enable:"+lock.lower()+":"+gp))
        if len(argt) == 3 :
            markup.add(argt[0],argt[1],argt[2])
            argt = []
    if len(argt) == 3 :
        markup.add(argt[0],argt[1],argt[2])
    elif len(argt) == 2 :
        markup.add(argt[0],argt[1])
    elif len(argt) == 1 :
        markup.add(argt[0])
    markup.add(types.InlineKeyboardButton(ln(l,"settings")+" ⚙",callback_data="settings:"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"back")+" 🔙",callback_data="gpinfo:"+gp))
    return markup
def settingkblock(l,gp) :
    gp = str(gp)
    markup = types.InlineKeyboardMarkup()
    argt = []
    for lock in telelocks :
        argt.append(types.InlineKeyboardButton(ln(l,"Lock",{"lock":lock,"res":gg(gp,lock.lower()+':Lock')}),callback_data="Lock:"+lock.lower()+":"+gp))
        if len(argt) == 3 :
            markup.add(argt[0],argt[1],argt[2])
            argt = []
    if len(argt) == 3 :
        markup.add(argt[0],argt[1],argt[2])
    elif len(argt) == 2 :
        markup.add(argt[0],argt[1])
    elif len(argt) == 1 :
        markup.add(argt[0])
    markup.add(types.InlineKeyboardButton(ln(l,"settings")+" ⚙",callback_data="settings:"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"back")+" 🔙",callback_data="gpinfo:"+gp))
    return markup
def settingkbprocess1(l,gp) :
    gp = str(gp)
    markup = types.InlineKeyboardMarkup()
    argt = []
    for lock in teletyps1 :
        procs = gg(gp,lock.lower()+':Lock')
        if not procs :
            procs = "off"
        markup.add(types.InlineKeyboardButton(lock,callback_data="Processhelp:"+gp),types.InlineKeyboardButton(ln(l,"P"+procs),callback_data="Process1:"+lock.lower()+":"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"page2")+" ▶️",callback_data="processsettings2:"+gp),types.InlineKeyboardButton(ln(l,"page3")+" ⏩",callback_data="processsettings3:"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"settings")+" ⚙",callback_data="settings:"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"back")+" 🔙",callback_data="gpinfo:"+gp))
    return markup
def settingkbprocess2(l,gp) :
    gp = str(gp)
    markup = types.InlineKeyboardMarkup()
    argt = []
    for lock in teletyps2 :
        procs = gg(gp,lock.lower()+':Lock')
        if not procs :
            procs = "off"
        markup.add(types.InlineKeyboardButton(lock,callback_data="Processhelp:"+gp),types.InlineKeyboardButton(ln(l,"P"+procs),callback_data="Process2:"+lock.lower()+":"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"page1")+" ◀️",callback_data="processsettings:"+gp),types.InlineKeyboardButton(ln(l,"page3")+" ▶️",callback_data="processsettings3:"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"settings")+" ⚙",callback_data="settings:"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"back")+" 🔙",callback_data="gpinfo:"+gp))
    return markup
def settingkbprocess3(l,gp) :
    gp = str(gp)
    markup = types.InlineKeyboardMarkup()
    argt = []
    for lock in teletyps3 :
        procs = gg(gp,lock.lower()+':Lock')
        if not procs :
            procs = "off"
        markup.add(types.InlineKeyboardButton(lock,callback_data="Processhelp:"+gp),types.InlineKeyboardButton(ln(l,"P"+procs),callback_data="Process3:"+lock.lower()+":"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"page1")+" ⏪",callback_data="processsettings:"+gp),types.InlineKeyboardButton(ln(l,"page2")+" ◀️",callback_data="processsettings2:"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"settings")+" ⚙",callback_data="settings:"+gp))
    markup.add(types.InlineKeyboardButton(ln(l,"back")+" 🔙",callback_data="gpinfo:"+gp))
    return markup
# --- Check Command ---
def CheckCmd(m,cmd,req=None,lower=False) :
    match = re.match(cmd,re.sub("[#!/]","",(m.text.lower() if lower else m.text)))
    if re.match("^[#!/]",(m.text.lower() if lower else m.text)) and match :
        if req == "Sudo" and not is_sudo(m.from_user.id) :
            bot.reply_to(m,'*Error*\n_You are not sudo_',parse_mode="Markdown")
            return False
        elif req == "Admin" and not is_admin(m.from_user.id) :
            bot.reply_to(m,'*Error*\n_You are not admin_',parse_mode="Markdown")
            return False
        elif req == "Mod" and not m.is_mod:
            bot.reply_to(m,'*Error*\n_You are not mod_',parse_mode="Markdown")
            return False
        return match
def warn(m,user,lock=None) :
    chat_id = m.chat.id
    msg_id = m.message_id
    user_id = user if isinstance(user, int) else user.id
    nwarn = int(db.hget('warns:gp:'+str(chat_id),user_id) or 0)
    wmax = int(gg(chat_id,'warn-number') or 3)
    if nwarn == wmax :
        wa = gg(chat_id,'warn-action') or "kick"
        if wa == "kick" :
            kick(m,user,fw=True)
        else :
            ban(m,user,fw=True)
        db.hset('warns:gp:'+str(chat_id),user_id,0)
    else :
        db.hset('warns:gp:'+str(chat_id),user_id,nwarn + 1)
        if not lock :
            bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] Warned !</i><b>('+str(nwarn + 1)+'/'+str(wmax)+')</b>',reply_to_message_id=msg_id,parse_mode="html")
        else :
            bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] Warned For "'+lock+'" Process !</i><b>('+str(nwarn + 1)+'/'+str(wmax)+')</b>',reply_to_message_id=msg_id,parse_mode="html")
def unwarn(m,user) :
    chat_id = m.chat.id
    msg_id = m.message_id
    user_id = user if isinstance(user, int) else user.id
    nwarn = int(db.hget('warns:gp:'+str(chat_id),user_id) or 0)
    wmax = int(gg(chat_id,'warn-number') or 3)
    if nwarn <= 0 :
        bot.send_message(chat_id,'*Error*\n_Use has not any warn!_',reply_to_message_id=msg_id,parse_mode="markdown")
        db.hset('warns:gp:'+str(chat_id),user_id,0)
    else :
        db.hset('warns:gp:'+str(chat_id),user_id,nwarn - 1)
        bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] UnWarned !</i><b>('+str(nwarn - 1)+'/'+str(wmax)+')</b>',reply_to_message_id=msg_id,parse_mode="html")
def mute(m,user,time=0) :
    chat_id = m.chat.id
    msg_id = m.message_id
    user_id = user if isinstance(user, int) else user.id
    if not time or time == 0 :
        tsadd('mutes:gp:'+str(chat_id),user_id)
        bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] Muted ...!</i>',reply_to_message_id=msg_id,parse_mode="html")
    else :
        tsadd('mutes:gp:'+str(chat_id),user_id,time)
        bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] Muted For '+timetostr(time,'en')+' !</i>',reply_to_message_id=msg_id,parse_mode="html")
def unmute(m,user) :
    chat_id = m.chat.id
    msg_id = m.message_id
    user_id = user if isinstance(user, int) else user.id
    tsrem('mutes:gp:'+str(chat_id),user_id)
    bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] UnMuted ...!</i>',reply_to_message_id=msg_id,parse_mode="html")
def kick(m,user,fw=None,lock=None) :
    chat_id = m.chat.id
    msg_id = m.message_id
    user_id = user if isinstance(user, int) else user.id
    try :
        bot.kick_chat_member(chat_id, user_id)
        bot.unban_chat_member(chat_id, user_id)
        if fw :
            bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] Kicked For Max Warning ...!</i>',reply_to_message_id=msg_id,parse_mode="html")
        elif lock :
            bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] Kicked For "'+lock+'" Process ...!</i>',reply_to_message_id=msg_id,parse_mode="html")
        else :
            bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] Kicked ...!</i>',reply_to_message_id=msg_id,parse_mode="html")
    except :
        pass
# --- Ban methods ---
def ban(m,user,time=0,fw=None,lock=None) :
    chat_id = m.chat.id
    msg_id = m.message_id
    user_id = user if isinstance(user, int) else user.id
    if not time or time == 0 :
        tsadd('bans:gp:'+str(chat_id),user_id)
        try :
            bot.kick_chat_member(chat_id, user_id)
        except :
            pass
        if fw :
            bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] Banned For Max Warning ...!</i>',reply_to_message_id=msg_id,parse_mode="html")
        elif lock :
            bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] Banned For "'+lock+'" Process ...!</i>',reply_to_message_id=msg_id,parse_mode="html")
        else :
            bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] Banned ...!</i>',reply_to_message_id=msg_id,parse_mode="html")
    else :
        tsadd('bans:gp:'+str(chat_id),user_id,time)
        try :
            bot.kick_chat_member(chat_id, user_id)
            bot.unban_chat_member(chat_id, user_id)
        except :
            pass
        bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] Banned For '+timetostr(time,'en')+' !</i>',reply_to_message_id=msg_id,parse_mode="html")
def unban(m,user) :
    chat_id = m.chat.id
    msg_id = m.message_id
    user_id = user if isinstance(user, int) else user.id
    tsrem('bans:gp:'+str(chat_id),user_id)
    try :
        bot.unban_chat_member(chat_id, user_id)
    except :
        pass
    bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] UnBanned ...!<i>',reply_to_message_id=msg_id,parse_mode="html")
# --- GBan methods ---
def gban(m,user,time=0,fw=None,lock=None) :
    chat_id = m.chat.id
    msg_id = m.message_id
    user_id = user if isinstance(user, int) else user.id
    if not time or time == 0 :
        tsadd('bot:gbans',user_id)
        try :
            bot.kick_chat_member(chat_id, user_id)
        except :
            pass
        if fw :
            bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] GloballyBanned For Max Warning ...!</i>',reply_to_message_id=msg_id,parse_mode="html")
        elif lock :
            bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] GloballyBanned For "'+lock+'" Process ...!</i>',reply_to_message_id=msg_id,parse_mode="html")
        else :
            bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] Banned ...!</i>',reply_to_message_id=msg_id,parse_mode="html")
    else :
        tsadd('bot:gbans',user_id,time)
        try :
            bot.kick_chat_member(chat_id, user_id)
        except :
            pass
        bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] GloballyBanned For '+timetostr(time,'en')+' !</i>',reply_to_message_id=msg_id,parse_mode="html")
def gunban(m,user) :
    chat_id = m.chat.id
    msg_id = m.message_id
    user_id = user if isinstance(user, int) else user.id
    tsrem('bot:gbans',user_id)
    try :
        bot.unban_chat_member(chat_id, user_id)
    except :
        pass
    bot.send_message(chat_id,'<b>Done</b>\n<i>User ['+inf(user)+'] GloballyUnBanned ...!<i>',reply_to_message_id=msg_id,parse_mode="html")
def is_back(m,l) :
    if m.text == ln(l,'back') :
        us(m.from_user.id,"waiting","main")
        bot.reply_to(m,ln(l,'backed'),reply_markup=mainkb(l),parse_mode="Markdown")
        return True
    return False 
# --- Lock Manager ---
def LockManager(m,lock) :
    llock = gg(m.chat.id,lock+":Lock")
    if llock and not m.is_mod :
        if llock == "gban" :
            gban(m,m.from_user,lock=lock)
        elif llock == "ban" :
            ban(m,m.from_user,lock=lock)
        elif llock == "kick" :
            kick(m,m.from_user,lock=lock)
        elif llock == "warn" :
            warn(m,m.from_user,lock=lock)
        try :
            bot.delete_message(m.chat.id,m.message_id)
        except :
            pass
        return False
    return True
def check_text(m) :
    if m.is_mod :
        return True
    text = m.caption or m.text
    # -- Check spam
    if len(text) >= int(gg(m.chat.id,"chare") or 500) and not LockManager(m,"spam"):
        return False
    # -- Check arabic
    elif re.match("[\u0600-\u06FF\uFB8A\u067E\u0686\u06AF]",text.lower()) and not LockManager(m,"arabic") :
        return False
    # -- Check english
    elif re.match("[a-z]",text.lower()) and not LockManager(m,"english"):
        return False
    # -- Check emoji
    elif re.match("[😀😬😁😂😃😀😬😁😂😃😄😅😆😇😉😊🙂🙃☺️😋😌😍😘😗😙😚😜😝😛🤑🤓😎🤗😏😶😐😑😒🙄🤔😳😞😟😠😡😔😕🙁☹️😣😖😫😩😤😮😱😨😰😯😦😧😢😥😪😓😭😵😲🤐😷🤒🤕😴💤💩😈👿👹👺💀👻👽🤖😺😸😹😻😼😽👍👋🏻👏🏻👍🏻🙌🏻😾😿🙀👎🏻👊🏻✊🏻✌🏻👌🏻✋🏻👐🏻💪🏻🙏🏻☝🏻️👆🏻👇🏻👈🏻👉🏻🖕🏻🖐🏻🤘🏻🖖🏻✍🏻💅🏻👄👅👂🏻👃🏻👁👀👤👥🗣👶🏻👦🏻👧🏻👨🏻👩🏻👱🏻👴🏻👵🏻👲🏻👳🏻👮🏻👷🏻💂🏻🕵🎅🏻👼🏻👸🏻👰🏻🚶🏻🏃🏻💃🏻👯👫👬👭🙇🏻💁🏻🙅🏻🙆🏻🙋🏻🙎🏻🙍🏻💇🏻💆🏻💑👩‍❤️‍👩👨‍❤️‍👨💏👩‍❤️‍💋‍👩👨‍❤️‍💋‍👨👪👨‍👩‍👧👨‍👩‍👧‍👦👨‍👩‍👦‍👦👨‍👩‍👧‍👧👩‍👩‍👦👩‍👩‍👧👩‍👩‍👧‍👦👩‍👩‍👦‍👦👩‍👩‍👧‍👧👨‍👨‍👦👨‍👨‍👧👨‍👨‍👧‍👦👨‍👨‍👦‍👦👨‍👨‍👧‍👧👚👕👖👔👗👙👘💄💋👣👠👡👢👞👟👒🎩🎓👑⛑🎒💍🕶👓💼👜👛👝🌂🐶🐱🐭🐹🐰🐻🐼🐸🐽🐷🐮🦁🐯🐨🐙🐵🙈🙉🙊🐒🐔🐗🐺🐥🐣🐤🐦🐧🐴🦄🐝🐛🐌🐞🐜🐟🐠🐢🐍🦀🦂🕷🐡🐬🐳🐊🐋🐆🐅🐐🐘🐫🐪🐄🐂🐃🐏🐑🐎🐖🐀🐁🐓🐿🐇🐈🐩🐕🕊🦃🐾🐉🐲🌵🎄🌲🌳🎋🎍🍀☘🌿🌱🌴🍃🍂🍁🌾🌺🌻🌹🎃🌰🍄💐🌸🌼🌷🐚🕸🌎🌍🌏🌕🌖🌚🌔🌓🌒🌑🌘🌗🌝🌛🌜🌞🌙⭐️🌟💫✨☄☀️🌤⛅️🌥🔥⚡️🌩⛈🌧☁️🌦💥❄️🌨☃⛄️🌬💨🌊💦💧☔️☂🌫🌪🍏🍎🍐🍊🍋🍌🍉🍅🍍🍑🍒🍈🍓🍇🍆🌶🌽🍠🍯🍞🧀🌭🍟🍔🍳🍤🍖🍗🍕🍝🌮🌯🍜🍲🍥🍢🍘🍚🍙🍛🍱🍣🍡🍧🍨🍦🍰🎂🍮🍺🍪🍩🍿🍫🍭🍬🍻🍷🍸🍹🍾🍶🍵☕️🍼🍴🍽⚽️🏀🏈⚾️🎾🏐🏉🏑🏒🏸🏓🏌⛳️🎱🏏🎿⛷🏂⛸🏹🎣🚴🏻🏋🏻⛹🏻🛀🏻🏄🏻🏊🏻🚣🏻🚵🏻🏇🏻🕴🏆🎽🏅🎖🎪🎨🎭🎟🎫🏵🎗🎤🎧🎼🎹🎷🎺🎸🎸🎺🎷🎼🎹🎧🎤🎻🎬🎮👾🎯🎲🎰🎳🚗🚕🚙🚌🚎🏎🚓🏍🚜🚛🚚🚐🚒🚑🚲🚨🚔🚍🚘🚖🚡🚅🚄🚝🚋🚃🚟🚠🚈🚞🚂🚆🚇🚊🚉🛥⛵️🛬🛫✈️🛩🚁🚤⛴??🚀🛰💺⚓️🚢🏁🚥🚦🚏⛽️🚧🎡🎢🎠🏗🌁🗼🏭🗾🌋🗻🏔⛰🎑⛲️🏕⛺️🏞🛣🛤🌅🌄🌃🏙🌆🌇🏝🏖🏜🌉🌌🌠🎇🎆🌈🏘🏰🏯🏟🗽🏠🏡🏚🏢🏬🏣🏤🏥🏦🏨🕌⛪️🏛💒🏩🏫🏪🕍🕋⛩⌚️📱📲💻⌨🖥🖨💿💾💽🗜🕹🖲🖱📀📼📷📹📹🎥📽📻📺📠📟☎️📞🎞🎙🎚🎛⏱⏲⏰🕰🔦💡🔌🔋📡⌛️⏳🕯🗑🛢💸💵💴💶⚒🛠⛏🔩⚙⛓🔫☠🚬🛡⚔🗡🔪💣💷💰💳💎⚖🔧🔨⚰⚱🏺🔮📿💈⚗🏷🌡💉💊🕳🔬🔭🔖🚽🚿🛁🔑🗝🛋⛱🗺🖼🛎🚪🛏🛌🗿🛍🎈🎏🎀🎁🎊📩✉️🏮🎌🎐🎎🎉📨📧💌📮📪📫📬📃📜📤📥📯📦📭📑📊📈📉📄📅📆🗒📋🗄🗳🗃📇🗓📁📂🗂🗞📰📓📕📖📚📒📔📙📘📗🔗📎🖇✂️📐📏📌🔓🔒🔐🏴🏳🚩📍🔏🖊🖋✒️📝✏️🖍🔎🖌❤️💛💚💙💜❣❣💝💘💖💗💞💕💟☮✝☪🕉☸✡♈️♏️♎️☸🛐♍️♌️☦♋️☯♊️🕎♉️🔯♐️♑️♒️♓️🆔⚛🈳🈚️🈶📳📴☣☢🈹🈸🈺🈷✴️🆚🉑💮🅰🈲🈵🈴㊗️㊙️🉐🅱🆎🆑🅾🆘⛔️📛🚫❌⭕️💢♨️🚷🚯❓❕❗️📵🔞🚱🚳❔‼️⁉️🔅💯🔆🔱🈯️♻️🔰🚸⚠️〽️⚜💹❇️✳️❎✅💠🌀🛃🛂🈂🏧Ⓜ️🌐➿🛄🛅♿️🚭🚾🅿️🚰📶🎦🚮🚻🚼🚺🚹🈁🆖🆗🆙🚻🆒🚮🆕🎦🆓📶0⃣1⃣2⃣3⃣4⃣5⃣6⃣⏸▶️🔢🔟9⃣8⃣7⃣⏯⏹⏺⏭⏮⏩⏪⏫🔽🔼◀️🔂🔁🔀⏬➡️⬅️⬆️⬇️↗️↘️🔡🔤ℹ️*⃣#⃣⤴️↙️↖️🔄↪️↩️↩️✔️➰〰🎵🔣🔠🔃➕➖✖️➗💲💱🔝🔛🔙™®©🔜☑️🔘⚪️⚫️🔴🔵▫️▪️🔺🔷🔶🔹🔸⬛️⬜️🔻◼️◻️◾️◽️📣🔇🔉🔳🔲📢🔔🔕🃏🀄️♠️♣️💬🗯👁‍🗨💭🎴♦️♦️♥️🕐🕑🕒🕓🕔🕕🕖🕤🕟🕞🕗🕜🕝🕥🕦🇦🇫🇦🇱🇩🇿🇩🇿🇦🇸🇦🇩🇦🇴🇦🇮🇦🇶🇦🇮🇦🇬🇦🇷🇧🇭🇧🇸🇦🇿🇦🇹🇦🇺🇦🇼🇦🇲🇧🇩🇧🇧🇧🇪🇧🇾🇧🇿🇧🇯🇧🇲🇻🇬🇮🇴🇧🇷🇧🇦🇧🇹🇧🇳🇧🇬🇧🇫🇧🇮🇨🇲🇨🇦🇧🇮🇨🇳🇨🇽🇨🇴🇰🇲🇨🇬🇨🇩🇨🇩🇨🇾🇨🇼🇨🇺🇨🇮🇨🇷🇨🇰🇸🇻🇬🇶🇪🇹🇪🇺🇫🇰🇪🇬🇨🇿🇫🇴🇫🇯🇫🇷🇵🇫🇹🇫🇹🇫🇬🇳🇬🇬🇬🇵🇬🇩🇬🇱🇬🇱🇬🇦🇬🇦🇬🇲🇬🇭🇬🇳🇮🇸🇭🇰🇭🇳🇬🇼🇮🇳🇮🇩🇮🇷🇮🇶🇮🇪🇮🇲🇮🇲🇮🇱🇰🇪🇰🇿🇯🇴🇯🇪🇯🇵🇯🇲🇮🇹🇰🇮🇽🇰🇰🇼🇰🇬🇱🇦🇱🇻🇱🇧🇲🇴🇱🇺🇱🇹🇱🇮🇱🇾🇱🇷🇱🇸🇲🇭🇲🇶🇲🇷🇲🇺🇾🇹🇲🇽🇫🇲🇲🇿🇲🇦🇲🇸🇲🇪🇲🇳🇲🇨🇲🇩🇲🇲🇳🇦🇳🇷🇳🇵🇳🇨🇳🇨🇳🇿🇲🇵🇰🇵🇳🇫🇳🇺🇳🇬🇳🇪🇳🇮🇳🇴🇴🇲🇵🇰🇵🇼🇵🇦🇵🇸🇵🇬🇸🇲🇼🇸🇵🇷🇵🇱🇵🇱🇵🇱🇷🇺🇵🇳🇷🇴🇵🇪🇷🇪🇵🇪🇶🇦🇴🇲🇵🇪🇵🇾🇸🇹🇸🇦🇸🇳🇸🇨🇸🇱🇸🇬🇿🇦🇸🇧🇸🇽🇰🇷🇸🇸🇪🇸🇧🇱🇸🇭🇰🇳🇸🇪🇸🇷🇸🇩🇱🇨🇨🇭🇸🇾🇹🇼🇹🇯🇹🇿🇹🇭🇹🇱🇹🇲🇹🇷🇹🇳🇹🇹🇹🇴🇹🇰🇹🇬🇹🇨🇹🇨🇹🇻🇻🇮🇺🇬🇺🇬🇺🇦🇬🇧🇦🇪🇬🇧🇺🇸🇺🇸🇺🇾🇺🇿🇺🇿🇻🇺🇻🇦🇻🇪🇻🇪🇻🇳🇿🇼🇾🇪🇼🇫😄😅😆😇😉😊🙂🙃☺️😋😌😍😘😗😙😚😜😝😛🤑🤓😎🤗😏😶😐😑😒🙄🤔😳😞😟😠😡😔😕🙁☹️😣😖😫😩😤😮😱😨😰😯😦😧😢😥😪😓😭😵😲🤐😷🤒🤕😴💤💩😈👿👹👺💀👻👽🤖😺😸😹😻😼😽🙀😿😾🙌👏👋👍👎👊✊✌️👌✋👐💪🙏☝️👆👇👈👉🖕🖐🤘🖖✍💅👄👅👂👃👁👀👤👥🗣👶👦👧👨👩👱👴👵👲👳👮👷💂🕵🎅👼👸👰🚶🏃💃👯👫👬👭🙇💁🙅🙆🙋🙎🙍💇💆💑👩‍❤️‍👩👨‍❤️‍👨💏👩‍❤️‍💋‍👩👨‍❤️‍💋‍👨👪👨‍👩‍👧👨‍👩‍👧‍👦👨‍👩‍👦‍👦👨‍👩‍👧‍👧👩‍👩‍👦👩‍👩‍👧👩‍👩‍👧‍👦👩‍👩‍👦‍👦👩‍👩‍👧‍👧👨‍👨‍👦👨‍👨‍👧👨‍👨‍👧‍👦👨‍👨‍👦‍👦👨‍👨‍👧‍👧👨‍👨‍👧‍👧👚👕👖👔👗👙👘💄💋👣👠👡👢👞👟👒🎩🎓👑⛑🎒👝👛👜💼👓🕶💍🌂❤️💛💚💙💖💗💓💞💕❣💔💜💘💝]",text.lower()) and LockManager(m,"emoji") :
        return False
    # -- Check Enitity
    for v in (m.entities or []) :
        if v.type == "text_mention" and not LockManager(m,"mention") :
            return False
        elif v.type == "mention" and not LockManager(m,"username") :
            return False
        elif (v.type == "bold" or v.type == "italic" or v.type == "code" or v.type == "pre") and not LockManager(m,"markdown") :
            return False
        elif (v.type == "url" or v.type == "text_link") and not LockManager(m,"links") :
            return False
        elif v.type == "hashtag" and not LockManager(m,"tag") :
            return False
    # -- Check Bad Words
    for v in db.smembers('badwords:gp:'+str(m.chat.id)) :
        if text.lower().find(v)  :
            bot.delete_message(m.chat.id,m.message_id)
            return False
    return True
print("Tele Magic Bot Started:)")
@bot.message_handler(func=lambda m: if_pv(m))
def pv_all(m) :
    def pv_all_multi() :
        try:
            db.sadd("bot:users",m.from_user.id)
            l = ug(m.from_user.id,'lang')
            w = ug(m.from_user.id,"waiting")
            # Anti flood
            if db.get('flood:' + str(m.from_user.id)) :
                return
            post_count = int(db.get('floodc:' + str(m.from_user.id)) or 0)
            if post_count >  4 and not is_admin(m.from_user.id):
                bot.send_message(m.from_user.id,ln(l,"fblocked"),parse_mode='markdown')
                db.setex('flood:' + str(m.from_user.id),5 * 60,True)
                return
            db.setex('floodc:' + str(m.from_user.id), 3, post_count+1)
            if not l :
                bot.reply_to(m,'*Please choose your language...*\n`لظفا زبان خود را انتخاب نمایید...`',reply_markup=langkb(),parse_mode='markdown')
                return
            elif m.text == "/start" :
                bot.reply_to(m,ln(l,'started'),reply_markup=mainkb(l),parse_mode='markdown')
            elif m.text == "🔄 تغییر زبان\Change Language" :
                ur(m.from_user.id,'lang')
                bot.reply_to(m,'*Please choose your language...*\n`لظفا زبان خود را انتخاب نمایید...`',reply_markup=langkb(),parse_mode='markdown')
            elif m.text == ln(l,"aboutus") :
                bot.send_message(m.from_user.id,ln(l,"started"),reply_markup=mainkb(l),parse_mode='markdown')
            elif m.text == ln(l,"contactus") :
                bot.send_message(m.from_user.id,ln(l,"contactust"),reply_markup=bkb(l),parse_mode='markdown')
                us(m.from_user.id,"waiting","contactus")
            elif w == "contactus" :
                if is_back(m,l) :
                    return
                if m.forward_from or m.forward_from_chat :
                    bot.send_message(m.from_user.id,ln(l,"dontfwd"),reply_markup=bkb(l),parse_mode='markdown')
                    return
                mm = bot.forward_message(log_chat,m.from_user.id,m.message_id)
                bot.send_message(log_chat,"#feedback",reply_to_message_id=mm.message_id)
                bot.send_message(m.from_user.id,ln(l,"contactuss"),reply_markup=mainkb(l),parse_mode='markdown',reply_to_message_id=m.message_id)
                us(m.from_user.id,"waiting","main")
        except Exception as e :
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            try :
                bot.send_message(m.chat.id,"❌ مشکل فنی رخ داد اطلاعات مشکل به مدیریت گزارش شد در صورت نیاز به توضیح بیشتر از قسمت \"ارتباط با ما\" گزارش دهید.")
            except :
                pass
            bot.send_message(errors_chat,"#خطا\nکاربر : "+str(m.from_user.id)+"\nنوع : "+str(exc_type)+"\nفایل : "+str(fname)+"\nخط : "+str(exc_tb.tb_lineno)+"\nشرح خطا : "+str(e))
            print(exc_type, fname, exc_tb.tb_lineno,e)
    freeze_support()
    Process(target=pv_all_multi).start()
@bot.edited_message_handler(func= lambda m : if_group(m),content_types=['text', 'audio', 'document', 'gif', 'photo', 'video', 'voice'])
def group_edit(m) :
    def group_edit_multi() :
        try :
            l = ug(m.from_user.id,'lang') or "fa"
            if not is_added(m)  :
                bot.leave_chat(m.chat.id)
            m.is_mod = is_mod(m.chat.id,m.from_user.id)
            # Anti flood
            max_flood = int(gg(m.chat.id,"flood-spam") or 4)
            max_flood_time = int(gg(m.chat.id,"flood-time") or 3)
            post_count = int(db.get('floodc:' + str(m.chat.id)+ ':'+str(m.from_user.id)) or 0)
            db.setex('floodc:' + str(m.chat.id)+ ':'+str(m.from_user.id), max_flood_time, post_count+1)
            if post_count >  max_flood :
                if not LockManager(m,"flood") :
                    return
            elif post_count == int(round(float(max_flood) / float(2))) and gg(m.chat.id,"flood:Lock") and gg(m.chat.id,"flood:Lock") != "delete" and not m.is_mod :
                bot.reply_to(m,"*Please dont flood !*\n_If you continue flooding you will be fucked!_",parse_mode="Markdown")
            if gg(m.chat.id,"bot:Lock") and (m.from_user.username or '').endswith("bot") and not m.is_mod:
                try :
                    bot.kick_chat_member(m.chat.id, m.from_user.id)
                    bot.unban_chat_member(m.chat.id,m.from_user.id)
                except :
                    pass
                return
            elif tsget("bot:gbans",m.from_user.id) :
                if not is_admin(m.from_user.id):
                    try :
                        bot.kick_chat_member(m.chat.id, m.from_user.id)
                    except :
                        pass
                else :
                    tsrem("bot:gbans",m.from_user.id)
                return
            elif tsget("bans:gp:"+str(m.chat.id),m.from_user.id) :
                if not m.is_mod :
                    try :
                        bot.kick_chat_member(m.chat.id, m.from_user.id)
                    except :
                        pass
                else :
                    tsrem('bans:gp:'+str(m.chat.id),m.from_user.id)
                return
                ma =  gg(m.chat.id,"muteall")
                if ma and ma != 'enabled' and int(ma) < int(round(tt())) :
                    gr(m.chat.id,"muteall")
                    ma = None
                if ma and not m.is_mod :
                    bot.delete_message(m.chat.id,m.message_id)
                    return
                bot.delete_message(m.chat.id,m.message_id)
                return
            elif tsget("mutes:gp:"+str(m.chat.id),m.from_user.id) and not m.is_mod :
                bot.delete_message(m.chat.id,m.message_id)
                return
            elif not LockManager(m,'edit') :
               return
            elif not LockManager(m,m.content_type) :
               return
            elif m.forward_date and not LockManager(m,"forward") :
                return
            elif m.reply_to_message and not LockManager(m,"reply") :
                return
            elif m.caption and (not LockManager(m,"caption") or not check_text(m)) :
                return
            if m.content_type != "text" :
                return
            if not check_text(m) or (gg(m.chat.id,"cmd:Lock") and not m.is_mod) or not gg(m.chat.id,"editprocess:Enable") :
                return
            check_cmds(bot,m,l)
        except Exception as e :
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            try :
                bot.send_message(m.chat.id,"❌ مشکل فنی رخ داد اطلاعات مشکل به مدیریت گزارش شد در صورت نیاز به توضیح بیشتر از قسمت \"ارتباط با ما\" گزارش دهید.")
            except :
                pass
            bot.send_message(errors_chat,"#خطا\nکاربر : "+str(m.from_user.id)+"\nگروه : "+str(m.chat.id)+"\nنوع : "+str(exc_type)+"\nفایل : "+str(fname)+"\nخط : "+str(exc_tb.tb_lineno)+"\nشرح خطا : "+str(e))
    freeze_support()
    Process(target=group_edit_multi).start()

@bot.message_handler(func= lambda m : if_group(m),content_types=['text', 'audio', 'document', 'gif', 'photo', 'sticker', 'video', 'voice', 'location', 'contact','game', 'new_chat_member', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message'])
def group_all(m):
    def group_all_multi() :
        try :
            if m.chat.id == log_chat:
                if not m.text :
                    return
                if m.text.startswith("/unblock")  :
                    matches = m.text.split()
                    if len(matches) == 2 and db.sismember("bot:users",matches[1]) :
                        if db.get('flood:' + str(matches[1])) :
                            db.delete('flood:' + str(matches[1]))
                            bot.send_message(str(matches[1]),ln(ug(matches[1],'lang'),'unblocked'),parse_mode='markdown')
                            bot.send_message(m.chat.id,"User unblocked!")
                        else :
                            bot.send_message(m.chat.id,"User not blocked!")
                    else :
                        bot.send_message(m.chat.id,"User nf!")
                elif m.text.startswith("/setjiko")  :
                    matches = m.text.split()
                    if len(matches) == 3 and db.sismember("bot:users",matches[1]) :
                        us(matches[1],"jiko",int(ug(matches[1],"jiko") or 0) + int(matches[2]))
                        bot.send_message(m.chat.id,"User jiko seted to "+matches[2]+" !")
                    else :
                        bot.send_message(m.chat.id,"User nf!")
                elif m.reply_to_message and m.reply_to_message.from_user.id == boti.id and m.reply_to_message.forward_from :
                    bot.send_message(m.reply_to_message.forward_from.id,"#feedback_answer\n\n"+str(m.text)+"\n\n"+str(m.from_user.first_name))
                return
            l = ug(m.from_user.id,'lang') or "fa"
            if m.content_type == 'new_chat_member' :
                if m.new_chat_member.id == boti.id :
                    if is_admin(m.from_user.id) or int(gg(m.chat.id,"inviter") or 0) == m.from_user.id :
                        bot.reply_to(m,"<b>Hi wlc to my self!</b>\n<code>I am magic api bot please set me admin to help you for managing your group!</code>\n<b>** Without admin access I am just a fun bot:)</b>",parse_mode="Html")
                        db.sadd("bot:groups",m.chat.id)
                        gs(m.chat.id,"inviter",m.from_user.id)
                        return
                    else :
                        bot.reply_to(m,"*Error*\n_You are not my admin and cant add me to groups!_\n\n*Group ID* : _"+str(m.chat.id)+"_",parse_mode="Markdown")
                        bot.leave_chat(m.chat.id)
                        return
                    if not is_added(m)  :
                        bot.leave_chat(m.chat.id)
                        return
                if tsget("bot:gbans",m.new_chat_member.id) :
                    if not is_admin(m.new_chat_member.id) and not is_admin(m.from_user.id):
                        try :
                            bot.kick_chat_member(m.chat.id, m.new_chat_member.id)
                        except :
                            pass
                        return
                    else :
                        tsrem("bot:gbans",m.new_chat_member.id)
                    return
                elif tsget("bans:gp:"+str(m.chat.id),m.new_chat_member.id) :
                    if not is_admin(m.new_chat_member.id) and not is_mod(m.chat.id,m.from_user.id) :
                        try :
                            bot.kick_chat_member(m.chat.id, m.new_chat_member.id)
                            bot.unban_chat_member(m.chat.id,m.new_chat_member.id)
                        except :
                            pass
                    else :
                        tsrem('bans:gp:'+str(m.chat.id),m.new_chat_member.id)
                    return
                elif gg(m.chat.id,"bot:Lock") and (m.new_chat_member.username or '').endswith("bot") and not is_mod(m.chat.id,m.from_user.id):
                    try :
                        bot.kick_chat_member(m.chat.id, m.new_chat_member.id)
                        bot.unban_chat_member(m.chat.id,m.new_chat_member.id)
                    except :
                        pass
                    return
                elif gg(m.chat.id,"joinmember:Lock") and not is_admin(m.new_chat_member.id) and not is_mod(m.chat.id,m.from_user.id)  :
                    try :
                        bot.kick_chat_member(m.chat.id, m.new_chat_member.id)
                        bot.unban_chat_member(m.chat.id,m.new_chat_member.id)
                    except :
                        pass
                    return
                elif gg(m.chat.id,"wlc") :
                    if not is_added(m)  :
                        bot.leave_chat(m.chat.id)
                        return
                    bot.reply_to(m,gg(m.chat.id,"wlcmessage") or "Wlc")
                return
            elif m.content_type == 'left_chat_member' :
                if m.left_chat_member == boti.id :
                    db.srem("bot:groups",m.chat.id)
                    gr(m.chat.id,"inviter")
                elif gg(m.chat.id,"bye") :
                    bot.reply_to(m,gg(m.chat.id,"byemessage") or "Bye")
                return
            if not is_added(m)  :
                bot.leave_chat(m.chat.id)
            if m.content_type in ['text', 'audio', 'document', 'photo', 'sticker', 'video', 'voice', 'location', 'contact','game','gif'] :
                collect_stats(m)
                m.is_mod = is_mod(m.chat.id,m.from_user.id)
                # Anti flood
                max_flood = int(gg(m.chat.id,"flood-spam") or 4)
                max_flood_time = int(gg(m.chat.id,"flood-time") or 3)
                post_count = int(db.get('floodc:' + str(m.chat.id)+ ':'+str(m.from_user.id)) or 0)
                db.setex('floodc:' + str(m.chat.id)+ ':'+str(m.from_user.id), max_flood_time, post_count+1)
                if post_count >  max_flood :
                    if not LockManager(m,"flood") :
                        return
                elif post_count == int(round(float(max_flood) / float(2))) and gg(m.chat.id,"flood:Lock") and gg(m.chat.id,"flood:Lock") != "delete" and not m.is_mod :
                    bot.reply_to(m,"*Please dont flood !*\n_If you continue flooding you will be fucked!_",parse_mode="Markdown")
                if gg(m.chat.id,"bot:Lock") and (m.from_user.username or '').endswith("bot") and not m.is_mod:
                    try :
                        bot.kick_chat_member(m.chat.id, m.from_user.id)
                        bot.unban_chat_member(m.chat.id,m.from_user.id)
                    except :
                        pass
                    return
                elif tsget("bot:gbans",m.from_user.id) :
                    if not is_admin(m.from_user.id):
                        try :
                            bot.kick_chat_member(m.chat.id, m.from_user.id)
                        except :
                            pass
                    else :
                        tsrem("bot:gbans",m.from_user.id)
                    return
                elif tsget("bans:gp:"+str(m.chat.id),m.from_user.id) :
                    if not m.is_mod :
                        try :
                            bot.kick_chat_member(m.chat.id, m.from_user.id)
                        except :
                            pass
                    else :
                        tsrem('bans:gp:'+str(m.chat.id),m.from_user.id)
                    return
                ma =  gg(m.chat.id,"muteall")
                if ma and ma != 'enabled' and int(ma) < int(round(tt())) :
                    gr(m.chat.id,"muteall")
                    ma = None
                if ma and not m.is_mod :
                    bot.delete_message(m.chat.id,m.message_id)
                    return
                elif tsget("mutes:gp:"+str(m.chat.id),m.from_user.id) and not m.is_mod :
                    bot.delete_message(m.chat.id,m.message_id)
                    return
                elif not LockManager(m,m.content_type) :
                   return
                elif m.forward_date and not LockManager(m,"forward") :
                    return
                elif m.reply_to_message and not LockManager(m,"reply") :
                    return
                elif m.caption and (not LockManager(m,"caption") or not check_text(m)) :
                    return
                if m.content_type != "text" :
                    return
                if not check_text(m) or (gg(m.chat.id,"cmd:Lock") and not m.is_mod):
                    return
                check_cmds(bot,m,l)
        except Exception as e :
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            try :
                bot.send_message(m.chat.id,"❌ مشکل فنی رخ داد اطلاعات مشکل به مدیریت گزارش شد در صورت نیاز به توضیح بیشتر از قسمت \"ارتباط با ما\" گزارش دهید.")
            except :
                pass
            bot.send_message(errors_chat,"#خطا\nکاربر : "+str(m.from_user.id)+"\nگروه : "+str(m.chat.id)+"\nنوع : "+str(exc_type)+"\nفایل : "+str(fname)+"\nخط : "+str(exc_tb.tb_lineno)+"\nشرح خطا : "+str(e))
            print(exc_type, fname, exc_tb.tb_lineno,e)
    freeze_support()
    Process(target=group_all_multi).start()

@bot.callback_query_handler(func=lambda m: True)
def callback_kb(m) :
    def callback_kb_multi() :
        try :
            if m.data == 'chooselang:en' :
                bot.edit_message_text('Your language has been set/updated to *ENGLISH!*',chat_id=m.from_user.id,message_id=m.message.message_id,parse_mode='markdown')
                bot.send_message(m.from_user.id,ln('en','started'),reply_markup=mainkb('en'),parse_mode='markdown')
                us(m.from_user.id,"lang",'en')
            elif m.data == 'chooselang:fa' :
                bot.edit_message_text('زبان شما با موفقیت به *فارسی* تنظیم شد/تغییر کرد',chat_id=m.from_user.id,message_id=m.message.message_id,parse_mode='markdown')
                bot.send_message(m.from_user.id,ln('fa','started'),reply_markup=mainkb('fa'),parse_mode='markdown')
                us(m.from_user.id,"lang",'fa')
            l = ug(m.from_user.id,'lang') or "fa"
            if m.data.startswith("gpinfo:") :
                gp = m.data.replace("gpinfo:","")
                if is_mod(gp,m.from_user.id) :
                    tex = getChatInfo(l,bot.get_chat(gp))
                    bot.edit_message_text(tex,chat_id=m.message.chat.id,message_id=m.message.message_id,parse_mode="html",reply_markup=panelmain(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            if m.data.startswith("chatinfo:") :
                gp = m.data.replace("chatinfo:","")
                if is_mod(gp,m.from_user.id) :
                    try :
                        tex = getChatInfo_long(l,bot.get_chat(gp))
                        bot.edit_message_text(tex,chat_id=m.message.chat.id,message_id=m.message.message_id,parse_mode="html",reply_markup=ibkb1(l,gp))
                    except :
                        pass
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("mutelist:") :
                gp = m.data.replace("mutelist:","")
                if is_mod(gp,m.from_user.id) :
                    mutelist = db.smembers('mutes:gp:'+gp)
                    if len(mutelist) == 0 :
                        bot.answer_callback_query(m.id, text=ln(l,"nmutelist"), show_alert=True)
                        return
                    text = ln(l,"mutelistbase",gp)
                    count = 1
                    for userj in mutelist :
                        user = json.loads(userj)
                        ekht = int(user['time']) - tt()
                        if user['time'] == 0 or ekht < 0 :
                            timet = ln(l,"mutelistforever")
                        else :
                            timet = ln(l,"mutelisttime",ekht)
                        text += ln(l,"mutelistt",{"count":count,"id":user['id'],"time":timet})
                        count += 1
                    bot.edit_message_text(text,chat_id = m.message.chat.id,message_id = m.message.message_id,parse_mode="markdown",reply_markup=ibkb1(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("banlist:") :
                gp = m.data.replace("banlist:","")
                if is_mod(gp,m.from_user.id) :
                    banlist = db.smembers('bans:gp:'+gp)
                    if len(banlist) == 0 :
                        bot.answer_callback_query(m.id, text=ln(l,"nbanlist"), show_alert=True)
                        return
                    text = ln(l,"banlistbase",gp)
                    count = 1
                    for userj in banlist :
                        user = json.loads(userj)
                        ekht = int(user['time']) - tt()
                        if user['time'] == 0 or ekht < 0 :
                            timet = ln(l,"banlistforever")
                        else :
                            timet = ln(l,"banlisttime",ekht)
                        text += ln(l,"banlistt",{"count":count,"id":user['id'],"time":timet})
                        count += 1
                    bot.edit_message_text(text,chat_id = m.message.chat.id,message_id = m.message.message_id,parse_mode="markdown",reply_markup=ibkb1(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("settings:") :
                gp = m.data.replace("settings:","")
                if is_mod(gp,m.from_user.id) :
                    bot.edit_message_text(text = ln(l,"getsettings",{"gp" : gp}),chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbmain(l,gp),parse_mode="markdown")
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("locksettings:") :
                gp = m.data.replace("locksettings:","")
                if is_mod(gp,m.from_user.id) :
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkblock(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("processsettings:") :
                gp = m.data.replace("processsettings:","")
                if is_mod(gp,m.from_user.id) :
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbprocess1(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("processsettings2:") :
                gp = m.data.replace("processsettings2:","")
                if is_mod(gp,m.from_user.id) :
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbprocess2(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("processsettings3:") :
                gp = m.data.replace("processsettings3:","")
                if is_mod(gp,m.from_user.id) :
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbprocess3(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("mainsettings:") :
                gp = m.data.replace("mainsettings:","")
                if is_mod(gp,m.from_user.id) :
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbother(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("enablesettings:") :
                gp = m.data.replace("enablesettings:","")
                if is_mod(gp,m.from_user.id) :
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbenable(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("floodhelp:") :
                gp = m.data.replace("floodhelp:","")
                if is_mod(gp,m.from_user.id) :
                    bot.answer_callback_query(m.id, text=ln(l,"floodhelp"), show_alert=True)
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("floodnum:up:") :
                gp = m.data.replace("floodnum:up:","")
                if is_mod(gp,m.from_user.id) :
                    floodnum = int(gg(gp,'flood-spam') or 3)
                    if (floodnum + 1) > 20 or (floodnum + 1) < 3 :
                        bot.answer_callback_query(m.id, text=ln(l,"invalidrange",{"r1":3,"r2":20}), show_alert=True)
                        return
                    gs(gp,'flood-spam',floodnum + 1)
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbother(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("floodnum:down:") :
                gp = m.data.replace("floodnum:down:","")
                if is_mod(gp,m.from_user.id) :
                    floodnum = int(gg(gp,'flood-spam') or 3)
                    if (floodnum - 1) > 20 or (floodnum - 1) < 3 :
                        bot.answer_callback_query(m.id, text=ln(l,"invalidrange",{"r1":3,"r2":20}), show_alert=True)
                        return
                    gs(gp,'flood-spam',floodnum - 1)
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbother(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("chare:up:") :
                gp = m.data.replace("chare:up:","")
                if is_mod(gp,m.from_user.id) :
                    floodnum = int(gg(gp,'chare') or 500)
                    if (floodnum + 10) > 4000 or (floodnum + 10) < 500 :
                        bot.answer_callback_query(m.id, text=ln(l,"invalidrange",{"r1":500,"r2":4000}), show_alert=True)
                        return
                    gs(gp,'chare',floodnum + 10)
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbother(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("chare:down:") :
                gp = m.data.replace("chare:down:","")
                if is_mod(gp,m.from_user.id) :
                    floodnum = int(gg(gp,'chare') or 500)
                    if (floodnum - 10) > 4000 or (floodnum - 10) < 500 :
                        bot.answer_callback_query(m.id, text=ln(l,"invalidrange",{"r1":500,"r2":4000}), show_alert=True)
                        return
                    gs(gp,'chare',floodnum - 10)
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbother(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("floodtime:up:") :
                gp = m.data.replace("floodtime:up:","")
                if is_mod(gp,m.from_user.id) :
                    floodnum = int(gg(gp,'flood-time') or 3)
                    if (floodnum + 1) > 5 or (floodnum  + 1) < 1 :
                        bot.answer_callback_query(m.id, text=ln(l,"invalidrange",{"r1":1,"r2":5}), show_alert=True)
                        return
                    gs(gp,'flood-time',floodnum + 1)
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbother(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("floodtime:down:") :
                gp = m.data.replace("floodtime:down:","")
                if is_mod(gp,m.from_user.id) :
                    floodnum = int(gg(gp,'flood-time') or 3)
                    if (floodnum - 1) > 5 or (floodnum  - 1) < 1 :
                        bot.answer_callback_query(m.id, text=ln(l,"invalidrange",{"r1":1,"r2":5}), show_alert=True)
                        return
                    gs(gp,'flood-time',floodnum - 1)
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbother(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
                    
                    
            elif m.data.startswith("warn:up:") :
                gp = m.data.replace("warn:up:","")
                if is_mod(gp,m.from_user.id) :
                    floodnum = int(gg(gp,'warn-number') or 3)
                    if (floodnum + 1) > 10 or (floodnum  + 1) < 2 :
                        bot.answer_callback_query(m.id, text=ln(l,"invalidrange",{"r1":2,"r2":10}), show_alert=True)
                        return
                    gs(gp,'warn-number',floodnum + 1)
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbother(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("warn:down:") :
                gp = m.data.replace("warn:down:","")
                if is_mod(gp,m.from_user.id) :
                    floodnum = int(gg(gp,'warn-number') or 3)
                    if (floodnum - 1) > 10 or (floodnum  - 1) < 2 :
                        bot.answer_callback_query(m.id, text=ln(l,"invalidrange",{"r1":2,"r2":10}), show_alert=True)
                        return
                    gs(gp,'warn-number',floodnum - 1)
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbother(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
                 
            elif m.data.startswith("warn:action:") :
                gp = m.data.replace("warn:action:","")
                if is_mod(gp,m.from_user.id) :
                    procs = gg(gp,'warn-action') or "kick"
                    if procs == "kick" :
                        procs = "ban"
                    elif procs == "ban" :
                        procs = "gban"
                    elif procs == "gban" :
                        procs = "kick"
                    gs(gp,'warn-action',procs)    
                    bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbother(l,gp))
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
                 
            elif m.data.startswith("charehelp:") :
                gp = m.data.replace("charehelp:","")
                if is_mod(gp,m.from_user.id) :
                    bot.answer_callback_query(m.id, text=ln(l,"charehelp"), show_alert=True)
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("warnhelp:") :
                gp = m.data.replace("warnhelp:","")
                if is_mod(gp,m.from_user.id) :
                    bot.answer_callback_query(m.id, text=ln(l,"warnhelp"), show_alert=True)
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("Processhelp:") :
                gp = m.data.replace("Processhelp:","")
                if is_mod(gp,m.from_user.id) :
                    bot.answer_callback_query(m.id, text=ln(l,"phelp"), show_alert=True)
                else :
                    bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            elif m.data.startswith("muteall:") :
                    gp = m.data.replace("muteall:","")
                    if is_mod(gp,m.from_user.id) :
                        if gg(gp,"muteall") :
                            gr(gp,"muteall")
                        else :
                            gs(gp,"muteall","enabled")
                        bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbother(l,gp))
                    else :
                        bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            for lock in telelocks :
                if m.data.startswith("Lock:"+lock.lower()) :
                    gp = m.data.replace("Lock:"+lock.lower()+":","")
                    if is_mod(gp,m.from_user.id) :
                        if gg(gp,lock.lower()+':Lock') :
                            gr(gp,lock.lower()+':Lock')
                        else :
                            gs(gp,lock.lower()+':Lock',"Locked")
                        bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkblock(l,gp))
                    else :
                        bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            for lock in teleenable :
                if m.data.startswith("Enable:"+lock.lower()) :
                    gp = m.data.replace("Enable:"+lock.lower()+":","")
                    if is_mod(gp,m.from_user.id) :
                        if gg(gp,lock.lower()+':Enable') :
                            gr(gp,lock.lower()+':Enable')
                        else :
                            gs(gp,lock.lower()+':Enable',"Locked")
                        bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbenable(l,gp))
                    else :
                        bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            for lock in teletyps1 :
                if m.data.startswith("Process1:"+lock.lower()) :
                    gp = m.data.replace("Process1:"+lock.lower()+":","")
                    if is_mod(gp,m.from_user.id) :
                        procs = gg(gp,lock.lower()+':Lock')
                        if procs :
                            if procs == "delete" :
                                procs = "warn"
                                gs(gp,lock.lower()+':Lock',"warn")
                            elif procs == "warn" :
                                procs = "kick"
                                gs(gp,lock.lower()+':Lock',"kick")
                            elif procs == "kick" :
                                procs = "ban"
                                gs(gp,lock.lower()+':Lock',"ban")
                            elif procs == "ban" :
                                procs = "gban"
                                gs(gp,lock.lower()+':Lock',"gban")
                            elif procs == "gban" :
                                procs = "off"
                                gr(gp,lock.lower()+':Lock')
                        else :
                            gs(gp,lock.lower()+':Lock',"delete")
                        bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbprocess1(l,gp))
                    else :
                        bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            for lock in teletyps2 :
                if m.data.startswith("Process2:"+lock.lower()) :
                    gp = m.data.replace("Process2:"+lock.lower()+":","")
                    if is_mod(gp,m.from_user.id) :
                        procs = gg(gp,lock.lower()+':Lock')
                        if procs :
                            if procs == "delete" :
                                procs = "warn"
                                gs(gp,lock.lower()+':Lock',"warn")
                            elif procs == "warn" :
                                procs = "kick"
                                gs(gp,lock.lower()+':Lock',"kick")
                            elif procs == "kick" :
                                procs = "ban"
                                gs(gp,lock.lower()+':Lock',"ban")
                            elif procs == "ban" :
                                procs = "gban"
                                gs(gp,lock.lower()+':Lock',"gban")
                            elif procs == "gban" :
                                procs = "off"
                                gr(gp,lock.lower()+':Lock')
                        else :
                            gs(gp,lock.lower()+':Lock',"delete")
                        bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbprocess2(l,gp))
                    else :
                        bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
            for lock in teletyps3 :
                if m.data.startswith("Process3:"+lock.lower()) :
                    gp = m.data.replace("Process3:"+lock.lower()+":","")
                    if is_mod(gp,m.from_user.id) :
                        procs = gg(gp,lock.lower()+':Lock')
                        if procs :
                            if procs == "delete" :
                                procs = "warn"
                                gs(gp,lock.lower()+':Lock',"warn")
                            elif procs == "warn" :
                                procs = "kick"
                                gs(gp,lock.lower()+':Lock',"kick")
                            elif procs == "kick" :
                                procs = "ban"
                                gs(gp,lock.lower()+':Lock',"ban")
                            elif procs == "ban" :
                                procs = "gban"
                                gs(gp,lock.lower()+':Lock',"gban")
                            elif procs == "gban" :
                                procs = "off"
                                gr(gp,lock.lower()+':Lock')
                        else :
                            gs(gp,lock.lower()+':Lock',"delete")
                        bot.edit_message_text(text=ln(l,"getsettings",{"gp" : gp}),parse_mode="Markdown",chat_id = m.message.chat.id,message_id = m.message.message_id,reply_markup=settingkbprocess3(l,gp))
                    else :
                        bot.answer_callback_query(m.id, text=ln(l,"nadmin"), show_alert=True)
        except ApiException as e :
            if e.result.json()['description'].startswith("Too Many Requests: retry after") :
                bot.answer_callback_query(m.id,text="⚠️ Please dont flood retry after "+str(e.result.json()['parameters']["retry_after"]))
                return
            elif e.result.json()['description'] == 'Bad Request: message is not modified':
                return
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            try :
                bot.answer_callback_query(m.id,text="❌ مشکل فنی رخ داد اطلاعات مشکل به مدیریت گزارش شد در صورت نیاز به توضیح بیشتر از قسمت \"ارتباط با ما\" گزارش دهید.")
                bot.answer_callback_query(m.id,text="❌ مشکل فنی رخ داد اطلاعات مشکل به مدیریت گزارش شد در صورت نیاز به توضیح بیشتر از قسمت \"ارتباط با ما\" گزارش دهید.")
            except :
                pass
            bot.send_message(errors_chat,"#خطا_کالبک\nکاربر : "+str(m.from_user.id)+"\nنوع : "+str(exc_type)+"\nفایل : "+str(fname)+"\nخط : "+str(exc_tb.tb_lineno)+"\nشرح خطا : "+str(e))
            print(exc_type, fname, exc_tb.tb_lineno,e)
        except Exception as e :
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            try :
                bot.answer_callback_query(m.id,text="❌ مشکل فنی رخ داد اطلاعات مشکل به مدیریت گزارش شد در صورت نیاز به توضیح بیشتر از قسمت \"ارتباط با ما\" گزارش دهید.")
            except :
                pass
            bot.send_message(errors_chat,"#خطا_کالبک\nکاربر : "+str(m.from_user.id)+"\nنوع : "+str(exc_type)+"\nفایل : "+str(fname)+"\nخط : "+str(exc_tb.tb_lineno)+"\nشرح خطا : "+str(e))
            print(exc_type, fname, exc_tb.tb_lineno,e)
    freeze_support()
    Process(target=callback_kb_multi).start()
bot.polling(none_stop=True)