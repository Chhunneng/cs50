PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE birthdays (
    id INTEGER,
    name TEXT,
    month INTEGER,
    day INTEGER,
    PRIMARY KEY(id)
);
INSERT INTO birthdays VALUES(1,'Harry',7,31);
INSERT INTO birthdays VALUES(2,'Ron',3,1);
INSERT INTO birthdays VALUES(3,'Hermione',9,19);
COMMIT;
