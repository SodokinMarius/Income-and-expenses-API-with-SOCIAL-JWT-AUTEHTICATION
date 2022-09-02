# API dont le but est de créer restaurants, les editer, et renvoyer
# les restaurants  se situant dans un rayon de 3km.
# l'API met en jeu aussi la securité via les permissions et l'authentification (à double clé) 

## How to run this project
### 1. Clone the project
 ```
 git clone git remote add origin https://https://github.com/SodokinMarius/Income-and-expenses-API-with-SOCIAL-JWT-AUTEHTICATION.git

 
 cd RestaurantAPI-USING-JWT-AUTHENTICATION
 ```

### 2. Creating the  virtuel environnement 
```
 python3 -m venv env

 source env/bin/activate
```

### 3. Installing the project requirements /dependencies
```
pip install -r requirements.txt
```

# 4. The project is built with docker. Then make sure that docker is 
# installed on your computer

```
consult the doc here
https://docs.docker.com/get-started/
```

### 5. Creating a virtual container (Make sure that docker service is running on your computer)
```
sudo docker-compose up -d --build
```

### 6. Migrations executions 
```
sudo docker-compose exec restaurant python3 manage.py makemigrations
sudo docker-compose exec restaurant python3 manage.py migrate
```


### 7. Running the project (with docker)
```
sudo docker-compose exec restaurant python3 manage.py runserver or
sudo docker-compose exec restaurant python manage.py runserver

```

