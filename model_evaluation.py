import cv2 as cv
import numpy as np
import time

#LABELED sudokus by human to evaluate model
sudokus=[
[[[-1,1,8],[4,9,-1],[-1,-1,3]],[[3,-1,-1],[1,-1,7],[2,8,4]],[[-1,-1,-1],[-1,3,2],[-1,-1,6]],[[-1,6,-1],[-1,8,-1],[3,-1,4]],[[-1,1,5],[7,6,3],[-1,-1,-1]],[[-1,-1,8],[-1,2,9],[-1,-1,-1]],[[-1,-1,1],[6,4,-1],[-1,2,-1]],[[-1,7,-1],[-1,-1,-1],[5,-1,-1]],[[-1,8,4],[2,-1,7],[6,-1,3]]],
[[[-1,-1,-1],[8,2,3],[-1,-1,-1]],[[-1,8,-1],[1,-1,7],[-1,-1,-1]],[[-1,-1,-1],[4,9,6],[-1,-1,8]],[[9,4,8],[-1,7,5],[6,-1,1]],[[-1,-1,2],[-1,-1,-1],[-1,4,9]],[[-1,-1,1],[6,-1,-1],[8,2,-1]],[[-1,8,-1],[-1,-1,-1],[5,1,-1]],[[-1,1,-1],[7,6,3],[9,2,8]],[[9,-1,2],[-1,-1,-1],[-1,7,4]]],
[[[4,-1,-1],[3,8,-1],[-1,1,-1]],[[-1,-1,6],[-1,5,-1],[2,-1,-1]],[[2,-1,-1],[-1,-1,-1],[7,5,3]],[[6,5,1],[-1,-1,-1],[7,-1,-1]],[[9,-1,-1],[7,-1,3],[-1,1,5]],[[-1,7,4],[1,-1,-1],[9,6,2]],[[-1,9,4],[1,-1,-1],[5,-1,-1]],[[6,7,-1],[-1,-1,9],[-1,-1,1]],[[-1,3,-1],[8,-1,-1],[6,-1,9]]],
[[[6, -1, 9], [5, -1, -1], [8, -1, -1]], [[-1, 5, 7], [-1, -1, 4], [6, -1, 3]], [[-1, 3, 1], [-1, -1, 2], [5, -1, -1]], [[9, -1, -1], [-1, 8, -1], [-1, 7, 4]], [[-1, -1, -1], [-1, 2, -1], [5, 6, 1]], [[-1, 1, 5], [7, -1, -1], [9, -1, -1]], [[4, 9, -1], [2, 1, -1], [-1, -1, -1]], [[-1, 3, 2], [7, -1, 5], [-1, -1, 6]], [[-1, -1, -1], [3, 9, 6], [-1, 8, -1]]],
[[[-1, 5, 8], [-1, 4, -1], [2, 9, 1]], [[-1, 7, -1], [-1, 6, 2], [-1, 3, -1]], [[-1, -1, 2], [-1, 9, 8], [7, -1, -1]], [[-1, -1, 6], [3, 2, -1], [-1, 7, -1]], [[9, -1, -1], [6, -1, -1], [2, 5, 4]], [[4, -1, 7], [-1, 1, 5], [6, -1, 3]], [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]], [[8, 9, 1], [-1, 2, -1], [-1, -1, -1]], [[2, -1, 6], [-1, 4, -1], [8, -1, 1]]],
[[[-1, 4, 5], [-1, 2, -1], [-1, -1, 1]], [[-1, 1, 7], [3, -1, -1], [-1, -1, -1]], [[-1, 2, -1], [1, -1, -1], [3, 7, 4]], [[-1, -1, 9], [1, -1, 2], [-1, -1, 8]], [[-1, -1, 3], [5, 8, -1], [7, -1, 6]], [[5, 8, -1], [4, 3, 7], [9, -1, -1]], [[-1, 1, -1], [-1, -1, 7], [-1, 5, 4]], [[4, 7, 2], [-1, -1, -1], [6, -1, -1]], [[-1, -1, 5], [2, -1, -1], [-1, -1, 1]]]
]

def readImg(src):
    img=cv.imread(src)
    img_canny = cv.Canny(img,125,175)
    contours,hierarchies= cv.findContours(img_canny,cv.RETR_LIST,cv.CHAIN_APPROX_NONE) #cv.RETR_LIST lists all contours
    #print(contours)

    #sort contours based on area 
    cont=sorted(contours,key=cv.contourArea,reverse=True)[0]

    #draw the contours on the resized image, -1 to draw all contours, color green, 1 is thickness
    #cv.drawContours(img, cont, -1, (0, 255, 0), 1) 
    x,y,w,h=cv.boundingRect(cont)
    #print(x,y,w,h)
    roi=img[y:y+h,x:x+w]

    cv.imwrite("board2.png",roi)
    img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    ret,img=cv.threshold(img,75,255,cv.THRESH_BINARY)
    #invert img 
    for i in range(0,len(img)):
        for j in range(0,len(img[0])):
            if img[i][j] == 255:
                img[i][j]=0
            else:
                img[i][j]=255
    cv.imwrite("board1.png",img)

    #img = cv.GaussianBlur(img,(3,3),cv.BORDER_DEFAULT) #filtering from noises, remove minor edges
    img = cv.dilate(img, np.ones((2, 2), np.uint8), iterations=2)




    arrayOfNums=[]
    for i in range(0,9):
        for j in range(0,9):
            arrayOfNums.append(img[int(y+h*(j)/9)+5:int(y+h*(j+1)/9)-5,int(x+w*(i)/9)+5:int(x+w*(i+1)/9)-5])
            n="Nums/"+str(i)+","+str(j)+".png"
            cv.imwrite(n,img[int(y+h*(j)/9)+5:int(y+h*(j+1)/9)-5,int(x+w*(i)/9)+5:int(x+w*(i+1)/9)-5])

    import pyteseract_Sudoku
    s = [[[1,2,3],[4,5,6],[7,8,9]],
        [[1,2,3],[4,5,6],[7,8,9]],
        [[1,2,3],[4,5,6],[7,8,9]],
        [[1,2,3],[4,5,6],[7,8,9]],
        [[1,2,3],[4,5,6],[7,8,9]],
        [[1,2,3],[4,5,6],[7,8,9]],
        [[1,2,3],[4,5,6],[7,8,9]],
        [[1,2,3],[4,5,6],[7,8,9]],
        [[1,2,3],[4,5,6],[7,8,9]]
        ]


    for i in range(0,9):
        for j in range(0,9):
            img_name=str(i)+","+str(j)+".png"
            reading=pyteseract_Sudoku.main('Nums/'+str(i)+','+str(j)+'.png')
            x=int(j/3)*3+int(i/3)
            y=j%3
            z=i%3
            if reading[0].isdigit():
                s[x][y][z]=int(reading[0])
            else:
                s[x][y][z]=-1
    print(s)
    return s


def modelEval():
    for i in range(1,7):
        errorCnt=0
        sud=readImg("Evaluating_images/s"+str(i)+".png")
        if sud==sudokus[(i-1)] :
            print(True)
        else:
            for b in range(0,9):
                for m in range(0,3):
                    for n in range(0,3):
                        if sud[b][m][n]!= sudokus[i-1][b][m][n]:
                            print("Wrong Reading in Evaluating_images/s"+str(i)+".png")
                            errorCnt=errorCnt+1 
        print("Error count in sudoku s"+str(i)+" is "+str(errorCnt))
t1=time.time()
modelEval()
t2=time.time()
print("Time taken to evaluate model is "+str(t2-t1)+" seconds")