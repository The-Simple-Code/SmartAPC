-- D:\SmartAPC\backend\database\ddl\create_tbl_users.sql
IF OBJECT_ID('dbo.tbl_users', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.tbl_users (
        us_no INT IDENTITY(1,1) PRIMARY KEY,
        us_id NVARCHAR(50) NOT NULL UNIQUE,
        us_pass NVARCHAR(256) NOT NULL,
        us_name NVARCHAR(100) NOT NULL,
        us_email NVARCHAR(100) NULL,
        us_phone NVARCHAR(20) NULL,
        us_role NVARCHAR(20) NOT NULL DEFAULT 'member',
        us_created DATETIME NOT NULL DEFAULT GETDATE()
    );
END;
GO
