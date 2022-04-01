# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3


def main():
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
            conn = sqlite3.connect('blockchain_book.db')
            cursor = conn.cursor()

            btype = b_type.get()
            cons = consensus.get()
            crypto = crypt.get()
            msg = ''

            try:
                cursor.execute(
                    """INSERT INTO blockchains(b_type, consensus_type,cryptography_type) 
                      VALUES(?,?,?)""",
                    (btype, cons, crypto), )

                msg = 'Blockchain added to database!'
                # Clear texboxes
                b_type.set('')
                consensus.set('')
                crypt.set('')
            except Exception as ep:
                messagebox.showerror('error', ep)

            messagebox.showinfo('message', msg)

            # Commit Changes
            conn.commit()
            # Close Connection
            conn.close()

        # Submit interoperable blockchain to database
        def submitInteroperability():
            conn = sqlite3.connect('blockchain_book.db')
            cursor = conn.cursor()

            btype1 = block1.get()
            btype2 = block2.get()
            checkboxes = [var1, var2, var3]

            strategy = ''
            for c in checkboxes:
               if c.get() == "Notary":
                  strategy += c.get()
               if c.get() == "HTLC":
                  strategy += c.get()
               if c.get() == "Relay":
                  strategy += c.get()

            msg = ''

            query = '''INSERT INTO interoperability(first_blockchain, second_blockchain,strategy_type)
                      VALUES(?,?,?)'''
            params = (btype1, btype2, strategy)

            try:
                cursor.execute(query, params,)

                msg = 'Interoperability created!'
                # Clear texboxes
                blockchain1combo_type.set('')
                blockchain2combo_type.set('')
                var1.set(0)
                var2.set(0)
                var3.set(0)
            except Exception as ep:
                messagebox.showerror('error', ep)

            messagebox.showinfo('message', msg)

            # Commit Changes
            conn.commit()
            # Close Connection
            conn.close()



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
            data = cursor.fetchall()

            # Show records
            for record in data:
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

            # Commit Changes and Close connection
            conn.commit()
            conn.close()

            def hideRecords():
               hide_button['state'] = 'disable'
               query_button['state'] = 'normal'
               tree_frame.destroy()

            hide_button = Button(tab1, text="Hide records", command=hideRecords)
            hide_button.grid(row=7, column=2, columnspan=2, pady=10, padx=10, ipadx=137)

        # Function to restrict the user to select only one strategy
        def varUpdate():
            v1 = var1.get()
            v2 = var2.get()
            v3 = var3.get()

            i = 0
            if v1 == "Notary": i = i + 1
            if v2 == "HTLC": i = i + 1
            if v3 == "Relay": i = i + 1

            if (i == 1):
                submitInteroperability_button['state'] = NORMAL
            else:
                submitInteroperability_button['state'] = DISABLED


        # Dropbown menu method based on the first input
        def pick_consensus(e):
            if b_type.get() == blockchainList[0]:
                consensus.config(value=consensusPublicList)
                consensus.current(0)
            if b_type.get() == blockchainList[1]:
                consensus.config(value=consensusPrivateList)
                consensus.current(0)

        # Method to prevent from choosing the same value in combobox
        def update_combos(e):
            blockchain1combo_type['values'] = [x for x in options if x != blockchain2combo_type.get()]
            blockchain2combo_type['values'] = [x for x in options if x != blockchain1combo_type.get()]

        def databaseConnection():
            # Database connection
            conn = sqlite3.connect('blockchain_book.db', timeout=50)
            cursor = conn.cursor()
            print('Database Initialization and Connection successful')

            # Create table for blockchains
            cursor.execute(""" CREATE TABLE IF NOT EXISTS blockchains (
                        b_type text,
                        consensus_type text,
                        cryptography_type BOOLEAN NOT NULL)""")

            # Create table for blockchain type
            cursor.execute(""" CREATE TABLE IF NOT EXISTS blockchainType (
                        id integer PRIMARY KEY UNIQUE NOT NULL, 
                        blockchain_type text)""")

            # Create table for consensus
            cursor.execute(""" CREATE TABLE IF NOT EXISTS consensus (
                           blockchain_id integer,
                           consensus_name text NOT NULL,
                           FOREIGN KEY (blockchain_id) REFERENCES blockchainType (id))""")

            # Create table for cryptography
            cursor.execute("""CREATE TABLE IF NOT EXISTS cryptography(
                            bol_cryptography BOOLEAN NOT NULL)""")

            # Create table for interoperability
            cursor.execute("""CREATE TABLE IF NOT EXISTS interoperability(
                        blockchain_id INTEGER,
                        first_blockchain text,
                        second_blockchain text, 
                        strategy_type text,
                        FOREIGN KEY (blockchain_id) REFERENCES blockchains(oid))""")

            # Data list
            blockchain_type = [(1, 'Public Blockchain'),
                               (2, 'Private Blockchain')]

            consenus_type = [(1, 'Proof-of-Work'),
                             (1, 'Proof-of-Stake'),
                             (2, 'POF')]

            # Insert data to database
            cursor.executemany('INSERT OR IGNORE INTO blockchainType VALUES(?,?)', blockchain_type)
            cursor.executemany('INSERT OR IGNORE INTO consensus VALUES(?,?)', consenus_type)

            cursor.execute('INSERT OR IGNORE INTO cryptography VALUES(TRUE)')
            cursor.execute('INSERT OR IGNORE INTO cryptography VALUES(FALSE)')

            # Commit Changes and Close connection
            conn.commit()
            cursor.close()

        # Run the database method
        databaseConnection()

        """--------------------- TAB 1 ---------------------"""
        # Database connection
        conn = sqlite3.connect('blockchain_book.db', timeout=50)
        cursor = conn.cursor()

        # Variable
        type1 = StringVar()
        type2 = StringVar()
        type3 = StringVar()

        # Get data from database
        query1 = cursor.execute(
            """SELECT DISTINCT blockchain_type 
               FROM blockchainType""")
        # store data in list
        blockchainList = [b for b, in query1]

        publicQuery2 = cursor.execute(
            """SELECT DISTINCT consensus_name 
               FROM blockchainType,consensus 
                  WHERE blockchain_id == blockchainType.id 
                     AND blockchainType.id == 1""")
        # store data in list
        consensusPublicList = [c for c, in publicQuery2]

        privateQuery2 = cursor.execute(
            """SELECT DISTINCT consensus_name 
               FROM consensus, blockchainType 
                     WHERE blockchain_id == blockchainType.id 
                           AND blockchain_id == 2""")
        # store data in list
        consensusPrivateList = [i for i, in privateQuery2]

        cryptoQuery = cursor.execute(
            """SELECT DISTINCT bol_cryptography
               FROM cryptography""")
        # store data in list
        cryptoList = [b for b, in cryptoQuery]
        trueOrFalse = [i > 0 for i in cryptoList]

        # Combobox
        b_type = ttk.Combobox(tab1, state="readonly", textvariable=type1, width=20, values=blockchainList)
        b_type.grid(row=0, column=1, padx=20, pady=10)
        # binding the combobox
        b_type.bind("<<ComboboxSelected>>", pick_consensus)

        consensus = ttk.Combobox(tab1, state="readonly", textvariable=type2, width=20, values=[" "])
        consensus.grid(row=1, column=1, padx=20, pady=10)

        crypt = ttk.Combobox(tab1, state="readonly", textvariable=type3, width=20, values=trueOrFalse)
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
        var1 = StringVar()
        var2 = StringVar()
        var3 = StringVar()
        block1 = StringVar()
        block2 = StringVar()


        # Combobox
        options = []
        cursor.execute("SELECT b_type,consensus_type from blockchains")
        records = cursor.fetchall()
        for i in records:
            options.append(str(i[0]) + " - " + i[1])

        blockchain1combo_type = ttk.Combobox(tab2, state="readonly", textvariable=block1, width=30, values=options)
        blockchain1combo_type.grid(row=0, column=1, padx=20, pady=10)
        blockchain1combo_type.bind("<<ComboboxSelected>>", update_combos)
        blockchain2combo_type = ttk.Combobox(tab2, state="readonly", textvariable=block2, width=30, values=options)
        blockchain2combo_type.grid(row=1, column=1, padx=20, pady=10)

        # Textbox
        notary = Checkbutton(tab2, text="Notary Scheme", variable=var1, onvalue="Notary", command=varUpdate).grid(row=2,
                                                                                                                  column=0,
                                                                                                                  pady=10,
                                                                                                                  padx=20)
        htlc = Checkbutton(tab2, text="HTLC", variable=var2, onvalue="HTLC", command=varUpdate).grid(row=2, column=1,
                                                                                                     pady=10)
        relay = Checkbutton(tab2, text="Relay/Sidechain", onvalue="Relay", variable=var3, command=varUpdate).grid(row=2,
                                                                                                                  column=3,
                                                                                                                  pady=10)

        # Textbox label
        blockchain1_type = Label(tab2, text="Blockchain A")
        blockchain1_type.grid(row=0, column=0)
        blockchain2_type = Label(tab2, text="Blockchain B")
        blockchain2_type.grid(row=1, column=0)

        # Submit Button
        submitInteroperability_button = Button(tab2, text="Create interoperability", command=submitInteroperability,
                                               state=DISABLED)
        submitInteroperability_button.grid(row=6, column=0, columnspan=4, pady=10, ipadx=100)

        # Commit Changes and Close connection
        conn.commit()
        cursor.close()
        conn.close()

    # Throw exception
    except sqlite3.Error as error:
        print('Error occured - ', error)


# RUN THE PROGRAM
if __name__ == '__main__':
    root = Tk()
    root.title("Blockchain interoperability")
    root.geometry("1000x500")
    main()
    root.mainloop()
