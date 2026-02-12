import cv2
import os
from deepface import DeepFace

# Dossier contenant les photos des utilisateurs autorisés
DATABASE_DIR = "database"

# Charger tous les utilisateurs de la base de données
def get_registered_users():
    users = {}
    for filename in os.listdir(DATABASE_DIR):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            name = os.path.splitext(filename)[0]  # Extrait le nom sans extension
            users[name] = os.path.join(DATABASE_DIR, filename)
    return users

cap = cv2.VideoCapture(0)
registered_users = get_registered_users()

print("=" * 50)
print("SYSTÈME DE CONTRÔLE D'ACCÈS FACIAL")
print("=" * 50)
print(f"Utilisateurs enregistrés: {list(registered_users.keys())}")
print("\nCommandes:")
print("  [v] - Vérifier l'accès")
print("  [q] - Quitter")
print("=" * 50)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur: Impossible de lire la caméra")
        break

    key = cv2.waitKey(1) & 0xFF

    if key == ord('v'):
        print("\n🔍 Analyse en cours...")
        recognized = False
        
        for name, img_path in registered_users.items():
            try:
                result = DeepFace.verify(
                    frame, 
                    img_path, 
                    model_name="Facenet", 
                    enforce_detection=False
                )
                if result['verified']:
                    print(f"✅ ACCÈS AUTORISÉ - Bienvenue {name.upper()} !")
                    recognized = True
                    break
            except Exception as e:
                print(f"Erreur lors de la vérification avec {name}: {e}")
        
        if not recognized:
            print("❌ ACCÈS REFUSÉ - Utilisateur non reconnu")

    elif key == ord('q'):
        print("\n👋 Fermeture du système...")
        break

    cv2.imshow("Controle d'Acces Facial", frame)

cap.release()
cv2.destroyAllWindows()