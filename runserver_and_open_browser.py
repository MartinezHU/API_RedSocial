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
    try:
        return subprocess.Popen(["python", "manage.py", "runserver"])
    except Exception as e:
        print(f"Error starting Django server: {e}")
        return None


def main():
    container_name = "base_local_postgres"

    if not is_container_running(container_name):
        print(f"Container {container_name} is not running. Starting it now...")
        start_container()
        # Wait a bit longer to ensure the container is fully up
        time.sleep(5)  # Adjust this time as necessary

    server_process = start_django_server()

    if server_process is None:
        print("Django server failed to start. Exiting...")
        return

    try:
        # Wait for the server to fully start
        time.sleep(5)  # Adjust this time as necessary

        # Open the browser at the desired URL
        webbrowser.open("http://localhost:8000/api/schema/swagger/")

        # Wait for the server process to end
        server_process.wait()

    except KeyboardInterrupt:
        # Handle keyboard interruption (Ctrl+C)
        print("Stopping the server...")
        server_process.terminate()
        server_process.wait()
        print("Server stopped successfully")

    except Exception as e:
        print(f"An error occurred: {e}")
        if server_process:
            server_process.terminate()
            server_process.wait()


if __name__ == "__main__":
    main()
