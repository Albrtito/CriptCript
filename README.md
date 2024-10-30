# CriptCript
A simple webapp that implements cibersecurity mechanisms so that it complies with the authentication, integrity and confdentiality objectives of the CIA triad.

+ Para más información en como y que mecanismos de seguridad se han implementado
  ver la memoria `memory/main.pdf` || `compile memory/main.tex`

This proyect is a fork of the backend builderplate provided by the repo:
+ https://github.com/jmartinpizarro/backend-builderplate.

The builderplate gives a basic local deployment structure using docker with two containers, one for the database (MariaDB) and another one for the backend (Flask). We have **added a third container runnign a python webserver in `p 8000` for the frontend**.

## How to develop and test this proyect / Como hacer desarrollo y testing del proyecto:
### Docker compose/ Despliege del docker:
La installación e inicialización del proyecto seguirá los siguientes pasos:

1. Clonar el repositiorio y entrar a la carpeta: 
```bash
git clone https://github.com/Albrtito/CriptCript.git

cd CriptCript
```

2. Construir desde cero el entorno de docker:

+ Si es la primera vez que se está inicializando el proyecto
+ Si se han realizado cambios en el código del backend
+ Si también se han realizado cambios en la estructura de la base de datos habrá
  que utilizar `rm -r db_data/` **antes de ejecutar el docker-compose**
```bash
docker-compose build && docker-compose up
```
+ Si no es la primera vez que se está inicializando el proyecto
```bash
docker-compose up
```

3. Comprobar que funciona entrando al puerto localhost:8000 en cualquier
   navegador.
```
https://localhost:8000
```
Debería de verse la página de inicio de la aplicación. 

También se puede usar curl
```bash
curl http://localhost:8000
```

### Desarrollo, debugging y testeo
Para desarrollar y comprobar el correcto uso de la aplicación se pueden usar
los siguientes métodos:

#### Interacción con la base de datos
1. Entrar al contenedor de la base de datos
```bash
sudo docker exec -it criptcript_db bash
```
2. Ejecutar en la nueva terminal 
```bash
mariadb -u admin@localhost.com -p
```
+ Donde la contraseña es: `1234`

3. una vez dentro de la base datos entrar a `backend_db`
```bash
use backend_db;
```

+ Desde aquí se puede acceder a todas las tablas que utiliza la app y su
estructura
```sql
SHOW TABLES;
DESCRIBE <table_name>;
```
+ Donde <table_name> es un nombre de alguna de las tablas mostradas.

> [!EXAMPLE] Por ejemplo:
>  + Se puede utilizar para comprobar que los usuarios se están guardando
>    correctamente en forma de hash:
>       ```sql 
>       SELECT * FROM users;
>       ```
>   + Se pude utilizar par comprobar que los desafíos se están guardando
>     encriptados y con una clave de autenticación.
>   ```sql
>       SELECT * FROM private_challenges;
>       SELECT * FROM public_challenges;
>   ```
>   

#### Interacción con los logs del docker:
La terminal en la que se ha inicializado el docker mostrara el conjunto de todos
los logs generaos por la aplicación, aquí se **pueden comprobar aspectos como que los desafíos
estén siendo correctamente cifrados**. Cualqueir excepción o error generado
aparecerá en este log.

+ Es aquí donde se ha implementado el log para saber que un mensaje se ha cifrado/descifrado

> [!danger] 
> Se genera una excepción cuando el número de desafíos públicos o privados es
> igual a 0. Esta excepción no influye al funcionamiento de la app.

### Proyect structure / Estructura del proyecto
El desarrollo de este proyecto se ha dividdo mayoritariamente en dos partes,
frontend y backend, cada una de estas partes tiene su propia carpeta global en
el repositorio. 

**Frontend**
La carpeta del frontend contiene todo lo relacionado con la visualización de la web, `html`, `css`, `javascript`. Los estilos (css) y scripts(Javascripts) tienen sus propias subcarpetas, el html se encuentra directamente bajo la carpeta frontend debido a que son pocos archivos y es ahí donde se inicializa el servidor del frontend. 

Actualmente no hay protección frente a un ataque de búsqueda de urls, cualquiera puede acceder a todo el contenido de la carpeta frontend desde la web.

**Backend**
La carpeta del backend contiene los archivos de `app.py` y `requirementes.txt` que recogen la creación de la api e instalación de los requisitos necesarios en el servidor de backend. El resto del código se encuentra bajo src. Aquí diferenciamos entre tres carpetas:
+ **mariaDB** -> Métodos relacionados con la conexión a la DB

+ **utils** -> Clases ocupadas de la autenticación, encriptación, generación de claves y hasheado, además del manager ocupado de utilizar todas esas clases para cifrar/descifrar y autenticar mensajes `MessageManager.py`.

> [!TODO] 
>Bajo la carpeta clásicos se encuentran clases de cifrado clásico,
> estas no se han implementado en la app para la primera entrega.

+ **unittest** -> Clases con test para la verificación del código.
> [!TODO]
> La primera entrega no ha implementado más que algunos tests para el HMAC.

Finalmente, bajo la carpeta src se encuentran también los archivos`<name>_routes.py` que contienen el routeado para la comunicación de la aplicación con el frontend


## TODO/IDEA LIST: (Pre final handoff)
Lista de tareas e ideas que se podrían implementar o faltan por implementar para la última entrega.
