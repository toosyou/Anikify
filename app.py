import os
import base64
import uuid

from faceswap import faceswap
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    image = request.files['fileToUpload']

    target_filename = '{}.jpg'.format(uuid.uuid4().hex)
    target_path = os.path.join('.', 'images', target_filename)
    image = image.read()

    with open(target_path, 'wb') as f:
        f.write(image)

    print('swaping faces!')
    try:
        output_image = faceswap(target_path, './images/handsome.jpg')
        encoded_string = base64.b64encode(output_image)

        with open('./images/{}_output.jpg'.format(target_filename.split('.')[0]), 'wb') as f:
            f.write(output_image)
    except:
        encoded_string = base64.b64encode(image)

    return '''
    <!DOCTYPE html>
    <html>
    <style>
        body, html {{
            height: 100%;
            margin: 0;
            padding: 0;
            background-color: #1E1E1E;
        }}
        img {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin: auto;
        }}
        .container {{
            display: flex;
            height: 100%;
        }}
    </style>

    <head>
        <title>金城武！</title>
    </head>
    <body>
        <div class='container'>
            <img src="data:image/jpeg;charset=utf-8;base64, {}">
        </div>
    </body>
    </html>
    '''.format(encoded_string.decode('utf-8'))

    return 'ok'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port='8080')
