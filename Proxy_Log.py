
from socket import *
#import select
import sys
from pathlib import*


ACCEPT= 'HTTP/1.1 200 OK'
ServerAdd = input('input server name:')
ServerPort= int(input('remote server port:'))
ProxyPort = int(input('listening port :'))
print('listening port '+ str(ProxyPort)+'.....')

def ToRemoteServer(RS_add,RS_Port):
    
    
        Pclientsock= socket(AF_INET,SOCK_STREAM)
        
        try:
           Pclientsock.connect((RS_add,RS_Port))
           print('Handshake Remote server'+ ServerAdd)
           return Pclientsock
        except Exception:
            print ('Remote server is down') 
            return False

def HTTP_request_analyser(rqst):
    
    request = rqst.decode('utf-8')
    m= request.split("\n")
    uri=m[0]
    uri= uri.split(" ")[1]
    uri= uri.lstrip('/')
    #URI ONLY NEEDED 
   # if(len(uri)==0):
       # filename= 'index.html'
    #else:
        #filename= uri.lstrip('http://')
        

    
    result = uri
    return result


def HTTP_response_analyser(rspns):
   
        s=rspns
        m= s.split(b'\r\n\r\n')
        header=m[0]
   
        status= header.split(b'\r\n')[0].decode('utf-8')
    
        hdr= header.decode('utf-8')
        html = m[1]
    
        return [status,hdr]
    
    

def recvall(sock, length):
    blocks = []
    l=length
    #i=0
    
    while l==length:
        
        block = sock.recv(length)
        
        if not block:
            raise EOFError('No data'.format(length))
        
        
       
        blocks.append(block)
        l= len(block)
        
    return b''.join(blocks)

def write_log(f,msg):
    
        fm = open(f,'a+')
        fm.write(msg+'\n')
        fm.close()
        fm=open(f,'r')
        print(fm.read())
        fm.close()
   
    


def ProxyServer(Proxy_add,Proxy_port,S_add):
    
        
        
        Pserversock= socket(AF_INET,SOCK_STREAM)
        Pserversock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) ##
        Pserversock.bind((Proxy_add,Proxy_port)) 
        Pserversock.listen(1)
        print('server proxy http log is ready')
     
        while True:
            to_remoteServer_sock= ToRemoteServer(ServerAdd,ServerPort)
            ClientSock, ClientAdd = Pserversock.accept()
            print('handshake Proxy with client: '+str(ClientAdd))
            ConnectionSock= ClientSock
            if to_remoteServer_sock:
                print(str(ClientAdd)+ ' Connected')
            else :
                print('could not establish connection with the remote server')
                print('Closing connection with the client'+ str(ClientAdd))
                ClientSock.close()
            rqst = ConnectionSock.recv(4096)
            if (len(rqst) == 0):
                ConnectionSock.close()
            else :
                print (str(rqst))
                request=rqst.decode('utf-8')                               
                uri= HTTP_request_analyser(rqst)
        
                to_remoteServer_sock.sendall(rqst)
                data= recvall(to_remoteServer_sock,4096)
                
                    
                
                result_s= HTTP_response_analyser(data)
                log='request from: '+str(ClientAdd)+'\n requesed uri:'+uri
                log+='\n request\n'
                log+= '\n Server respones: \n'+str(result_s[1])+'\n end log\r\n'
                if(result_s[0]== ACCEPT):
                    print('creating Log file ....\n')
                    f= Path('log.txt')
                    write_log(f,log)
                    file= open(f,'r')
                    
                    
                    print('\n\n Log File saved')
                    
                    
                ConnectionSock.sendall(data)
                    
                    
              
            
            
ProxyServer('',ProxyPort,ServerAdd)

