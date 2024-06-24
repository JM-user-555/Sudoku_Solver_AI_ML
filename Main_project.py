import cv2 as cv
import numpy as np


img=cv.imread("sudoku3.png")
#print(img)

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
import SolveSudoku
s=SolveSudoku.solveSudoku(s)
print(s)

def findXY(b,i,j):
    x=((b%3)*3+j)*int(roi.shape[0]/9)+20
    y=(int(b/3)*3+i)*int(roi.shape[1]/9)+60
    return (x,y)

for b in range(0,9):
    for i in range(0,3):
        for j in range(0,3):
            cv.putText(roi,str(s[b][i][j]), findXY(b,i,j), cv.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 2, cv.LINE_AA)
cv.imwrite("Sudoku_Solution.png",roi)
print("You can check the solved Sudoku in Sudoku_Solution.png")