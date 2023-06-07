from dotenv import load_dotenv
load_dotenv()
import os
import mysql.connector

connection = mysql.connector.connect(
  host= os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  passwd= os.getenv("DB_PASSWORD"),
  db= os.getenv("DB_DATABASE"),
  ssl_verify_identity=True,
  ssl_ca='C:\ssl\certs\cacert.pem'
)

cursor = connection.cursor(dictionary=True)
'''
cursor.execute("""
    CREATE TABLE guest (
        id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
        guest_name VARCHAR(100),
        email VARCHAR(100)
    );
""")
'''

#cursor.execute("INSERT INTO guest (guest_name, email) VALUES ('Anthony', 'anthony@gmail.com');")

#guest_name = "Britney"
#email = "britney@yahoo.com"

#cursor.execute("INSERT INTO guest (guest_name, email) VALUES (%s, %s);", (guest_name, email))

#cursor.execute("SELECT * FROM guest;")
#results = cursor.fetchall()
#print(results)

cursor.execute("SELECT * FROM guest WHERE id = 2;")
result = cursor.fetchone()
print(result)

connection.commit()

cursor.close()
connection.close()