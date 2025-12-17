# Smart Vending Machine
## Project Overview
Verbena, Smart Vending Machine was created to simulate purchasing of digital items. It prioritizes: 
- Viewing Inventory and Selection: Viewing products with their pricing and stock. Easily add or remove items from cart.
- Cart and Inventory Management: Live updation of stock when changes have been made to cart/inventory.
- Payment Simulation: Card information is prompted for purchase to be confirmed.
- Transaction History: Display previous transaction details when required.
- User-friendly and interactive interface: GUI implementation for positive user experience.
- Client-Server Communication: Program handled by the communication between client and server – client handles user interfaces, sends requests and handles responses while server updates database, manages inventory and transaction processing.

## File Functionalities
client.py 
The client establishes communication with the server using sockets. Methods send requests to the server along with data needed to perform tasks. The received responses are then formatted into structured strings with consideration of GUI to display data precisely.


gui.py 
Displaying the client responses received from the server as a graphical interface and enabling the user to interact with the program is handled by GUI. Tkinter elements - buttons, textwidgets, radiobuttons are linked to backend client functions. 
Matplotlib library is used to display graphical representation of data.


server.py 
Server is the backbone for the program functioning. It processes client requests, updates and retrieves data from the database. Each class, Product, Cart, Transactions and Server, ensures error handling by a combination of conditional and try-except statements. Threading is implemented to enable a multi-client environment.


smart_vending_machine.db 
It is the repository of data. It has five database tables: ClientID, Products, Cart, Transactions, PaymentMethod. The server works in close relation with the database for updation of data and performing tasks. 

## Instructions:
1. Download the 'Smart_Vending_Machine.zip' from GitHub. Next, unzip the folder's contents.
2. Run the server (server.py) from Python IDE: to run using a new database, ensure ‘smart_vending_machine.db’ does not preexist in the current directory and that the ‘initialise_database()’ server function is not commented out.
3. Run the client (client.py): in command prompt from within the same directory, enter ‘python client.py’. 
