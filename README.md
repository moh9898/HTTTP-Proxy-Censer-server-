# HTTTP-Proxy-Censer-server-


This project is a realisation of an HTTP Proxy-Censer-Cache Server, that does :

- a basic proxy role by sending back web content of website to client
- a cache proxy that sends back an HTML that's already saved in cache memory after a precedent request (Proxy_cache.py) if it's not done then the request is sent 
to the original server.
- a censer proxy that analyse the client's request and checking the web sites destination request in black list (Proxy_censer.py)
- a proxy log that collect informations of clients that are connected to the web server.

the total proxy is a combination of these 3 programs :  client <=> proxy_Cache <=> Proxy_censer <=> Proxy_log <=> webserver 
