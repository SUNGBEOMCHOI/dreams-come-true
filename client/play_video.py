import cv2

def makeframe(): ## 임의로 640x480 frame 만듦
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    ret, frame = capture.read()
    return frame

def get_fontpos(playerA, font, length, width, font_size, font_thick, startx, starty):
    playerA_size = cv2.getTextSize(playerA, font, font_size, font_thick)[0]
    playerAX = (length - playerA_size[0]) // 2
    playerAY = (width + playerA_size[1]) // 2
    fontpos = (startx+playerAX, starty+playerAY)
    return fontpos

def PlayVideo(frame, play_time, name_lst, score_lst):
    ## resize frame to (1920x1080)
    video_size = (1920, 1080) #(500, 500)#(1920, 1080)
    frame = cv2.resize(frame.copy(), dsize=video_size, interpolation=cv2.INTER_AREA)
    
    blue = (183, 57, 25)
    dark_blue = (122, 26, 9)
    black = (0, 0, 0)
    white= (255, 255, 255) 
    font =  cv2.FONT_HERSHEY_PLAIN
    font_size = 1.5
    font_thick = 1
    
    ## title 
    title = "2023 YAICON ROBOT SOCCER"
    frame = cv2.rectangle(frame.copy(), (10, 20), (460, 50), dark_blue, -1)
    frame = cv2.putText(frame.copy(), str(title), (50, 45), font, font_size, white, font_thick, cv2.LINE_AA)
    
    # ## time
    time_min = play_time//60
    time_sec = play_time%60
    time = str(time_min)+':'+str(time_sec)
    length_t, width_t, startx_t, starty_t = 100, 30, 460, 50
    fontpos_t = get_fontpos(time, font, length_t, width_t, font_size, font_thick, startx_t, starty_t)
    frame = cv2.rectangle(frame.copy(), (460, 50), (560, 80), white, -1)
    frame = cv2.putText(frame.copy(), time, fontpos_t, font, 1.5, black, 1, cv2.LINE_AA)
    
    # frame = cv2.rectangle(frame.copy(), (10, 10), (200, 30), (51, 255, 153), -1)
    # frame = cv2.putText(frame.copy(), str(time_min)+' : '+str(time_sec), (50, 30), font, 1.5, black, 1, cv2.LINE_AA)
    
    # ## name
    playerA = str(name_lst[0])
    playerB = str(name_lst[1])
    lengthA, widthA, startxA, startyA = 170, 30, 10, 50
    lengthB, widthB, startxB, startyB = 170, 30, 290, 50
    fontposA = get_fontpos(playerA, font, lengthA, widthA, font_size, font_thick, startxA, startyA)
    fontposB = get_fontpos(playerB, font, lengthB, widthB, font_size, font_thick, startxB, startyB)
    frame = cv2.rectangle(frame.copy(), (10, 50), (180, 80), blue, -1)
    frame = cv2.rectangle(frame.copy(), (290, 50), (460, 80), blue, -1)
    frame = cv2.putText(frame.copy(), playerA, fontposA, font, font_size, white, font_thick, cv2.LINE_AA)
    frame = cv2.putText(frame.copy(), playerB, fontposB, font, font_size, white, font_thick, cv2.LINE_AA)
    # frame = cv2.rectangle(frame.copy(), (10, 10), (200, 30), (51, 255, 153), -1)
    # frame = cv2.putText(frame.copy(), str(time_min)+' : '+str(time_sec), (50, 30), font, 1.5, black, 1, cv2.LINE_AA)
    
    # ## score
    scoreA = score_lst[0]
    scoreB = score_lst[1]
    score = str(scoreA)+':'+str(scoreB)
    length_sc, width_sc, startx_sc, starty_sc = 110, 30, 180, 50
    fontpos_sc = get_fontpos(score, font, length_sc, width_sc, font_size, font_thick, startx_sc, starty_sc)
    frame = cv2.rectangle(frame.copy(), (180, 50), (290, 80), white, -1)
    frame = cv2.putText(frame.copy(), score, fontpos_sc, font, 1.5, black, 1, cv2.LINE_AA)
    
    ## 보조지표,,?
    
    return frame
    
if __name__ == '__main__':
    frame = makeframe()
    # cv2.imshow('frame',frame)
    # cv2.waitKey(1500)  
    play_time, name_lst, score_lst = 100, ['ROBOT', 'HUMAN'], [10, 10]
    frame_1 = PlayVideo(frame.copy(), play_time, name_lst, score_lst)
    cv2.imshow('frame',frame_1)
    if cv2.waitKey(0)==ord('q'):
        cv2.destroyAllWindows()
    # cv2.waitKey(1500)     
    
