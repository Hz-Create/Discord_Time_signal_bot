import discord
import datetime
import random
import time
import asyncio

from discord import channel
from discord import message
from discord.utils import snowflake_time

client = discord.Client()
say_task = None
setting_task = None
# 管理者ロールを追加する場合はここに[~, ROLEID]
# ここからサーバーによる
admin_roles = ["ROLES",]
set_time = []

CHANNEL_ID ='CHANNEL_ID' 
async def start_bot():
    channel = client.get_channel(CHANNEL_ID)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await start_bot()

    ch_name = "CH_NAME"
# ここまで
    for channel in client.get_all_channels():
        if channel.name == ch_name:
            await channel.send('こんにちは！ ヘルプを参照するには[>help]と入力してください。\nHi! If you need help, type[>help].')

@client.event
async def on_message(message):
    # global定義
    global set_time
    global say_task
    global count
    is_intask = False
    global setting_task
    global check_ad
    check_ad = False
    global is_seted_up
    is_seted_up = False
    global second_time_loop
    second_time_loop = False
    
    def get_h_m_s(td):
        m, s = divmod(td.seconds, 60)
        h, m = divmod(m, 60)
        return h, m, s

    
    
    if message.author == client.user:
        return
# 時報時刻設定
    if message.content.startswith('>set time') and is_intask == False:
        print(is_intask)
        def check(msg):
            return msg.author == message.author
            # ユーザー確認
        for p in admin_roles:
            if p in [users_role.id for users_role in message.author.roles]:
                
                set_time = []
                # 各種設定
                await message.channel.send("時報の時間設定をします。")
                await message.channel.send("設定したい時間の数を入力してください。1時と2時を指定したい場合は(2と入力)")
                need_set_time_row = await client.wait_for("message", check=check)
                set_time_row = int(need_set_time_row.content)
                a = 0
                while set_time_row != a:
                    await message.channel.send("設定したい時間の時を24時間表記で入力してください。(Type: PM2時半の場合は今は,14)")
                    set_time_input_h_m = await client.wait_for("message", check=check)
                    await message.channel.send("設定したい時間の分を入力してください。(Type: PM2時半の場合は今は, 30)")
                    set_time_input_m_m = await client.wait_for("message", check=check)
                    set_time_input_h = int(set_time_input_h_m.content)
                    set_time_input_m = int(set_time_input_m_m.content)
                    set_time_input_h_s = set_time_input_h * 60 * 60
                    set_time_input_m_s = set_time_input_m * 60
                    set_time_input = set_time_input_h_s + set_time_input_m_s
                    set_time.append(set_time_input)
                    a += 1
                await message.channel.send("設定が完了しました。このコマンドを再度実行すると設定した時間は削除されます。")
                print(set_time)
                break


        else :
            await message.channel.send("権限がありません。")
    # 時報機能 
    if message.content.startswith('>start time signal') and is_intask == False:
        print(is_intask)
        print("a")
        for p in admin_roles:
            print("fp")
            if p in [users_role.id for users_role in message.author.roles]:
                check_ad = True
                await message.channel.send("時報システムを起動します。終了するには[>stop time signal]を入力してください。")
                # タスク開始
                say_task = asyncio.current_task()
                is_intask = True
                check_ad = False
                # 現在時刻取得
                # sb_now  = datetime.datetime.fromtimestamp(time.time())
                DIFF_JST_FROM_UTC = 9
                sb_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
                sb_now_h = int(sb_now.hour)
                print(sb_now_h)
                sb_now_m = int(sb_now.strftime('%M'))
                print(sb_now_m)
                sb_now_s = int(sb_now.strftime('%S'))
                print(sb_now_s)
                print(sb_now)
                s_now = ((sb_now_h * 60) * 60) + (sb_now_m * 60) + sb_now_s

                print("farst",s_now)
                paa = 0
                is_farst = False
                count = 0
                # 時間設定確認
                if len(set_time) != 0:
                    print("S")
                    set_time.sort()
                    # ループ開始
                    while True:
                        for set_time_r in set_time:
                            print("settime"+str(set_time_r))
                            # forによる配列の取り出し
                            # および秒数化
                            DIFF_JST_FROM_UTC = 9
                            sb_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
                            sb_now_h = int(sb_now.strftime('%H'))
                            print(sb_now_h)
                            sb_now_m = int(sb_now.strftime('%M'))
                            print(sb_now_m)
                            sb_now_s = int(sb_now.strftime('%S'))
                            print(sb_now_s)
                            print(sb_now)
                            s_now = ((sb_now_h * 60) * 60) + (sb_now_m * 60) + sb_now_s

                            print("second",s_now)
                            # 現在時刻との比較
                            if set_time_r > s_now or set_time_r < 901 and second_time_loop == True:
                                second_time_loop = False
                                print(set_time_r > s_now)
                                
                                print(len(set_time))
                                # if set_time[0] < 300:
                                # # 86399
                                # s_now_24 = 86400 + int(set_time[0])
                                # wait_time_24 = s_now_24 - s_now
                                # print("24time_wait"+str(wait_time_24))
                                # 設定時間が901秒（つまり0時15分）以下の場合時間を逆算する。Memo.最初からこうすればよかったｗ
                                if set_time_r < 901:
                                    print(set_time_r < 901)
                                    s_wait_24 = 86400 + int(set_time_r)
                                    wait_time = s_wait_24 - s_now
                                    
                                else:
                                    second_time_loop = True
                                    wait_time = set_time_r - s_now
                                # 待ち時間の計算
                                wait_time_center = wait_time // 2
                                # 表示用の時間を秒から復元
                                td = datetime.timedelta(seconds=set_time_r)
                                set_time_show_list = get_h_m_s(td)
                                print(set_time_show_list)

                                print("full_time"+str(wait_time))
                                print("check point"+ str(wait_time_center))
                                # 表示分岐
                                if len(str(set_time_show_list[1])) == 1:
                                    await message.channel.send("次の時報> "+str(set_time_show_list[0])+":0"+str(set_time_show_list[1]))
                                else:
                                    await message.channel.send("次の時報> "+str(set_time_show_list[0])+":"+str(set_time_show_list[1]))
                                    # 一回目の待機
                                while count != wait_time_center:
                                    await asyncio.sleep(1)
                                    count += 1
                                    print(count)
                                # 二回目の処理
                                DIFF_JST_FROM_UTC = 9
                                sb_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
                                sb_now_h = int(sb_now.strftime('%H'))
                                print(sb_now_h)
                                sb_now_m = int(sb_now.strftime('%M'))
                                print(sb_now_m)
                                sb_now_s = int(sb_now.strftime('%S'))
                                print(sb_now_s)
                                print(sb_now)
                                s_now = ((sb_now_h * 60) * 60) + (sb_now_m * 60) + sb_now_s

                                print(s_now)
                                # 二回目の待機
                                if set_time_r < 901:
                                    print(set_time_r < 901)
                                    s_wait_24 = 86400 + int(set_time_r)
                                    wait_time = s_wait_24 - s_now
                                    
                                else:
                                    second_time_loop = True
                                    wait_time = set_time_r - s_now
                                wait_time_right = wait_time // 2
                                print("full_time"+str(wait_time))
                                print("check point"+ str(wait_time_right))
                                count = 0
                                while count != wait_time_right:
                                    await asyncio.sleep(1)
                                    count += 1
                                    print(count)
                                # 長さでの分岐 5000以上
                                if wait_time_right >= 5000 :
                                    # 三回目の処理
                                    DIFF_JST_FROM_UTC = 9
                                    sb_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
                                    print(sb_now_h)
                                    sb_now_m = int(sb_now.strftime('%M'))
                                    print(sb_now_m)
                                    sb_now_s = int(sb_now.strftime('%S'))
                                    print(sb_now_s)
                                    print(sb_now)
                                    s_now = ((sb_now_h * 60) * 60) + (sb_now_m * 60) + sb_now_s

                                    print(s_now)
                                    # 三回目の待機
                                    if set_time_r < 901:
                                        print(set_time_r < 901)
                                        s_wait_24 = 86400 + int(set_time_r)
                                        wait_time = s_wait_24 - s_now
                                    
                                    else:
                                        second_time_loop = True
                                        wait_time = set_time_r - s_now
                                    wait_time_right = wait_time // 2
                                    print("full_time"+str(wait_time))
                                    print("check point"+ str(wait_time_right))
                                    count = 0
                                    while count != wait_time_right:
                                        await asyncio.sleep(1)
                                        count += 1
                                        print(count)
                                    
                                    # 四回目の処理
                                    DIFF_JST_FROM_UTC = 9
                                    sb_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC) 
                                    sb_now_h = int(sb_now.strftime('%H'))
                                    print(sb_now_h)
                                    sb_now_m = int(sb_now.strftime('%M'))
                                    print(sb_now_m)
                                    sb_now_s = int(sb_now.strftime('%S'))
                                    print(sb_now_s)
                                    print(sb_now)
                                    s_now = ((sb_now_h * 60) * 60) + (sb_now_m * 60) + sb_now_s

                                    print(s_now)
                                    # 四回目の待機
                                    if set_time_r < 901:
                                        print(set_time_r < 901)
                                        s_wait_24 = 86400 + int(set_time_r)
                                        wait_time = s_wait_24 - s_now
                                        
                                    else:
                                        second_time_loop = True
                                        wait_time = set_time_r - s_now
                                    wait_time_right = wait_time // 2
                                    print("full_time"+str(wait_time))
                                    print("check point"+ str(wait_time_right))
                                    count = 0
                                    while count != wait_time_right:
                                        await asyncio.sleep(1)
                                        count += 1
                                        print(str(count))
                                # 時間での分岐 1500以上
                                elif wait_time_right >= 1500 :
                                    print("1step pass")
                                    # 三回目の処理
                                    DIFF_JST_FROM_UTC = 9
                                    sb_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
                                    sb_now_h = int(sb_now.strftime('%H'))
                                    print(sb_now_h)
                                    sb_now_m = int(sb_now.strftime('%M'))
                                    print(sb_now_m)
                                    sb_now_s = int(sb_now.strftime('%S'))
                                    print(sb_now_s)
                                    print(sb_now)
                                    s_now = ((sb_now_h * 60) * 60) + (sb_now_m * 60) + sb_now_s

                                    print(s_now)
                                    # 三回目の待機
                                    if set_time_r < 901:
                                        print(set_time_r < 901)
                                        s_wait_24 = 86400 + int(set_time_r)
                                        wait_time = s_wait_24 - s_now
                                        
                                    else:
                                        second_time_loop = True
                                        wait_time = set_time_r - s_now
                                    wait_time_right = wait_time // 2
                                    print("full_time"+str(wait_time))
                                    print("check point"+ str(wait_time_right))
                                    count = 0
                                    while count != wait_time_right:
                                        await asyncio.sleep(1)
                                        count += 1
                                        print(count)
                                # 時間での分岐 1499以下
                                if wait_time_right <= 1499 :
                                    print("2step pass")
                                # 五回目の処理
                                DIFF_JST_FROM_UTC = 9
                                sb_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
                                sb_now_h = int(sb_now.strftime('%H'))
                                print(sb_now_h)
                                sb_now_m = int(sb_now.strftime('%M'))
                                print(sb_now_m)
                                sb_now_s = int(sb_now.strftime('%S'))
                                print(sb_now_s)
                                print(sb_now)
                                s_now = ((sb_now_h * 60) * 60) + (sb_now_m * 60) + sb_now_s

                                print(s_now)
                                # 五回目の待機
                                if set_time_r < 901:
                                        print(set_time_r < 901)
                                        s_wait_24 = 86400 + int(set_time_r)
                                        wait_time = s_wait_24 - s_now
                                        
                                else:
                                    second_time_loop = True
                                    wait_time = set_time_r - s_now
                                print("break point"+ str(wait_time))
                                count = 0
                                while count != wait_time:
                                    await asyncio.sleep(1)
                                    count += 1
                                    print(str(count))
                                    # 終了処理 分が0であれば
                                if str(set_time_show_list[1]) == 0 :
                                    await message.channel.send(str(set_time_show_list[0])+"時をお知らせします。")
                                elif len(str(set_time_show_list[1])) == 1:
                                    await message.channel.send(str(set_time_show_list[0])+"時0"+str(set_time_show_list[1])+"分をお知らせします。")
                                else:
                                    await message.channel.send(str(set_time_show_list[0])+"時"+str(set_time_show_list[1])+"分をお知らせします。")
                                count = 0
                                
                                print(count, "pass")
                                
                                print("end roop")

                        else:
                            print(set_time_r > s_now)
                            second_time_loop = True
                            if is_farst == False:
                                # 表示用の時間を秒から復元
                                td = datetime.timedelta(seconds=set_time[0])
                                set_time_show_list = get_h_m_s(td)
                                print(set_time_show_list)
                                # 表示分岐
                                if set_time_r >= 901: 
                                    pass
                                else:
                                    if len(str(set_time_r)) == 1:
                                        await message.channel.send("次の時報> "+str(set_time_show_list[0])+":0"+str(set_time_show_list[1]))
                                    else:
                                        await message.channel.send("次の時報> "+str(set_time_show_list[0])+":"+str(set_time_show_list[1]))
                                is_farst = True
                            
                            print("pass")
                            paa += 1
                            paaw = 0
                            if paa >= 10:

                                while paaw != 900:
                                    await asyncio.sleep(1)
                                    paaw += 1
                                    print(paaw)
                                paa = 0
                            continue

                else:
                    await message.channel.send("時間が設定されていません")
            
        else :
            await message.channel.send("権限がありません。")

    if message.content.startswith('>stop time signal'):
        try: 
            say_task.cancel()
            is_intask = False
            await message.channel.send("システムが停止しました。")
        except: 
            print("no runnig task")
    
    
    if message.content.startswith('>emergency stop'):
        try: 
            say_task.cancel()
            is_intask = False
            await message.channel.send("システムを緊急停止しました。管理者にご連絡ください。")
        except: 
            print("no runnig task")

    
    if message.content.startswith(">help"):
        await message.channel.send('このシステムのヘルプです。\nAn: 適切な権限を所有している必要あり。\n[>set time]An: 時報の時間の指定に使用します。\n[>start time signal]An: 時報を起動させます。事前の時間設定が必要です。\n[>stop time signal]An: 時報を停止します。\n[>emergency stop]: 時報を緊急停止させます。\n不具合の場合は管理者に連絡してください。\n©2021 Hz')

client.run('TOKEN')


# message.content.startswith(''):
# await message.channel.send('')
# wait_time_user_set = await client.wait_for("message", check=check)
# stay_time_s = int(wait_time_user_set.content)
# def check(msg):
# return msg.author == message.author
# wait_time_right = wait_time // 2