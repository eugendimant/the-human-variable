"""Start the game, live classroom and tutor on this computer.
Run: python start_classroom.py      then open http://localhost:8502/ (game) or /classroom (instructor)."""
from server.app import serve
if __name__ == '__main__':
    serve()
