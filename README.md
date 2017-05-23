# chat-service-protocol
A network protocol that provides a plaintext chat service running on a simple cli. 

To establish a connection between the server and the client:
Run 'python server.py &' - This will run the server in background.
Then run 'python client.py' - This will connect the client to the server, and once the server receives this connection, it will automatically close the port it was listening on.
