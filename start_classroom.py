"""Launch classroom server locally. Run: python start_classroom.py"""
import os
from server.app import connect, DB, Handler, ThreadingHTTPServer
if __name__ == '__main__':
    DB.parent.mkdir(parents=True, exist_ok=True)
    with connect(): pass
    port=int(os.environ.get('PORT','8502'))
    print(f'Open http://localhost:{port}/classroom for classroom mode')
    print(f'Open http://localhost:{port}/ for individual game')
    ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
