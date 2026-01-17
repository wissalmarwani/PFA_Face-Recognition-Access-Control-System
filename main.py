import cv2
from deepface import DeepFace
import os

reference_img_path = "database/user.jpg"

# Initialisation de la capture vidéo (0 = webcam par défaut)
cap = cv2.VideoCapture(0)

print("Système de contrôle d'accès activé. Appuyez sur 'q' pour quitter.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Pour ne pas ralentir l'ordinateur, on analyse une image toutes les 30 frames
    if cv2.waitKey(1) & 0xFF == ord('v'): # Appuie sur 'v' pour vérifier
        try:
            # Analyse du visage actuel par rapport à la référence
            result = DeepFace.verify(frame, reference_img_path, model_name="Facenet", enforce_detection=False)
            
            if result['verified']:
                color = (0, 255, 0) # Vert
                label = "ACCES AUTORISE"
            else:
                color = (0, 0, 255) # Rouge
                label = "ACCES REFUSE"
                
            print(f"Résultat: {label} (Distance: {round(result['distance'], 2)})")
        except Exception as e:
            print(f"Erreur d'analyse: {e}")

    # 2. Affichage (Optionnel pour l'instant)
    cv2.imshow("Controle d'Acces Facial", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()