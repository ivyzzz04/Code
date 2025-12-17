import sqlite3
import socket
from datetime import datetime
import threading

# Class handling all methods related to inventory management
class Product:
    def __init__(self,conn):
        self.conn=conn
        self.cursor=self.conn.cursor()

    # Method that handles retrieving available products from Product database table
    def load_inventory_from_db(self):
        self.cursor.execute("SELECT * FROM Products")
        products = self.cursor.fetchall() 
        response = "\n".join(
            f"{row[0]}|{row[1]}|{row[2]}|{row[3]}" for row in products
        )
        return response
    
    # Method to handle stock adjustments to Product database table when items are added to or removed from the cart
    def update_inventory_in_db(self,cart_action,product_id,quantity):
        if cart_action=="add":
            self.cursor.execute("UPDATE Products SET stock = stock - ? WHERE productID = ?", (quantity, product_id))
            self.conn.commit() 

        if cart_action=="remove":
            self.cursor.execute("UPDATE Products SET stock = stock + ? WHERE productID = ?", (quantity, product_id))
            self.conn.commit()     

# Class to handle all tasks in relation to current cart
class Cart:
    def __init__(self,conn,product_manager):
        self.conn=conn
        self.cursor=self.conn.cursor()
        self.product=product_manager

    # Method to add items to cart i.e., to Cart database table
    def add_to_cart(self,client_id,product_id,quantity):
        try:
            self.cursor.execute("SELECT productName, stock, price FROM Products WHERE productID = ?", (product_id,))
            product = self.cursor.fetchone()
            if product:
                if product[1] >= quantity:
                    self.cursor.execute("SELECT quantity FROM Cart WHERE clientID = ? AND productID = ?", (client_id, product_id))
                    item = self.cursor.fetchone()
                    # If item already in cart, quantity of existing item is incremented 
                    if item:
                        add_quantity=item[0]+quantity
                        self.cursor.execute("UPDATE Cart SET quantity = ? WHERE clientID = ? AND productID = ?", (add_quantity,client_id,product_id))
                        self.product.update_inventory_in_db("add",product_id,quantity)
                        self.conn.commit()
                        response= f"\nSuccessfully added {quantity} more of {product[0]} to cart."
                    # Else, the item is newly added to cart 
                    else:
                        self.cursor.execute("INSERT INTO Cart (clientID, productID, quantity) VALUES (?, ?, ?)", (client_id, product_id, quantity))
                        self.product.update_inventory_in_db("add",product_id,quantity)
                        self.conn.commit()
                        response= f"\nSuccessfully added {quantity} of {product[0]} to cart."   
                else:
                    response=f"\nInsufficient stock for {product[0]}."
            else:
                response=f"\nInvalid input. Try again."
        except Exception as e:
            response=f"\nError: {e}"

        return response
    
    # Method to remove an item from cart i.e., Cart database table
    def remove_from_cart(self,client_id,product_id,quantity):
        try:
            self.cursor.execute("SELECT productID, quantity FROM Cart WHERE clientID = ? AND productID = ?", (client_id,product_id))
            item = self.cursor.fetchone()
            if item:
                # If cart quantity > user given quantity, the given quantity is removed from cart and added back to inventory
                if item[1]>quantity:
                    new_quantity=item[1]-quantity
                    self.cursor.execute("UPDATE Cart SET quantity = ? WHERE clientID = ? AND productID = ?",(new_quantity,client_id,product_id))
                    self.product.update_inventory_in_db("remove",product_id,quantity)
                    self.conn.commit()
                    response = f"\nSuccessfully removed {quantity} of Product {product_id} from cart."

                # If cart quantity = user given quantity, the entire item is removed from cart and added back to inventory 
                elif quantity==item[1]:
                    self.cursor.execute("DELETE FROM Cart WHERE clientID = ? AND productID = ?", (client_id, product_id))
                    self.product.update_inventory_in_db("remove",product_id,quantity)
                    self.conn.commit()
                    response = f"\nSuccessfully removed Product {product_id} from cart."
                
                # If user given quantity exceeds in value, error message is returned
                else:
                    response = f"\nInsufficient stock. Availability is {item[1]} only."
            else:
                response=f"\nInvalid input. Try again."
        except Exception as e:
            response = f"\nError: {e}"
        return response
    
    # Method retrieving current items in cart i.e, from Cart database table
    def view_cart_from_db(self,client_id):
        try:
            self.cursor.execute("""
            SELECT c.cartID, p.productName, c.quantity, p.price, (c.quantity * p.price) AS totalPrice
            FROM Cart c
            JOIN Products p ON c.productID = p.productID 
            WHERE c. clientID = ?
            """,(client_id,))
            cart_items = self.cursor.fetchall()
            # If cart is empty, returns string carrying said response
            if not cart_items:
                response = f"Your cart is empty."
            # Else, returns string of cart details values including id, product name, quantity, price, and total price
            else:
                response = "\n".join(
                    f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}" for row in cart_items
                )
        except Exception as e:
            response = f"\nError: {e}"
        return response
    
    # Method handling retrieving cart contents i.e, from Cart database table when proceeding to checkout
    def checkout_payment(self,client_id):
        try:
            self.cursor.execute("""
            SELECT c.productID, p.productName, c.quantity, (c.quantity * p.price) AS totalPrice
            FROM Cart c
            JOIN Products p ON c.productID = p.productID
            WHERE clientID = ?""", (client_id,))
            cart_items = self.cursor.fetchall()
            # If cart is empty, returns string carrying the response
            if not cart_items:
                response = "\nYour cart is empty."
            # Else, returns string of values of current cart details including product name, quantity and total price
            else:
                response = "\n".join(
                    f"{row[1]}|{row[2]}|{row[3]}" for row in cart_items
                            )
        except Exception as e:
            response = f"\nError: {e}"
        return response    

# Class handling execution with PaymentMethod database table and transaction related operations
class Transaction:
    def __init__(self,conn):
        self.conn=conn
        self.cursor=self.conn.cursor()
        self.date_and_time=(datetime.now()).strftime("%d/%m/%Y %H:%M:%S")

    # Method to verify and insert card information to PaymentMethod database table
    def payment(self, payment_method, client_id, name, card_number, expiry_date, cvc):     
        try:
            # If card number or cvc are not solely integers, or the card number is not equal to 16 - transaction does not go through
            if not card_number.isdigit() or len(card_number)!=16 or not cvc.isdigit():
                response=f"\nPayment Unsuccessful"
            else:
                card_number_modified = "XXXXXXXXXXXX" + card_number[-4:]                            # Hiding card number digits to implement security and privacy                                             
                # Saving card details into PaymentMethod database table to keep a record of it
                self.cursor.execute(
                    "INSERT INTO PaymentMethod (paymentClient, paymentDate, nameCard, paymentType, cardNumber, cardDate, cardCvc) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                    (client_id, self.date_and_time, name, payment_method,card_number_modified, expiry_date, cvc)
                )
                self.conn.commit()
                response=f"\nTransaction Complete."
        except Exception as e:
            response=f"Error: {e}"

        return response
    
    # Method to insert and save transaction purchases to Transactions database table 
    def save_transaction_in_db(self,client_id):
        self.cursor.execute("""
        SELECT p.productName, c.quantity, (c.quantity * p.price) AS totalPrice
        FROM Cart c
        JOIN Products p ON c.productID = p.productID
        WHERE clientID = ?""",(client_id,))
        cart_items = self.cursor.fetchall()

        for i in cart_items:
            self.cursor.execute("""
            INSERT INTO Transactions (transactionClient,transactionDate,productName,quantity,totalAmount) VALUES(?,?,?,?,?)
            """,(client_id,self.date_and_time,i[0],i[1],i[2]))

        self.conn.commit()
    
    # Method retrieving previous transaction history by accessing Transaction database table
    def view_transaction_from_db(self,client_id):
        try:
            self.cursor.execute("SELECT transactionDate,productName,quantity,totalAmount FROM Transactions WHERE transactionClient = ?",(client_id,))
            transaction = self.cursor.fetchall()
            # If cart is empty, returns string carrying the response
            if not transaction:
                response="\nNo previous transactions found."
            # Else, returns string of values of previous transaction details including date, product name, quantity and total price
            else:
                response = "\n".join(
                    f"{row[0]}|{row[1]}|{row[2]}|{row[3]}" for row in transaction
                )
        except Exception as e:
            response=f"Error: {e}"
        return response

# Class to handle client-server communication
class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_counter=0
        self.server_socket.bind(('localhost',5000))
        self.server_socket.listen(5)
        print("Server is running on port 5000...")
        #initialise_database()

    # Method that handles client request, executes and sends response back, which is then displayed in GUI
    def handle_client(self,client_socket,client_id):
        try:    
            conn = sqlite3.connect("smart_vending_machine.db")
            cursor = conn.cursor()
            product = Product(conn)
            cart = Cart(conn,product)
            transaction = Transaction(conn)

            while True:
                # If no response, it will break the infinite while loop
                request = client_socket.recv(4096).decode()
                if not request:
                    break  

                command,*args = request.split("|")

                if command == "view_products":
                    response=product.load_inventory_from_db()
                    client_socket.send(response.encode())

                elif command == "add_to_cart":
                    product_id, quantity = map(int, args)
                    response=cart.add_to_cart(client_id,product_id,quantity)
                    client_socket.send(response.encode())

                elif command=="remove_from_cart":
                    product_id, quantity = map(int, args)
                    response=cart.remove_from_cart(client_id,product_id,quantity)
                    client_socket.send(response.encode())

                elif command == "view_cart":
                    response=cart.view_cart_from_db(client_id)
                    client_socket.send(response.encode())

                elif command == "checkout":
                    response=cart.checkout_payment(client_id)
                    client_socket.send(response.encode())
    
                elif command == "payment_transaction":
                    payment_method, name, card_number, expiry_date, cvc = args
                    response=transaction.payment(payment_method, client_id, name, card_number, expiry_date, cvc)

                    if "Transaction Complete" in response: 
                        transaction.save_transaction_in_db(client_id)
                        cursor.execute("DELETE FROM Cart WHERE clientID = ?", (client_id,))  
                        conn.commit()
                        client_socket.send("\nPayment successful. Transaction Complete.".encode())

                    else:
                        client_socket.send(response.encode())
                                                    
                elif command=="view_transactions":
                    response=transaction.view_transaction_from_db(client_id)
                    client_socket.send(response.encode())

                else:
                    client_socket.send("Invalid input".encode())

        except Exception as e:
            client_socket.send(f"Error: {str(e)}".encode())
        finally:
            print(f"Closing connection for {client_id}")
            conn.close()
            client_socket.close()

    # Method to create unique client ID which is not preexisitng in .db 
    def client_id_check(self,addr):
        conn = sqlite3.connect("smart_vending_machine.db")
        cursor = conn.cursor()
        cursor.execute("SELECT clientID FROM ClientID")
        existing_client = cursor.fetchall()
        if not existing_client:
            self.client_counter=1
        else:
            client_list=[]
            for i in existing_client:
                exisiting_id = int(i[0].split('_')[1])
                client_list.append(exisiting_id)
            self.client_counter = max(client_list) + 1

        final_id = f"Client_{self.client_counter}"
        addr_str=addr[0]
        cursor.execute("INSERT INTO ClientID (clientID, connectionAdd) VALUES (?, ?)", (final_id,addr_str))
        conn.commit()
        return final_id
    
    # Method handling accepting client connections
    def start_server(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            client_id = self.client_id_check(addr)
            print(f"Connection from {addr} | Client ID: {client_id}")
            
            # Implementing threading to make it multi client; for each a new thread is created to handle communication 
            # between client - server concurrently
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,client_id))
            client_handler.start()

# Function to initialise and create database using sql file if doesn't already exist
'''def initialise_database():
    conn=sqlite3.connect("smart_vending_machine.db")
    cursor=conn.cursor()
    with open("smart_vending_machine.sql",'r') as sql_file:
        sql_script=sql_file.read()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()'''

# Main function to initialize and start the server
def main():
    server=Server()
    server.start_server()

# The entry point of the program where execution of program begins
if __name__=="__main__":
    main() 
