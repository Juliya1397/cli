import sqlite3
import csv


def create_connection():
    try:
        con=sqlite3.connect("users.sqlite3")
        return con
    except Exception as e:
        print(e)






def create_table(conn):
    create_users_table_query="""
    create table IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name CHAR(255) NOT NULL,
    last_name CHAR(255) NOT NULL,
    company_name CHAR(255) NOT NULL,
    address CHAR(255) NOT NULL,
    city CHAR(255) NOT NULL,
    country CHAR(255) NOT NULL,
    state CHAR(255) NOT NULL,
    zip REAL NOT NULL,
    phone1 CHAR(255),
    phone2 CHAR,
    email CHAR(255) NOT NULL,
    web text
    );
    """
    cur=conn.cursor()
    cur.execute(create_users_table_query)
    print("user table was acreated sucessfully.")



# to read sample csv
def read_csv():
    users=[]
    with open("sample_users.csv","r") as f:
        data=csv.reader(f)
        for user in data:
            users.append(tuple(user))
    return users[1:]


def insert_users(con, users):
    user_add_query="""
      insert into users
      (
         first_name,
         last_name,
         company_name,
         address,
         city,
         country,
         state,
         zip,
         phone1,
         phone2,
         email,
         web
         )
         values(?,?,?,?,?,?,?,?,?,?,?,?);
    """
    cur=con.cursor()
    cur.executemany(user_add_query,users)
    con.commit()
    print(f"{len(users)}users were imported  sucessfully.")

Input_string="""
enter the option:
1. create table
2. dump users from csv Into users table
3. add new users into users table 
4. query all users from table 
5. query users by id from table 
6. query specified no. of records from table
7. delete all users
8. delete users by id
9. update user
10. press any key to exit
"""
def select_users(con,no_of_records=0):
    cur=con.cursor()
    if no_of_records:
        users=cur.execute('SELECT * from users LIMIT ?;',(no_of_records,))
    else:
        users=cur.execute("SELECT * from users")
    for user in users:
        print(user)


def select_users_by_id(con,user_id):
    cur=con.cursor()
    users=cur.execute("select * from users where id=?;",(user_id,))
    for user in users:
        print(user)
        
   
def delete_users(con):
    cur=con.cursor()
    cur.execute("DELETE from users;")
    con.commit()
    print("all users were deleted sucessfully")  

def delect_user_by_id(con,user_id):
    cur=con.cursor()
    cur.execute("delete from users where id=?;",(user_id,))
    con.commit()
    print(f'user with id[{user_id}])was sucessfully deleted.')
COLUMNS=(
    "first_name",
    "last_name",
    "company_name",
    "address",
    "city",
    "country",
    "state",
    "zip",
    "phone1",
    "phone2",
    "email",
    "web",
)

def update_user_by_id(con,user_id,column_name,column_value):
    update_query=f"UPDATE users set {column_name}=? where id=?;"
    cur=con.cursor()
    cur.execute(update_query,(column_value,user_id))
    con.commit()
    print(
        f"[{column_name}] was updated with value [{column_value}]of user with id[{user_id}]"
    )
        
def main():
    con=create_connection()
    user_input=input(Input_string)
    if user_input=='1':
        create_table(con)
    elif user_input=="2":
        users=read_csv()
        insert_users(con,users)
    
    elif user_input=="3":
        user_data=[]
        for column in COLUMNS:
            column_value=input(f'enter{column}:')
            user_data.append(column_value)
        insert_users(con,[tuple(user_data)])
    elif user_input=="4":
        select_users(con)
    elif user_input=="5":
        user_id=input("enter the id of user:")
        select_users_by_id(con,user_id)
    elif user_input=="6":
        no_of_records=input("how many users you want to fetch?")
        if no_of_records.isnumeric():
            select_users(con,int(no_of_records))
    elif user_input=="7":
        delete_users(con)
    elif user_input=="8":
        user_id=input("enter the id of user:")
        delect_user_by_id(con,user_id)
    elif user_input=="9":
        user_id=input("enter id of user:")
        if user_id.isnumeric():
            column_name=input(
                f"enter the column you want to edit. please make sure column is with in {COLUMNS}:"
            )
            if column_name in COLUMNS:
                column_value=input(f"enter the value of {column_name}:")
                update_user_by_id(con,user_id,column_name,column_value) 
                
    else:
        exit()
main()

