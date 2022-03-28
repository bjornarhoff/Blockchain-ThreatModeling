# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3


def main():
   root = Tk()
   root.title("Blockchain interoperability")
   root.geometry("1000x500")

   # Add Some Style
   style = ttk.Style()

   # Pick A Theme
   style.theme_use('clam')

   # Configure the Treeview Colors
   style.configure("Treeview",
                   background="#D3D3D3",
                   foreground="black",
                   rowheight=25,
                   fieldbackground="#D3D3D3")

   # Change Selected Color
   style.map('Treeview',
             background=[('selected', "#347083")])

   # Creating tabs
   tab_control = ttk.Notebook(root)
   tab1 = Frame(tab_control)
   tab_control.add(tab1, text="Add blockchain")

   tab2 = Frame(tab_control)
   tab_control.add(tab2, text="Create blockchain interoperability")
   tab_control.pack(expand=1, fill="both", padx=100)


   try:

      # Submit blockchain to database
      def submitBlockchain():
         #conn = sqlite3.connect('blockchain_book.db')
         #cursor = conn.cursor()

         btype = b_type.get()
         cons = consensus.get()
         crypto = crypt.get()
         msg = ''

         cursor.execute("""INSERT INTO blockchains(b_type, consensus_type,cryptography_type) VALUES(?,?,?)""", (btype, cons,crypto),)
         cursor.execute("""SELECT * from blockchains""")
         print(cursor.fetchall())

         # Insert into tables
         # cursor.execute("INSERT INTO blockchains(b_type,consensus,crypt) VALUES('{}','{}','{}');".format(btype,cons,crypto))
         # cursor.execute("INSERT INTO blockchains VALUES('Public','POS',FALSE)")


         """         if cons=="" & str(crypto)=="" & btype=="":
            msg = 'Input fields can\'t be empty'
         else:
            try:
                  msg = 'Blockchain added to database!'
                  # Clear texboxes
                  b_type.delete(0, END)
                  consensus.delete(0, END)
                  crypt.delete(0, END)
            except Exception as ep:
               messagebox.showerror('error', ep)

         messagebox.showinfo('message', msg)"""



         # Commit Changes
         conn.commit()
         # Close Connection
         conn.close()

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
         query_button['state'] = 'disable'

         # Treeview Frame
         tree_frame = Frame(root)
         tree_frame.pack(pady=10)

         # Treeview Scrollbar
         tree_scroll = Scrollbar(tree_frame)
         tree_scroll.pack(side=RIGHT, fill=Y)

         # Treeview
         tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
         tree.pack()

         # Scrollbar
         tree_scroll.config(command=tree.yview)

         # Define Columns
         tree['columns'] = ("ID", "Blockchain Type", "Consensus", "Cryptography")

         # Format Colums
         tree.column("#0", width=0, stretch=NO)
         tree.column("ID", width=100, anchor=CENTER)
         tree.column("Blockchain Type", anchor=CENTER, width=140)
         tree.column("Consensus", anchor=CENTER, width=140)
         tree.column("Cryptography", anchor=CENTER, width=100)

         # Column Heading
         tree.heading("ID", text="ID", anchor=CENTER)
         tree.heading("Blockchain Type", text="Blockchain Type", anchor=CENTER)
         tree.heading("Consensus", text="Consensus", anchor=CENTER)
         tree.heading("Cryptography", text="Cryptography", anchor=CENTER)

         # Clear the Treeview
         for record in tree.get_children():
            tree.delete(record)

         # Add our data to the screen
         global counter
         counter = 0

         # Query the database
         cursor.execute("SELECT *, oid from blockchains")
         records = cursor.fetchall()

         for record in records:
            if counter % 2 == 0:
               tree.insert(parent='', index='end', iid=counter, text='',
                           values=(record[3], record[0], record[1], record[2]),
                           tags=('evenrow',))
            else:
               tree.insert(parent='', index='end', iid=counter, text='',
                           values=(record[3], record[0], record[1], record[2]),
                           tags=('oddrow',))
            # increment counter
            counter += 1

         # Commit Changes
         conn.commit()
         # Close Connection
         conn.close()

      # Function to restrict the user to select only one strategy
      def varUpdate():
         i = 0
         if (var1.get() == 1): i = i + 1
         if (var2.get() == 1): i = i + 1
         if (var3.get() == 1): i = i + 1
         if (i == 1):
            submitInteroperability_button['state'] = NORMAL
         else:
            submitInteroperability_button['state'] = DISABLED

      def pick_consensus(e):
         if b_type.get() == blockchainList[0]:
            consensus.config(value=consensusPublicList)
            consensus.current(0)
         if b_type.get() == blockchainList[1]:
            consensus.config(value=consensusPrivateList)
            consensus.current(0)

      # Database
      conn = sqlite3.connect('blockchain_book.db', timeout=50)
      cursor = conn.cursor()
      print('Database Initialization and Connection successful')

      # Create table for blockchains
      cursor.execute(""" CREATE TABLE IF NOT EXISTS blockchains (
                     b_type text,
                     consensus_type text,
                     cryptography_type BOOLEAN NOT NULL
                     )""")

      # Create table for blockchain type
      cursor.execute(""" CREATE TABLE IF NOT EXISTS blockchainType (
                     id integer PRIMARY KEY UNIQUE NOT NULL, 
                     blockchain_type text
                     )""")

      # Create table for consensus
      cursor.execute(""" CREATE TABLE IF NOT EXISTS consensus (
                        blockchain_id integer,
                        consensus_name text NOT NULL,
                        FOREIGN KEY (blockchain_id) REFERENCES blockchainType (id))""")

      # Create table for cryptography
      cursor.execute(""" CREATE TABLE IF NOT EXISTS cryptography (
                        bol_cryptography BOOLEAN NOT NULL 
                        )""")

      cursor.execute("""INSERT INTO blockchainType VALUES(1,'Public Blockchain')""")
      cursor.execute("""INSERT INTO blockchainType VALUES(2, 'Private Blockchain')""")

      cursor.execute("""INSERT INTO consensus VALUES(1, 'Proof-of-Work')""")
      cursor.execute("""INSERT INTO consensus VALUES(1, 'Proof-of-Stake')""")
      cursor.execute("""INSERT INTO consensus VALUES(2, 'POF')""")

      cursor.execute("""INSERT INTO cryptography VALUES(TRUE)""")
      cursor.execute("""INSERT INTO cryptography VALUES(FALSE)""")

      cursor.execute("""SELECT * from blockchains""")

      """--------------------- TAB 1 ---------------------"""
      type1 = StringVar()
      query1 = cursor.execute("SELECT DISTINCT blockchain_type FROM blockchainType")
      blockchainList = [b for b, in query1]

      type2 = StringVar()
      publicQuery2 = cursor.execute(
         "SELECT DISTINCT consensus_name from blockchainType,consensus WHERE blockchain_id == blockchainType.id AND blockchainType.id ==1")
      consensusPublicList = [c for c, in publicQuery2]
      print(consensusPublicList)

      privateQuery2 = cursor.execute(
         "SELECT DISTINCT consensus_name FROM consensus, blockchainType WHERE blockchain_id == blockchainType.id AND blockchain_id == 2")
      consensusPrivateList = [i for i, in privateQuery2]
      print(consensusPrivateList)

      type3 = StringVar()
      cryptoQuery = cursor.execute("SELECT DISTINCT bol_cryptography FROM cryptography")
      cryptoList = [b for b, in cryptoQuery]
      trueOrFalse = [i > 0 for i in cryptoList]

      # opt = ['Private blockchain', 'Public blockchain']

      # Combobox
      b_type = ttk.Combobox(tab1, textvariable=type1, width=20, values=blockchainList)
      b_type.grid(row=0, column=1, padx=20, pady=10)
      # bind the combobox
      b_type.bind("<<ComboboxSelected>>", pick_consensus)

      consensus = ttk.Combobox(tab1, textvariable=type2, width=20, values=[" "])
      consensus.grid(row=1, column=1, padx=20, pady=10)

      crypt = ttk.Combobox(tab1, textvariable=type3, width=20, values=trueOrFalse)
      crypt.grid(row=2, column=1, padx=20, pady=10)

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
      query_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

      """--------------------- TAB 2 ---------------------"""

      # Variables
      var1 = IntVar()
      var2 = IntVar()
      var3 = IntVar()
      block1 = StringVar()
      block2 = StringVar()

      # Combobox
      options = []
      # Query the database
     # conn = sqlite3.connect('blockchain_book.db')
      #cursor = conn.cursor()
      cursor.execute("SELECT oid,blockchain_type from blockchainType")
      records = cursor.fetchall()
      for i in records:
         options.append(str(i[0]) + " - " + i[1])

      blockchain1_type = ttk.Combobox(tab2, textvariable=block1, width=20, values=options)
      blockchain1_type.grid(row=0, column=1, padx=20, pady=10)
      blockchain2_type = ttk.Combobox(tab2, textvariable=block2, width=20, values=options)
      blockchain2_type.grid(row=1, column=1, padx=20, pady=10)

      # Textbox
      notary = Checkbutton(tab2, text="Notary Scheme", variable=var1, command=varUpdate).grid(row=2, column=0, pady=10,
                                                                                              padx=20)
      htlc = Checkbutton(tab2, text="HTLC", variable=var2, command=varUpdate).grid(row=2, column=1, pady=10)
      relay = Checkbutton(tab2, text="Relay/Sidechain", variable=var3, command=varUpdate).grid(row=2, column=3, pady=10)

      # Textbox label
      blockchain1_type = Label(tab2, text="Blockchain A")
      blockchain1_type.grid(row=0, column=0)
      blockchain2_type = Label(tab2, text="Blockchain B")
      blockchain2_type.grid(row=1, column=0)

      # Submit Button
      submitInteroperability_button = Button(tab2, text="Create interoperability", command=submitInteroperability,
                                             state=DISABLED)
      submitInteroperability_button.grid(row=6, column=0, columnspan=4, pady=10, ipadx=100)

      # Commit Changes
      conn.commit()

      root.mainloop()

      # get data
      record = cursor.fetchall()
      print(f'SQLite Version - {record}')
      cursor.close()

   except sqlite3.Error as error:
      print('Error occured - ', error)

   finally:
      # If the connection was established then close it
      if conn:
         conn.close()
         print('SQLite Connection closed')




# RUN THE PROGRAM
if __name__ == '__main__':
    main()
