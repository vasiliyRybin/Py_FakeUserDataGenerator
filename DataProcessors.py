from Queries import GetDataForSpecifiedColsAndTable, CreateUsersTable, InsertNewUsers, Check_UsersTableExists, GetSomeValueFromSomeTable_ReturnNumberOfRows, MaintainIndex_DropIdx, MaintainIndex_CreateIdx, MaintainDB_VacuumDB
import sqlite3
import csv

def CheckUsersTableAvailability(PathToDBFile):
    Connection = sqlite3.connect(PathToDBFile)
    Cursor = Connection.cursor()   
    
    GetTable = Cursor.execute(Check_UsersTableExists).fetchone()
    IsTableAvailable = False if GetTable is None else True
    
    Connection.close()
    return IsTableAvailable

def GetAllDataFromSomeTable(PathToDBFile, ColumnNames, TableName):
    if TableName.strip().replace(" ", "").startswith('select') == False:        
        PathToDBFile = str(PathToDBFile)
        ColumnNames = str(ColumnNames)
        TableName = str(TableName)
        
        Query = GetDataForSpecifiedColsAndTable.replace("@cols", ColumnNames).replace("@tbl", TableName)
        
        Connection = sqlite3.connect(PathToDBFile)
        Cursor = Connection.cursor()   
    
        UsersData = Cursor.execute(Query).fetchall()
    
        Connection.close()
        return UsersData
    return []

def IsValueExistsInDB(PathToDBFile, TableName, ColumnName, Value):
    PathToDBFile = str(PathToDBFile)
    TableName = str(TableName)
    ColumnName = str(ColumnName)
    Value = str(Value)
    
    Connection = sqlite3.connect(PathToDBFile)
    Cursor = Connection.cursor()   
    
    Query = GetSomeValueFromSomeTable_ReturnNumberOfRows.replace("@col", ColumnName).replace("@tbl", TableName).replace("@value", Value)

    Result = Cursor.execute(Query).fetchone()[0]    
    Connection.close()
    
    Result = int(Result)
    
    if Result > 0:
        return True    
    return False

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
    

def MaintainUsersTable(PathToDBFile, IndexName, TableName, ColumnName):
    PathToDBFile = str(PathToDBFile)
    TableName = str(TableName)
    IndexName = str(IndexName)
    ColumnName = str(ColumnName)
    
    Connection = sqlite3.connect(PathToDBFile)
    Cursor = Connection.cursor()
    
    IsUsersExists = Cursor.execute(Check_UsersTableExists).fetchone()

    if IsUsersExists == None:
        Cursor.execute(CreateUsersTable)    
    
    Query_DropIdx = MaintainIndex_DropIdx.replace("@idx_name", IndexName)    
    Query_CreateIdx = MaintainIndex_CreateIdx.replace("@col_name", ColumnName).replace("@tbl_name", TableName).replace("@idx_name", IndexName)
    Query_VacuumDB = MaintainDB_VacuumDB   
    
    Cursor.execute(Query_DropIdx).fetchone()
    Cursor.execute(Query_CreateIdx).fetchone()
    Cursor.execute(Query_VacuumDB).fetchone()
    
    Connection.commit()
    Connection.close()