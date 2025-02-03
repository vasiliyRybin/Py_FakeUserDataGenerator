Check_UsersTableExists = "SELECT name FROM sqlite_master WHERE name = 'Users'"

GetSomeValueFromSomeTable_ReturnNumberOfRows = "SELECT COUNT(@col) AS Cnt FROM @tbl WHERE @col = '@value'"

CreateUsersTable = "CREATE TABLE Users(TaxID INTEGER PRIMARY KEY, Comment TEXT, Email TEXT, FirstName TEXT, LastName TEXT, PassNumber TEXT, PhoneNumber TEXT)"

InsertNewUsers = "INSERT INTO Users(TaxID, Comment, Email, FirstName, LastName, PassNumber, PhoneNumber) VALUES(:TaxID, :Comment, :Email, :FirstName, :LastName, :PassNumber, :PhoneNumber)"

GetAllUsers = "SELECT * FROM Users"

GetDataForSpecifiedColsAndTable = "SELECT @cols FROM @tbl"

MaintainIndex_DropIdx = "DROP INDEX IF EXISTS @idx_name;"
MaintainIndex_CreateIdx = "CREATE INDEX @idx_name ON @tbl_name(@col_name);"
MaintainDB_VacuumDB = "VACUUM;"