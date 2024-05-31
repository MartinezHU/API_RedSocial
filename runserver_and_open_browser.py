import subprocess
import time
import webbrowser


def is_container_running(container_name):
    """Check if the Docker container is running."""
    try:
        output = subprocess.check_output(
            ['docker', 'ps', '--filter', f'name={container_name}', '--filter', 'status=running', '--format',
             '{{.Names}}'])
        return container_name in output.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return False


def start_container():
    """Start the Docker container using docker-compose."""
    try:
        subprocess.check_call(['docker-compose', 'up', '-d'])
        print("Docker container started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting Docker container: {e}")


def start_django_server():
    """Start the Django server."""
    return subprocess.Popen(["python", "manage.py", "runserver"])


def main():
    container_name = "base_local_postgres"

    if not is_container_running(container_name):
        print(f"Container {container_name} is not running. Starting it now...")
        start_container()
        # Espera unos segundos para asegurarse de que el contenedor esté completamente arrancado
        time.sleep(2)  # Ajusta este tiempo según sea necesario

    server_process = start_django_server()

    try:
        # Espera a que el servidor se inicie completamente
        time.sleep(3)  # Ajusta este tiempo según sea necesario

        # Abre el navegador en la URL deseada
        webbrowser.open("http://127.0.0.1:8000/api/v1")

        # Espera a que el proceso del servidor termine
        server_process.wait()

    except KeyboardInterrupt:
        # Manejar la interrupción del teclado (Ctrl+C)
        print("Deteniendo el servidor...")
        server_process.terminate()
        server_process.wait()
        print("Servidor detenido correctamente")


if __name__ == "__main__":
    main()
