import cv2
import mediapipe as mp
import sys

# 1. Inicializar MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# 2. Intentar abrir la cámara con V4L2 (compatible con libcamerify)
print("Iniciando cámara IMX708...")
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    sys.exit()

# Forzar una resolución estándar para evitar el error de 'reshape'
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Cámara configurada. Iniciando procesamiento...")
print("Presiona ESC para salir.")

while cap.isOpened():
    success, frame = cap.read()
   
    # Si el frame es nulo o falla la lectura, saltar al siguiente ciclo
    if not success or frame is None:
        continue

    # Convertir a RGB para MediaPipe
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    # Dibujar los resultados en el frame original (BGR)
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    # Mostrar ventana
    cv2.imshow('MediaPipe Pose IMX708', frame)
   
    # Salir con ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Limpieza final
cap.release()
cv2.destroyAllWindows()
