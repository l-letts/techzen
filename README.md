# techzen
Techzen - SLB 


Remember to always create a virtual environment and install the packages in your requirements file

```bash
$ python -m venv venv (you may need to use python3 instead)
$ source venv/bin/activate (or .\venv\Scripts\activate on Windows)
$ pip install -r requirements.txt 
$ python run.py
```

## How to Import Database:
Ensure XAMPP is open as ADMIN, start Apache, MySQL

ensure you run pip install -r requirements.txt

```
Run "python createdb.py"

Open Python terminal by:
open python terminal (type "python" or "winpy")

In Python terminal run:
    from models import db
    db.create_all()
```

check PHPMyAdmin to see the tables if created.
