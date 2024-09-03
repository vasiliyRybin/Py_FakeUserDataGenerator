from Queries import CreateUsersTable, InsertNewUsers, Check_UsersTableExists, GetSomeValueFromSomeTable_ReturnNumberOfRows
import sqlite3
import csv

def CheckUsersTableAvailability(PathToDBFile):
    Connection = sqlite3.connect(PathToDBFile)
    Cursor = Connection.cursor()   
    
    GetTable = Cursor.execute(Check_UsersTableExists).fetchone()
    IsTableAvailable = False if GetTable is None else True
    
    Connection.close()
    return IsTableAvailable

def GetAllDataFromSomeTable(PathToDBFile, Query):
    if Query.strip().lower().startswith("select"):        
        Connection = sqlite3.connect(PathToDBFile)
        Cursor = Connection.cursor()   
    
        UsersData = Cursor.execute(Query).fetchall()
    
        Connection.close()
        return UsersData
    return []

def GetSomeValueFromSomeTable(PathToDBFile, TableName, ColumnName, Value):
    PathToDBFile = str(PathToDBFile)
    TableName = str(TableName)
    ColumnName = str(ColumnName)
    Value = str(Value)
    
    Connection = sqlite3.connect(PathToDBFile)
    Cursor = Connection.cursor()   
    
    Query = GetSomeValueFromSomeTable_ReturnNumberOfRows.replace("@col", ColumnName).replace("@tbl", TableName).replace("@value", Value)

    Result = Cursor.execute(Query).fetchone()[0]
    
    Connection.close()
    return Result

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
    Connection.close()

def WriteInfoToAllOutputSources(Users, Paths):
    WriteInfoToFile(Users, Paths["PathToCSV"])
    WriteInfoToDB(Users, Paths["PathToDB"])