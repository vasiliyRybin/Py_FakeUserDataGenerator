Check_UsersTableExists = "SELECT name FROM sqlite_master WHERE name = 'Users'"

CreateUsersTable = "CREATE TABLE Users(FirstName, LastName, PhoneNumber, Email, TaxID, PassNumber, Comment)"

InsertNewUsers = "INSERT INTO Users VALUES(:FirstName, :LastName, :PhoneNumber, :Email, :TaxID, :PassNumber, :Comment)"

GetAllUsers = ""