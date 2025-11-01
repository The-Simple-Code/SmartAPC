-- D:\SmartAPC\backend\database\ddl\create_authcode.sql
IF OBJECT_ID('dbo.AuthCode', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.AuthCode (
        ac_id INT IDENTITY(1,1) PRIMARY KEY,
        channel NVARCHAR(10) NOT NULL,     -- 'email' | 'sms'
        target  NVARCHAR(100) NOT NULL,    -- 이메일 또는 숫자만의 전화
        code    NVARCHAR(10) NOT NULL,     -- 6자리
        expires_at DATETIME NOT NULL,
        used    BIT NOT NULL DEFAULT 0,
        used_at DATETIME NULL,
        created_at DATETIME NOT NULL DEFAULT GETUTCDATE()
    );
    CREATE INDEX IX_AuthCode_Target ON dbo.AuthCode(target);
END;
GO
