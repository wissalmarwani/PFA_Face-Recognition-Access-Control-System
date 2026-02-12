from flask import Flask, Response, jsonify, render_template
import cv2
import os
from deepface import DeepFace
from datetime import datetime

app = Flask(__name__)

# Dossier contenant les photos des utilisateurs autorisés
DATABASE_DIR = "database"

# Variable globale pour stocker la dernière frame capturée
latest_frame = None
camera = cv2.VideoCapture(0)

# Charger tous les utilisateurs de la base de données
def get_registered_users():
    users = {}
    for filename in os.listdir(DATABASE_DIR):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            name = os.path.splitext(filename)[0]
            users[name] = os.path.join(DATABASE_DIR, filename)
    return users

def generate_frames():
    global latest_frame
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            latest_frame = frame.copy()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    users = get_registered_users()
    return render_template('index.html', user_count=len(users), user_names=list(users.keys()))

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/user_photo/<name>')
def user_photo(name):
    """Serve the registered user's photo for display in the result panel."""
    users = get_registered_users()
    if name in users:
        img_path = users[name]
        with open(img_path, 'rb') as f:
            img_data = f.read()
        ext = os.path.splitext(img_path)[1].lower()
        mime = 'image/png' if ext == '.png' else 'image/jpeg'
        return Response(img_data, mimetype=mime)
    return Response(status=404)

@app.route('/verify')
def verify():
    global latest_frame
    
    if latest_frame is None:
        return jsonify({'verified': False, 'error': 'Pas de frame disponible'})
    
    registered_users = get_registered_users()
    
    for name, img_path in registered_users.items():
        try:
            result = DeepFace.verify(
                latest_frame, 
                img_path, 
                model_name="Facenet", 
                enforce_detection=False
            )
            if result['verified']:
                now = datetime.now()
                return jsonify({
                    'verified': True,
                    'name': name,
                    'photo_url': f'/user_photo/{name}',
                    'employee_id': f'EMP-{abs(hash(name)) % 100000:05d}',
                    'designation': 'Member',
                    'entry_time': now.strftime('%I:%M %p'),
                })
        except Exception as e:
            print(f"Erreur avec {name}: {e}")
    
    return jsonify({'verified': False, 'name': None})

if __name__ == "__main__":
    print("=" * 50)
    print("FACEID — ACCESS CONTROL SYSTEM")
    print("=" * 50)
    print(f"Registered users: {list(get_registered_users().keys())}")
    print("Open http://127.0.0.1:5000 in your browser")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000)