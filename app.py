from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='public', template_folder='public')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

if __name__ == '__main__':
    app.run(debug=True)
