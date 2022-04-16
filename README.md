# techzen
Techzen - SLB 


Remember to always create a virtual environment and install the packages in your requirements file

```bash
$ python -m venv venv (you may need to use python3 instead)
$ source venv/bin/activate (or .\venv\Scripts\activate on Windows)
$ pip install -r requirements.txt 
$ python run.py
```

## How to Use Database:

Programs needed: 
1. XAMPP
2. MYSQL

Steps:

### 1. Create the Database Manually
To do this, open up XAMPP as administrator, and start Apache and MYSQL.
Once these are started, open the MYSQL Shell
<img width="497" alt="image" src="https://user-images.githubusercontent.com/53978750/160508813-410a7057-42f5-4939-b1b3-4ecb534706eb.png">

Inside the shell, run these commands:
```bash
mysql -u root
```
This should log you into the mysql server

At this point, run this command:
```bash
CREATE DATABASE techzendb;
```

Once this is done, you can run "SHOW DATABASES;" in which a list should appear, and the database "dbtester" should be in the list.
<img width="200" alt="image" src="https://user-images.githubusercontent.com/53978750/160509059-891113b5-710a-429e-a24a-6d2f50eef3d7.png">

Next, run the command:
```bash
use techzendb;
```
This will set the dbtester database as current working database.

Next you need to create a USER to use with the database, I recommend the name techzen with the password 123. The command is:
```bash
CREATE USER 'techzen'@'localhost' IDENTIFIED BY '123'
```

After this, grant ADMIN privileges.
```bash
GRANT ALL PRIVILEGES ON techzendb.* TO 'techzen'@'localhost';
```

The database should be created and running now.

### 2. Using the Database
In VSCODE, open the terminal, run the commands to enter your virtual environment, and pip install the requirements txt.
```bash
$ python -m venv venv (you may need to use python3 instead)
$ source venv/bin/activate (or .\venv\Scripts\activate on Windows)
$ pip install -r requirements.txt 
```

After this, run the following commands:
```bash
flask db init
flask db migrate
flask db upgrade
```

After you run these commands, run the program using 
```bash
python run.py
```

Navigate to the Sign Up Page, and try to sign up. When complete you should be redirected to the homepage and see this.

<img width="285" alt="image" src="https://user-images.githubusercontent.com/53978750/160509762-8f8d0b2d-dcc3-463e-a075-8d7d6454d4f8.png">

This means the information was added to the database. To check this information for yourself, open up the shell from before, ensure you're logged in still, and
run this command:
``` bash
select * from studentssignup;
```

The information stored should show up.

<img width="332" alt="image" src="https://user-images.githubusercontent.com/53978750/160509868-ad45344e-a3c5-4c9b-bf8e-162076d8b9d4.png">

Congratulations, the database is working, and you don't need to follow this guide anymore.
