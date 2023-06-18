import mysql.connector
from mysql.connector import Error

while True:
    qa = input("Do you want to add hand text? (Y/y)(N/n): ")

    if(qa == "Y" or qa == "y"):
        hand_text = input("Enter hand text: ")

        try:
            conn = mysql.connector.connect(host='db4free.net', database='test_resto_sys2', user='resto_sys2',
                                           password='resto12345')
            query = "INSERT INTO hand_gesture(hand_text) VALUES('" + hand_text + "')"
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            cur.close()
            print("Insert Successfully")

        except Error as error:
            print("Failed to insert {}".format(error))
    else:
        break
