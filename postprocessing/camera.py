import cv2
from label_cards import find_sets

# Replace 2 with whatever camera index you want
cap = cv2.VideoCapture(3)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

snapshot_interval = 1  # Interval in seconds

while True:
    
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break
    
    # Process the frame
    processed_frame = find_sets(frame)

    # Display the frame
    cv2.imshow("sets:", processed_frame)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
