from collections import deque
import copy
#import sys,pygame as pg
import time
#forwardchecking, timer,drawings,try all sudoku
Sudoku1 = [[[1,2,3],[4,5,6],[7,8,9]],
           [[1,2,3],[4,5,6],[7,8,9]],
           [[1,2,3],[4,5,6],[7,8,9]],
           [[1,2,3],[4,5,6],[7,8,9]],
           [[1,2,3],[4,5,6],[7,8,9]],
           [[1,2,3],[4,5,6],[7,8,9]],
           [[1,2,3],[4,5,6],[7,8,9]],
           [[1,2,3],[4,5,6],[7,8,9]],
           [[1,2,3],[4,5,6],[7,8,9]]
           ]

Sudoku2 = [[[4,5,3],[8,9,2],[1,6,7]],
           [[8,2,6],[5,7,1],[4,9,3]],
           [[1,9,7],[6,3,4],[5,2,8]],
           [[7,1,4],[5,8,6],[3,2,9]],
           [[9,5,2],[1,3,7],[6,8,4]],
           [[8,6,3],[2,4,9],[7,5,1]],
           [[9,3,5],[6,7,1],[2,4,8]],
           [[2,1,8],[3,4,5],[7,6,9]],
           [[4,7,6],[9,8,2],[3,1,5]]
           ] #is solution of Sudoku4

Sudoku3 = [[[-1,-1,2],[-1,6,8],[1,-1,-1]],
           [[-1,-1,1],[7,-1,-1],[3,6,8]],
           [[6,-1,7],[9,-1,-1],[-1,5,4]],
           [[-1,-1,-1],[7,-1,4],[-1,1,-1]],
           [[-1,-1,3],[-1,-1,-1],[-1,7,6]],
           [[4,7,9],[-1,-1,2],[-1,-1,-1]],
           [[-1,5,-1],[9,2,-1],[4,7,3]],
           [[-1,3,-1],[1,-1,-1],[-1,2,5]],
           [[-1,-1,-1],[3,-1,5],[8,-1,1]]
           ]#easy

Sudoku4 = [[[4,5,-1],[-1,-1,2],[-1,-1,-1]],
           [[-1,-1,-1],[-1,7,-1],[-1,-1,-1]],
           [[-1,-1,-1],[6,3,-1],[-1,2,8]],
           [[-1,-1,-1],[-1,8,6],[-1,2,-1]],
           [[9,5,-1],[-1,-1,-1],[6,-1,-1]],
           [[-1,-1,-1],[2,-1,-1],[7,5,-1]],
           [[-1,-1,-1],[-1,7,-1],[-1,-1,8]],
           [[-1,-1,-1],[-1,4,5],[-1,-1,9]],
           [[4,7,6],[-1,-1,-1],[-1,-1,-1]]
           ]

Sudoku5 = [[[-1,-1,-1],[-1,7,-1],[2,-1,-1]],
           [[-1,-1,-1],[-1,1,9],[-1,8,6]],
           [[-1,-1,-1],[3,4,-1],[1,-1,-1]],
           [[4,-1,7],[1,2,-1],[-1,8,-1]],
           [[2,-1,-1],[-1,-1,-1],[-1,6,7]],
           [[6,-1,5],[-1,-1,4],[-1,-1,9]],
           [[-1,-1,-1],[3,5,4],[-1,-1,-1]],
           [[-1,4,3],[1,7,-1],[-1,-1,-1]],
           [[-1,-1,-1],[-1,-1,6],[-1,-1,3]]
           ] #medium

Sudoku6 = [[[6,2,7],[-1,-1,3],[-1,9,-1]],
           [[3,5,-1],[-1,6,-1],[-1,-1,-1]],
           [[-1,-1,-1],[-1,-1,-1],[-1,1,-1]],
           [[-1,7,-1],[3,-1,-1],[-1,-1,8]],
           [[9,4,6],[-1,-1,-1],[-1,-1,3]],
           [[-1,-1,-1],[7,4,-1],[1,-1,-1]],
           [[4,-1,-1],[-1,-1,-1],[-1,-1,-1]],
           [[-1,-1,-1],[-1,1,-1],[-1,-1,-1]],
           [[-1,-1,8],[4,-1,9],[-1,6,-1]]
           ] #hard

Sudoku7 = [[[-1,9,-1],[-1,-1,-1],[-1,-1,8]],
           [[-1,-1,-1],[-1,-1,5],[4,-1,-1]],
           [[2,-1,-1],[-1,8,-1],[-1,1,-1]],
           [[-1,-1,6],[-1,5,-1],[4,-1,-1]],
           [[-1,-1,1],[-1,-1,9],[2,-1,-1]],
           [[3,-1,5],[7,-1,6],[-1,-1,-1]],
           [[-1,-1,-1],[7,3,4],[-1,-1,-1]],
           [[-1,-1,2],[-1,-1,-1],[-1,6,-1]],
           [[-1,-1,9],[-1,-1,-1],[-1,-1,-1]]
           ] #expert


#the user can change the Sudoku selected here and choose whether forward checking is implemented or not
#SudokuSelected=Sudoku2
forwardCheckingImplemented = False



domain = []
for w in range(1,10):
    domain.append(w) #domain = [1,2,3,4,5,6,7,8,9]


#available assignemts that can be assigned for each variable
availableAssignments=[]

domainStack=deque()



S1=[] #S1 determines whether the variable is changeable (-1) or predefined in Sudoku,True--> is variable   False-->constant (can't change)
availableAssignments=[] #it is [1,2,3,4,5,6,7,8,9] for all variables initially
def init_solving(sud):
    for x1 in range(0,9):
        availableAssignments.append([])
        S1.append([])
        for y1 in  range(0,3):
            availableAssignments[x1].append([])
            S1[x1].append([])
            for z1 in range(0,3):
                availableAssignments[x1][y1].append(copy.copy(domain))
                if sud[x1][y1][z1] == -1:
                    S1[x1][y1].append(True)
                else:
                    S1[x1][y1].append(False)
                
            
indeX2 = [0,0,0] #[box,row,column], it is an example of how the format of index is


def checkDuplicatesInArray(a):
    #a is 1D array
    for element in a:
        k=0
        for x in a:
            if x== element and element!=-1:#dont count element -1 in array
                k=k+1
        if k>1: #if each element in a is repeated more than once return true else loop again"""
            return True
    return False #if no element is found repeated more than once return false

def combineArray(b):
    #b is 2D array'
    #function will return an array containing all elements of b in 1D array'
    a=[]
    for element in b:
        for x in element:
            a.append(x)
    return a

def checkDuplicatesInBox(Sudoku,index):
    a=Sudoku[index[0]]
    b=combineArray(a)
    return checkDuplicatesInArray(b)

def findRowNumber(index):
    rowNumber=0
    rowNumber = int(index[0]/3)*3+index[1] #finding row number in  terms on index[0] and index[1]
    return rowNumber

def findRow(Sudoku,index):
    #  index[0/1/2,0,k] row0
    #  index[0/1/2,1,k] row1
    #  index[0/1/2,2,k] row2
    #  index[3/4/5,0,k] row3
    #  index[3/4/5,1,k] row4
    #  index[3/4/5,2,k] row5
    #  index[6/7/8,0,k] row6
    #  index[6/7/8,1,k] row7
    #  index[6/7/8,2,k] row8
    #  index[for(int(row/3)*3),row%3,k]
    row = []
    rowNumber = findRowNumber(index)
    a=int(rowNumber/3)*3
    b= rowNumber%3
    k=a
    for k in range(a,a+3):
        for j in range(0,3):
            row.append(Sudoku[k][b][j])
            j=j+1
        k=k+1
    return row


def checkDuplicatesInRow(Sudoku,index):
    row = findRow(Sudoku,index)
    return checkDuplicatesInArray(row)

    
    
def printSudoku(Sudoku):
    s=[]
    for i in [0,3,6]:
        for j in [0,1,2]:
            a=[i,j,0]
            r=findRow(Sudoku,a) #find all rows in sudoku and push to s
            s.append(r)
    for element in s:
        print(element) #print each row to print the whole sudoku


def findColumnNumber(index):
    columnNumber=0
    columnNumber= (index[0]%3)*3+index[2]%3 #count number of boxes to the left then multiply by 3 (each box has 3 columns)
                                            #then add index[2] which represents column number in box
    return columnNumber

def findColumn(Sudoku,index):
    ColumnNum = findColumnNumber(index)
    #index[index[0]%3,[0,1,2],columnNumber%3]
    column = []
    a=index[0]%3
    for i in [a,a+3,a+6]:
        for j in [0,1,2]:
            column.append(Sudoku[i][j][ColumnNum%3])
            j=j+1
        i=i+1
    return column #this will return 1D array of the column

def checkDuplicatesInColumn(Sudoku,index):
    column = findColumn(Sudoku,index)
    return checkDuplicatesInArray(column)

#print(checkDuplicatesinColumn(Sudoku1,[3,2,1]))

def goalTest(Sudoku):
    for i in range(0,9):
        for j in range(0,3):
            for k in range(0,3):
                index = [i,j,k]
                if Sudoku[i][j][k] == -1: #checking if there is no -1 in Sudoku --> Sudoku is fully assigned
                    return False
    
    return True

#print(goalTest(Sudoku2))

def getUnassignedVariable(Sudoku):
    for i in range(0,9):
        for j in range(0,3):
            for k in range(0,3):
                index=[i,j,k]
                if Sudoku[i][j][k] == -1: #return index of variable having value -1
                    return index
    return[-1,-1,-1]

def isValidContraint(Sudoku,index,value):
    Sudoku[index[0]][index[1]][index[2]]=value
    if checkDuplicatesInBox(Sudoku,index) or checkDuplicatesInRow(Sudoku,index) or checkDuplicatesInColumn(Sudoku,index):
        return False #if there are any duplicates in box, or row, or column, return False (invalid constraint)
    return True #if there are no duplicates in box, row, column, return True (valid constraint)

#goaltest is to check if assignments are complete
#isvalidContraint checks if the value in this index is valid
cnt=0
def removeAssignedVariables(Sudoku,index):
    Sudoku[index[0]][index[1]][index[2]] = -1
    cnt=0
    
    #for same box
    x = index[1]*3+index[2]
    l=8
    while l>x:#for next variables not previous
        b1=index[0]
        x1=int(l/3)
        y1=l%3
        if S1[b1][x1][y1] == True: #if variable is not predefined (it is -1 initailly), give it -1
            Sudoku[b1][x1][y1]=-1
        availableAssignments[b1][x1][y1]=copy.deepcopy(domain)
        l=l-1

    
    #count based on index(int) and compare based on int of index
    #for next boxes
    for i in range(index[0]+1,9):
        for j in range(0,3):
            for k in range(0,3):
                if S1[i][j][k] == True:
                    Sudoku[i][j][k]=-1
                    availableAssignments[i][j][k]=copy.deepcopy(domain)

    return Sudoku

def forwardChecking(availableAssignments,index,value):
    #remove value from available assignments of box
    x=index[1]*3+index[2]
    for i in range(0,3):
        for j in range(0,3):
            if (i*3+j)>x: #remove value from variables after not before
                if value in availableAssignments[index[0]][i][j]:
                    availableAssignments[index[0]][i][j].remove(value)
    
    #remove value from available assignments of row
    rowNum = findRowNumber(index)
    a=rowNum%3
    b=(int(rowNum/3))*3
    for i in range(b,b+3):
        for k in range(0,3):
            if findColumnNumber([i,a,k]) > findColumnNumber(index): #remove value from variables after not before
                if value in availableAssignments[i][a][k]:
                    availableAssignments[i][a][k].remove(value)
    
    #remove value from available assignments of column
    colNum=findColumnNumber(index)
    c=colNum%3
    d=int(colNum/3)
    for i in [d,d+3,d+6]:
        for j in range(0,3):
            if findRowNumber([i,j,c]) > findRowNumber(index): #remove value from variables after not before
                if value in availableAssignments[i][j][c]:
                    availableAssignments[i][j][c].remove(value)
    

def csp(Sudoku,step=0):
    
    if (goalTest(Sudoku)): #check if goal is achieved
        return True
    i,j,k=getUnassignedVariable(Sudoku) #get unassigned variable (index of variable having value of -1)
    
    while availableAssignments[i][j][k]: #while there are available assignments
    
        value=availableAssignments[i][j][k].pop() #get value from available assignments
        #print(step," ",[i,j,k]," ",value," ",[availableAssignments[i][j][k]])
        if isValidContraint(Sudoku,[i,j,k],value): #if value is valid in the index
            Sudoku[i][j][k]=value #assign value
            if forwardCheckingImplemented == True:
                forwardChecking(availableAssignments,[i,j,k],value) #apply forward checking if boolean is True
            res=csp(Sudoku,step+1) # call the recursive function
            if res==True:
                return True #return True if there is solution
            if Sudoku[i][j][k] != -1:
                removeAssignedVariables(Sudoku,[i,j,k]) #in case of back tracking,remove assigned variables and reset the domain back

    return False


def solveSudoku(sud):
    init_solving(sud)
    printSudoku(sud)
    t1 = time.time()
    print(csp(sud))
    printSudoku(sud)
    t2 = time.time()
    print("Time it takes to solve Sudoku: ",(t2-t1))
    return sud
    
    
#solveSudoku(SudokuSelected)

def get2Dsudoku(Sudoku):
    a=[]
    for i in range(0,9):
        a.append(findRow(Sudoku,[0,i,0]))
    return a




def draw_background():
    screen.fill(pg.Color("white")) #background color white
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(15, 15, 720, 720), 10) #draw border
    i = 1
    while (i * 80) < 720:
        line_width = 5 if i % 3 > 0 else 10 # in order to make the box border thick each 3 (10 instead of 5)
        pg.draw.line(screen, pg.Color("black"), pg.Vector2((i * 80) + 15, 15), pg.Vector2((i * 80) + 15, 735), line_width) #vertical lines
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(15, (i * 80) + 15), pg.Vector2(735, (i * 80) + 15), line_width) #horizental lines
        i = i + 1

def game_loop():
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit() #if exit is pressed, exit system
        
        
        
    
    draw_background()
    draw_numbers()
    pg.display.flip()
    
def draw_numbers(): #draw numbers into the Sudoku
    row = 0
    offset = 35 #oofset is used in order to center the number well in its position
    while row < 9:
        col = 0
        while col < 9:
            output = number_grid[row][col]
            n_text = font.render(str(output), True, pg.Color('black'))
            screen.blit(n_text, pg.Vector2((col * 80) + offset + 5, (row * 80) + offset - 2))
            col += 1
        row += 1            
            

def draw():
    #draw Sudoku

    number_grid=get2Dsudoku(SudokuSelected) #Sudoku as 2D array

    pg.init() #initiate pygame
    screen_size = 750,750 #declare screen size (width and height)
    screen = pg.display.set_mode(screen_size)
    font = pg.font.SysFont("Calibri", 65)
    while 1:
        game_loop()
    
