# BarChat


<p align="center">
  <img src= "https://github.com/barShadmi/BarChat/blob/b573e100abaa99516c1e75f2a5829bf1094fcef4/BarChatReadmefiles/012-user-avatar-5.png" width="100" height="100">
</p>
An app for communicating between users, finding friends, corresponding in groups, sending files, messages, photos and downloading them, saving each user information in the data base of the server. (Server and client attached)

<br></br>

## basic overview

- **Log In**
<p align="center">
  <img src= "https://github.com/barShadmi/BarChat/blob/b573e100abaa99516c1e75f2a5829bf1094fcef4/BarChatReadmefiles/LogIn.gif" height="250">
</p>

- **Sign In**
<p align="center">
  <img src= "https://github.com/barShadmi/BarChat/blob/b573e100abaa99516c1e75f2a5829bf1094fcef4/BarChatReadmefiles/SignIn.gif" height="250">
</p>

- **Add and remove friends**
<p align="center">
  <img src= "https://github.com/barShadmi/BarChat/blob/b573e100abaa99516c1e75f2a5829bf1094fcef4/BarChatReadmefiles/AddRemoveFriend2.gif" height="250">
</p>

- **Accept or ignore friends requests**
<p align="center">
  <img src= "https://github.com/barShadmi/BarChat/blob/b573e100abaa99516c1e75f2a5829bf1094fcef4/BarChatReadmefiles/AcceptFriend.gif" height="250">
</p>

- **Add and remove group and members**
<p align="center">
  <img src= "https://github.com/barShadmi/BarChat/blob/b573e100abaa99516c1e75f2a5829bf1094fcef4/BarChatReadmefiles/AddRemoveGroup2.gif" height="250">
</p>

- **Send files, pictures, massages and download them**
<p align="center">
  <img src= "https://github.com/barShadmi/BarChat/blob/b573e100abaa99516c1e75f2a5829bf1094fcef4/BarChatReadmefiles/AddFile.gif" height="250">
</p>

- **Leave groups**
<p align="center">
  <img src= "https://github.com/barShadmi/BarChat/blob/b573e100abaa99516c1e75f2a5829bf1094fcef4/BarChatReadmefiles/LeaveGroup.gif" height="250">
</p>

<br></br>

## Special Usage
- Using the rsa package for making a asymmetric keys and cryptograpthy to make symmetric key which are used for making a secured connection between the server and client. this is possible by the server sending the encrypt asymmetric key which the client use for sending the server the symmetric key, this key will be used for the connection.
- The server is able to have multiple client connenction so many clients can talk and use the app together
- The server and client supports FTP (File Transformation protocol) so clients can shere files and pictures for downloading and viewing it.
- The client graphic interface is simple and easy to use for talking with friends in dm's and groups.



## installation Options

1. **Server:**
- Download [MySQL](https://dev.mysql.com/downloads/installer/) Windows (x86, 32-bit), MSI Installer	8.0.29	439.6M 
- Write user and password of Mysql in bar_chat_server.py at database object  <img src= "https://github.com/barShadmi/BarChat/blob/b573e100abaa99516c1e75f2a5829bf1094fcef4/BarChatReadmefiles/code.png">
- Download Server Files (BarChat/Server) and Install all missing packages
2. **Client:**
- Download Client Files (BarChat/Client) and enter Server IPv4 to bar_chat_client.py <img src= "https://github.com/barShadmi/BarChat/blob/b573e100abaa99516c1e75f2a5829bf1094fcef4/BarChatReadmefiles/code2.png">
- Change to the correct path of the Client folder to RUN_ME.py <img src= "https://github.com/barShadmi/BarChat/blob/b573e100abaa99516c1e75f2a5829bf1094fcef4/BarChatReadmefiles/Code3.png">

## credits
- This project is using the MySQL database as a data structure
- This project is using tesx box from Github

