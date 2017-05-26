# chat-service-protocol
A network protocol that provides a plaintext chat service running on a simple cli. 

## To establish a connection between the server and the client:
* Run 'python server.py &' - This will run the server in background.
* Then run 'python threads.py' - This will connect the client to the server, and once the server receives this connection, it will automatically close the port it was listening on.
* Once the connection has been closed, you will manually have to kill the process that was running the server, otherwise you'll get a 'Address already in use' error. 
