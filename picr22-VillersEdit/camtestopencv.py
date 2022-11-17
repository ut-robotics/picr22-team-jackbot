import cv2

cap = cv2.VideoCapture(4)
cap.set(3, 840)
cap.set(4, 320)

try:
    while True:
        ret, frame = cap.read()
        # This call waits until a new coherent set of frames is available on a device
        cv2.imshow('original', frame)
except Exception as e:
    print(e)
    pass

finally:
    cap.release()
    cv2.destroyAllWindows()