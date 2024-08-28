from Queries import CreateUsersTable, InsertNewUsers, Check_UsersTableExists
import sqlite3
import csv

def WriteInfoToFile(Users, PathToCSVFile):    
    with open(PathToCSVFile, mode="a+", encoding="utf-8-sig", newline='') as CsvFile:
        FieldNames = ["First name", "Last name", "Phone number", "Email", "Tax payer number", "Pass number", "Comment"]
        writer = csv.DictWriter(CsvFile, fieldnames=FieldNames, extrasaction="ignore", delimiter=";")
        writer.writeheader()

        for user in Users:
            writer.writerow(
                             {
                                 "First name": user.FirstName, 
                                 "Last name" : user.LastName,
                                 "Phone number" : user.PhoneNumber,
                                 "Email" : user.Email,
                                 "Tax payer number" : user.TaxesPayerNumber,
                                 "Pass number" : user.PassNumber,
                                 "Comment" : user.Comment
                             }
                           )
def WriteInfoToDB(Users, PathToDBFile):
    Connection = sqlite3.connect(PathToDBFile)
    Cursor = Connection.cursor()
    
    IsUsersExists = Cursor.execute(Check_UsersTableExists).fetchone()

    if IsUsersExists == None:
        Cursor.execute(CreateUsersTable)
    
    users_data = [
                    {
                        'FirstName': user.FirstName,
                        'LastName': user.LastName,
                        'PhoneNumber': user.PhoneNumber.replace('\'', ''),
                        'Email': user.Email,
                        'TaxID': user.TaxesPayerNumber,
                        'PassNumber': user.PassNumber,
                        'Comment': user.Comment
                    } 
                    for user in Users]
        
    Cursor.executemany(InsertNewUsers, users_data)
    Connection.commit()

def WriteInfoToAllOutputSources(Users, Paths):
    WriteInfoToFile(Users, Paths["PathToCSV"])
    WriteInfoToDB(Users, Paths["PathToDB"])