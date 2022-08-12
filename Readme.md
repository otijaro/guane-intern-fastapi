Bienvenido al sistema de usuarios de caninos
El sistema está integrado con una base de datos Postgres Sql.
El usuario es postgres
La base de datos se le nombró: fundacion_vet
A partir del Docker-compose puede iniciar la aplicación con el comando
docker-compose build
docker-compose up -d

Para finalizar el servicio, se deben enviar el comando:
docker-compose down

Desde el servicio Web se deben ingresar usuarios para poder luego ingresar los registros de la clase Dog, y adicionalmente, es importante hacer un registro de usuario (sign in) para poder hacer el registro de un nuevo "Dog".
