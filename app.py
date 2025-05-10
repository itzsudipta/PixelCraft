from flask import Flask, render_template, request, jsonify
import cv2
import os
import uuid

app = Flask(__name__, template_folder='.', static_folder='static')
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files.get('image')
    if file:
        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return jsonify({'filename': filename})
    return jsonify({'error': 'No file uploaded'}), 400

@app.route('/edit/<action>/<filename>')
def edit_image(action, filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    img = cv2.imread(filepath)

    if img is None:
        return jsonify({'error': 'Image not found'}), 404

    if action == 'grayscale':
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif action == 'flip-horizontal':
        img = cv2.flip(img, 1)
    elif action == 'flip-vertical':
        img = cv2.flip(img, 0)
    elif action == 'resize':
        img = cv2.resize(img, (200, 200))
    
    new_filename = f"{uuid.uuid4().hex}.png"
    new_path = os.path.join(UPLOAD_FOLDER, new_filename)
    cv2.imwrite(new_path, img)

    return jsonify({'filename': new_filename})

@app.route('/resize/<filename>/<int:width>/<int:height>')
def custom_resize(filename, width, height):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    img = cv2.imread(filepath)

    if img is None:
        return jsonify({'error': 'Image not found'}), 404

    resized = cv2.resize(img, (width, height))
    new_filename = f"{uuid.uuid4().hex}.png"
    new_path = os.path.join(UPLOAD_FOLDER, new_filename)
    cv2.imwrite(new_path, resized)

    return jsonify({'filename': new_filename})

@app.route('/crop/<filename>/<int:x>/<int:y>/<int:width>/<int:height>')
def crop_image(filename, x, y, width, height):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    img = cv2.imread(filepath)

    if img is None:
        return jsonify({'error': 'Image not found'}), 404

    # Ensure crop dimensions are within the image bounds
    height_img, width_img = img.shape[:2]
    x_end = min(x + width, width_img)
    y_end = min(y + height, height_img)

    if x < 0 or y < 0 or x >= width_img or y >= height_img:
        return jsonify({'error': 'Invalid crop dimensions'}), 400

    cropped = img[y:y_end, x:x_end]
    new_filename = f"{uuid.uuid4().hex}.png"
    new_path = os.path.join(UPLOAD_FOLDER, new_filename)
    cv2.imwrite(new_path, cropped)

    return jsonify({'filename': new_filename})

# Export the app for Vercel
app = app