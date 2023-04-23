# FLASK MVC WEB
Se utilizaron los siguientes módulos
- flask Model View Controller(MVC) architecture
- flask login
- flask migrate
- flask admin
- flask sql database configuration

### Instalar
- to install all the requirements run the command
```
    pip install -r requiremets.txt
```

### Ejecutar aplicación
```
    flask run
```
or 
```
    python app.py
```



### Tiempo excedido de sessión
- En el archivo main.py actulizar el tiempo en minutos 
```python
    app.permanent_session_lifetime=timedelta(minutes=5) #set more minutes or change to hours
```



### Notes
- El usuario por defecto es admin y su contraceña es admin
- En caso de tener problemas con la base de datos ejecutar los comandos.

```
flask db stamp head
ask db migratefl
flask db upgrade
```

