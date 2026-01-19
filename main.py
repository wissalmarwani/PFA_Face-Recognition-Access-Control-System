import cv2
from deepface import DeepFace

# Chemin de ta photo
reference_img_path = "database/user.jpg"

cap = cv2.VideoCapture(0)

print("Système prêt ! Cliquez sur la fenêtre vidéo et appuyez sur 'v' pour tester.")

while True:
    ret, frame = cap.read()
    if not ret: break

    # Écoute du clavier (indispensable pour que la fenêtre reste ouverte)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('v'):
        print("Analyse...")
        try:
            # On utilise Facenet comme tu l'as demandé
            result = DeepFace.verify(frame, reference_img_path, model_name="Facenet", enforce_detection=False)
            status = "ACCES AUTORISE" if result['verified'] else "ACCES REFUSE"
            print(f"--- {status} ---")
        except Exception as e:
            print(f"Erreur: {e}")

    elif key == ord('q'):
        break

    cv2.imshow("Controle d'Acces", frame)

cap.release()
cv2.destroyAllWindows()