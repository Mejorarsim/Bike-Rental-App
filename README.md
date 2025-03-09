# **Team_M_15_Project**

## **Table of Contents**
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [How to Run](#how-to-run)
5. [User Roles and Credentials](#user-roles-and-credentials)
6. [Usage Guide](#usage-guide)
    - [User Page](#user-page)
    - [Operator Page](#operator-page)
    - [Manager Page](#manager-page)
7. [Database Schema](#database-schema)
8. [Project Structure](#project-structure)
9. [Contributing](#contributing)
10. [License](#license)

---

## **Project Overview**
**Team_M_15_Project** is a Python-based bike rental management system that provides a map-based interface for managing bikes, users, operators, and administrators. It features a multi-role access system to facilitate smooth management of bike rentals, payments, and issue reporting.

---

## **Features**
- Map-based interface for bike management.
- Multi-role access control: User, Operator, and Manager.
- Secure login with encrypted passwords.
- Wallet system for users.
- Comprehensive report handling (broken bikes, payment issues, etc.).
- Admin dashboard for managing bikes, users, and reports.

---

## **Installation**
### **Requirements**
- Python 3.x
- Required Python libraries:
   ```bash
   pip install PIL
   ```

---

## **How to Run**
1. **Navigate to the project directory:**
   ```bash
   cd C:\Users\Simran\Desktop\Team_M_15_Project
   ```

2. **Install required libraries:**
   ```bash
   pip install PIL
   ```

3. **Run the main script:**
   ```bash
   python log.py
   ```

---

## **User Roles and Credentials**
### **1. Manager**
- **Username:** admin@qq.com  
- **Password:** 123456  

### **2. Operators**
- **Glasgow:**
   - **Username:** Glasgow@qq.com  
   - **Password:** 123456  
- **Edinburgh:**
   - **Username:** Edinburgh@qq.com  
   - **Password:** 123456  
- **Aberdeen:**
   - **Username:** Aberdeen@qq.com  
   - **Password:** 123456  
- **Dundee:**
   - **Username:** Dundee@qq.com  
   - **Password:** 123456  

### **3. Users**
- **Glasgow:**
   - **Username:** 123@qq.com  
   - **Password:** 123456  
- **Edinburgh:**
   - **Username:** Cb@qq.com  
   - **Password:** 123456  
- **Aberdeen:**
   - **Username:** V@qq.com  
   - **Password:** 123456  
- **Dundee:**
   - **Username:** D@qq.com  
   - **Password:** 123456  

---

## **Usage Guide**

### **User Page**
- **Rent a Bike:** Click on a point on the map to rent a bike.  
- **Return a Bike:** Click on the green point, enter the final X and Y positions.  
- **Add Money:** Click the "Add" button to top up your wallet.  
- **Submit Reports:** Click the "Reports" button to submit a new report.  
- **Order History:** View past orders and submit reports if needed.  

---

### **Operator Page**
- **Manage Bikes:** Move, fix, or charge bikes on the map.  
- **Handle Reports:** View, check, and resolve user reports.  
- **Detailed View:** Access detailed information about bikes and reports.  

---

### **Manager Page**
- **Fleet Management:**  
   - Add or delete bikes.  
   - Move bikes across cities.  
- **User and Operator Management:**  
   - View and manage users and operators.  
- **Visualizations:**  
   - Access analytics through the "Visualization" button.  

---

## **Database Schema**
### **1. Bike Table**
- **Fields:** ID, type, location (X, Y), status, battery, city.

### **2. User Table**
- **Fields:** ID, username, email, phone, wallet balance, encrypted password.

### **3. Order Table**
- **Fields:** Order ID, user ID, bike ID, start and end coordinates, cost, date.

### **4. Report Table**
- **Fields:** Report ID, user ID, bike ID, issue type (Broken, Payment, Other), status.

---

## **Project Structure**
```
Team_M_15_Project/
├── db/                     # Database handling files
│   ├── db_config.py        # Database configuration
│   ├── Bike.py             # Bike-related operations
│   ├── Order.py            # Order-related operations
│   ├── Report.py           # Report-related operations
│   ├── User.py             # User-related operations
├── managerPage.py          # Manager's GUI and functions
├── opertorPage.py          # Operator's GUI and functions
├── userPage.py             # User's GUI and functions
├── register.py             # User registration handling
├── log.py                  # Login handling
├── README.md               # Project documentation
```

---

## **Security**
- **Password Encryption:**  
   - Uses MD5 and random salt to encrypt passwords for secure authentication.

---

## **Contributing**
1. **Fork the repository.**  
2. **Create a new branch:**
   ```bash
   git checkout -b feature-name
   ```
3. **Commit changes:**
   ```bash
   git commit -m "Added new feature"
   ```
4. **Push to the branch:**
   ```bash
   git push origin feature-name
   ```
5. **Submit a pull request.**

---

## **License**
This project is licensed under the MIT License.
