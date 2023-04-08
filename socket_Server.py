#完整功能
import PySimpleGUI as sg
import socket
# from time import ctime
import json
import sys
# import time
import os
import threading   #多线程

res=res1=res2=res_data=res_check=res1_check=res2_check=res_data_check=''
deploy={}
def tcpServer():
    BUFFSIZE = 1024
    MAX_LISTEN = 5
    global res,res1,res2,res_data,res_check,res1_check,res_data_check,res2_check
    BUFFSIZE = 1024
    MAX_LISTEN = 5
    ADDR = ('', deploy['port'])
    # TCP服务
    # print(ADDR)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 绑定服务器地址和端口
        socket_link=s.bind(ADDR) 
        # 启动服务监听
        s.listen(MAX_LISTEN)
        res='等待客户端接入。。。。。。。。。。。。'
        # window['-socket list-'].print(res)
        while True:
            # 等待客户端连接请求,获取connSock
            conn, addr = s.accept()
            # print(addr[0])
            res1='远端客户:{!s}已接入！！！'.format(addr)
            # print('远端客户:{} 接入系统！！！'.format(addr))

            with conn:
                while True:
                    # print('接收请求信息。。。。。')
                    res2='接收请求信息。。。。。'
                    # 接收请求信息
                    data = conn.recv(BUFFSIZE)
                    data_len=len(data)   #判断接收数据长度，如果为0，客户端断开，或者网络断开，跳出当前接收状态，重新启动服务。
                    # print('接受到的数据长度：'+str(data_len))
                    # res='接受到的数据长度：'+str(data_len)
                    if data_len ==0:
                        res='客户端已退出'
                        return
                    # print('接收到的数据：{!r}'.format(data.decode('utf-8')))
                    res_data='接收到的数据：{!r}'.format(data.decode('utf-8'))
                    # 发送请求数据
                    conn.send(data)
                    # conn.send(data.encode('utf-8'))
                    # print('发送返回完毕！！！')
        s.close()
def socket_start(): #创建线程，启动socket
    t1 = threading.Thread(target=tcpServer,args=(),name='_socket')  #为socket单开一个线程
    t1.daemon = True #设置为守护线程，主程序关闭后，该线程自动关闭
    t1.start()
def deploy_json(a):  #配置数据读写
    global deploy
    inifile=os.path.dirname(os.path.realpath(sys.argv[0]))+'/ini.json'
    # print(inifile)
    if a == 'read':
        with open(inifile, encoding='UTF-8') as f:
            deploy = json.load(f)
            # print(deploy['port'])
            return
    elif a == 'write':
        with open(inifile, 'w', encoding='UTF-8') as f:
            # print(deploy)
            json.dump(deploy, f,ensure_ascii=False)  #ensure_ascii=False:输出保证将所有输入的非 ASCII 字符转义
            return 
def get_local_ip():  #获取本机IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return (IP)

def main():
    global res,res1,res2,res_data,res_check,res1_check,res_data_check,res2_check,PORT
    deploy_json('read')
    ip = get_local_ip()
    ip_txt='Socket服务器地址:'+str(ip)
    port_txt="Socket端口:"+str(deploy['port'])

    sg.change_look_and_feel("GreenMono")
    socket_ip = sg.Text(ip_txt)
    now_port = sg.Text(port_txt,key='-port-')
    change = sg.Text('修改Socket端口:')
    text1 = sg.Text("TCP协议，仅支持单客户端接入，支持客户端断开后自动重连，更改端口后需要重新启动程序才能生效。")
    textinput = sg.InputText(default_text = deploy['port'],size = (8, 1),disabled = False,key='-in port-')
    socket_list= [[sg.Multiline('',size=(100, 30),disabled = False,background_color = 'slategray3',font=('',12,),key='-socket list-')],]
    bt = sg.Button('确认更改',size=(8,1,),font=(10),disabled = False)
    btn_col=sg.Column([[sg.Button('清空数据',font=(10),disabled = False,size=(8,1),pad=(50,0)),sg.Button('退出',font=(10),disabled = False,size=(5,1),pad=(50,0))]],justification = 'center')
    layout = [[socket_ip,now_port,change,textinput,bt],[text1],[socket_list],[btn_col],]
    window = sg.Window('Socket服务器端软件  V1.0  Tusi版权所有', layout,font=(10))
    socket_start()
    while True:
        event, values = window.read(timeout=10)
        if event in (None, '退出'):
            break#相当于关闭界面
        if event == '清空数据':
            window['-socket list-'].update('数据已清空！！！')

        if event == '确认更改':
            try:
                if int(values['-in port-'])>=0 and int(values['-in port-'])<65536:
                    deploy['port']=int(values['-in port-'])
                    port_txt="Socket端口:"+str(deploy['port'])
                    window['-port-'].update(port_txt)
                    deploy_json('write')
                else:
                    sg.popup('错误！','端口必须在0-65535范围内','请重新输入！',auto_close = 3,font=('',12))
            except:
                sg.popup('错误！','端口必须输入0-65535的整数数字','请重新输入！',auto_close = 3,font=('',12))
        if res !=res_check:
            window['-socket list-'].print(res)
            res_check=res
        if res1 !=res1_check:
            window['-socket list-'].print(res1)
            res1_check=res1    
        if res2 !=res2_check:
            window['-socket list-'].print(res2)
            res2_check=res2 
        if res_data !=res_data_check:
            window['-socket list-'].print(res_data)
            res_data_check=res_data
        if res == '客户端已退出':
            res=res1=res2=res_data=res_check=res1_check=res2_check=res_data_check=''
            socket_start()
            # print(threading.enumerate())
    window.close()

if __name__ == '__main__':
    main()
