# Setup

After cloning the repo, in the folder execute these commands:

- Be sure to have python3 installed
   
```
python3 -m venv venv

source venv/bin/activate

pip3 (or pip) install -r requirements.txt
```

## Setting Environment Variables

Set Flask Enviroment Variables in `.flaskenv`

- Example: FLASK_ENV=development

Set Credentials in `.env`

- Example: DB_USER=user

## Connecting to Google Cloud SQL

- Download and install [Google Cloud SDK](https://cloud.google.com/sdk/docs/downloads-interactive)

  - Once installation is completed you must run `gcloud init` in your terminal and login with the google account associated with the Google Cloud Platform

  - For the Cloud Project select **united-triode-233023**

  - For the Google Compute Engine zone select **us-east1-d**

- Download or compile [Cloud SQL Proxy](https://cloud.google.com/sql/docs/mysql/connect-external-app#proxy)

## Running Server

- Create a folder in the root directory named `cloudsql`

- Run the cloud_sql_proxy executable
  - Linux/Mac
    ```
    ./cloud_sql_proxy -dir=/cloudsql &
    ```
  - Windows
    ```
    cloud_sql_proxy.exe -dir=\cloudsql &
    ```
* You can then run the server locally by issuing the command

  ```
  python main.py
  ```
## Documentation

  - Description of all routes and the way they are used can be found at the endpoint __/api/ui__