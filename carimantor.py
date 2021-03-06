import cv2
import numpy as np


def cal_scale_size(img , height_scale):
    img_height, img_width = img.shape[0:2]
    height_scale_size = float(height_scale) / float(img_height)
    return height_scale_size

def scale(img , scale_size):
    scaled_img = cv2.resize(img , None , fx=scale_size , fy=scale_size , interpolation=cv2.INTER_NEAREST)
    return scaled_img.copy()

def ellipse(img , Axes):
    mask = np.zeros_like(img)
    rows , cols = mask.shape[0:2]
    cv2.ellipse(mask , center=(cols/2 , rows/2) , axes=Axes , angle=0 , startAngle=0,
                endAngle=360 , color=(255,255,255) , thickness=-1)
    return cv2.bitwise_and(img , mask)

def circle(img , Radius , center=-1):
    mask = np.zeros_like(img)
    rows , cols = mask.shape[0:2]
    if( center != -1):
        rows , cols = center
    cv2.circle(mask , center=(cols/2 , rows/2) , radius=Radius , color=(255,255,255) , thickness=-1 )
    return cv2.bitwise_and(img , mask)

def find_face(img , img_gray):
    face_cascade = cv2.CascadeClassifier('haar_cascade_files/haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(image=img_gray, scaleFactor=1.05, minNeighbors=10 , flags=cv2.CASCADE_FIND_BIGGEST_OBJECT)
    (x , y , w , h) = faces[0]
    return img[y:y+h ,  x:x+w]

def find_nose(img , img_gray):
    nose_cascade = cv2.CascadeClassifier('haar_cascade_files/haarcascade_mcs_nose.xml')
    noses = nose_cascade.detectMultiScale(image=img_gray, scaleFactor=1.05, minNeighbors=10)
    (x, y, w, h) = noses[0]
    return (img[y:y + h, x:x + w] , (x,y,w,h))

def find_mouth(img , img_gray):
    mouth_cascade = cv2.CascadeClassifier('haar_cascade_files/haarcascade_mcs_mouth.xml')
    mouthes = mouth_cascade.detectMultiScale(image=img_gray, scaleFactor=1.05, minNeighbors=10)
    (x, y, w, h) = mouthes[0]
    return (img[y:y + h, x:x + w] , (x,y,w,h))

def find_left_eye(img , img_gray):
    left_eye_cascade = cv2.CascadeClassifier('haar_cascade_files/haarcascade_lefteye_2splits.xml')
    left_eyes = left_eye_cascade.detectMultiScale(image=img_gray, scaleFactor=1.05, minNeighbors=10)
    (x, y, w, h) = left_eyes[0]
    return (img[y:y + h, x:x + w] , (x,y,w,h))

def find_right_eye(img , img_gray):
    right_eye_cascade = cv2.CascadeClassifier('haar_cascade_files/haarcascade_righteye_2splits.xml')
    right_eyes = right_eye_cascade.detectMultiScale(image=img_gray, scaleFactor=1.05, minNeighbors=10)
    (x, y, w, h) = right_eyes[0]
    return (img[y:y + h, x:x + w] , (x,y,w,h))

def gray_scale(img):
    try:
        if(img.shape[2] == 4):
            img_gray = cv2.cvtColor(img , cv2.COLOR_BGRA2GRAY)
            return img_gray
        else:
            img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
            return img_gray
    except:
        return img

def equalize_image(img):
    return cv2.equalizeHist(img)

def bilateralFilter(image):
    size = 17
    sigmacolor = 9
    sigmaspace = 7
    return cv2.bilateralFilter(image, size, sigmaColor=sigmacolor, sigmaSpace=sigmaspace)
    #return cv2.bilateralFilter(image, size, 0, 20.0 , 2.0)

def dodgeNaive(image, mask):
    return cv2.divide(image, 255-mask, scale=256)

def filter_image_RGB(image):
    image_3 = cv2.cvtColor(image , cv2.COLOR_RGB2GRAY)
    image_4 = cv2.medianBlur(image_3 , 3)
    image_5 = cv2.adaptiveThreshold(image_4 , 255 , cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY_INV , blockSize=9 , C=2)
    image_5 = cv2.cvtColor(image_5 , cv2.COLOR_GRAY2RGB)
    return image_5

def filter_image_GRAY(image_gray):
    image_4 = cv2.medianBlur(image_gray , 7)
    image_5 = cv2.adaptiveThreshold(image_4 , 255 , cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY , blockSize=9 , C=2)
    return image_5

def remove_pepper_noise(mask):
    rows , cols = mask.shape[0:2]
    y = 2
    while( y < rows-2 ):
        pThis = y
        pUp1 = y - 1
        pUp2 = y - 2
        pDown1 = y + 1
        pDown2 = y + 2
        x = 2
        while( x < cols-2 ):
            if ( mask[pThis , x] == 0):
                allAbove = ( (mask[pUp2 , x - 2]) and (mask[pUp2 , x - 1]) and (mask[pUp2 , x]) and (mask[pUp2 , x+1]) and (mask[pUp2 , x+2]) )
                allLeft = ( (mask[pUp1, x - 2]) and (mask[pThis, x - 2]) and (mask[pDown1, x-2]) )
                allBelow = ( (mask[pDown2, x - 2]) and (mask[pDown2, x - 1]) and (mask[pDown2, x]) and (mask[pDown2, x+1]) and (mask[pDown2, x+2]) )
                allRight = ((mask[pUp1, x + 2]) and (mask[pThis, x + 2]) and (mask[pDown1, x + 2]))
                surroundings = allAbove and allLeft and allBelow and allRight
                if( surroundings == True):
                    mask[pUp1, x - 1] = 255
                    mask[pUp1, x] = 255
                    mask[pUp1, x + 1] = 255
                    mask[pThis, x - 1] = 255
                    mask[pThis, x] = 255
                    mask[pThis, x + 1] = 255
                    mask[pDown1, x - 1] = 255
                    mask[pDown1, x] = 255
                    mask[pDown1, x + 1] = 255
            x += 1
        y += 1
    return mask

def sketch(image):
    image_3 = cv2.cvtColor(image , cv2.COLOR_RGB2GRAY)
    image_4 = cv2.medianBlur(image_3 , 3)
    image_5 = cv2.adaptiveThreshold(image_4 , 255 , cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY , blockSize=9 , C=2)
    image_5 = cv2.cvtColor(image_5 , cv2.COLOR_GRAY2RGB)
    return image_5

def cartoonify(image):
    rows , cols = image.shape[0:2]
    try:
        img_gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
    except:
        img_gray = image
    image_median_blur = cv2.medianBlur(img_gray , 7)

    #mask = np.zeros_like(image)
    mask = np.zeros((rows , cols , 3) , dtype=np.uint8)
    #edges = np.zeros_like(image)
    edges = np.zeros((rows , cols , 3) , dtype=np.uint8)

    edges = cv2.Laplacian(image_median_blur , cv2.CV_8U , 5)
    ret , mask = cv2.threshold(edges , 4 , 255 , cv2.THRESH_BINARY_INV)
    #mask = remove_pepper_noise(mask)
    sketch = cv2.cvtColor(mask , cv2.COLOR_GRAY2BGR)
    repitition = 3
    cpy_image = image.copy()
    for i in range(repitition):
        size = 10
        sigmacolor = 20
        sigmaspace = 20
        tmp = cv2.bilateralFilter(cpy_image, size, sigmaColor=sigmacolor, sigmaSpace=sigmaspace)
        cpy_image = cv2.bilateralFilter(tmp, size, sigmaColor=sigmacolor, sigmaSpace=sigmaspace)
    return cpy_image

def remove_white_pixel(image):
    img_copy = image.copy()
    rows , cols = img_copy.shape[0:2]
    i = 0
    while( i < rows ):
        j = 0
        while( j < cols ):
            first_val = img_copy.item(i , j)
            if( first_val >= 230):
                img_copy[i , j] = 0
            j += 1
        i += 1
    return img_copy

def black_to_RGB(image , color):
    img = image.copy()
    rows , cols = img.shape[0:2]
    i = 0
    while( i < rows ):
        j = 0
        while( j < cols ):
            fir_val = img.item(i , j , 0)
            sec_val = img.item(i , j , 1)
            thr_val = img.item(i , j , 2)
            if (fir_val == 0) and (sec_val == 0) and (thr_val == 0):
                img[i , j] = color
            j += 1
        i += 1
    return img

def black_to_GRAY(image , color):
    img = image.copy()
    rows , cols = img.shape[0:2]
    i = 0
    while( i < rows ):
        j = 0
        while( j < cols ):
            fir_val = img.item(i , j , 0)
            sec_val = img.item(i , j , 1)
            thr_val = img.item(i , j , 2)
            if (fir_val == 0) and (sec_val == 0) and (thr_val == 0):
                img[i , j] = color
            j += 1
        i += 1
    return img

def write_mat_to_file(mat , file_name):
    f = open(file_name , 'w')
    rows, cols = mat.shape[0:2]
    i = 0
    while (i < rows):
        j = 0
        while (j < cols):
            fir_val = mat.item(i, j, 0)
            sec_val = mat.item(i, j, 1)
            thr_val = mat.item(i, j, 2)
            f.write('[' + str(fir_val) + ',' + str(sec_val) + ',' + str(thr_val) + ']')
            f.write('\t')
            j += 1
        f.write('\n')
        i += 1
    return

def whiter(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(img)
    return cl1

def create_caricature_RGB(face , caricature , transition_y , transition_x):
    # Scaled Face information
    face_height, face_width = face.shape[0:2]
    # ROI
    roi = caricature[transition_y:transition_y+face_height ,transition_x:transition_x+face_width]
    # Scaled Face Gray
    scaled_face_gray = cv2.cvtColor(face , cv2.COLOR_RGB2GRAY)
    # Ret and Mask
    ret , mask = cv2.threshold(scaled_face_gray , 0 , 255 , cv2.THRESH_BINARY)
    # Mask inverse
    mask_inv = cv2.bitwise_not(mask)
    # caricature background
    caricature_bg = cv2.bitwise_and(roi , roi , mask=mask_inv)
    # Scaled Face foreground
    face_fg = cv2.bitwise_and(face , face , mask=mask_inv)
    # Do Mix
    dst = cv2.add(caricature_bg , face_fg)
    dst = black_to_RGB(dst , [102 , 132 , 150] )
    caricature[transition_y:transition_y+face_height ,transition_x:transition_x+face_width ] = dst
    return caricature

def create_caricature_GRAY(face_gray , caricature , transition_y , transition_x):
    # Scaled Face information
    caricature = gray_scale(caricature)
    face_height, face_width = face_gray.shape[0:2]
    # ROI
    roi = caricature[transition_y:transition_y+face_height ,transition_x:transition_x+face_width]
    # Ret and Mask
    ret , mask = cv2.threshold(face_gray , 0 , 255 , cv2.THRESH_BINARY)
    # Mask inverse
    mask_inv = cv2.bitwise_not(mask)
    # caricature background
    caricature_bg = cv2.bitwise_and(roi , roi , mask=mask_inv)
    # Scaled Face foreground
    scaled_face_fg = cv2.bitwise_and(face_gray , face_gray , mask=mask)
    # Do Mix
    dst = cv2.add(caricature_bg , scaled_face_fg)
    caricature[transition_y:transition_y+face_height ,transition_x:transition_x+face_width ] = dst
    return caricature

def show_and_destroy(image):
    cv2.imshow('Hi', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    exit()

def create_face(mask , right_eye , left_eye , nose , mouth , right_eye_coor , left_eye_coor , nose_coor , mouth_coor):
    mask[ right_eye_coor[1]:right_eye_coor[1]+right_eye_coor[3] , right_eye_coor[0]:right_eye_coor[0]+right_eye_coor[2] ] = right_eye
    mask[ left_eye_coor[1]:left_eye_coor[1] + left_eye_coor[3] , left_eye_coor[0]:left_eye_coor[0] + left_eye_coor[2] ] = left_eye
    mask[ nose_coor[1]:nose_coor[1] + nose_coor[3] , nose_coor[0]:nose_coor[0] + nose_coor[2] ] = nose
    mask[ mouth_coor[1]:mouth_coor[1] + mouth_coor[3] , mouth_coor[0]:mouth_coor[0] + mouth_coor[2]] = mouth
    return mask

if( __name__ == '__main__'):
    # img = cv2.imread(sys.argv[1])
    # caricature = cv2.imread(sys.argv[2])

    img = cv2.imread('pics/g.jpg')
    show_and_destroy(cartoonify(img))
    caricature = cv2.imread('caricature/man_2.jpg')

    img_gray = gray_scale(img.copy())
    #img_gray = equalize_image(img_gray)

    # Find Face & Gray Face
    face_color = find_face(img , img_gray)
    face_gray = gray_scale(face_color.copy())

    # Find scale size
    scale_size = cal_scale_size(face_gray.copy() , 150)

    # Scale Face
    face_color = scale(face_color , scale_size)
    face_gray = scale(face_gray , scale_size)

    # Find Nose & Gray Nose
    tmp = find_nose(face_color.copy() , face_gray.copy())
    nose_color = tmp[0]
    nose_gray = gray_scale(nose_color.copy())
    nose_coordinate = tmp[1]

    ### Filter nose
    invert_gray_nose = 255 - nose_gray
    invert_gray_gaussian_blur_nose = cv2.GaussianBlur(invert_gray_nose, (121, 121), 0)
    invert_gray_gaussian_blur_dodge_nose = dodgeNaive(nose_gray, invert_gray_gaussian_blur_nose)
    nose_gray = remove_white_pixel(invert_gray_gaussian_blur_dodge_nose)

    # Find Mouth & Gray Mouth
    tmp = find_mouth(face_color.copy() , face_gray.copy())
    mouth_color = tmp[0]
    mouth_gray = gray_scale(mouth_color.copy())
    mouth_coordinate = tmp[1]

    ### Filter mouth
    invert_gray_mouth = 255 - mouth_gray
    invert_gray_gaussian_blur_mouth = cv2.GaussianBlur(invert_gray_mouth , (121,121) , 0)
    invert_gray_gaussian_blur_dodge_mouth = dodgeNaive(mouth_gray , invert_gray_gaussian_blur_mouth)
    mouth_gray = remove_white_pixel(invert_gray_gaussian_blur_dodge_mouth)

    # Find Left Eye & Gray
    tmp = find_left_eye(face_color.copy() , face_gray.copy())
    left_eye_color = tmp[0]
    left_eye_gray = gray_scale(left_eye_color.copy())
    left_eye_coordinate = tmp[1]

    ### Filter left eye
    invert_gray_left_eye = 255 - left_eye_gray
    invert_gray_gaussian_blur_left_eye = cv2.GaussianBlur(invert_gray_left_eye , (121,121) , 0)
    invert_gray_gaussian_blur_dodge_left_eye = dodgeNaive(left_eye_gray , invert_gray_gaussian_blur_left_eye)
    left_eye_gray = remove_white_pixel(invert_gray_gaussian_blur_dodge_left_eye)

    # Find Right Eye & Gray
    tmp = find_right_eye(face_color.copy() , face_gray.copy())
    right_eye_color = tmp[0]
    right_eye_gray = gray_scale(right_eye_color.copy())
    #right_eye_gray = whiter(right_eye_gray)
    right_eye_coordinate = tmp[1]

    ### filter right eye
    invert_gray_right_eye = 255 - right_eye_gray
    invert_gray_gaussian_blur_right_eye = cv2.GaussianBlur(invert_gray_right_eye , (121,121) , 0)
    invert_gray_gaussian_blur_dodge_right_eye = dodgeNaive(right_eye_gray , invert_gray_gaussian_blur_right_eye)
    right_eye_gray = remove_white_pixel(invert_gray_gaussian_blur_dodge_right_eye)

    ## ellipse
    right_eye_gray = ellipse(right_eye_gray, Axes=(20, 35))
    left_eye_gray = ellipse(left_eye_gray, Axes=(20, 35))
    nose_gray = circle(nose_gray , 27)
    mouth_gray = circle(mouth_gray , 35)
    #show_and_destroy(right_eye_gray)

    ### create caricature
    final_caricature = create_caricature_GRAY(nose_gray.copy() , caricature.copy() , 55 + nose_coordinate[1] , 110 + nose_coordinate[0])
    final_caricature = create_caricature_GRAY(right_eye_gray.copy() , final_caricature.copy() , 55 + right_eye_coordinate[1] , 110 + right_eye_coordinate[0])
    final_caricature = create_caricature_GRAY(left_eye_gray.copy() , final_caricature.copy() , 55 + left_eye_coordinate[1] , 110 + left_eye_coordinate[0])
    final_caricature = create_caricature_GRAY(mouth_gray.copy() , final_caricature.copy() , 55 + mouth_coordinate[1] , 110 + mouth_coordinate[0])

    show_and_destroy(final_caricature)

# gushe ha gefte behse
# smooth. hazf sefida