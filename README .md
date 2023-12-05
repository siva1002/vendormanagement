
# Vendor management

System with Performance Metrics


## Tech Stack

**Server:** Django,REST

**Database:** postgres

**Api documentation:** drf-yasg


## Installation

clone the vendor management to localmachine and run below command 


```bash
  cd vendormanagement
```

create virtualenvironment 

```bash
   py -m venv env
```

Activate the virtualenvironment with below command

```bash
   windows  -> env/scripts/activate
   ubuntu   -> source env/bin/activate
```

Install dependecies

```bash
   pip install -r requirements.txt
````

### Migration

###### Create a new postgres server in pgadmin and change the DB connection and run below command to apply migration

```bash
 py manage.py makemigration

```
above command will generate migration folder in "vendorapp"

```bash
   py manage.py migrate
```

above command will apply the migrations in the database


## Run project




Start the server

```bash
   py manage.py runserver
```
click the generated localhost to view the project



## API Reference


 ### REST apis
 On browser call the below route it will show the routes available in project

 ```http
    <host>/api/
 ````
#### Api documentation


```http
   <host>/apidoc
```
 above route will shows what are the apis available and shows request and response for those apis


