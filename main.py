import sqlite3 as sql
import sys
from random import randint
import pyperclip
import getpass

symbols = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz!@#$%^&*_1234567890'

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

def insertMP(toCheck, __list__):

    if toCheck in __list__:
                
        out = input("Insert the MASTER PASSWORD:    ")

    else:

        out = getpass.getpass("Insert the MASTER PASSWORD:    ")


    return out

def copy_to_clipboard(obj):
    pyperclip.copy(str(obj))

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
            if 'allHash' in sys.argv:
                cur.execute("SELECT * FROM hashTable")
                rows = cur.fetchall()
                line = '\nNAME : [PASSWORD]\n\n'

                for row in rows:
                    line += f'{row[0]} : {[row[1]]}\n'
                copy_to_clipboard(line)

                print("{NAME: HASH} dict was COPIED TO THE CLIPBOARD")

                return 
            
            MasterPassword = insertMP('show', sys.argv)
            
            inp = input("Insert the place: ")
            cur.execute("SELECT * FROM hashTable WHERE NAME = ? LIMIT 1", (inp,))
            rows = cur.fetchall()
            if rows:
                _hash_ = rows[0][1]  # Adjust the index based on your schema
                password = hashToPassword(MasterPassword, _hash_)
                copy_to_clipboard(password)
                print('\n',"The PASSWORD was copied to the CLIPBOARD!", '\n')
            else:
                print("\nNo results found.\n")

        elif com == 'insert':

            MasterPassword = insertMP('show', sys.argv)

            inp1 = input("Insert the NAME:     ")
                
            if 'genPW' in sys.argv:

                inp2 = generatePassword(len(MasterPassword))

                print(f"Password generated successful!")


            else: 

                inp2 = input("Insert the PASSWORD: ")

            if inp2 == 'genPW':

                inp2 = generatePassword(len(MasterPassword))

                print(f"Password generated successful!")

            hashed_password = passwordToHash(MasterPassword, inp2)

            cur.execute("INSERT INTO hashTable (NAME, HASH) VALUES (?, ?)", (inp1, hashed_password))
            print("FINISHED!")

        elif com == 'list':
                cur.execute("SELECT * FROM hashTable")
                rows = cur.fetchall()
                print()
                for i in rows:
                    print(i[0])
                print()

        elif com == 'genPW':

                MasterPassword = input("Insert the MASTER PASSWORD:    ")

                copy_to_clipboard(generatePassword(len(MasterPassword)))

                print("The PASSWORD is GENERATED and copied to the CLIPBOARD!")

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

        elif com == 'init':

            cur.execute('''

            CREATE TABLE IF NOT EXISTS hashTable (
                NAME TEXT,
                HASH TEXT,
                PRIMARY KEY(NAME)
            )

            ''')

            print("\nThe database was created successfuly!\n")

        elif com == 'commitInfo':

            print()

        elif com == 'help':
            print("\nIf You wanna get the password, so enter 'pm get', if you wanna insert the password - enter 'pm insert', if you want to see list of all Password Names, so enter 'pm list'\n")



if __name__ == '__main__':
    main()

