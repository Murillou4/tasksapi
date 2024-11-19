Estrutura do Banco de Dados

Tabela USERS
uid (TEXT PRIMARY KEY)
name (TEXT)
email (TEXT)
password (BLOB)
photo (BLOB)

Tabela TASKS
id (INTEGER PRIMARY KEY)
topic (TEXT)
created_at (TEXT)
completed (BOOLEAN)
uid (TEXT FOREIGN KEY)