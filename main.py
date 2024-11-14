# To run this file, you should enter python3 into the terminal, but I've added this command to .zshrc and named it 'pm'.
import sqlite3 as sql
import sys
from random import randint

symbols = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz!@#$%^&*_'

def generatePassword(lenght):

    out = str()

    for i in range(lenght):

        out += symbols[randint(0, lenght - 1)]

    return out

def hashToPassword(inputCode, hashPassword):

    password = ''

    for i, b in zip(inputCode, hashPassword):
        
        password += chr(ord(b) - ord(i))

    return password

def passwordToHash(inputCode, password):

    hashP = ''

    for i,b in zip(inputCode, password):

        hashP += chr(ord(i) + ord(b))        

    return hashP

def main(): 
    with sql.connect("hash.db") as conn:
        cur = conn.cursor()

        lnarg = 1

        if len(sys.argv) <= 1:
            print("\nIf You wanna get the password, so enter 'pm get', if you wanna insert the password - enter 'pm insert', if you want to see list of all Password Names, so enter 'pm list'\n")
            return
        elif len(sys.argv) > 2:
            lnarg = len(sys.argv)

        com = sys.argv[1]

        
        if com == 'get':
            if lnarg > 1:
                if sys.argv[2] == 'allHash':
                    cur.execute("SELECT * FROM hashTable")
                    rows = cur.fetchall()
                    print()
                    for row in rows:
                        print(f"'{row[0]}':    ", [row[1]])
                    print()
            else: 
                MasterPassword = input("Insert the MASTER PASSWORD:    ")
                inp = input("Insert the place: ")
                cur.execute("SELECT * FROM hashTable WHERE NAME = ? LIMIT 1", (inp,))
                rows = cur.fetchall()
                if rows:
                    _hash_ = rows[0][1]  # Adjust the index based on your schema
                    password = hashToPassword(MasterPassword, _hash_)
                    print('\n',f"'{password}'", '\n')
                else:
                    print("\nNo results found.\n")

        elif com == 'insert':
                MasterPassword = input("Insert the MASTER PASSWORD:    ")

                inp1 = input("Insert the NAME:     ")
                
                if lnarg > 1:
                    if sys.argv[2] == 'genPW':

                        inp2 = generatePassword(len(MasterPassword))

                        print(f"Password generated successful! Generated PASSWORD:   '{inp2}'")


                else: 

                    inp2 = input("Insert the PASSWORD: ")

                if inp2 == 'genPW':

                    inp2 = generatePassword(len(MasterPassword))

                    print(f"Password generated successful! Generated PASSWORD:   '{inp2}'")

                hashed_password = passwordToHash(MasterPassword, inp2)

                cur.execute("INSERT INTO hashTable (NAME, HASH) VALUES (?, ?)", (inp1, hashed_password))
                print("FINISHED!")

        elif com == 'list':
                cur.execute("SELECT * FROM hashTable")
                rows = cur.fetchall()
                print()
                for i in rows:
                    print(i[0])  # Assuming you want to print just the NAME
                print()

        elif com == 'genPW':

                MasterPassword = input("Insert the MASTER PASSWORD:    ")

                print(generatePassword(len(MasterPassword)))

        elif com == 'DONTDOTHISIFYOUARENTSURE':

            cur.execute("DROP TABLE IF EXISTS hashTable")
            
            cur.execute('''

            CREATE TABLE IF NOT EXISTS hashTable (
                NAME TEXT,
                HASH TEXT,
                PRIMARY KEY(NAME)
            )

            ''')

            print("\nTHE DATABASE WAS CLEARED\n")

        elif com == 'help':
            print("\nIf You wanna get the password, so enter 'pm get', if you wanna insert the password - enter 'pm insert', if you want to see list of all Password Names, so enter 'pm list'\n")



if __name__ == '__main__':
    main()
