# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd
from re import search


def main():
    # Add Some Style
    style = ttk.Style()

    # Pick A Theme
    style.theme_use('clam')

    # Configure the Treeview Colors
    style.configure("Treeview",
                    background="#ededed",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#ededed")

    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Arial', 13), rowheight=40, fieldbackground="#ededed", background="#ededed",)  # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", font=('Arial', 13, 'bold'))  # Modify the font of the headings
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

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
            bname = b_name.get()
            cons = consensus.get()
            crypto = crypt.get()
            msg = ''

            try:
                cursor.execute(
                    """INSERT INTO blockchains(BtypeID, B_name, ConsensusID,CryptographyID) 
                      VALUES(?,?,?,?)""",
                    (btype, bname, cons, crypto), )

                msg = 'Blockchain added to database!'
                # Clear texboxes
                b_type.set('')
                b_name.delete(0, END)
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
               if c.get() == "Notary Scheme":
                  strategy += c.get()
               if c.get() == "HTLC":
                  strategy += c.get()
               if c.get() == "Relay/Sidechain":
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



        # Show records from database function
        def showRecords():
            conn = sqlite3.connect('blockchain_book.db')
            cursor = conn.cursor()
            query_button['state'] = 'disable'

            # Treeview Frame
            tree_frame = Frame(root)
            tree_frame.pack(fill='x',pady=10)

            # Treeview Scrollbar
            tree_scroll = Scrollbar(tree_frame)
            tree_scroll.pack(side=RIGHT, fill=Y)

            # Treeview
            tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
            tree.pack()

            # Scrollbar
            tree_scroll.config(command=tree.yview)

            # Define Columns
            tree['columns'] = ("ID", "Name", "Blockchain Type", "Consensus", "Cryptography")

            # Format Colums
            tree.column("#0", width=0, stretch=NO)
            tree.column("ID", width=100, anchor=CENTER)
            tree.column("Name", width=100, anchor=CENTER)
            tree.column("Blockchain Type", anchor=CENTER, width=140)
            tree.column("Consensus", anchor=CENTER, width=140)
            tree.column("Cryptography", anchor=CENTER, width=100)

            # Column Heading
            tree.heading("ID", text="ID", anchor=CENTER)
            tree.heading("Name", text = "Name", anchor=CENTER)
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
            cursor.execute("SELECT *,oid from blockchains")
            data = cursor.fetchall()

            # Show records
            for record in data:
                if counter % 2 == 0:
                    tree.insert(parent='', index='end', iid=counter, text='',
                                values=(record[0], record[1], record[3], record[2], record[4]),
                                tags=('evenrow',))
                else:
                    tree.insert(parent='', index='end', iid=counter, text='',
                                values=(record[0], record[1], record[3], record[2], record[4]),
                                tags=('oddrow',))
                # increment counter
                counter += 1

            # Commit Changes and Close connection
            conn.commit()
            conn.close()
            # Button for hide records
            def hideRecords():
               hide_button['state'] = 'disable'
               query_button['state'] = 'normal'
               tree_frame.destroy()

            hide_button = Button(tab1, text="Hide records", command=hideRecords)
            hide_button.grid(row=7, column=2, columnspan=2, pady=10, padx=10, ipadx=137)




        # Show threats in treeview
        def showThreats():
            conn = sqlite3.connect('blockchain_book.db')
            cursor = conn.cursor()
            show_threats_button['state'] = 'disable'
            blockchain1combo_type['state'] = 'disable'
            blockchain2combo_type['state'] = 'disable'
            htlc.config(state=DISABLED)
            relay.config(state=DISABLED)
            notary.config(state=DISABLED)

            bcombo1 = blockchain1combo_type.get()
            bcombo2 = blockchain2combo_type.get()
            checkboxes = [var1, var2, var3]

            strategy = ''
            for c in checkboxes:
               if c.get() == "Notary Scheme":
                  strategy += c.get()
               if c.get() == "HTLC":
                  strategy += c.get()
               if c.get() == "Relay/Sidechain":
                  strategy += c.get()



            def url_collect(e):
                curItem = htree.focus()
                threat_url = ''
                if (htree.item(curItem)['values'] != ''):
                    threat_url = htree.item(curItem)['values'][0]  # collect selected row id
                    print(threat_url)


            # Query the database
            cursor.execute(
                """SELECT Description, Consensus_name, URL
                    FROM threat,consensus 
                    JOIN consensusThreat 
                    ON consensusThreat.ThreatID = threat.ThreatID 
                    AND consensusThreat.ConsensusID = consensus.ConsensusID 
                    WHERE Consensus_name = 'Proof-of-Work' 
                    GROUP BY Description""")

            pow_data = cursor.fetchall()

            # Query the database
            cursor.execute(
                """SELECT Description, Consensus_name, URL
                    FROM threat,consensus 
                    JOIN consensusThreat 
                    ON consensusThreat.ThreatID = threat.ThreatID 
                    AND consensusThreat.ConsensusID = consensus.ConsensusID 
                    WHERE Consensus_name = 'Proof-of-Stake' 
                    GROUP BY Description""")

            pos_data = cursor.fetchall()

            # Query the database
            cursor.execute(
                """SELECT Description, Strategy_name, URL
                    FROM threat,strategy 
                    JOIN interoperabilityThreat 
                    ON interoperabilityThreat.ThreatID = threat.ThreatID 
                    AND interoperabilityThreat.StrategyID = strategy.StrategyID""")

            interoperability_data = cursor.fetchall()


            # Create frame for treeview
            treeview = Frame(root)
            treeview.pack(expand=True, anchor='c')
            # Label Heading
            Label(treeview,
                            text="Hierarchical Threats Data",
                            fg="black",
                            font="Arial 15 bold").pack()
            # Treeview Scrollbar
            scroll = Scrollbar(treeview)
            scroll.pack(side=RIGHT, fill=Y)

            # Treeview
            htree = ttk.Treeview(treeview, yscrollcommand=scroll.set, height=15,selectmode="browse", style="mystyle.Treeview", columns=("url"))
            htree.pack(expand=True)
            htree.bind("<<TreeviewSelect>>", url_collect)
            # Scrollbar
            scroll.config(command=htree.yview)
            # Clear the Treeview
            for record in htree.get_children():
                htree.delete(record)

            htree.heading('#0', text='Threats Categorized', anchor='c')
            htree.heading('url', text='URL', anchor='c')

            # adding data
            htree.insert('', END, text='Consensus', iid=0, open=False)
            htree.insert('', END, text='Network', iid=1, open=False)
            htree.insert('', END, text='Transaction', iid=2, open=False)
            htree.insert('', END, text='Block Creation', iid=3, open=False)
            htree.insert('', END, text='Human error/Code Exploiting', iid=4, open=False)
            htree.insert('', END, text='Interoperability', iid=5, open=False)

            # adding children of first node
            htree.insert('', tk.END, text='Proof-of-work', iid=6, open=False)
            htree.insert('', tk.END, text='Proof-of-stake', iid=7, open=False)
            htree.move(6,0,1)
            htree.move(7,0,2)

            # ID counter to display hierarchical data
            id_counter = 8
            if search(pow_data[1][1], bcombo1) or search(pow_data[1][1], bcombo2):
                # Show records
                for pow in pow_data:
                    if (pow != ''):
                        htree.insert(parent=6, index='end', iid=id_counter, text=(pow[0]),values=(pow[2]))
                        id_counter += 1
                    else:
                        print("Did not found proof-of-work data")
            else:
                print("Input doesnt match proof of work ")

            if search(pos_data[1][1], bcombo1) or search(pos_data[1][1], bcombo2):
                # Show records
                for pos in pos_data:
                    if (pos != ''):
                        htree.insert(parent=7, index='end', iid=id_counter, text=(pos[0]),values=(pos[2]))
                        id_counter += 1
                    else:
                        print("Did not found proof-of-stake data ")
            else:
                print("Input doesnt match proof of stake ")


            # Show records
            for int in interoperability_data:
                print(int)
                for j in int:
                    print(j)
                    if (j == strategy):
                        htree.insert(parent=5, index='end', iid=id_counter, text=(int[0]), values=(int[2]))
                        id_counter += 1


            # Hide threats
            def hideThreats():
                hide_threats['state'] = 'disable'
                show_threats_button['state'] = 'normal'
                blockchain1combo_type['state'] = 'normal'
                blockchain2combo_type['state'] = 'normal'
                notary.config(state=NORMAL)
                htlc.config(state=NORMAL)
                relay.config(state=NORMAL)
                treeview.destroy()

            # Button for hiding threat treeview
            hide_threats = Button(tab2, text="Hide threats", command=hideThreats)
            hide_threats.grid(row=7, column=0, columnspan=4, pady=10, ipadx=100)

            # Commit Changes and Close connection
            conn.commit()
            conn.close()


        """
        # Show records from database function
        def showThreats():
            conn = sqlite3.connect('blockchain_book.db')
            cursor = conn.cursor()
            show_threats_button['state'] = 'disable'

            bcombo1 = blockchain1combo_type.get()
            bcombo2 = blockchain2combo_type.get()

            def selectItemTreeview(a):
                curItem = tree.focus()
                input_item = tree.item(curItem)
                item_list = input_item.get('values')
                url = item_list[2]

                import webbrowser
                webbrowser.open(url)


            # Query the database
            cursor.execute(
                SELECT Description, Consensus_name, URL
                    FROM threat,consensus 
                    JOIN consensusThreat 
                    ON consensusThreat.ThreatID = threat.ThreatID 
                    AND consensusThreat.ConsensusID = consensus.ConsensusID 
                    WHERE Consensus_name = 'Proof-of-Work' 
                    GROUP BY Description)

            pow_data = cursor.fetchall()

            # Query the database
            cursor.execute(
                SELECT Description, Consensus_name, URL
                    FROM threat,consensus 
                    JOIN consensusThreat 
                    ON consensusThreat.ThreatID = threat.ThreatID 
                    AND consensusThreat.ConsensusID = consensus.ConsensusID 
                    WHERE Consensus_name = 'Proof-of-Stake' 
                    GROUP BY Description)

            pos_data = cursor.fetchall()





            if search(pow_data[1][1], bcombo1) or search(pow_data[1][1], bcombo2):
                # Treeview Frame 2
                tree_frame2 = Frame(root)
                tree_frame2.pack(expand=True,side='left')
                # Treeview Scrollbar
                tree_scroll2 = Scrollbar(tree_frame2)
                tree_scroll2.pack(side=RIGHT, fill=Y)
                # Treeview
                tree2 = ttk.Treeview(tree_frame2, yscrollcommand=tree_scroll2.set, selectmode="extended")
                tree2.pack()

                # Scrollbar
                tree_scroll2.config(command=tree2.yview)

                # Define Columns
                tree2['columns'] = ("Attack", "Consensus", "URL")

                # Format Colums
                tree2.column("#0", width=0, stretch=NO)
                tree2.column("Attack", width=200, anchor=CENTER)
                tree2.column("Consensus", width=200, anchor=CENTER)
                tree2.column("URL", width=200, anchor=CENTER)

                # Column Heading
                tree2.heading("Attack", text="Attack", anchor=CENTER)
                tree2.heading("Consensus", text = "Consensus", anchor=CENTER)
                tree2.heading("URL", text="URL", anchor=CENTER)

                # Clear the Treeview
                for record in tree2.get_children():
                    tree2.delete(record)

                # Add our data to the screen
                global counter2
                counter2 = 0

                # Show records
                for record in pow_data:
                    if counter2 % 2 == 0:
                        tree2.insert(parent='', index='end', iid=counter2, text='',
                                     values=(record[0], record[1], record[2]),
                                     tags=('evenrow',))
                    else:
                        tree2.insert(parent='', index='end', iid=counter2, text='',
                                     values=(record[0], record[1], record[2]),
                                     tags=('oddrow',))
                    # increment counter
                    counter2 += 1
            else:
                print("Did not found proof-of-work")

            if search(pos_data[1][1], bcombo2) or search(pos_data[1][1], bcombo1):
                # Treeview Frame 1
                tree_frame = Frame(root)
                tree_frame.pack(expand=True, side='left')
                # Treeview Scrollbar
                tree_scroll = Scrollbar(tree_frame)
                tree_scroll.pack(side=RIGHT, fill=Y)

                # Treeview
                tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
                tree.pack()
                tree.bind('<Double-1>', selectItemTreeview)

                # Scrollbar
                tree_scroll.config(command=tree.yview)

                # Define Columns
                tree['columns'] = ("Attack", "Consensus", "URL")

                # Format Colums
                tree.column("#0", width=0, stretch=NO)
                tree.column("Attack", width=200, anchor=CENTER)
                tree.column("Consensus", width=200, anchor=CENTER)
                tree.column("URL", width=200, anchor=CENTER)

                # Column Heading
                tree.heading("Attack", text="Attack", anchor=CENTER)
                tree.heading("Consensus", text = "Consensus", anchor=CENTER)
                tree.heading("URL", text="URL", anchor=CENTER)

                # Clear the Treeview
                for record in tree.get_children():
                    tree.delete(record)

                # Add our data to the screen
                global counter
                counter = 0

                # Show records
                for record in pos_data:
                    if counter % 2 == 0:
                        tree.insert(parent='', index='end', iid=counter, text='',
                                    values=(record[0], record[1], record[2]),
                                    tags=('evenrow',))
                    else:
                        tree.insert(parent='', index='end', iid=counter, text='',
                                    values=(record[0], record[1], record[2]),
                                    tags=('oddrow',))
                    # increment counter
                    counter += 1
                else:
                    print("Did not found proof-of-stake")



            def hideThreats():
                hide_threats['state'] = 'disable'
                show_threats_button['state'] = 'normal'
                tree_frame.destroy()
                tree_frame2.destroy()

            hide_threats = Button(tab2, text="Hide threats", command=hideThreats)
            hide_threats.grid(row=7, column=0, columnspan=4, pady=10, ipadx=100)

            # Commit Changes and Close connection
            conn.commit()
            conn.close()
            """


        # Function to restrict the user to select only one strategy
        def varUpdate():
            v1 = var1.get()
            v2 = var2.get()
            v3 = var3.get()

            i = 0
            if v1 == 'Notary Scheme': i = i + 1
            if v2 == 'HTLC': i = i + 1
            if v3 == 'Relay/Sidechain': i = i + 1

            if (blockchain1combo_type.get() != '' and blockchain2combo_type.get() != '' and i == 1):
                show_threats_button['state'] = NORMAL
            else:
                show_threats_button['state'] = DISABLED


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
            #if (blockchain1combo_type.get() != '' and blockchain2combo_type.get() != ''):
             #   show_threats_button['state'] = NORMAL
            #else:
             #   show_threats_button['state'] = DISABLED


        def databaseConnection():
            # Database connection
            conn = sqlite3.connect('blockchain_book.db', timeout=50)
            cursor = conn.cursor()
            print('Database Initialization and Connection successful')

            # Create table for blockchains
            cursor.execute(""" CREATE TABLE IF NOT EXISTS blockchains (
                        BlockchainID INTEGER PRIMARY KEY,
                        B_name text NOT NULL,
                        ConsensusID text NOT NULL,
                        BtypeID text NOT NULL,
                        CryptographyID BOOLEAN NOT NULL,
                        FOREIGN KEY (BtypeID) REFERENCES btype (BtypeID),
                        FOREIGN KEY (CryptographyID) REFERENCES cryptography (CryptographyID)
                        FOREIGN KEY (ConsensusID) REFERENCES consensus (ConsensusID))""")

            # Create table for blockchain type
            cursor.execute(""" CREATE TABLE IF NOT EXISTS btype (
                        BtypeID INTEGER PRIMARY KEY, 
                        Btype_name text)""")

            # Create table for consensus
            cursor.execute(""" CREATE TABLE IF NOT EXISTS consensus (
                           ConsensusID INTEGER PRIMARY KEY,
                           Consensus_name text NOT NULL,
                           BtypeID INTEGER,
                           FOREIGN KEY (BtypeID) REFERENCES btype (BtypeID))""")

            # Create table for cryptography
            cursor.execute("""CREATE TABLE IF NOT EXISTS cryptography(
                            CryptographyID INTEGER PRIMARY KEY,
                            Bol_cryptography BOOLEAN NOT NULL)""")

            # Create table for strategy
            cursor.execute("""CREATE TABLE IF NOT EXISTS strategy(
                            StrategyID INTEGER PRIMARY KEY,
                            Strategy_name NOT NULL)""")

            # Create table for threats
            cursor.execute("""CREATE TABLE IF NOT EXISTS threat(
                                       ThreatID INTEGER PRIMARY KEY,
                                       Description NOT NULL,
                                       URL text)""")

            # Create table for consensus threats
            cursor.execute("""CREATE TABLE IF NOT EXISTS consensusThreat(
                                            ThreatID INTEGER,
                                            ConsensusID INTEGER,
                                            FOREIGN KEY (ThreatID) REFERENCES threat(ThreatID),
                                            FOREIGN KEY (ConsensusID) REFERENCES consensus(ConsensusID))""")

            # Create table for interoperability threats
            cursor.execute("""CREATE TABLE IF NOT EXISTS interoperabilityThreat (
                                                ThreatID INTEGER,
                                                StrategyID INTEGER,
                                                FOREIGN KEY (ThreatID) REFERENCES threat(ThreatID),
                                                FOREIGN KEY (StrategyID) REFERENCES strategy(StrategyID))""")
            # Create table for interoperability
            #cursor.execute("""CREATE TABLE IF NOT EXISTS interoperability(
             #           interoperabilityID PRIMARY KEY,
              #          blockchain_id INTEGER,
               #         first_blockchain text,
                #        second_blockchain text,
                 #       strategy_ID text,
                  #      FOREIGN KEY (blockchain_id) REFERENCES blockchains(blockchainID),
                   #     FOREIGN KEY (strategy_ID) REFERENCES blockchains(strategyID))""")


            cursor.execute('INSERT OR IGNORE INTO cryptography VALUES(NULL,TRUE)')
            cursor.execute('INSERT OR IGNORE INTO cryptography VALUES(NULL,FALSE)')

            # Read data from csv
            blockchain_type = pd.read_csv('data/btype.csv', sep = ';')
            consensus_type = pd.read_csv('data/consensus.csv', sep = ';')
            strategy = pd.read_csv('data/strategy.csv', sep=';')
            threats = pd.read_csv('data/threat.csv', sep=';')
            consensus_threats = pd.read_csv('data/consensusThreat.csv', sep=';')
            interoperability_threats = pd.read_csv('data/interoperabilityThreat.csv', sep =';')

            # Insert dato to sqlite
            blockchain_type.to_sql('btype', conn, if_exists='replace', index=False)
            consensus_type.to_sql('consensus', conn, if_exists='replace', index=False)
            strategy.to_sql('strategy', conn, if_exists='replace', index=False)
            threats.to_sql('threat', conn, if_exists='replace', index=False)
            consensus_threats.to_sql('consensusThreat', conn, if_exists='replace', index=False)
            interoperability_threats.to_sql('interoperabilityThreat', conn, if_exists='replace', index=False)


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
            """SELECT DISTINCT Btype_name 
               FROM btype""")
        # store data in list
        blockchainList = [b for b, in query1]

        publicQuery2 = cursor.execute(
            """SELECT DISTINCT Consensus_name 
               FROM btype,consensus 
                  WHERE consensus.BtypeID == btype.BtypeID
                     AND btype.BtypeID == 1""")
        # store data in list
        consensusPublicList = [c for c, in publicQuery2]

        privateQuery2 = cursor.execute(
            """SELECT DISTINCT consensus_name 
               FROM consensus, btype 
                     WHERE consensus.BtypeID == btype.BtypeID
                     AND btype.BtypeID == 2""")
        # store data in list
        consensusPrivateList = [i for i, in privateQuery2]

        cryptoQuery = cursor.execute(
            """SELECT DISTINCT Bol_cryptography
               FROM cryptography""")
        # store data in list
        cryptoList = [b for b, in cryptoQuery]
        trueOrFalse = [i > 0 for i in cryptoList]

        # Combobox
        b_type = ttk.Combobox(tab1, state="readonly", textvariable=type1, width=20, values=blockchainList)
        b_type.grid(row=0, column=1, padx=20, pady=10)
        # binding the combobox
        b_type.bind("<<ComboboxSelected>>", pick_consensus)

        b_name = ttk.Entry(tab1, text= 'Name')
        b_name.grid(row=1, column=1, padx=20, pady=10)

        consensus = ttk.Combobox(tab1, state="readonly", textvariable=type2, width=20, values=[" "])
        consensus.grid(row=2, column=1, padx=20, pady=10)

        crypt = ttk.Combobox(tab1, state="readonly", textvariable=type3, width=20, values=trueOrFalse)
        crypt.grid(row=3, column=1, padx=20, pady=10)

        # Textbox label
        b_type_label = Label(tab1, text="Blockchain Type")
        b_type_label.grid(row=0, column=0)
        b_name_label = Label(tab1, text="Name")
        b_name_label.grid(row=1, column=0)
        consensus_label = Label(tab1, text="Consensus")
        consensus_label.grid(row=2, column=0)
        crypt_label = Label(tab1, text="Cryptography")
        crypt_label.grid(row=3, column=0)

        # Submit Button
        submit_button = Button(tab1, text="Add blockchain to database", command=submitBlockchain)
        submit_button.grid(row=6, column=0, columnspan=2, pady=10, ipadx=100)

        # Query button
        query_button = Button(tab1, text="Show records", command=showRecords)
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
        cursor.execute("SELECT B_name,ConsensusID from blockchains")
        records = cursor.fetchall()

        for i in records:
            options.append(i[0] +' : ' + i[1])

        blockchain1combo_type = ttk.Combobox(tab2, state="readonly", textvariable=block1, width=30, values=options)
        blockchain1combo_type.grid(row=0, column=1, padx=20, pady=10)
        blockchain1combo_type.bind("<<ComboboxSelected>>", update_combos)
        blockchain2combo_type = ttk.Combobox(tab2, state="readonly", textvariable=block2, width=30, values=options)
        blockchain2combo_type.grid(row=1, column=1, padx=20, pady=10)
        blockchain2combo_type.bind("<<ComboboxSelected>>", update_combos)

        cursor.execute("SELECT * FROM strategy")
        strategy_data = cursor.fetchall()

        # Checkbutton
        htlc = Checkbutton(tab2, text="HTLC", variable=var2, onvalue=strategy_data[1][1], command=varUpdate)
        htlc.grid(row=2, column=1,pady=10)

        notary = Checkbutton(tab2, text="Notary Scheme", variable=var1, onvalue=strategy_data[0][1], command=varUpdate)
        notary.grid(row=2,column=0,pady=10,padx=20)

        relay = Checkbutton(tab2, text="Relay/Sidechain", onvalue=strategy_data[2][1], variable=var3, command=varUpdate)
        relay.grid(row=2,column=3,pady=10)

        # Textbox label
        blockchain1_type = Label(tab2, text="Blockchain A")
        blockchain1_type.grid(row=0, column=0)
        blockchain2_type = Label(tab2, text="Blockchain B")
        blockchain2_type.grid(row=1, column=0)

        # Submit Button
        show_threats_button = Button(tab2, text="Show threats", command=showThreats, state=DISABLED)
        show_threats_button.grid(row=6, column=0, columnspan=4, pady=10, ipadx=100)

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
    root.geometry("2000x1000")
    main()
    root.mainloop()
