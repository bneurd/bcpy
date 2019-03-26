from bcpy.acquisition import Connection

con = Connection("openBCI", ["O1", "O2", "Oz"])
con.listen()
