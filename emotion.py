from deepface import DeepFace
from utils.cv_utils import overlay
import cv2

ICONS = ['auto', 'smile', 'happy', 'lol', 'starstruck', 'love', 'shades', 'explode', 'angry', 'yawn', 'surprise', 'sad', 'neutral']
ICON_WIDTH = 49
mode = None

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while cap.isOpened():
        ready, flipped_frame = cap.read()
        if ready:
            try:
                frame = cv2.flip(flipped_frame, 1)
                emotions = DeepFace.analyze(img_path = frame, actions = ['emotion'], enforce_detection=False)
                for i, emotion in enumerate(emotions):
                    if emotion['face_confidence'] > 0.5:
                        dominant_emotion = emotion['dominant_emotion']

                        x = emotion['region']['x']
                        y = emotion['region']['y']
                        w = emotion['region']['w']
                        h = emotion['region']['h']
                        
                        # Define the rectangle
                        start_point = (x, y)
                        end_point = (x + w, y + h)
                        color = (175, 175, 175)  # BGR
                        thickness = 2
                    
                        if mode == None:
                            pass
                        elif mode == 'auto':
                            # Draw the rectangle on the image
                            cv2.rectangle(frame, start_point, end_point, color, thickness)
                            
                            confidence = emotion['emotion'][dominant_emotion]
                            if confidence > 70:
                                # Print dominant emotion
                                print_string(frame, dominant_emotion, x, y, w, h, 1.1, 2)
                                
                                # Print confidence                            
                                print_string(frame, str(int(confidence)) + '%', x, y + 40, w, h, 0.7, 1)

                                # Print emoji
                                overlay(frame, dominant_emotion, 440,  i*200, 200, 200)
                        else:
                          overlay(frame, mode, int(x-(w*0.25)), int(y-(h*0.25)), int(w*1.6), int(h*1.6))  
                
                print_menu(frame)
                cv2.namedWindow('Emotion', cv2.WINDOW_NORMAL)
                cv2.setMouseCallback('Emotion', on_mouse)
                cv2.imshow('Emotion', frame)
            except Exception as e:
                print(e)

            if cv2.waitKey(1) == 27:  # 27 == ESC key
                break

    cap.release()
    cv2.destroyAllWindows()

def print_menu(frame):
    for i, icon in enumerate(ICONS):
        overlay(frame, icon, i*ICON_WIDTH,  480-ICON_WIDTH, ICON_WIDTH, ICON_WIDTH)
    
def on_mouse(event, x, y, flags, param):
    global mode
    if event == cv2.EVENT_LBUTTONDOWN:
        if y > 480-ICON_WIDTH:
            for i, icon in enumerate(ICONS):
                if x < (i+1)*ICON_WIDTH:
                    mode = icon if mode != icon else None
                    return

def print_string(i, s, x, y, w, h, fs, ft):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = fs
    font_color = (175, 175, 175)  # BGR
    font_thickness = ft

    text_size = cv2.getTextSize(s, font, font_scale, font_thickness)[0]
    text_x = x + (w - text_size[0]) // 2 # Center
    text_y = y + h + int(fs*30)  # 30 pixels-ish below the rectangle, adjust for scale

    cv2.putText(i, s, (text_x, text_y), font, font_scale, font_color, font_thickness)

if __name__ == '__main__':
    main()