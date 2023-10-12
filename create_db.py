import sqlite3

conn = sqlite3.connect('database.db')
print("DB 생성 성공")

conn.execute(
    '''
    CREATE TABLE member (
        num int,
        userid varchar(30) not null,
        pw varchar(30) not null,
        nickname varchar(255) not null,
        primary key(num)
    );

    CREATE TABLE homepage (
        num int,
        userid varchar(30) not null,
        isSecret boolean not null,
        title varchar(255) not null,
        content varchar(255),
        primary key(num)
    );

    CREATE TABLE comment (
        num int,
        userid varchar(30) not null,
        content varchar(255) not null,
        primary key(num)
    );
    '''
)

print("Table 생성 완료")

conn.close()