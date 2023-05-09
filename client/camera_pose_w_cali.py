"""
Thanks to njanirudh
Reference : Aruco_Tracker (https://github.com/njanirudh/Aruco_Tracker.git)
"""

import numpy as np
import cv2
import cv2.aruco as aruco
import glob

def calibration(cap):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob('calib_images/test_checkerboard/*.png')

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

        if ret == True:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)
            img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    return ret, mtx, dist, rvecs, tvecs

def aruco_detect(cap, ret, mtx, dist, rvecs, tvecs):
    while (True):
        ret, frame = cap.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_100)
        parameters = aruco.DetectorParameters_create()
        parameters.adaptiveThreshConstant = 10
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        font = cv2.FONT_HERSHEY_SIMPLEX
        
        if np.all(ids != None):

            rvec, tvec ,_ = aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)

            for i in range(0, ids.size):
                frame_makrers_1 = cv2.drawFrameAxes(frame.copy(), mtx, dist, rvec[i], tvec[i], 0.1)
            # draw a square around the markers
            # aruco.drawDetectedMarkers(frame_makrers_1, corners)

            frame_markers_2 = aruco.drawDetectedMarkers(frame_makrers_1.copy(), corners, ids)
                
            num_id = 66 # [70 42 24 66 87]
            if num_id in np.ravel(ids) :
                index = np.where(ids == num_id)[0][0] #Extract index of num_id
                cornerUL = corners[index][0][0]
                cornerUR = corners[index][0][1]
                cornerBR = corners[index][0][2]
                cornerBL = corners[index][0][3]

                center = [ (cornerUL[0]+cornerBR[0])/2 , (cornerUL[1]+cornerBR[1])/2 ]
                
                text='[' + str(center[0]) + ','+ str(center[1])  + ']' 
                org=(50, 100) # (int(center[0]), int(center[1]))
                arrow_i = (int(center[0]), int(center[1]))
                arrow_f = (int(cornerUR[0]), int(cornerUR[1]))
                font=cv2.FONT_HERSHEY_SIMPLEX
                frame_markers_3 = cv2.putText(frame_markers_2.copy(),text,org,font,1,(255,0,0),2)
                frame_markers_4 = cv2.arrowedLine(frame_markers_3.copy(), arrow_i, arrow_f, (255,255,0), 2)
            else:
                frame_markers_4 = frame_markers_2.copy()
            
            strg = ''
            for i in range(0, ids.size):
                strg += str(ids[i][0])+', '

            cv2.putText(frame_markers_4, "Id: " + strg, (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)

        else:
            frame_markers_4 = frame.copy()
            # code to show 'No Ids' when no markers are found
            cv2.putText(frame_markers_4, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)

        # display the resulting frame
        cv2.imshow('frame',frame_markers_4)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    
    cap = cv2.VideoCapture(0)

    ret, mtx, dist, rvecs, tvecs = calibration(cap)
    aruco_detect(cap, ret, mtx, dist, rvecs, tvecs)
    
