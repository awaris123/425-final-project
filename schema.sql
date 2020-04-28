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
EmployeeID integer primary key autoincrement,
FirstName varchar(20),
LastName varchar(20),
SSN int,
Salary double,
IsSalaried boolean,
JobType int
);

create table Login (
EmployeeID int,
Privilege int,
LoginTime datetime,
LogoutTime datetime,

foreign key (EmployeeID) references Employee
);

create table Inventory (
InventoryID integer primary key autoincrement,
ModelNumber int,
Cost double,
LeadTime datetime,
Category smallint,
Number int
);

create table Model (
ModelNumber int primary key,
InventoryID int,
SalePrice double,

foreign key (InventoryID) references Inventory
);

create table CustomerOrder (
OrderNumber integer primary key autoincrement,
CustomerID int,
EmployeeID int,
ModelNumber int,
SaleValue double,

foreign key (CustomerID) references Customer,
foreign key (EmployeeID) references Employee,
foreign key (ModelNumber) references Model
);