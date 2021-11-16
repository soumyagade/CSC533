from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
import face_recognition

class FaceIdAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, face_id=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and self.check_face_id(face_id=user.userfaceimage.image,
                                                                    uploaded_face_id=face_id):
                return user
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)

    def check_face_id(self, face_id=None, uploaded_face_id=None):
        face1 = face_recognition.load_image_file(face_id)
        face2 = face_recognition.load_image_file(uploaded_face_id)

        print(len(face_recognition.face_encodings(face1)))
        print(len(face_recognition.face_encodings(face2)))

        encoding1 = face_recognition.face_encodings(face1)[0]
        encoding2 = face_recognition.face_encodings(face2)[0]

        return face_recognition.compare_faces([encoding1], encoding2)