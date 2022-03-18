# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import ttk
import sqlite3


def main():
   root = Tk()
   root.title("Blockchain interoperability")
   root.geometry("500x500")

   # Creating tabs
   tab_control = ttk.Notebook(root)
   tab1 = Frame(tab_control)
   tab_control.add(tab1, text="Add blockchain")

   tab2 = Frame(tab_control)
   tab_control.add(tab2, text="Create blockchain interoperability")
   tab_control.pack(expand=1, fill="both")

   # Database
   conn = sqlite3.connect('blockchain_book.db')
   cursor = conn.cursor()

   # Create table
   '''cursor.execute(""" CREATE TABLE blockchains (
                  blockchain_type text, 
                  consensus text, 
                  cryptography text
                  )""")
   '''

   # Submit function database
   def submit():
      conn = sqlite3.connect('blockchain_book.db')
      cursor = conn.cursor()

      # Insert into tables
      cursor.execute("INSERT INTO blockchains VALUES(:b_type, :consensus, :crypt)",
                     {
                        'b_type': b_type.get(),
                        'consensus': consensus.get(),
                        'crypt': crypt.get()
                     })

      # Commit Changes
      conn.commit()
      # Close Connection
      conn.close()

      # Clear texboxes
      b_type.delete(0, END)
      consensus.delete(0,END)
      crypt.delete(0,END)

   # Create Query function
   def query():
      conn = sqlite3.connect('blockchain_book.db')
      cursor = conn.cursor()

      # Query the database
      cursor.execute("SELECT *, oid from blockchains")
      records = cursor.fetchall()

      # Loop through results
      prt_records =''
      for record in records:
         prt_records += str(record) + "\n"

      query_label = Label(tab1, text=prt_records)
      query_label.grid(row=8, column=0, columnspan=2)


      # Commit Changes
      conn.commit()
      # Close Connection
      conn.close()

   # Drop down
   """options = [
      "Public blockchain",
      "Private blockchain"
   ]

   clicked = StringVar()
   clicked.set(options[0])
   b_type = OptionMenu(root, clicked, *options, command=display_selected)
   b_type.grid(row=0, column=1, padx=20) """

   # Textbox
   b_type = Entry(tab1, width=30)
   b_type.grid(row=0, column=1, padx=20)
   consensus = Entry(tab1, width=30)
   consensus.grid(row=1, column=1, padx=20)
   crypt = Entry(tab1, width=30)
   crypt.grid(row=2, column=1, padx=20)

   # Textbox label
   b_type_label = Label(tab1, text="Blockchain Type")
   b_type_label.grid(row=0, column=0)
   consensus_label = Label(tab1, text="Consensus")
   consensus_label.grid(row=1, column=0)
   crypt_label = Label(tab1, text="Cryptography")
   crypt_label.grid(row=2, column=0)

   # Submit Button
   submit_button = Button(tab1, text="Add blockchain to database", command=submit)
   submit_button.grid(row=6, column=0, columnspan=2, pady=10, ipadx=100)

   # Query button
   query_button = Button(tab1, text="Show records", command=query)
   query_button.grid(row=7, column =0, columnspan= 2, pady=10, padx=10, ipadx=137)


   # Commit Changes
   conn.commit()
   # Close Connection
   conn.close()

   root.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
