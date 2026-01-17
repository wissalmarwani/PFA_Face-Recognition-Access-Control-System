import cv2
from deepface import DeepFace

img_reference = "database/user.jpg" 
img_test = "database/user.jpg"      

print("Analyse en cours... (Cela peut prendre un peu de temps la première fois)")

try:
    
    resultat = DeepFace.verify(
        img1_path = img_reference, 
        img2_path = img_test, 
        model_name = "Facenet"
    )

    if resultat['verified'] == True:
        print("✅ ACCÈS AUTORISÉ : C'est bien la même personne !")
        print(f"Distance (Précision) : {resultat['distance']}")
    else:
        print("❌ ACCÈS REFUSÉ : Visages différents.")

except Exception as e:
    print(f"Erreur : {e}")
    print("Vérifie que le nom de ta photo est correct et qu'elle est bien dans le dossier database.")