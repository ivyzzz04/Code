CREATE TABLE ClientID (
	clientID TEXT NOT NULL,
	connectionAdd TEXT NOT NULL
);

CREATE TABLE Products (
	productID INTEGER PRIMARY KEY AUTOINCREMENT,
	productName TEXT NOT NULL,
	price REAL NOT NULL,
	stock INTEGER NOT NULL
);

CREATE TABLE Cart (
	cartID INTEGER PRIMARY KEY AUTOINCREMENT,
	clientID TEXT NOT NULL,
	productID INTEGER NOT NULL,
	quantity INTEGER NOT NULL,
    FOREIGN KEY (productID) REFERENCES Products(productID)
);

CREATE TABLE Transactions (
	transactionID INTEGER PRIMARY KEY AUTOINCREMENT,
	transactionClient TEXT NOT NULL,
    transactionDate TEXT NOT NULL,
    productName TEXT NOT NULL,
	quantity INTEGER NOT NULL,
    totalAmount REAL NOT NULL
);

CREATE TABLE PaymentMethod (
	paymentID INTEGER PRIMARY KEY AUTOINCREMENT,
	paymentClient TEXT NOT NULL,
    paymentDate TEXT NOT NULL,
	paymentType TEXT NOT NULL,
    nameCard TEXT NOT NULL,
	cardNumber TEXT NOT NULL,
    cardDate TEXT NOT NULL,
	cardCvc TEXT NOT NULL
);

INSERT INTO Products (productName,price,stock) VALUES
('Cybersecurity_101_eBook',14.99,30),
('Programming_101_eBook',17.99,30),
('Scripting_101_eBook',17.99,30),
('Graphics_Editor_License',10.00,35),
('Video_Editor_License',10.00,35),
('Visual_Effects_Editing',11.00,30),
('Python_Beginners_MP4',20.00,10),
('Research_Ethics_MP4',20.00,6),
('Module_Playlist',20.00,5);