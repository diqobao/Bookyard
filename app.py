from flask import Flask
from bookyardApp import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
