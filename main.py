# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1

df_boston = pd.read_sql("""
SELECT firstName, lastName
FROM employees
JOIN offices
USING(officeCode)
WHERE city = 'Boston';
""",conn)
print(df_boston)

# STEP 2

df_zero_emp = pd.read_sql("""
SELECT officeCode, city, state, country
FROM offices
LEFT JOIN employees
USING(officeCode)
WHERE employeeNumber IS NULL;
""", conn)
print(df_zero_emp)


# STEP 3
# Replace None with your code
df_employee = pd.read_sql("""
SELECT firstName, lastName, city, state
FROM employees
JOIN offices
USING(officeCode)
ORDER BY firstName, lastName;
""", conn)
print(df_employee)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""
SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber
FROM customers
LEFT JOIN orders 
USING(customerNumber)
WHERE orderNumber IS NULL
ORDER BY contactLastName;
""", conn)
print(df_contacts)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql("""
SELECT contactFirstName, contactLastName, CAST(amount AS INTEGER) AS amount, paymentDate
FROM customers
JOIN payments
USING(customerNumber)
ORDER BY amount DESC;
""", conn)
print(df_payment)
# STEP 6
# Replace None with your code
cols = pd.read_sql("""
PRAGMA table_info(customers);
""", conn)
print(cols)



df_credit = pd.read_sql("""
SELECT employeeNumber, firstName, lastName, COUNT(customerNumber) AS customer_count
FROM employees
JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY employeeNumber, firstName, lastName
HAVING AVG (creditLimit) > 90000
ORDER BY customer_count DESC;
""", conn)
print(df_credit)
# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql("""
SELECT productName, COUNT(orderNumber) AS numOrders, SUM(quantityOrdered) AS totalunits
FROM products
JOIN orderdetails
USING(productCode)
GROUP BY productCOde, productName
ORDER BY totalunits DESC;
""", conn)
print(df_product_sold)
# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql("""
SELECT productName, productCode, COUNT(DISTINCT customerNumber) AS numpurchasers
from products
JOIN orderDetails
USING(productCode)
JOIN orders
USING(orderNumber)
GROUP BY productCode, productName
ORDER BY numpurchasers DESC;
""", conn)
print(df_total_customers)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql("""
SELECT COUNT(customerNumber) AS n_customers, officeCode, offices.city 
FROM offices
JOIN employees
using(officeCode)
JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY officeCode, offices.city;
""", conn)
print(df_customers)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql("""
SELECT DISTINCT
       employees.employeeNumber,
       employees.firstName,
       employees.lastName,
       offices.city,
       offices.officeCode
FROM employees
JOIN offices
USING (officeCode)
JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
JOIN orders
USING (customerNumber)
JOIN orderDetails
USING (orderNumber)
WHERE productCode IN (
    SELECT productCode
    FROM orderDetails
    JOIN orders
    USING (orderNumber)
    GROUP BY productCode
    HAVING COUNT(DISTINCT customerNumber) < 20
)
ORDER BY employees.lastName;
""", conn)

print(df_under_20)
conn.close()