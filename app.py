from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    string = '<br>'.join([f'{header[0]}: {header[1]}' for header in request.headers])
    return '<h1>Request headers</h1>' + string


if __name__ == '__main__':
    app.run()
