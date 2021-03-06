/*
For Employee.JobType and Login.Privilege:
0 = Unspecified
1 = HR
2 = Sales
3 = Engineering
4 = Admin
*/

create table Customer (
CustomerID integer primary key autoincrement,
FirstName varchar(20),
LastName varchar(20)
);

create table Employee (
EmployeeID integer primary key,
FirstName varchar(20),
LastName varchar(20),
SSN integer,
Salary double,
IsSalaried boolean,
JobType integer
);

create table Login (
EmployeeID integer,
Privilege integer,
LoginTime datetime,
LogoutTime datetime,

foreign key (EmployeeID) references Employee
);

create table Inventory (
InventoryID integer primary key autoincrement,
ModelNumber integer,
Cost double,
LeadTime datetime,
Category integer,
Quantity integer
);

create table Model (
ModelNumber integer primary key,
InventoryID integer,
SalePrice double,

foreign key (InventoryID) references Inventory
);

create table CustomerOrder (
OrderNumber integer primary key autoincrement,
CustomerID integer,
EmployeeID integer,
ModelNumber integer,
SaleValue double,
Quantity integer,

foreign key (CustomerID) references Customer,
foreign key (EmployeeID) references Employee,
foreign key (ModelNumber) references Model
);

/* Views */

CREATE VIEW totalRevenue AS
SELECT ModelNumber, SUM(SaleValue)
FROM CustomerOrder
GROUP BY ModelNumber;

CREATE VIEW customerModel AS
SELECT FirstName, LastName, ModelNumber, Quantity
FROM CustomerOrder
NATURAL LEFT JOIN Customer;

CREATE VIEW partAvailability AS
SELECT OrderNumber, CustomerOrder.ModelNumber, Inventory.Quantity
FROM CustomerOrder
INNER JOIN Inventory ON CustomerOrder.ModelNumber = Inventory.ModelNumber;

CREATE VIEW expenseReport AS
SELECT FirstName, LastName, Salary, SUM(Cost * CustomerOrder.Quantity)
FROM Employee
NATURAL JOIN CustomerOrder JOIN Inventory ON CustomerOrder.ModelNumber
GROUP BY EmployeeID;