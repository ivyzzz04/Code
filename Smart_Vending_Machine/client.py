import socket
from gui import *

# Class to handle vending machine tasks i.e., involves communication with server
class ClientFunctions:
    def __init__(self,client_socket):
        self.client_socket = client_socket

    # Method handling sending request to server and receiving response 
    def send_request(self,request):
        self.client_socket.send(request.encode())
        response = self.client_socket.recv(4096).decode()
        if not response:
            self.client_socket.close()
        return response

    # Method to retrieve avaliable products by request to server and return value is string of formatted display for GUI
    def view_products(self): 
        response = self.send_request("view_products")
        inventory=""
        inventory+=f"\n{"ID":<3}{"Product Name":<40}{"Price":<10}{"Stock":<10}\n"
        inventory+="_" * 80 + "\n"

        for line in response.split("\n"):
            if line.split():
                product_id, name, price, stock = line.split("|")
                inventory+=f"{product_id:<3}{name:<40}${float(price):<10.2f}{stock:<10}\n"
        return inventory

    # Method to send request to server to add a product to cart
    def add_to_cart(self,product_id,quantity): 
        response = self.send_request(f"add_to_cart|{product_id}|{quantity}")
        return response

    # Method to send request to server to remove a product from cart
    def remove_from_cart(self,product_id,quantity): 
        response = self.send_request(f"remove_from_cart|{product_id}|{quantity}")
        return response
    
    # Method to retrieve items in cart by request to server and return value is string of formatted display for GUI
    def view_cart(self): 
        response = self.send_request("view_cart")
        current_cart=""
        if response:
            if "Your cart is empty." in response:
                current_cart+=response
            else:
                current_cart+=f"\n{"ID":<3}{"Product Name":<40}{"Quantity":<10}{"Price":<10}{"Total":<10}\n"
                current_cart+="_" * 80 + "\n"
                for line in response.split("\n"):
                    if line.split():
                        cart_id, name, quantity, price, total = line.split("|")
                        current_cart+=f"{cart_id:<3}{name:<40}{quantity:<10}${float(price):<10.2f}${float(total):<10.2f}\n"

            return current_cart
    
    # Method to send request to server to process payment transaction and save to database table
    def payment_transaction(self, payment_method, name, card_number, expiry_date, cvc):
        response = self.send_request(f"payment_transaction|{payment_method}|{name}|{card_number}|{expiry_date}|{cvc}")
        return response
    
    # Method to retrieve final items in cart by request to server and return value is string of formatted display for GUI on checkout
    def checkout(self):
        response = self.send_request("checkout")
        checkout_info=""
        if response:
            if "Your cart is empty." in response:
                checkout_info+="Your cart is empty. No requirement for checkout."
            else:
                total_cost = 0
                checkout_info+="_" * 80 +"\n"
                for line in response.split("\n"):
                    if line.strip():
                        name, quantity, total = line.split("|")
                        checkout_info+=f"{name}|{quantity}|{float(total):.2f}\n"
                        total_cost += float(total)
                checkout_info+=f"\nTotal cost: ${total_cost:.2f}"

            return checkout_info

    # Method to retrieve previous transaction history by request to server and return value is string of formatted display for GUI
    def view_transactions(self):
        response = self.send_request("view_transactions")
        transaction_info=""
        if response:
            if "No previous transactions found." in response:
                transaction_info+="No previous transactions found."
            else:
                transaction_info+=f"{"Transaction Date":<25}{"Product Name":<40}{"Quantity":<15}{"Total Amount":<7}\n"
                transaction_info+="_" * 100 + "\n"
                for line in response.split("\n"):
                    if line.split():
                        transaction_date,product_name,quantity,total_amount = line.split("|")
                        transaction_info+=f"{transaction_date:<25}{product_name:<40}{quantity:<15}${float(total_amount):<7.2f}\n"

        return transaction_info
    
    # Method to close the client socket connection
    def close_connection(self):
        self.client_socket.close()

# Main function to set up the client and establish communication with server
def main():  
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    client = ClientFunctions(client_socket)

# The entry point of the program where execution of program begins  
if __name__ == "__main__":
    main()