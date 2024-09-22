# face_detection/views.py
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from .models import FaceSignIn
import cv2
import numpy as np
import time
def save_reference_photo(username):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Cannot open camera")
        return
    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("test", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            print("Escape hit, closing...")
            break
        elif k == 32:
            try:
                _, buffer = cv2.imencode('.png', frame)
                binary_data = buffer.tobytes()

                FaceSignIn.objects.create(username=username, photo=binary_data)
                print(f"Image for {username} inserted into database")
                cam.release()
                cv2.destroyAllWindows()
                return
            except Exception as e:
                print(e, "error while processing photo")
                continue

    cam.release()
    cv2.destroyAllWindows()

def detect_reference_image(username):
    user = FaceSignIn.objects.get(username=username)
    blob = user.photo
    nparr = np.frombuffer(blob, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is not None:
        print("Image decoded successfully!")
    else:
        print("Failed to decode image.")

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Cannot open camera")
        return

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        result = cv2.matchTemplate(frame, img, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(result >= threshold)
        starttime = time.time()
        for pt in zip(*loc[::-1]):
            cv2.rectangle(frame, pt, (pt[0] + img.shape[1], pt[1] + img.shape[0]), (0, 0, 255), 2)
        endtime = time.time()
        if endtime-starttime > 2:
            break
        cv2.imshow("Reference Image Detection", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            print("Escape hit, closing...")
            break

    cam.release()
    cv2.destroyAllWindows()

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            save_reference_photo(username)
            return render(request,'face_detection/success.html',{'word':'signed'})
    else:
        form = SignUpForm()
    return render(request, 'face_detection/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = FaceSignIn.objects.get(username=username)
                detect_reference_image(username)
                return render(request, 'face_detection/success.html', {'word': 'loggedin'})
            except FaceSignIn.DoesNotExist:
                form.add_error('username', 'User does not exist')
    else:
        form = LoginForm()
    return render(request, 'face_detection/login.html', {'form': form})

def success(request):
    return render(request, 'face_detection/success.html')
