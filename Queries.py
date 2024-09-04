Check_UsersTableExists = "SELECT name FROM sqlite_master WHERE name = 'Users'"

GetSomeValueFromSomeTable_ReturnNumberOfRows = "SELECT COUNT(@col) AS Cnt FROM @tbl WHERE @col = '@value'"

CreateUsersTable = "CREATE TABLE Users(FirstName TEXT, LastName TEXT, PhoneNumber TEXT, Email TEXT, TaxID INTEGER, PassNumber TEXT, Comment TEXT)"

InsertNewUsers = "INSERT INTO Users VALUES(:FirstName, :LastName, :PhoneNumber, :Email, :TaxID, :PassNumber, :Comment)"

GetAllUsers = "SELECT * FROM Users"

GetAllTaxAndPassNumbers = "SELECT TaxID, PassNumber FROM Users"

MaintainIndex_DropIdx = "DROP INDEX IF EXISTS @idx_name;"
MaintainIndex_CreateIdx = "CREATE INDEX @idx_name ON @tbl_name(@col_name);"
MaintainDB_VacuumDB = "VACUUM;"