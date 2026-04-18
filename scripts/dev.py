import subprocess
import sys
import signal
import os

processes = []

def start_process(name, commmand, cwd=None, env=None):
    print(f"Starting {name}...")
    process = subprocess.Popen(
        commmand,
        cwd=cwd,
        env=env,
        stdout=sys.stdout,
        stderr=sys.stderr,
        shell=True,
        text=True
    )
    processes.append((name, process))
    print(f"{name} started with PID {process.pid}")

def shutdown_processes():
    print("Shutting down processes...")
    for name, process in processes:
        print(f"Terminating {name} (PID {process.pid})...")
        process.terminate()
        try:
            process.wait(timeout=5)
            print(f"{name} terminated gracefully.")
        except subprocess.TimeoutExpired:
            print(f"{name} did not terminate in time. Killing it...")
            process.kill()
            print(f"{name} killed.")
    print("All processes have been shut down.")
    sys.exit(0)

def main():
    # Handle CTRL+C gracefully
    signal.signal(signal.SIGINT, lambda sig, frame: shutdown_processes())
    signal.signal(signal.SIGTERM, lambda sig, frame: shutdown_processes())

    print("Starting development environment...\n")

    # Start the Flask backend
    flask_env = os.environ.copy()
    flask_env['FLASK_APP'] = 'flaskr'
    flask_env['FLASK_ENV'] = 'development'
    start_process("Flask Backend", "flask run", env=flask_env)

    # Start the React frontend
    start_process("React Frontend", "npm start", cwd="frontend")

    # Wait for all processes to finish
    try:
        for _, process in processes:
            process.wait()
    except KeyboardInterrupt:
        shutdown_processes()

if __name__ == "__main__":
    main()