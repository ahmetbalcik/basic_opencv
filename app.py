import cv2
import numpy as np
from tkinter import filedialog, Tk

MODE_ORIGINAL, MODE_GRAY, MODE_BLUR, MODE_OBJ, MODE_THRESHOLD = 0, 1, 2, 3, 4

class ImageProcessor:
    def __init__(self):
        self.blur_size = 15

    def gray_tone(self, view):
        gray = cv2.cvtColor(view, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    def blur(self, view):
        if self.blur_size % 2 == 0:
            self.blur_size += 1
        return cv2.GaussianBlur(view, (self.blur_size, self.blur_size), 0)
    
    def detect_person(self, view):
        try:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(view, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            result = view.copy()
            for (x,y,w,h) in faces:
                cv2.rectangle(result, (x,y), (x+w, y+h), (255,0,0), 3)
                cv2.putText(result, "Person", (x,y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
            if len(faces) == 0:
                _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > 1000:
                        x,y,w,h = cv2.boundingRect(contour)
                        if h > w * 1.13:
                            cv2.rectangle(result, (x,y), (x+w, y+h), (255,0,0), 3)
                            cv2.putText(result, "Obj", (x,y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
            return result
        except: 
            gray = cv2.cvtColor(view, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            result = view.copy()
            for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > 1000:
                        x,y,w,h = cv2.boundingRect(contour)
                        if h > w * 1.13:
                            cv2.rectangle(result, (x,y), (x+w, y+h), (255,0,0), 3)
                            cv2.putText(result, "Obj", (x,y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
            return result
    
    def thresh_value(self,view):
        gray = cv2.cvtColor(view, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        return cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    
    def run(self, view, mode):
        if mode == MODE_ORIGINAL:
            return view
        elif mode == MODE_GRAY:
            return self.gray_tone(view)
        elif mode == MODE_BLUR:
            return self.blur(view)
        elif mode == MODE_OBJ:
            return self.detect_person(view)
        elif mode == MODE_THRESHOLD:
            return self.thresh_value(view)
        
class CameraManager:
    def __init__(self):
        self.camera = None
        self.active = False

    def open(self, camera_id = 0):
        try:
            self.camera = cv2.VideoCapture(camera_id)
            self.active = self.camera.isOpened()
            return self.active
        except:
            return False
    def close(self):
        if self.camera:
            self.camera.release()
            self.active = False
    def read(self):
        if self.camera and self.active == True:
            return self.camera.read()
        return False, None
    
def upload_image(file_path):
    view = cv2.imread(file_path, cv2.IMREAD_COLOR)
    if view is None:
        print("Image couldn't uploaded")
    return view

def create_btn(view, x,y,w,h, text, active=False):
    color = (255,0,0) if active else (100,100,100)
    cv2.rectangle(view, (x,y), (x+w, y+h), color, -1)
    cv2.rectangle(view, (x,y), (x+w, y+h), (255, 255, 255), 2)
    (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, 0.5, 2)
    text_x = x + (w - text_w) // 2
    text_y = y + (h - text_h) // 2
    cv2.putText(view, text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,100,0), 2)

camera_mode = False
camera = None
active_mode = MODE_ORIGINAL
view_size = None

def mouse_callback(event, x, y, flags, param):
    global camera_mode, camera, active_mode, view_size
    if event == cv2.EVENT_LBUTTONDOWN:
        if 10 <= x <= 160 and 10 <= y <= 50:
            if camera_mode:
                camera.close()
                camera_mode = False
                print("Camera closed!")
            else:
                if camera and camera.open(0):
                    camera_mode = True
                    print("Camera opened!")
                else:
                    print("Camera couldn't be opened")
        if view_size:
            h = view_size[0]
            btn_w = 120
            btn_h = 40
            btn_y = h - btn_h - 10
            if 10 <= x <= 10+ btn_w and btn_y <= y + btn_h:
                active_mode = MODE_ORIGINAL
            elif 140 <= x <= 140+ btn_w and btn_y <= y + btn_h:
                active_mode = MODE_GRAY
            elif 270 <= x <= 270+ btn_w and btn_y <= y + btn_h:
                active_mode = MODE_BLUR
            elif 400 <= x <= 400+ btn_w and btn_y <= y + btn_h:
                active_mode = MODE_OBJ
            elif 530 <= x <= 530+ btn_w and btn_y <= y + btn_h:
                active_mode = MODE_THRESHOLD

def main_gui():
    global camera_mode, camera, active_mode, view_size
    processor = ImageProcessor()
    camera = CameraManager()
    view = None

    mode_processes = ["Original", "Gray", "Blur", "Object", "Threshold"]

    window_name = "Virtual Process"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, mouse_callback)
    print(f"F: File, S:Save, ESC: Cancel, Processes: Press Buttons")

    while True:
        if camera_mode and camera.active:
            ret, frame = camera.read()
            if ret:
                view = frame
            else:
                camera.close()
                camera_mode = False
        if view is not None:
            processed = processor.run(view, active_mode)
            view_size = processed.shape[:2]
            btn_text = "Close Camera" if camera_mode else "Open Camera"
            create_btn(processed, 10, 10, 150, 40, btn_text, camera_mode)

            btn_w = 120
            btn_h = 40
            btn_y = processed.shape[0] - btn_h - 10
            create_btn(processed,  10, btn_y, btn_w, btn_h, "Original", active_mode == MODE_ORIGINAL)
            create_btn(processed, 140, btn_y, btn_w, btn_h, "Gray", active_mode == MODE_GRAY)
            create_btn(processed, 270, btn_y, btn_w, btn_h, "Blur", active_mode == MODE_BLUR)
            create_btn(processed, 400, btn_y, btn_w, btn_h, "Obj", active_mode == MODE_OBJ)
            create_btn(processed, 530, btn_y, btn_w, btn_h, "Threshhold", active_mode == MODE_THRESHOLD)

            cv2.putText(processed, f"Active Mode: {mode_processes[active_mode]}", (10,70), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,50,50), 2)
            cv2.putText(processed, f"F: File, S: Save, ESC: Cancel, Processes: Press Buttons", (10, 100), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,50,50), 2)
        
            cv2.imshow(window_name, processed)
        else:
            empty_screen = np.zeros((480, 640, 3), dtype=np.uint8)
            create_btn(empty_screen, 10, 10, 150, 40, "Open the Camera", False)
            cv2.putText(empty_screen, "F: File, S: Save, ESC: Cancel, Processes: Press Buttons", (150,240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 100,50), 2)
            cv2.imshow(window_name, empty_screen)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            break
        elif key == ord('f') or key == ord('F'):
            root = Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(
                title="Select Image",
                filetypes=[("Images", "*.jpg, *.png, *.jpeg"), ("All of Them", "*.*")]
            )
            root.destroy()
            if file_path:
                if camera_mode:
                    camera.close()
                    camera_mode = False
                view = upload_image(file_path)
        elif key == ord('s') or key == ord("S"):
            if view is not None:
                root = Tk()
                root.withdraw()
                save_path = filedialog.asksaveasfilename(
                    title="Save",
                    defaultextension=".jpg",
                    filetypes=[("JPEG", "*.jpg"),("PNG", "*.png")]
                ) 
                root.destroy()
                if save_path:
                    processed = processor.run(view, active_mode)
                    cv2.imwrite(save_path, processed)
                    print("Successfully saved")

    if camera_mode:
        camera.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main_gui()
    except KeyboardInterrupt:
        print("Programme Was Closed")
    except Exception as e:
        print(f"Hata: {e}")