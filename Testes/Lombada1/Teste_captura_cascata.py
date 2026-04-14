import cv2

webcamera = cv2.VideoCapture(0)
classificaddorVideoFace = cv2.CascadeClassifier("Lombada-eletronica\cars.xml")


while True:
     camera, frame = webcamera.read()

#     cinza  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Converte o frame para escala de cinza
#     detecta  = classificaddorVideoFace.detectMultiScale(cinza)
#     cv2.imshow("Image WebCamera", frame)

     if cv2.waitKey(1) == ord('f'):
         break

webcamera.release()
cv2.destroyAllWindows()    