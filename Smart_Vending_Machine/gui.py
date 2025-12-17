import socket
from tkinter import *
import tkinter as tk
from tkinter import messagebox  
from client import ClientFunctions 
import matplotlib.pyplot as plt

# Establish connection to server and receive response from client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5000))  
client = ClientFunctions(client_socket)

# Function handling greeting window
def greeting():
    greeting_window = tk.Tk()
    greeting_window.title('Welcome!')
    greeting_window.geometry('550x435+350+140')
    greeting_window.config(bg="#bedbba")
    
    # Adding logo to greeting window
    photo=tk.PhotoImage(file="images/logo.png")
    photo_resized=photo.subsample(2,2)
    photo_label=tk.Label(greeting_window,image=photo_resized, bg="#bedbba")
    photo_label.grid(row=0,column=0,columnspan=2,pady=5)

    name_label=tk.Label(greeting_window,text="Enter in your name ", font=("Helvetica", 11), bg="#bedbba")
    name_label.grid(row=1,column=0,padx=10,pady=2)

    username_var=tk.StringVar()

    # Entry field to get name of user 
    username_entry=tk.Entry(greeting_window,textvariable=username_var)
    username_entry.grid(row=1,column=1,padx=10,pady=5)

    # Button - clicking it will call function for confirmation of username
    button = tk.Button(greeting_window, text="Click", font=("Helvetica", 10, "bold"), bg="#babedb", width=25, command=lambda: username_confirmation(username_var,greeting_window))
    button.grid(row=2, column=0, columnspan=2, pady=10)

    greeting_window.mainloop()

# Function to display messagebox if username entry is empty, else it will display instructions on how to use the vending machine
def username_confirmation(username_var,greeting_window):
    user_name = username_var.get()
    if not user_name:
        messagebox.showerror("Error", "Please enter your name.")
        return
    instructions(user_name,greeting_window)

# Function handling instructions display
def instructions(user_name,greeting_window):
    text=f"""
Verbena - Smart Vending Machine welcomes you, {user_name}. Here are the instructions 
for shopping:
    1. Browse through the various selection of products Verbena provides.
    2. Simply click on the 'Add to Cart' button to purchase items you'd like.
    3. View your cart anytime by clicking the 'View Cart' button.
    4. Wish to remove an item from cart? Simply enter in product ID and quantity to 
    remove.
    5. Proceed to checkout to view your subtotal and process your payment.
    6. Enjoy shopping :]"""

    instructions_label=tk.Label(greeting_window,text=text,justify='left', font=("Helvetica", 10), bg="#bedbba")
    instructions_label.grid(row=3,column=0,columnspan=2,padx=10,pady=5)

    # Button - on clicking main window is displayed
    button = tk.Button(greeting_window, text="Start Shopping", width=25, font=("Helvetica", 10, "bold"), bg="#babedb", command=lambda: main_frame(greeting_window))
    button.grid(row=5, column=0, columnspan=2, pady=10)

# Function handling main window display
def main_frame(greeting_window):
    greeting_window.destroy()
    main_window = tk.Tk()
    main_window.title('Verbena - Smart Vending Machine')
    main_window.geometry('800x610+10+10')

    main_window.config(bg="#d7badb")

    # ------------------------ Left frame -----------------------------
    left_frame = tk.LabelFrame(master=main_window, relief = FLAT, borderwidth = 3, bg='#c7badb', width=500)
    left_frame.grid(row=0, column=0, padx=5, pady=5)
    
    frame1_1 = tk.LabelFrame(master=left_frame, relief = FLAT, borderwidth = 3, bg='#c7badb')
    frame1_1.grid(row=0, column=0, padx=5, pady=5)
    l1 = tk.Label(master=frame1_1, text=f"Welcome to Verbena - Smart Vending Machine!", font=("Helvetica", 13, "bold"), bg="#d7badb")
    l1.grid(row=0, column=0)

    frame1_2 = tk.LabelFrame(master=left_frame, relief = FLAT, borderwidth = 3, bg='#c7badb')
    frame1_2.grid(row=1, column=0, padx=5, pady=5)

    # ------------------------ Right frame --------------------------------------
    right_frame = tk.LabelFrame(master=main_window, relief = RAISED, borderwidth = 3,bg='#c7badb',width=100)
    right_frame.grid(row=0, column=1, padx=5, pady=5,sticky='n')

    frame2_1 = tk.LabelFrame(master=right_frame, relief = FLAT, borderwidth = 3, bg='#c7badb')
    frame2_1.grid(row=0,column=0,padx=5, pady=5,sticky='nsew')

    # ------------------------ Scroll bar --------------------------------------
    scroll_bar = tk.Scrollbar(main_window)
    scroll_bar.grid(row=0, column=3, sticky='ns')

    # ------------------------ Display all Products  ----------------------------------
    frame_item = tk.LabelFrame(master=left_frame, text='Products', relief = RAISED, borderwidth = 3, bg='#c7badb')
    frame_item.grid(row=2, column=0, padx=5, pady=5)

    width_grid=135                                      # Width set for each grid to display product 
    height_grid=115                                     # Height set for each grid to display product 
    number=1

    # Creating a 3x3 grid using for loop, displaying image and 'add to cart' button with product ID for each
    for i in range(3):
        for j in range(3):
            frame_add_to_cart = tk.Frame(master=frame_item, relief=tk.RAISED, borderwidth=3, width=width_grid, height=height_grid)
            frame_add_to_cart.grid(row=i, column=j, padx=5, pady=5)
            photo=tk.PhotoImage(file=f"images/{number}.png")
            photo_resized=photo.subsample(4,4)
            label = tk.Label(master=frame_add_to_cart, image=photo_resized, bg="#f1eef6", width=width_grid, height=height_grid)
            label.grid(row=0, column=0)

            # Image reference to prevent garabage collection
            label.image = photo_resized
            
            btn_add_to_cart = tk.Button(frame_add_to_cart, text=f"Add to Cart - {number}", font=("Helvetica", 10, "bold"), bg="#cfc9a2",  relief="ridge", command=lambda num=number: add_to_cart(num))
            btn_add_to_cart.grid(row=1, column=0, pady=5)
            
            number += 1

    # Buttons on right frame for viewing details of available products, viewing cart, previous transactions, to checkout and exit out of the program
    button1 = tk.Button(frame2_1, text="View Products", width=25, font=("Helvetica", 10, "bold"), bg="#dbd7ba", command=lambda: view_products(main_window))
    button1.grid(row=0, padx=20, pady=10)

    button2 = tk.Button(frame2_1, text="View Cart", width=25, font=("Helvetica", 10, "bold"), bg="#dbd7ba", command=lambda: view_cart(main_window))
    button2.grid(row=1, padx=20, pady=10)

    button3 = tk.Button(frame2_1, text="Display Previous Transactions", width=25, font=("Helvetica", 10, "bold"), bg="#dbd7ba", command=lambda: view_transaction(main_window))
    button3.grid(row=2, padx=20, pady=10)

    button4 = tk.Button(frame2_1, text="Checkout", width=25, font=("Helvetica", 10, "bold"), bg="#dbd7ba", command=lambda: checkout())
    button4.grid(row=3, padx=20, pady=10)

    button5 = tk.Button(frame2_1, text="Exit", width=25, font=("Helvetica", 10, "bold"), bg="#dbd7ba", command=lambda: exit(main_window))
    button5.grid(row=5, padx=20, pady=40)

    # Adding a poster to bottom of right frame
    photo_ad=tk.PhotoImage(file="images/ad.png")
    photo_ad_resized=photo_ad.subsample(4,4)
    l1=tk.Label(frame2_1, image = photo_ad_resized)
    l1.grid(row=6, column=0, columnspan=2, pady=5, padx=10)

    main_window.mainloop()

# Function handling adding items to cart
def add_to_cart(num):
    product_id=num
    quantity=1
    response = client.add_to_cart(product_id, int(quantity))                        # Calling client method to receive response from server

    # Depending on response, messagebox is displayed
    if "Insufficient" in response or "Invalid" in response:
        messagebox.showerror(f"Error", response)
    else:
        messagebox.showinfo(f"Successfully added {quantity} item to cart", response)

# Function handling viewing details of available products in inventory on window
def view_products(main_window):
    response = client.view_products()                                               # Calling client method to receive response from server
    product_window=tk.Toplevel(master=main_window)
    product_window.title("Avaliable Products")
    product_window.geometry("680x340+595+10")

    product_window.config(bg="#dbbad7")

    top_frame = tk.LabelFrame(master=product_window, relief = FLAT, borderwidth = 3, bg='#dbbad7',width=500)
    top_frame.grid(row=0, column=0, padx=5, pady=5)

    product=tk.Text(top_frame,width=80,height=12, bg="#cea0c8")
    product.grid(padx=10,pady=10)                                  
    product.delete(1.0, tk.END)                                     # Deleting an existing content in text widget
    product.insert(tk.END,response)                                 # Inserting received response 
    product.config(state=tk.DISABLED)                               # Disabling editing of text widget

    # Button - clicking it will close view products window
    close_button = tk.Button(product_window, text="Close", font=("Helvetica", 10, "bold"), bg= "#bad7db", command=product_window.destroy)
    close_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    # Button - clicking it will display graphical representation of the available products
    graph_button = tk.Button(product_window, text="Graphical Analysis", font=("Helvetica", 10, "bold"), bg= "#bad7db", width=25, command=lambda: show_graph_stock())
    graph_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

# Function creating bar graph for representing stock distribution of the available products 
def show_graph_stock():
    product_name=[]
    product_quantity=[]
    # Retrieving data for plotting
    response=client.view_products()
    for line in response.split("\n"):
        if line.startswith("ID Product Name") or line.startswith("____________"):
            continue
        if line.strip():
            fields = line.split()
            product_id, name, price, stock = fields
            product_name.append(name)
            product_quantity.append(int(stock))

    plt.figure(figsize=(8, 4),facecolor="#f0e4e5")
    plt.barh(product_name, product_quantity, color="#cea0c8")
    plt.title('Stock Distribution of Available Products')
    plt.xlabel('Product Names')
    plt.ylabel('Stock Available')
    plt.tight_layout()
    plt.show()

# Function handling display of previous transaction history on window
def view_transaction(main_window):
    response = client.view_transactions()                                           # Calling client method to receive response from server
    button_window=tk.Toplevel(master=main_window)
    button_window.title("Your Transaction History")
    button_window.geometry("800x360+440+10")
    button_window.config(bg="#dbbad7")
    
    transaction=tk.Text(button_window,width=107,height=13, bg="#cea0c8")
    transaction.grid(padx=10,pady=10)
    transaction.delete(1.0, tk.END)                                     # Deleting an existing content in text widget
    transaction.insert(tk.END,response)                                 # Inserting received response
    transaction.config(state=tk.DISABLED)                               # Disabling editing of text widget

    # Button - clicking will close view transaction window
    close_button = tk.Button(button_window, text="Close", font=("Helvetica", 10, "bold"), bg= "#bad7db", width=25, command=button_window.destroy)
    close_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    # Button - clicking it will display graphical representation of purchasing trends
    graph_button = tk.Button(button_window, text="Graphical Analysis", font=("Helvetica", 10, "bold"), bg= "#bad7db", width=25, command=lambda: show_graph_trends(graph_button))
    graph_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

# Function creating line graph for representing purchasing trends per checkout; *displays only when atleast one transaction has been made by user*
def show_graph_trends(graph_button):
    trend_list = [0] 
    purchase_list = [0]  
    quantity_dict = {}
    # Retrieving data for plotting
    response = client.view_transactions()
    if not response.startswith("No previous"):
        for line in response.split("\n"):
            if line.startswith("Transaction Date") or line.startswith("____________"):
                continue
            if line.strip():
                fields = line.split()  
                transaction_date = fields[0] 
                quantity = fields[-2]
                quantity = int(quantity)
                key = transaction_date  
                if key not in quantity_dict:
                    quantity_dict[key] = quantity
                else:
                    quantity_dict[key] += quantity
                trend_list.append(quantity_dict[key])
                purchase_list.append(len(purchase_list))

        plt.figure(figsize=(6, 4), facecolor="#f0e4e5")
        plt.plot(purchase_list, trend_list, marker='o', color="#cea0c8", linestyle='-', linewidth=2)
        plt.xlim(0, len(purchase_list))  
        plt.ylim(0, max(trend_list) + 1)  
        plt.title('Purchasing Trends Per Transaction')
        plt.xlabel('Purchase Instance')
        plt.ylabel('Number of Items Purchased')
        plt.tight_layout()
        plt.show()

    else:
        graph_button.config(state="disabled")

# Function to display contents of current cart on window
def view_cart(main_window): 
    response = client.view_cart()                                                   # Calling client method to receive response from server
    cart_window=tk.Toplevel(master=main_window)
    cart_window.title("Your Cart Details")
    cart_window.geometry("680x470+595+10")
    cart_window.config(bg="#dbbad7")

    top_frame = tk.LabelFrame(master=cart_window, relief = FLAT, borderwidth = 3, bg='#dbbad7', width=500)
    top_frame.grid(row=0, column=0, padx=5, pady=5)

    cart=tk.Text(top_frame,width=80,height=13, bg="#cea0c8")
    cart.grid(padx=10,pady=10)
    cart.delete(1.0, tk.END)                                              # Deleting an existing content in text widget
    cart.insert(tk.END,response)                                          # Inserting received response
    cart.config(state=tk.DISABLED)                                        # Disabling editing of text widget

    # Button - clicking will close view cart window
    close_button = tk.Button(cart_window, text="Close", font=("Helvetica", 9, "bold"), bg= "#bad7db", command=cart_window.destroy)
    close_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    # Removing items from cart - to display in view cart window
    remove_from_cart(cart_window)

# Function to confirm exiting out of program  
def exit(main_window): 
    answer=messagebox.askyesno("Exit?","Would you like to exit out of Smart Vending Machine??")
    if answer:
        client.close_connection()                                                   
        main_window.destroy()

# Function to display entry for removing item from cart       
def remove_from_cart(cart_window): 
    bottom_frame = tk.LabelFrame(master=cart_window, relief = RAISED, borderwidth = 3,bg='#dbbac7',width=300)
    bottom_frame.grid(row=2, column=0, padx=5, pady=5,sticky="ew")

    l1=tk.Label(bottom_frame,text="Remove Product from Cart")
    l1.grid(column=0, row=0, padx=10, pady=20)

    product_var=tk.StringVar()
    quantity_var=tk.StringVar()

    # Entry field to get product ID to remove
    l2=tk.Label(bottom_frame,text="Enter product ID of the product you'd like to remove ")
    l2.grid(row=1, column=0, padx=10, pady=5)
    entry_product_id=tk.Entry(bottom_frame,textvariable=product_var, bg='#dbbac7')
    entry_product_id.grid(row=1, column=1, padx=10, pady=5)

    # Entry field to get quantity to remove
    l3=tk.Label(bottom_frame,text="Enter quantity to remove from your cart ")
    l3.grid(row=2, column=0, padx=10, pady=5)
    entry_quantity=tk.Entry(bottom_frame,textvariable=quantity_var, bg='#dbbac7')
    entry_quantity.grid(row=2, column=1, padx=10, pady=5)

    # Button - clicking it will call function to display messagebox based on response from client
    remove_button = tk.Button(bottom_frame, text="Remove Item", width=40, font=("Helvetica", 10, "bold"), bg="#badbce", command=lambda: remove_product(product_var,quantity_var,cart_window))
    remove_button.grid(row=3, column=1, padx=10, pady=5)

# Function to handle messagebox display based on client received response
def remove_product(product_var,quantity_var,cart_window):
    product_id = product_var.get()
    quantity = quantity_var.get()

    if not quantity.isdigit() or not product_id or not quantity:
        messagebox.showerror("Error", "Please provide all fields with valid inputs.")
        return
    response = client.remove_from_cart(product_id, int(quantity))                             # Calling client method to receive response from server

    if "Insufficient" in response or "Invalid" in response:
        messagebox.showerror(f"Error", response)
    else:
        messagebox.showinfo(f"Successfully removed {quantity} from cart",response)
        cart_window.destroy()

# Function handling checkout process display on window
def checkout(): 
    checkout_window = tk.Toplevel()
    checkout_window.title('Checkout')
    checkout_window.geometry('360x550+850+10')
    checkout_window.config(bg="#dbbad7")

    response = client.checkout()                                                            # Calling client method to receive response from server

    checkout_frame = tk.LabelFrame(master=checkout_window, relief=tk.RAISED, borderwidth=3, bg='#dbbad7')
    checkout_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    statement = """Your cart is empty. Add items to cart first before proceeding to checkout."""

    # Depending on response, text is displayed in window
    if "Your cart is empty. No requirement for checkout." in response:
        frame1 = tk.LabelFrame(master=checkout_frame, text="\t\tCheckout", font=("Helvetica", 11, "bold"), relief=tk.FLAT, borderwidth=3, bg='#dbbad7')
        frame1.grid(row=0, padx=10, pady=5, sticky='nsew')

        l1 = tk.Label(master=frame1, text=statement,font=("Helvetica", 11), bg='#dbbad7', fg="black", wraplength=300, width=35, anchor="w")
        l1.grid(row=0, padx=10, pady=5, sticky="w")

        # Button - clicking it will close checkout window
        close_button= tk.Button(frame1, text="Close", font=("Helvetica", 10, "bold"), bg= "#bad7db", width=25,  command=lambda: checkout_window.destroy())
        close_button.grid(row=1, column=0, padx=20, pady=10, sticky="w")

    else:
        frame1 = tk.LabelFrame(master=checkout_frame, text="\t\tCheckout", font=("Helvetica", 11, "bold"), relief=tk.FLAT, borderwidth=3, bg='#dbbad7')
        frame1.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        l1 = tk.Label(master=frame1, text="Current Order", font=("Helvetica", 9, "bold"), width=20, height=2)
        l1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        frame1_1 = tk.LabelFrame(master=checkout_frame, relief=tk.FLAT, borderwidth=3, bg='#dbbad7')
        frame1_1.grid(row=1, padx=5, pady=5, sticky="nsew", columnspan=2)

        l2 = tk.Label(master=frame1_1, text="Discount code:", font=("Helvetica", 9, "bold"), bg='#dbbad7')
        l2.grid(row=1, column=0, padx=10, pady=5)
        l3 = tk.Label(master=frame1_1, text="CODE321238921", font=("Helvetica", 9, "bold"), bg='#dbbad7')
        l3.grid(row=1, column=1, padx=10, pady=5)

        frame1_2 = tk.LabelFrame(master=checkout_frame, text="Items in your Cart", font=("Helvetica", 10, "bold"), relief=tk.FLAT, borderwidth=3, bg='#cea0c8')
        frame1_2.grid(row=2, column=0, padx=10, pady=5, sticky="w", columnspan=2)

        # Displaying items in cart along with subtotal
        l_header = tk.Label(master=frame1_2, text=f"\n{"Product Name":<50}{"Quantity":<10}{"Total Price"}", font=("Helvetica", 9, "bold"),  anchor="w")
        l_header.grid(row=0, column=0, padx=1, pady=5, sticky="w")

        row = 1
        subtotal = 0
        for line in response.split("\n"):
            if "|" in line:    
                if line.strip():
                    name, quantity, total = line.split("|")
                    l = tk.Label(master=frame1_2, text=f"{name:<50}{quantity:<10}{total}", font=("Helvetica", 9, "bold"),  anchor="w")
                    l.grid(row=row, column=0, padx=1, pady=5, sticky="nsew")
                    row += 1
            elif "Total" in line:
                subtotal_line = line.split(":")[-1].strip()
                subtotal_line = subtotal_line.replace("$", "")
                subtotal += float(subtotal_line)

        frame1_3 = tk.LabelFrame(master=checkout_frame, relief=tk.FLAT, borderwidth=3, bg='#cea0c8')
        frame1_3.grid(row=3, padx=5, pady=5, sticky="nsew")

        order = f'''
        Subtotal:                       ${subtotal}
        Discount sales:                  $5.00
        Total sale tax:                  $2.25
        --------------------------------------------
        TOTAL:                          ${((subtotal-5)+2.25):.2f}'''

        l = tk.Label(master=frame1_3, text=order, font=("Helvetica", 9, "bold"), justify=tk.LEFT, anchor="w")
        l.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        frame1_4 = tk.LabelFrame(master=checkout_frame, text="Proceed to payment", font=("Helvetica", 9, "bold"), relief=tk.FLAT, borderwidth=3, bg='#cea0c8')
        frame1_4.grid(row=4, padx=5, pady=5, sticky="ew")

        frame1_5 = tk.LabelFrame(master=checkout_frame, relief=tk.FLAT, borderwidth=3, bg='#cea0c8')
        frame1_5.grid(row=5, padx=5, pady=5, sticky="nsew")

        # Button - clicking it will display payment window
        button_pay= tk.Button(frame1_5, text="Click to pay", font=("Helvetica", 10, "bold"), bg= "#bad7db", width=25, command=lambda: payment(checkout_window))
        button_pay.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        # Button - clicking it will close checkout window
        close_button= tk.Button(frame1_5, text="Close", font=("Helvetica", 10, "bold"), bg= "#bad7db", width=25,  command=lambda: checkout_window.destroy())
        close_button.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
    checkout_window.mainloop()

# Function that displays entries to fill for payment transaction on payment window
def payment(checkout_window): 
    payment_window = tk.Toplevel(master=checkout_window)
    payment_window.title("Payment")
    payment_window.geometry("410x300+850+80")
    payment_window.config(bg="#dbbad7")

    payment_var=tk.StringVar()
    name_var=tk.StringVar()
    number_var=tk.StringVar()
    date_var=tk.StringVar()
    cvc_var=tk.StringVar()

    # Radiobuttons - choose whether to pay by credit or debit
    RBttn1=Radiobutton(payment_window,text="Credit", font=("Helvetica", 10, "bold"), bg="#dbbad7", variable=payment_var,value="credit_card")
    RBttn1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    RBttn2=Radiobutton(payment_window,text="Debit", font=("Helvetica", 10, "bold"), bg="#dbbad7", variable=payment_var,value="debit_card")
    RBttn2.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Setting credit as default
    payment_var.set("credit_card")

    # Entry to receive card information from user
    l1=tk.Label(payment_window,text="Name of card holder ", bg="#dbbad7", font=("Helvetica", 9, "bold"))
    l1.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    name_entry=tk.Entry(payment_window,textvariable=name_var)
    name_entry.grid(row=1, column=1, padx=10, pady=5)

    l2=tk.Label(payment_window,text="Card Number (no spaces)", bg="#dbbad7",font=("Helvetica", 9, "bold"))
    l2.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    number_entry=tk.Entry(payment_window,textvariable=number_var)
    number_entry.grid(row=2, column=1, padx=10, pady=5)

    l3=tk.Label(payment_window,text="Expiry Date ", bg="#dbbad7", font=("Helvetica", 9, "bold"))
    l3.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    date_entry=tk.Entry(payment_window,textvariable=date_var)
    date_entry.grid(row=3, column=1, padx=10, pady=5)

    l4=tk.Label(payment_window,text="CVC ", bg="#dbbad7", font=("Helvetica", 9, "bold"))
    l4.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    cvc_entry=tk.Entry(payment_window,textvariable=cvc_var)
    cvc_entry.grid(row=4, column=1, padx=10, pady=5)

    # Button - clicking it will call function that verifies given data
    pay_button = tk.Button(payment_window, text="Complete Transaction", font=("Helvetica", 10, "bold"), bg= "#bad7db", width=20, command=lambda: on_payment(payment_window,checkout_window,payment_var,name_var,number_var,date_var,cvc_var))
    pay_button.grid(row=5, column=0, padx=20, pady=10)
    # Button - clicking it will call show messagebox for confirmation to cancel
    cancel_checkout_button = tk.Button(payment_window, text="Cancel Checkout", width=20, font=("Helvetica", 10, "bold"), bg= "#bad7db", command=lambda: cancel_checkout(payment_window,checkout_window))
    cancel_checkout_button.grid(row=5, column=1, padx=20, pady=10)

    payment_window.mainloop()

# Function to verify details and display messageboxes accordingly as per client received response
def on_payment(payment_window,checkout_window,payment_var,name_var,number_var,date_var,cvc_var):
    payment_method=payment_var.get()
    name=name_var.get()
    card_number=number_var.get()
    expiry_date=date_var.get()
    cvc=cvc_var.get()

    if not name or not card_number or not expiry_date or not cvc:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    response = client.payment_transaction(payment_method,name,card_number,expiry_date,cvc)                  # Calling client method to receive response from server

    if "Payment Unsuccessful" in response:
        messagebox.showerror("Error", "Failed to accept payment. Please check card number and CVC.")
    else:
        messagebox.showinfo("Payment Status", "Payment Successful. Transaction Complete.")
        payment_window.destroy()
        checkout_window.destroy()

# Function to cancel checkout
def cancel_checkout(payment_window,checkout_window):
    answer=messagebox.askyesno("Cancel Checkout?", "Want to return back to main menu?")
    if answer:
        payment_window.destroy()
        checkout_window.destroy()

greeting()