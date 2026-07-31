
# FastApi Example Project

> [查看中文入门说明 / Read the Chinese guide](README.zh-CN.md)

FastApi Example Project Structure

## Project Structure

```bash
project_name/
├── app/ 
│   ├── api/
│   │   ├── controllers/
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   └── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── ...
│   ├── services/
│   │   ├── __init__.py
│   │   └── ...
│   ├── utils/
│   │   ├── __init__.py
│   │   └── ...
│   ├── database/
│   │   ├── __init__.py
│   │   └── ...
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── ...
│   ├── routes/
│   │   ├── __init__.py
│   │   └── ...
│   ├── main.py
│   └── settings.py
├── tests/
│   ├── test_<module>.py
│   └── ...
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```


- **app**: The main application package.
-    **api**: Contains API-related code and endpoints.
-    **controllers**: Individual API Controllers (endpoints) are defined here.
-    **models**: Contains data models or Pydantic models.
-    **services**: Houses business logic or service layer components.
-    **utils**: Contains utility functions or helper modules.
-    **database**: Handles database-related code, such as database connection and schemas.
-    **dependencies**: Contains dependencies or dependency providers.
-    **main.py**: Entry point of the application.
-    **routes/api.py**: Base Routes Configuration.
-    **settings.py**: Configuration settings for the application.
-    **tests**: Contains test modules and test cases.
-    **.env**: Environment variables for the project.
-    **.gitignore**: Specifies the files and directories to be ignored by Git.
-    **requirements.txt**: List of project dependencies.


## Run Locally

Clone the project

```bash
  git clone https://github.com/vahidrezazadeh/fastapi-example
```

Go to the project directory

```bash
  cd fastapi-example
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start the server

```bash
  uvicorn main:app --reload
```

or This Command in Windows

```bash
  python -m uvicorn main:app --reload
```


## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://vahidrezazadeh.github.io/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vahidrezazadeh/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/vahdirezazadeh5)

