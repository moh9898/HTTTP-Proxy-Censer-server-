
from socket import *
#import select
import sys
from pathlib import*


ProxyPort = 4490
ServerPort= 80
ServerAdd = 'localhost'


def ToRemoteServer(RS_add,RS_Port):
    
    
        Pclientsock= socket(AF_INET,SOCK_STREAM)
        
        try:
           Pclientsock.connect((RS_add,RS_Port))
           print('Handshake Remote server')
           return Pclientsock
        except Exception:
            print (Exception) 
            return False

def HTTP_request_analyser(rqst):
    
    request = rqst.decode('utf-8')
    m= request.split("\n")
    #print(m)
    uri=m[0]
    #print(uri)
    uri= uri.split(" ")[1]
    #print(uri)
    uri= uri.lstrip('/')
    #print(uri)
    if(len(uri)==0):
        filename= 'index.html'
    else:
        filename= uri 
        
    #print(filename)
    
    Hostname = m[1].split(" ")[1].lstrip('\r')
    result = [Hostname,filename]
    return result

def HTTP_response_analyser(rspns):
    print(rspns)
    response = rspns.decode('utf-8')
    m = response.split('\r\n\r\n\n')
    header= m[0]
    Content_length= header.split('\r\n')[6].split(" ")
    length= Content_length[1]
    html = m[1]
    result = [length,html]
    return result

def recvall(sock, length):
    blocks = []
    l=length
    #i=0
    s= True
    while l==length:
        
        block = sock.recv(length)
        
        if not block:
            raise EOFError('socket closed with %d bytes left in this block'.format(length))
        
        
       # i+=1
        #print('--------block'+ str(i)+'------length= '+str(len(block))+'--------')
        #print(str(block))
        blocks.append(block)
        l= len(block)
        
    return b''.join(blocks)


def ProxyServer(Proxy_add,Proxy_port,S_add):
    
        Cache= Path('cache')
       # if  not Cache.is_dir:
        if(Cache.is_dir()== False):
            Cache.mkdir()
            print('Cache directory created')
        
        Pserversock= socket(AF_INET,SOCK_STREAM)
        Pserversock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) ##
        Pserversock.bind((Proxy_add,Proxy_port)) 
        Pserversock.listen(1)
     
        while True:
            to_remoteServer_sock= ToRemoteServer(ServerAdd,ServerPort)
            ClientSock, ClientAdd = Pserversock.accept()
            print('handshake Proxy with client')
            ConnectionSock= ClientSock
            if to_remoteServer_sock:
                print(str(ClientAdd)+ ' Connected')
            else :
                print('could not establish connection with the remote server')
                print('Closing connection with the client'+ ClientAdd)
                ClientSock.close()
            data = ConnectionSock.recv(4096)
            if (len(data) == 0):
                ConnectionSock.close()
            else :
                print (str(data))
                req =HTTP_request_analyser(data)
                hostname=req[0]
                file_name= req[1]
                print(hostname)
                print(file_name)
               # if(not(hostname == S_add)):
                 #  print('host: '+ hostname+ ' not found')
                    #   ConnectionSock.close()
                    #break;
                
                
                print('\n'+ file_name+' requested to remote server...')
                f_= Path('cache/'+file_name)
                if(f_.is_file()):
                    html=open(f_,'rb')
                    ConnectionSock.sendall(html.read())
                else:        
                    to_remoteServer_sock.sendall(data)
                    data= recvall(to_remoteServer_sock,4096)
                    #print(data.decode('utf-8'))
                    html=HTTP_response_analyser(data)[1]
                    file = Path('cache/'+file_name)
                    file.write_text(html)
                    print('file:')
                    f= open(file,'rb')
                   
                    #print(f.read().decode('utf-8'))
                    ConnectionSock.sendall(f.read())
                    f.close()
                
                   
            
ProxyServer('',ProxyPort,ServerAdd)




-----------------------------------------------------


--------------------------------------------------------------------------------------------------------

from socket import *
from pathlib import*

ACCEPT= 'HTTP/1.1 200 OK'
NOT_FOUND='HTTP/1.1 404 Not Found'

ServerAdd = input('input server name:')
ServerPort= 80
ProxyPort = int(input('listening port :'))
print('listening port '+ str(ProxyPort)+'.....')




def ToRemoteServer(RS_add,RS_Port):
    
    
        Pclientsock= socket(AF_INET,SOCK_STREAM)
        
        try:
           Pclientsock.connect((RS_add,RS_Port))
           print('Handshake with Remote server: '+ ServerAdd)
           return Pclientsock
        except Exception:
            print ('the remote server : '+ServerAdd+' is down') 
            return False

def HTTP_request_analyser(rqst):
    
    request = rqst.decode('utf-8')
    m= request.split("\n")
    uri=m[0]
    uri= uri.split(" ")[1]
    uri= uri.lstrip('/')
    
    if(len(uri)==0):
        filename= 'index.html'
    else:
        filename= uri.lstrip('http://')
        print(filename)
        
        

    
    Hostname = m[1].split(" ")[1].lstrip('\r')
    
    filename_list= filename.split('/')
    print(filename_list)
    filename= filename_list[len(filename_list)-1].lstrip('/')
    print(filename)
    
    result = [Hostname,filename]
    return result

def HTTP_response_analyser(rspns):
    s=rspns
    m= s.split(b'\r\n\r\n')
    header=m[0]
    status= header.split(b'\r\n')[0].decode('utf-8')
    
    return status
    
    
   
   
        

   

def recvall(sock, length):
    blocks = []
    l=length
    
    while l==length:
        
        block = sock.recv(length)
        
        if not block:
            raise EOFError('No data'.format(length))
      
        blocks.append(block)
        l= len(block)
        
    return b''.join(blocks)



def ProxyServer(Proxy_add,Proxy_port,S_add):
    
        Cache= Path('cache')
        if(Cache.is_dir()== False):
            Cache.mkdir()
            print('Cache directory created')
        
        Pserversock= socket(AF_INET,SOCK_STREAM)
        Pserversock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) ##
        Pserversock.bind((Proxy_add,Proxy_port)) 
        Pserversock.listen(1)
        print('proxy http cache is ready')
        while True:
            to_remoteServer_sock= ToRemoteServer(ServerAdd,ServerPort)
            ConnectionSock, ClientAdd = Pserversock.accept()
            print('handshake Proxy with '+ str(ClientAdd)+'.....\n')
            
            
            if to_remoteServer_sock:
                print(str(ClientAdd)+ ' Connected\n')
            else :
                print('could not establish connection with the remote server\n')
                print('\nClosing connection with the client'+ str(ClientAdd))
                ClientSock.close()
            
            
            request = ConnectionSock.recv(4096)
            
            if (len(request) == 0):
                ConnectionSock.close()
                print('NO REQUEST\n')
            else :
                print ('\n Request: '+request.decode('utf-8'))
                
                req =HTTP_request_analyser(request)
                hostname=req[0]
                file_name= req[1]
               
               
                
                
                print('\n'+ file_name+' requested to remote server...\n')
                
            
                f_= Path('cache/'+S_add+'_'+file_name)
                
                if(f_.is_file()):
                    print('file exists\n')
                    html=open(f_,'br')
                    ConnectionSock.sendall(html.read())
                    print('file sent to :'+ str(ClientAdd))
                    print('\n Connection Socket closed\n')
                else:        
                    
                    to_remoteServer_sock.sendall(request)
                    data= recvall(to_remoteServer_sock,4096)
                    print('data received from remote server\n')
                    
                     
                    status= HTTP_response_analyser(data)
                    
                    
                    
                    if status ==ACCEPT:
                        
                        print(' file creation ....\n')
                        
                        f_.write_bytes(data)
                        ConnectionSock.sendall(data)
                        print('file sent to' + str(ClientAdd))
                        
                        print('file saved in cache memory\n')
                        ConnectionSock.close()
                        print('Connection Socket close\n')
                        
                   
                    else:
                        
                        print('data sent without cache saving')
                        
                        ConnectionSock.sendall(data)
                        ConnectionSock.close()
                        
                   
                    
                    
                    
              
            
            
ProxyServer('',ProxyPort,ServerAdd)


