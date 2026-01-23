import os
import sys

# Add PostgreSQL DLL directory on Windows for psycopg
if os.name == 'nt':
    pg_bin = r"C:\Program Files\PostgreSQL\18\bin"
    if os.path.exists(pg_bin):
        os.add_dll_directory(pg_bin)
        os.environ["PATH"] = pg_bin + os.pathsep + os.environ["PATH"]



def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cwpai.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
