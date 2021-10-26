import face_recognition


def check_face(image1, image2):
    """
    This function takes 2 file paths of images of faces as input, and returns true if they are the same person.
    If an image contains multiple faces, only the most prominent face will be considered.

    :param image1: File path of the first image
    :param image2: File path of the second image
    :return: True if faces match, false otherwise
    """

    face1 = face_recognition.load_image_file(image1)
    face2 = face_recognition.load_image_file(image2)

    encoding1 = face_recognition.face_encodings(face1)[0]
    encoding2 = face_recognition.face_encodings(face2)[0]

    return face_recognition.compare_faces([encoding1], encoding2)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    hugh_face = "data/Hugh.jpg"
    other_hugh = "data/Hugh2.jpg"
    stranger_face = "data/Stranger.jpg"

    print(check_face(hugh_face, other_hugh))
    print(check_face(hugh_face, stranger_face))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
