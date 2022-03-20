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

   # Create table for blockchain
   '''cursor.execute(""" CREATE TABLE blockchains (
                  blockchain_type text, 
                  consensus text, 
                  cryptography text
                  )""")
   '''

   # Create table for interoperability
   '''cursor.execute(""" CREATE TABLE interoperability (
                  blockchain_type text, 
                  consensus text, 
                  cryptography text
                  )""")
   '''

   # Submit blockchain to database
   def submitBlockchain():
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


   # Submit interoperable blockchain to database
   def submitInteroperability():
      """
      :return:
      conn = sqlite3.connect('blockchain_book.db')
      cursor = conn.cursor()

      # Commit Changes
      conn.commit()
      # Close Connection
      conn.close()

      # Clear texboxes
      blockchain1_type.delete(0, END)
      blockchain2_type.delete(0,END)
      notary.delete(0,END)
      htlc.delete(0,END)
      relay.delete(0,END)
      """
      return


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


   """--------------------- TAB 1 ---------------------"""
   type = StringVar()
   opt = ['Private blockchain', 'Public blockchain']

   b_type = ttk.Combobox(tab1, textvariable=type, width=20, values=opt)
   b_type.grid(row=0, column=1, padx=20)
   # Textbox
   #b_type = Entry(tab1, width=30)
   #b_type.grid(row=0, column=1, padx=20)
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
   submit_button = Button(tab1, text="Add blockchain to database", command=submitBlockchain)
   submit_button.grid(row=6, column=0, columnspan=2, pady=10, ipadx=100)

   # Query button
   query_button = Button(tab1, text="Show records", command=query)
   query_button.grid(row=7, column =0, columnspan= 2, pady=10, padx=10, ipadx=137)

   """--------------------- TAB 2 ---------------------"""

   # Variables
   var1 = IntVar()
   var2 = IntVar()
   var3 = IntVar()
   block1= StringVar()
   block2 = StringVar()

   # Combobox
   options = []
   # Query the database
   conn = sqlite3.connect('blockchain_book.db')
   cursor = conn.cursor()
   cursor.execute("SELECT oid,blockchain_type from blockchains")
   records = cursor.fetchall()
   for i in records:
      options.append(str(i[0]) + " - " + i[1])

   blockchain1_type = ttk.Combobox(tab2, textvariable=block1, width=20, values=options)
   blockchain1_type.grid(row=0, column=1, padx=20)
   blockchain2_type = ttk.Combobox(tab2, textvariable=block2, width=20, values=options)
   blockchain2_type.grid(row=1, column=1, padx=20)

   # Textbox
   #blockchain1_type = Entry(tab2, width=15)
   #blockchain1_type.grid(row=0, column=1, padx=20)
   #blockchain2_type = Entry(tab2, width=15)
   #blockchain2_type.grid(row=1, column=1, padx=20)
   notary = Checkbutton(tab2, text="Notary Scheme", variable=var1).grid(row=2, column=0)
   htlc = Checkbutton(tab2, text="HTLC", variable=var2).grid(row=2,column=1)
   relay = Checkbutton(tab2, text="Relay/Sidechain", variable=var3).grid(row=2, column=3)

   # Textbox label
   blockchain1_type = Label(tab2, text="Blockchain A")
   blockchain1_type.grid(row=0, column=0)
   blockchain2_type = Label(tab2, text="Blockchain B")
   blockchain2_type.grid(row=1, column=0)

   # Submit Button
   submit_button = Button(tab2, text="Create interoperability", command=submitInteroperability)
   submit_button.grid(row=6, column=0, columnspan=4, pady=10, ipadx=100)

   # Commit Changes
   conn.commit()
   # Close Connection
   conn.close()

   root.mainloop()


# RUN THE PROGRAM
if __name__ == '__main__':
    main()
