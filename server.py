from flask import Flask, send_file, make_response
from zipfile import ZipFile
import io
import os
import hashlib

app = Flask(__name__)
base_dir = os.path.dirname(os.path.abspath(__file__))

@app.route('/script')
def script():
    return send_file(os.path.join(base_dir, 'script.ps1'))

@app.route('/filesZip')
def sendFiles():
    zip_buffer = io.BytesIO()
    files_dir = os.path.join(base_dir, 'files')

    with ZipFile(zip_buffer, 'w') as zip_files:
        for file in os.listdir(files_dir):
            zip_files.write(os.path.join(files_dir, file), arcname=file)

    zip_buffer.seek(0)

    hash_zip = hashlib.sha256(zip_buffer.getvalue()).hexdigest()

    response = make_response(send_file(
        zip_buffer,
        download_name="naxelfiles.zip",
        as_attachment=True
    ))
    response.headers['X-Zip-Hash'] = hash_zip
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True)