# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import textwrap
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
                    rowheight=40,
                    fieldbackground="#ededed",
                    highlightthickness=0,
                    bd=0,
                    font=('Arial', 13))
    style.configure("Treeview.Heading", font=('Arial', 13, 'bold'))

    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Arial', 13), rowheight=65, fieldbackground="#ededed", background="#ededed")  # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", font=('Arial', 13, 'bold'))  # Modify the font of the headings
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

    # Change Selected Color
    style.map('Treeview',
              background=[('selected', "#347083")])

    # Creating tabs
    tab_control = ttk.Notebook(root)
    tab1 = Frame(tab_control)
    tab_control.add(tab1, text="Add blockchains")

    tab2 = Frame(tab_control)
    tab_control.add(tab2, text="Discover threats")
    tab_control.pack(expand=1, fill="both", padx=100)

    tab3 = Frame(tab_control)
    tab_control.add(tab3, text="Add threats")
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
            network = network_type.get()

            msg = ''

            try:
                if (btype != '' and bname != '' and cons != '' and crypto != '' and network != ''):
                    cursor.execute(
                        """INSERT INTO blockchains(BtypeID, B_name, ConsensusID,CryptographyID, NetworkTypeID) 
                          VALUES(?,?,?,?,?)""",
                        (btype, bname, cons, crypto, network), )

                    msg = 'Blockchain added to database!'
                    # Clear texboxes
                    b_type.set('')
                    b_name.delete(0, END)
                    consensus.set('')
                    crypt.set('')
                    network_type.set('')
                else:
                    msg = 'Fill inn fields!'
            except Exception as ep:
                messagebox.showerror('error', ep)

            messagebox.showinfo('message', msg)

            # Commit Changes
            conn.commit()
            # Close Connection
            conn.close()

        # Submit interoperable blockchain to database
        def submitThreat():
            threats = pd.read_csv('data/threat.csv', sep=';')
            last_id = threats.tail(1).ThreatID

            name_threat = t_name.get()
            description_threat = t_description.get()
            url_threat = t_url.get()
            cat1 = t_category.get()
            cat2 = t_category2.get()

            msg = ''

            try:
                new_threat = pd.DataFrame(
                    {'ThreatID': last_id + 1, 'Threat_Name': name_threat, 'Description': description_threat,
                     'URL': url_threat})
                df_full = pd.concat([threats, new_threat])
                last_id = df_full.tail(1).ThreatID

                if (cat1 == 'Consensus'):
                    consensusThreat = pd.read_csv('data/consensusThreat.csv', sep=';')
                    if (cat2 == 'Proof-of-Work'):
                        new_consensus_threat = pd.DataFrame({'ThreatID': last_id, 'ConsensusID': 1})
                        consensus_updated = pd.concat([consensusThreat, new_consensus_threat])

                    if (cat2 == 'Proof-of-Stake'):
                        new_consensus_threat = pd.DataFrame({'ThreatID': last_id, 'ConsensusID': 2})
                        consensus_updated = pd.concat([consensusThreat, new_consensus_threat])

                df_full.to_csv('data/threat.csv', sep=';', index=False)
                consensus_updated.to_csv('data/consensusThreat.csv', sep=';', index=False)


                msg = 'Threat created!'
                # Clear texboxes

            except Exception as ep:
                messagebox.showerror('error', ep)

            messagebox.showinfo('message', msg)



        # Show records from database function
        def showRecords():
            conn = sqlite3.connect('blockchain_book.db')
            cursor = conn.cursor()
            query_button['state'] = 'disable'
            submit_button['state'] = 'disable'
            b_type['state'] = 'disable'
            b_name.config(state=DISABLED)
            consensus['state'] = 'disable'
            crypt.config(state=DISABLED)
            network_type.config(state=DISABLED)


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
            tree['columns'] = ("ID", "Name", "Blockchain Type", "Consensus", "Cryptography", "Network")

            # Format Colums
            tree.column("#0", width=0, stretch=NO)
            tree.column("ID", width=50, anchor=CENTER)
            tree.column("Name", width=200, anchor=CENTER)
            tree.column("Blockchain Type", anchor=CENTER, width=150)
            tree.column("Consensus", anchor=CENTER, width=300)
            tree.column("Cryptography", anchor=CENTER, width=100)
            tree.column("Network", anchor=CENTER, width=200)

            # Column Heading
            tree.heading("ID", text="ID", anchor=CENTER)
            tree.heading("Name", text = "Name", anchor=CENTER)
            tree.heading("Blockchain Type", text="Blockchain Type", anchor=CENTER)
            tree.heading("Consensus", text="Consensus", anchor=CENTER)
            tree.heading("Cryptography", text="Cryptography", anchor=CENTER)
            tree.heading("Network", text="Network", anchor=CENTER)

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
                                values=(record[0], record[1], record[3], record[2], record[4], record[5]),
                                tags=('evenrow',))
                else:
                    tree.insert(parent='', index='end', iid=counter, text='',
                                values=(record[0], record[1], record[3], record[2], record[4], record[5]),
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
               submit_button['state'] = 'normal'
               b_type['state'] = 'normal'
               b_name.config(state=NORMAL)
               consensus['state'] = 'normal'
               crypt.config(state=NORMAL)
               network_type.config(state=NORMAL)
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
                    threat_url = htree.item(curItem)['values'][2]  # collect selected row id
                    import webbrowser
                    webbrowser.open(threat_url)


            # Query the database
            cursor.execute(
                """SELECT Threat_Name,Description, Consensus_name, URL, GROUP_CONCAT(Stride_Name) 
                    FROM threat,consensus
                    JOIN consensusThreat 
                    ON consensusThreat.ThreatID = threat.ThreatID 
                    JOIN strideThreat ON threat.threatID = strideThreat.ThreatID
                    JOIN stride ON strideThreat.StrideID = stride.StrideID
                    AND consensusThreat.ConsensusID = consensus.ConsensusID 
                    WHERE Consensus_name = 'Proof-of-Work' 
                    GROUP BY Threat_Name""")

            pow_data = cursor.fetchall()

            # Query the database
            cursor.execute(
                """SELECT Threat_Name,Description, Consensus_name, URL, GROUP_CONCAT(Stride_Name) 
                    FROM threat,consensus
                    JOIN consensusThreat 
                    ON consensusThreat.ThreatID = threat.ThreatID 
                    JOIN strideThreat ON threat.threatID = strideThreat.ThreatID
                    JOIN stride ON strideThreat.StrideID = stride.StrideID
                    AND consensusThreat.ConsensusID = consensus.ConsensusID 
                    WHERE Consensus_name = 'Proof-of-Stake' 
                    GROUP BY Threat_Name""")

            pos_data = cursor.fetchall()

            # Query the database
            cursor.execute(
                """SELECT Threat_Name, Description, Strategy_name, URL, GROUP_CONCAT(Stride_Name)
                    FROM threat,strategy 
                    JOIN interoperabilityThreat 
                    ON interoperabilityThreat.ThreatID = threat.ThreatID
                    JOIN strideThreat ON threat.threatID = strideThreat.ThreatID
                    JOIN stride ON strideThreat.StrideID = stride.StrideID
                    AND interoperabilityThreat.StrategyID = strategy.StrategyID
                    GROUP BY Threat_Name, Strategy_Name""")

            interoperability_data = cursor.fetchall()

            # Query the database
            cursor.execute(
                """SELECT Threat_Name,Description, Btype_name, URL, GROUP_CONCAT(Stride_Name) 
                    FROM threat,btype
                    JOIN networkThreat ON networkThreat.ThreatID = threat.ThreatID 
                    JOIN strideThreat ON threat.threatID = strideThreat.ThreatID
                    JOIN stride ON strideThreat.StrideID = stride.StrideID
                    AND networkThreat.BtypeID = btype.BtypeID 
                    WHERE Btype_name = 'Public Blockchain' 
                    GROUP BY Threat_Name""")

            network_public_data = cursor.fetchall()

            # Query the database
            cursor.execute(
                """SELECT Threat_Name,Description, Btype_name, URL, GROUP_CONCAT(Stride_Name) 
                    FROM threat,btype
                    JOIN networkThreat ON networkThreat.ThreatID = threat.ThreatID 
                    JOIN strideThreat ON threat.threatID = strideThreat.ThreatID
                    JOIN stride ON strideThreat.StrideID = stride.StrideID
                    AND networkThreat.BtypeID = btype.BtypeID 
                    WHERE Btype_name = 'Private Blockchain' 
                    GROUP BY Threat_Name""")

            network_private_data = cursor.fetchall()

            # Query the database
            cursor.execute(
                """SELECT Threat_Name,Description, Network_name, URL, GROUP_CONCAT(Stride_Name) 
                    FROM threat,networkType
                    JOIN networkTypeThreat ON networkTypeThreat.ThreatID = threat.ThreatID 
                    JOIN strideThreat ON threat.threatID = strideThreat.ThreatID
                    JOIN stride ON strideThreat.StrideID = stride.StrideID
                    AND networkTypeThreat.NetworkTypeID = networkType.NetworkTypeID 
                    WHERE Network_name = 'Synchronous' 
                    GROUP BY Threat_Name""")

            synchronous_type_data = cursor.fetchall()

            # Query the database
            cursor.execute(
                """SELECT Threat_Name,Description, Network_name, URL, GROUP_CONCAT(Stride_Name) 
                    FROM threat,networkType
                    JOIN networkTypeThreat ON networkTypeThreat.ThreatID = threat.ThreatID 
                    JOIN strideThreat ON threat.threatID = strideThreat.ThreatID
                    JOIN stride ON strideThreat.StrideID = stride.StrideID
                    AND networkTypeThreat.NetworkTypeID = networkType.NetworkTypeID 
                    WHERE Network_name = 'Partially synchronous' 
                    GROUP BY Threat_Name""")

            psynchronous_type_data = cursor.fetchall()

            # Query the database
            cursor.execute(
                """SELECT Threat_Name,Description, Network_name, URL, GROUP_CONCAT(Stride_Name) 
                    FROM threat,networkType
                    JOIN networkTypeThreat ON networkTypeThreat.ThreatID = threat.ThreatID 
                    JOIN strideThreat ON threat.threatID = strideThreat.ThreatID
                    JOIN stride ON strideThreat.StrideID = stride.StrideID
                    AND networkTypeThreat.NetworkTypeID = networkType.NetworkTypeID 
                    WHERE Network_name = 'Asynchronous' 
                    GROUP BY Threat_Name""")

            asynchronous_type_data = cursor.fetchall()

            # Query the database
            cursor.execute(
                """SELECT Threat_Name,Description, cryptographyThreat.ThreatID, URL, GROUP_CONCAT(Stride_Name)
                    FROM threat,cryptographyThreat
                    JOIN strideThreat ON threat.threatID = strideThreat.ThreatID
                    JOIN stride ON strideThreat.StrideID = stride.StrideID
                    AND cryptographyThreat.ThreatID = threat.ThreatID 
                    GROUP BY Threat_Name""")

            cryptography_data = cursor.fetchall()

            cursor.execute("""SELECT B_name, CryptographyID FROM blockchains""")
            cryptography_boolean = cursor.fetchall()


            # Create frame for treeview
            treeview = Frame(root)
            treeview.pack(expand=True, anchor='c')
            # Label Heading
            Label(treeview,
                            text="Hierarchical Threats Data",
                            fg="black",
                            font="Arial 15 bold").pack()
            Label(treeview,
                            text="Double click to get more information about the threat",
                            fg="black",
                            font="Arial 12 bold",
                            pady= 5).pack()
            # Treeview Scrollbar
            scroll = Scrollbar(treeview)
            scroll.pack(side=RIGHT, fill=Y)

            # Treeview
            htree = ttk.Treeview(treeview, yscrollcommand=scroll.set, height=15,selectmode="browse", style="mystyle.Treeview",columns=('Description','STRIDE',"URL"))
            htree.pack(expand=True)
            htree.bind("<Double-1>", url_collect)
            # Scrollbar
            scroll.config(command=htree.yview)
            # Clear the Treeview
            for record in htree.get_children():
                htree.delete(record)


            htree.heading('#0', text='THREATS CATEGORIZED', anchor='c')
            htree.column('#0', width=350)
            htree.heading('Description', text='DESCRIPTION', anchor='c')
            htree.column('Description', width=400)
            htree.heading('STRIDE', text='STRIDE', anchor='c')
            htree.column('STRIDE', width=400)
            htree.heading('URL', text='URL', anchor='c')
            htree.column('URL', width=200)

            # adding data
            htree.insert('', END, text='Consensus', iid=0, open=False)
            htree.insert('', END, text='Network', iid=1, open=False)
            htree.insert('', END, text='Transaction', iid=2, open=False)
            htree.insert('', END, text='Block Creation', iid=3, open=False)
            htree.insert('', END, text='Human error/Code Exploiting', iid=4, open=False)
            htree.insert('', END, text='If not using cryptography', iid=12, open=False)
            htree.insert('', END, text='Interoperability' + ': '+ strategy, iid=5, open=False)

            # adding children of first node
            htree.insert('', tk.END, text='Proof-of-work', iid=6, open=False)
            htree.insert('', tk.END, text='Proof-of-stake', iid=7, open=False)
            htree.insert('', tk.END, text='Practical Byzantine Fault Tolerance', iid=8, open=False)
            htree.insert('', tk.END, text='Synchronous', iid=9, open=False)
            htree.insert('', tk.END, text='Partially Synchronous', iid=10, open=False)
            htree.insert('', tk.END, text='Asynchronous', iid=11, open=False)
            htree.move(6,0,1)
            htree.move(7,0,2)
            htree.move(8, 0, 3)
            htree.move(9, 1, 1)
            htree.move(10, 1, 2)
            htree.move(11, 1, 3)

            # ID counter to display hierarchical data
            id_counter = 13

            if search(pow_data[1][2], bcombo1) or search(pow_data[1][2], bcombo2):
                # Show records
                for pow in pow_data:
                    if (pow != ''):
                        htree.insert(parent=6, index='end', iid=id_counter, text=(pow[0]),values=(wrap(pow[1]),pow[4],pow[3]))
                        id_counter += 1
                    else:
                        print("Did not found proof-of-work data")
            else:
                print("Input doesnt match proof of work ")

            if search(pos_data[1][2], bcombo1) or search(pos_data[1][2], bcombo2):
                # Show records
                for pos in pos_data:
                    if (pos != ''):
                        htree.insert(parent=7, index='end', iid=id_counter, text=(pos[0]),values=(wrap(pos[1]),pos[4],pos[3]))
                        id_counter += 1
                    else:
                        print("Did not found proof-of-stake data ")
            else:
                print("Input doesnt match proof of stake ")

            # Show interoperability data
            for intData in interoperability_data:
                for j in intData:
                    if (j == strategy):
                        htree.insert(parent=5, index='end', iid=id_counter, text=(intData[0]), values=(wrap(intData[1]), intData[4], intData[3]))
                        id_counter += 1

            # Check synchronous data
            if search(synchronous_type_data[0][2], bcombo1) or search(asynchronous_type_data[0][2], bcombo2):
                # Show records
                for s in synchronous_type_data:
                    if (s != ''):
                        htree.insert(parent=9, index='end', iid=id_counter, text=(s[0]),
                                     values=(wrap(s[1]), s[4], s[3]))
                        id_counter += 1
                    else:
                        print("Did not found synchronous network data ")
            else:
                print("Input doesnt match network type ")


            # Check partially synchronous data
            if search(psynchronous_type_data[0][2], bcombo1) or search(psynchronous_type_data[0][2], bcombo2):
                # Show records
                for s in synchronous_type_data:
                    if (s != ''):
                        htree.insert(parent=10, index='end', iid=id_counter, text=(s[0]),
                                     values=(wrap(s[1]), s[4], s[3]))
                        id_counter += 1
                    else:
                        print("Did not found partially synchronous network data ")
            else:
                print("Input doesnt match network type ")

            # Check asynchronous data
            if search(asynchronous_type_data[0][2], bcombo1) or search(asynchronous_type_data[0][2], bcombo2):
                # Show records
                for s in synchronous_type_data:
                    if (s != ''):
                        htree.insert(parent=11, index='end', iid=id_counter, text=(s[0]),
                                     values=(wrap(s[1]), s[4], s[3]))
                        id_counter += 1
                    else:
                        print("Did not found asynchronous network data ")
            else:
                print("Input doesnt match network type ")

            # Show cryptography data
            #for cryptData in cryptography_boolean:
              #  if (search(cryptData[0],bcombo1) and cryptData[1] == "False"):
               #     for a in cryptography_data:
                #        htree.insert(parent=12, index='end', iid=id_counter, text=(a[0]),
                 #                    values=(wrap(a[1]), a[4], a[3]))
                  #      id_counter += 1

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

        # Function to wrap text
        def wrap(string, lenght=60):
            if (string != None):
                return '\n'.join(textwrap.wrap(string, lenght))
            else:
                pass

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


        def select_using_text(e):
            conn = sqlite3.connect('blockchain_book.db', timeout=50)
            cursor = conn.cursor()
            category_input = category1.get()

            sql = ''
            t_category2.set('')
            if (category_input == 'Consensus'):
                t_category2.config(state='enabled')
                sql = 'SELECT Consensus_name FROM consensus'

            if (category_input == 'Network'):
                t_category2.config(state='enabled')
                sql=''

            if (category_input == 'Cryptography'):
                t_category2.config(state='disabled')
                sql=''

            cursor.execute(sql)
            result = cursor.fetchall()
            t_category2['values'] = result




            # Database connection
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
                        NetworkTypeID text NOT NULL,
                        FOREIGN KEY (BtypeID) REFERENCES btype (BtypeID),
                        FOREIGN KEY (CryptographyID) REFERENCES cryptography (CryptographyID)
                        FOREIGN KEY (ConsensusID) REFERENCES consensus (ConsensusID)
                        FOREIGN KEY (NetworkTypeID) REFERENCES networkType(NetworkTypeID))""")

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
                                       ThreatID INTEGER PRIMARY KEY NOT NULL UNIQUE,
                                       Threat_Name NOT NULL,
                                       URL text)""")

            # Create table for stride
            cursor.execute("""CREATE TABLE IF NOT EXISTS stride(
                                                   StrideID INTEGER PRIMARY KEY,
                                                   Stride_Name text)""")

            # Create table for stride threats
            cursor.execute("""CREATE TABLE IF NOT EXISTS strideThreat(
                                            ThreatID INTEGER,
                                            StrideID INTEGER,
                                            FOREIGN KEY (ThreatID) REFERENCES threat(ThreatID),
                                            FOREIGN KEY (StrideID) REFERENCES stride(ConsensusID))""")

            # Create table for consensus threats
            cursor.execute("""CREATE TABLE IF NOT EXISTS consensusThreat(
                                            ThreatID INTEGER,
                                            ConsensusID INTEGER,
                                            FOREIGN KEY (ThreatID) REFERENCES threat(ThreatID),
                                            FOREIGN KEY (ConsensusID) REFERENCES consensus(ConsensusID))""")

            # Create table for network threats
            cursor.execute("""CREATE TABLE IF NOT EXISTS networkThreat(
                                                       ThreatID INTEGER,
                                                       BtypeID INTEGER, 
                                                       FOREIGN KEY (ThreatID) REFERENCES threat(ThreatID),
                                                       FOREIGN KEY (BtypeID) REFERENCES btype(BtypeID))""")

            # Create table for cryptography threats
            cursor.execute("""CREATE TABLE IF NOT EXISTS cryptographyThreat(
                                                                   ThreatID INTEGER,
                                                                   FOREIGN KEY (ThreatID) REFERENCES threat(ThreatID))""")

            # Create table for application/human error threats
            cursor.execute("""CREATE TABLE IF NOT EXISTS errorThreat(
                                                                   ThreatID INTEGER,
                                                                   FOREIGN KEY (ThreatID) REFERENCES threat(ThreatID))""")


            # Create table for interoperability threats
            cursor.execute("""CREATE TABLE IF NOT EXISTS interoperabilityThreat (
                                                ThreatID INTEGER,
                                                StrategyID INTEGER,
                                                FOREIGN KEY (ThreatID) REFERENCES threat(ThreatID),
                                                FOREIGN KEY (StrategyID) REFERENCES strategy(StrategyID))""")

            # Create table for network type
            cursor.execute("""CREATE TABLE IF NOT EXISTS networkType (
                                                          NetworkTypeID INTEGER PRIMARY KEY,
                                                          Network_name text)""")

            # Create table for networkType threats
            cursor.execute("""CREATE TABLE IF NOT EXISTS networkTypeThreat (
                                                ThreatID INTEGER,
                                                NetworkTypeID INTEGER,
                                                FOREIGN KEY (ThreatID) REFERENCES threat(ThreatID),
                                                FOREIGN KEY (NetworkTypeID) REFERENCES networkType(NetworkTypeID))""")

            cursor.execute('INSERT OR IGNORE INTO cryptography VALUES(NULL,TRUE)')
            cursor.execute('INSERT OR IGNORE INTO cryptography VALUES(NULL,FALSE)')

            # Read data from csv
            blockchain_type = pd.read_csv('data/btype.csv', sep = ';')
            consensus_type = pd.read_csv('data/consensus.csv', sep = ';')
            strategy = pd.read_csv('data/strategy.csv', sep=';')
            threats = pd.read_csv('data/threat.csv', sep=';')
            consensus_threats = pd.read_csv('data/consensusThreat.csv', sep=';')
            interoperability_threats = pd.read_csv('data/interoperabilityThreat.csv', sep =';')
            stride = pd.read_csv('data/stride.csv', sep=';')
            stride_threats = pd.read_csv('data/strideThreat.csv', sep=';')
            network_threats = pd.read_csv('data/networkThreat.csv', sep=';')
            network_type = pd.read_csv('data/networkType.csv', sep=';')
            network_type_threat = pd.read_csv('data/networkTypeThreat.csv', sep=';')
            cryptography_threats = pd.read_csv('data/cryptographyThreat.csv', sep=';')
            error_threats = pd.read_csv('data/errorThreat.csv', sep=';')

            # Insert dato to sqlite
            blockchain_type.to_sql('btype', conn, if_exists='replace', index=False)
            consensus_type.to_sql('consensus', conn, if_exists='replace', index=False)
            strategy.to_sql('strategy', conn, if_exists='replace', index=False)
            threats.to_sql('threat', conn, if_exists='replace', index=False)
            consensus_threats.to_sql('consensusThreat', conn, if_exists='replace', index=False)
            interoperability_threats.to_sql('interoperabilityThreat', conn, if_exists='replace', index=False)
            stride.to_sql('stride', conn, if_exists='replace', index=False)
            stride_threats.to_sql('strideThreat', conn, if_exists='replace', index=False)
            network_threats.to_sql('networkThreat', conn, if_exists='replace', index=False)
            cryptography_threats.to_sql('cryptographyThreat', conn, if_exists='replace', index=False)
            error_threats.to_sql('errorThreat', conn, if_exists='replace', index=False)
            network_type.to_sql('networkType', conn, if_exists='replace', index=False)
            network_type_threat.to_sql('networkTypeThreat', conn, if_exists='replace', index=False)


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
        type4 = StringVar()


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

        networkQuery = cursor.execute(
            """SELECT DISTINCT Network_name
               FROM networkType""")
        networkList = [i for i, in networkQuery]

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

        network_type = ttk.Combobox(tab1, state="readonly", textvariable=type4, width=20, values=networkList)
        network_type.grid(row=4, column=1, padx=20, pady=10)

        # Textbox label
        b_type_label = Label(tab1, text="Blockchain Type")
        b_type_label.grid(row=0, column=0)
        b_name_label = Label(tab1, text="Name")
        b_name_label.grid(row=1, column=0)
        consensus_label = Label(tab1, text="Consensus")
        consensus_label.grid(row=2, column=0)
        crypt_label = Label(tab1, text="Cryptography")
        crypt_label.grid(row=3, column=0)
        network_type_label = Label(tab1, text="Network")
        network_type_label.grid(row=4, column=0)

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
        cursor.execute("SELECT B_name,ConsensusID,NetworkTypeID from blockchains")
        records = cursor.fetchall()
        print(records)

        for i in records:
            options.append(i[0] +' : ' + i[1] + ' : ' + i[2])

        blockchain1combo_type = ttk.Combobox(tab2, state="readonly", textvariable=block1, width=40, values=options)
        blockchain1combo_type.grid(row=0, column=1, padx=20, pady=10)
        blockchain1combo_type.bind("<<ComboboxSelected>>", update_combos)
        blockchain2combo_type = ttk.Combobox(tab2, state="readonly", textvariable=block2, width=40, values=options)
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



        """--------------------- TAB 3 ---------------------"""
        category_options = ['Consensus',
                            'Network',
                            'Cryptography',
                            'Human Error',
                            'Transaction',
                            'Block creation']

        category1 = StringVar()
        category2 = StringVar()

        t_name = ttk.Entry(tab3, text='Name')
        t_name.grid(row=0, column=1, padx=20, pady=10)
        t_description = ttk.Entry(tab3, text='Description')
        t_description.grid(row=1, column=1, padx=20, pady=10)
        t_url = ttk.Entry(tab3, text='Url')
        t_url.grid(row=2, column=1, padx=20, pady=10)

        t_category = ttk.Combobox(tab3, state="readonly", textvariable=category1, width=15, values=category_options)
        t_category.grid(row=3, column=1, padx=10, pady=10)
        t_category.bind("<<ComboboxSelected>>", select_using_text)
        t_category2 = ttk.Combobox(tab3, state="disabled", textvariable=category2, width=15,
                                   values=category_options)
        t_category2.grid(row=4, column=1, padx=10, pady=10)


        # Textbox label
        threat_name = Label(tab3, text="Name")
        threat_name.grid(row=0, column=0)
        threat_description = Label(tab3, text="Description")
        threat_description.grid(row=1, column=0)
        threat_url = Label(tab3, text="URL")
        threat_url.grid(row=2, column=0)
        threat_category = Label(tab3, text="Category")
        threat_category.grid(row=3, column=0)



        # Submit Button
        submit_threats = Button(tab3, text="Submit threat", command=submitThreat)
        submit_threats.grid(row=5, column=0, columnspan=4, pady=10, ipadx=100)




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
