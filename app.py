from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)


def gen_frames():
    while True:
        success, frame = camera.read()  # read camera frame

        face_cascade = cv2.CascadeClassifier(
            'haarcascade_frontalface_default.xml')
        found = face_cascade.detectMultiScale(frame,
                                              minSize=(20, 20))

        if not success:
            break
        else:
            # There may be more than one
            # sign in the image
            for (x, y, width, height) in found:

                # We draw a green rectangle around
                # every recognized sign
                cv2.rectangle(frame, (x, y),
                              (x + height, y + width),
                              (0, 255, 0), 5)
                frame = cv2.putText(frame, 'Monkey', (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (255, 255, 255), 2, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
