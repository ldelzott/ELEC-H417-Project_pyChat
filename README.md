

# ELEC-H417-Project_pyChat
## Basic description of the project
The goal of this project is to design and implement a basic chat app 
enabling private communication. It will be an opportunity to have a 
practical under-standing of different concepts in cryptography and 
networking studied in thetheoretical classes.This app should be based on
central server allowing an arbitrary numberof clients to create an account
and have encrypted conversation between oneanother.We ask you to be
creative as well, and to implement any features that feelsfunny and/or 
interesting to you. Feel free to go any directions, as long as youmatch 
the requirements.
## Report
https://www.overleaf.com/8771966626yrrznqcxhjmc
..

#Requirements
##Server 

###User management system
- All messages pass through the server
- A new user should be able to create an account on the server, using a tuple (username, password)
- A non-new user should be able to login after proving his identity (username, password)
###Message management system
- Storing conversations linked to tuples (username1, username2)
- Be the 'middleground' for authentication (storing the publics key of the users (?))
- Not able to see the plaintext of conversations between users
##Client
###User management
- Allows users to signup and login
- The user can create a new conversation with another existing username (and help manage the security aspects)
- The user will be able to post/fetch message to/from an existing conversation

#Discussions for the current state of the project:
## Authenticity, confidentiality, integrity
A way to perform encryption could be to follow the method that could be given in the course lecture soon (at least the
method should be inside the book the course is based upon and is defined briefly here : 
https://www.youtube.com/watch?v=1DOVflbRqIU&list=PLo80JwUm6hSSwGLJmS_quaeJgx9SILLiI&index=54 )
The server could be used to store a public key that correspond to each user. The server then act as a "Certificate 
Authority CA" (?). The public/private key of the user could then be used to transfer the symmetric encryption key from 
one user to the other under confidentiality. Then the users could store that symmetric encryption key on their computer 
since this key is the only one that allows to decrypt the encrypted conversations stored on the server. 

## Connecting the clients with the server 
From a customer point of view, the IP address given by an ISPs to the 'internet box' should be dynamic (i.e not fixed in 
time). However, services like dynDNS allows to associate dynamically a domain name to a variable IP address. It means
that the server app (i.e the IP address of the internet box) could have a specific domain name and the clients could, 
from an external subnetwork, query the dynDNS service to receive the current IP address of the server (to be able 
to connect to him even if his IP address is changing from time to time). 
The NAT of the box that "hide" the local network where the server resides should maybe be configured to allows the 
incoming packets to be forwarded to the local IP of the server.

