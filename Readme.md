Bienvenido al sistema de usuarios de caninos
El sistema está integrado con una base de datos Postgres Sql.
El usuario es postgres
El nombre de la base de datos: fundacion_vet
Para iniciar, debes iniciar en la raiz de la aplicación y ejecutar
uvicorn app.main:app --reload

Se sugiere ingresar los datos del usuario primero y luego realizar la autenticación con su nombre y password.
Después de hacer tal autenticación, se pueden ingresar los "dogs"

Celery genera una tarea de demora de 3 segundos para la creación del dog, al ejecutarse muestra en consola tres veces un mensaje con el "dog" creado. 

Desde el servicio Web se deben ingresar usuarios para poder luego ingresar los registros de la clase Dog, y adicionalmente, es importante hacer un registro de usuario (sign in) para poder hacer el registro de un nuevo "Dog".