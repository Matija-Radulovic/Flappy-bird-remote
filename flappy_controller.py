import socket 
import pickle
import threading 
import tkinter as tk 

#class for msg and this?
#goofy ass code

bird_x=0
curr_bird_y =0
curr_x_speed_pxps=0
curr_y_speed_pxps=0

bird_r =0

screen_w=0
screen_h=0

gravity_pxps=0
jump_vel_pxps=0

pipes=[]

client_socket=None 
connected=False 

listening_thread=None
def JumpPressed(socket):
    if(connected):
        socket.sendall(('j').encode("ASCII")) 
        Log("Jumped.")


def ConnectPressed():#hmmmmm
    global listening_thread,client_socket, connected, screen_h,screen_w,bird_x,bird_r,gravity_pxps,jump_vel_pxps, connected 

    if(connected):
        return#?
    address=server_address_var.get()
    port=server_port_var.get()
    
    
    client_socket=Connect(address,port)
    
    if(not client_socket):
        return
    Log("Connected.")
    
    raw=client_socket.recv(1024)
    data=pickle.load(raw)
    
    (screen_w,screen_h)=data[0]
    (bird_x,bird_r,jump_vel_pxps,gravity_pxps)=data[1]
    
    connected=True

    listening_thread=threading.Thread(target=Listener,args=(port))
    listening_thread.setDaemon(True)
    listening_thread.start()
    
def Connect(ip,port):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sock.connect((ip,int(port)))
    except Exception as e:
        print(e)
        return None
    return sock


def Listener(sock):#hmmmmm
    global connected

    while (connected):
        raw=sock.recv(1024)
        if(len(raw)==0):#hmmmmm
            connected=False
            client_socket.close()
        
        data=pickle.load(raw)
        
        global curr_bird_y,curr_x_speed_pxps,curr_y_speed_pxps,pipes
        
        (curr_bird_y,curr_y_speed_pxps)=data[0]
        curr_x_speed_pxps=data[1]
        pipes=data[2]
def Log(msg):
    log.insert(tk.END, msg+"\n")

window=tk.Tk()
window.title("Flappy client")
window.geometry('400x300')

input_address_label=tk.Label(text="Insert IP address")
input_address_label.pack()

server_address_var=tk.StringVar()
input_address=tk.Entry(window,textvariable=server_address_var)
input_address.insert(0,"127.0.0.1")
input_address.pack()

input_port_label=tk.Label(text="Insert port")
input_port_label.pack()

server_port_var=tk.StringVar()
input_port=tk.Entry(window,textvariable=server_port_var)
input_port.insert(0,"3334")
input_port.pack()

connect_button=tk.Button(window,text="Connect",command=ConnectPressed)
connect_button.pack()

jump_button=tk.Button(window,text="Jump",command=JumpPressed)
jump_button.pack()

log=tk.Text(window,height=10,width=50)
log.pack()

window.mainloop()
