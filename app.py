from flask import Flask, render_template, request, jsonify
import cv2
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    filename = f"{uuid.uuid4().hex}.png"
    path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(path)
    return jsonify({'filename': filename})

@app.route('/grayscale/<filename>')
def grayscale(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path, gray)
    return jsonify({'filename': filename})

@app.route('/flip-horizontal/<filename>')
def flip_horizontal(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    img = cv2.imread(path)
    flipped = cv2.flip(img, 1)
    cv2.imwrite(path, flipped)
    return jsonify({'filename': filename})

@app.route('/flip-vertical/<filename>')
def flip_vertical(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    img = cv2.imread(path)
    flipped = cv2.flip(img, 0)
    cv2.imwrite(path, flipped)
    return jsonify({'filename': filename})

@app.route('/resize/<filename>')
def resize_default(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    img = cv2.imread(path)
    resized = cv2.resize(img, (200, 200))
    cv2.imwrite(path, resized)
    return jsonify({'filename': filename})

@app.route('/resize/<filename>/<int:width>/<int:height>')
def resize_custom(filename, width, height):
    path = os.path.join(UPLOAD_FOLDER, filename)
    img = cv2.imread(path)
    resized = cv2.resize(img, (width, height))
    cv2.imwrite(path, resized)
    return jsonify({'filename': filename})

if __name__ == '__main__':
    app.run(debug=True)
