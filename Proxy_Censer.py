
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
    
    return status


def forbidden():
    Sites_interdis=[]
    while True:
        site=input('input forbidden website:')
        if site=='end':
            break;
        else:
            Sites_interdis.append(site)
    
    return Sites_interdis


def reject(Sites,uri):
    uri= uri.lstrip('http://')
    m= uri.split('/')
    for s in Sites:
        for x in m: 
            if s==x :
                return True
                print('\n\n web site forbidden')
            else :
                return False  


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
    
        
        Sites = forbidden()
        Pserversock= socket(AF_INET,SOCK_STREAM)
        Pserversock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) ##
        Pserversock.bind((Proxy_add,Proxy_port)) 
        Pserversock.listen(1)
        print('proxy http censer is ready')
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
                
                uri =HTTP_request_analyser(request)
                print('requested uri : '+ uri)
                if (reject(Sites,uri)):
                    print('Forbidden web site')
                    rej='HTTP/1.1 403 Forbidden\r\n\r\n'
                    rej+= 'FORBIDDEN'
                    
                    ConnectionSock.sendall(rej.encode('utf-8'))
                else:  
                    to_remoteServer_sock.sendall(request)
                    data=recvall(to_remoteServer_sock,4096)
                    ConnectionSock.sendall(data)
            ConnectionSock.close()
                    
                    
                
            
               
               
              
            
            
ProxyServer('',ProxyPort,ServerAdd)
