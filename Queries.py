Check_UsersTableExists = "SELECT name FROM sqlite_master WHERE name = 'Users'"

CreateUsersTable = "CREATE TABLE Users(FirstName TEXT, LastName TEXT, PhoneNumber TEXT, Email TEXT, TaxID INTEGER, PassNumber TEXT, Comment TEXT)"

InsertNewUsers = "INSERT INTO Users VALUES(:FirstName, :LastName, :PhoneNumber, :Email, :TaxID, :PassNumber, :Comment)"

GetAllUsers = "SELECT * FROM Users"