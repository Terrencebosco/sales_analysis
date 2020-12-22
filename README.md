# sales_analysis

started work with sales data.

converted sql fiel to sqlite for ease of access with python. (better way?). installed and played with mysql via command line.

---

mysql locally: [helped](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04), [doc](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)

command line -> sudo mysql

to access local sql dump file:

mysql > CREATE DATABASE >name<

mysql > use >name<

mysql > source /filepath/>name<.sql

---

to convert sql to sqlite3 for ease of use: [converter](https://github.com/Terrencebosco/mysql2sqlite)


cd -> utilites/mysql2sqlite

terminal -> ./mysql2sqlite dump_mysql.sql | sqlite3 mysqlite3.db
