from queue import PriorityQueue
import copy
import random
import time
import tkinter
from tkinter import *
import os

window = tkinter.Tk()
window.title("N-Puzzle Problem")
window.geometry("820x500+50+50")
window.resizable(True, True)


# N-Puzzle 클래스
# 퍼즐의 기본 정보와 퍼즐 노드 확장 등의 함수들을 내포
class Problem:
    def __init__(self, puzzle, g_val, f_val):
        self.puzzle = puzzle  
        self.g_val = g_val  
        self.f_val = f_val  
        self.str_puzzle = "".join(map(str, [j for i in self.puzzle for j in i]))

    def __lt__(self, other):
        return self.f_val < other.f_val

    def expand_node(self):
        result = []  # 이동 가능한 경우의 객체를 저장하는 변수
        x, y = self.find_location(self.puzzle, 0)
        move_func = [[x, y-1], [x, y+1],[x-1, y], [x+1, y]]  # up, down, left, right 좌표
        
        for i in move_func:
            new_puzzle = self.get_new_puzzle(x, y, i[0], i[1])
            if new_puzzle is not None:
                child = Problem(new_puzzle, self.g_val+1, 0)
                result.append(child)
        return result

    # 빈 칸과 이동할 위치를 바꾸는 함수
    def get_new_puzzle(self, x1, y1, x2, y2):
        if x2 >= 0 and x2 < len(self.puzzle) and y2 >= 0 and y2 < len(self.puzzle):
            temp_puz = copy.deepcopy(self.puzzle)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None
    
    def find_location(self, puz, val):
        xy_list = [(i, j) for i in range(len(puz)) for j in range(len(puz)) if puz[i][j]==val]
        return xy_list[0][0], xy_list[0][1]



class Algorithm:
    def __init__(self):
        return
    
    def init_table(self, n):
        newlist = []
        for i in range(n):
            newlist.append([])
            for j in range(n):
                cal = i * n + j + 1
                if cal == n*n:
                    newlist[i].append(0)
                else:
                    newlist[i].append(cal)
        return newlist

    # 휴리스틱의 값과 함수 g값을 더해서 반환하는 함수
    def f(self, start, goal):
        return self.h(start.puzzle, goal) + start.g_val
    
    # 휴리스틱 함수의 값을 계산해서 반환하는 함수 
    def h(self, start, goal):
        global n
        temp = 0
        for i in range(n):
            for j in range(n):
                if start[i][j] != goal[i][j] and start[i][j] != 0:
                    temp += 1
        return temp
    
    # 실질적으로 A* 알고리즘이 실행되는 함수 (A* 알고리즘 => 탐색 알고리즘)
    def tree_search(self, start, goal):
        global path_list
        node = Problem(goal, 0, 0)
        que = PriorityQueue()
        que.put(start)
        # 딕셔너리에 {튜플 : 튜플}로 저장(리스트는 사용이 안됨....)
        marked = {tuple(tuple(i) for i in start.puzzle) : None}  
        
        while True:
            if que.empty():
                return False
            temp = que.get()
            if temp.puzzle == node.puzzle:
                continue
            else:
                node = temp
            if node.puzzle == goal:
                break
            for i in node.expand_node():
                if tuple(tuple(j) for j in i.puzzle) not in marked:
                    marked[tuple(tuple(j) for j in i.puzzle)] = tuple(tuple(j) for j in node.puzzle)
                    i.f_val = self.f(i, goal)
                    que.put(i)
        return marked, node
    
    def search_path(self, start, goal, marked):
        path = []
        node = goal
        while node != start:
            path.append(node)
            node = marked[node]

        path.append(start)
        return path



def update_puzzle():
    global path_one, table, n
    
    for i in range(n):
        for j in range(n):
            table[i*n+j].configure(text=str(path_one[i][j]))
    window.update()

    temp = []
    for i in range(n):
        temp.append([])
        for j in range(n):
            if i == n-1 and j == n-1:
                temp[i].append(0)
            else:
                temp[i].append(i*n+j+1)
    
    if path_one == tuple(tuple(i) for i in temp):
        return
    else:
        window.after(1000, update_puzzle)

def restart():
    window.destroy()  # window.destroy()는 위젯을 초기화하고 종료하지만 인터프리터(코드 진행)는 수행
    os.system('python3 8_Puzzle_AStar.py')  # 윈도우 닫고 cmd 상에서 ()안에 내용을 실행

def input_reset(value):
    global path, path_one, table, n
    global frame1, frame2

    path = []
    path_one = ""
    table = []
    n = int(value)
    frame1.destroy()
    frame2.destroy()
    main()

def exit():
    window.quit()

def make_menubar():
    menubar = tkinter.Menu(window)
    menu = tkinter.Menu(menubar, tearoff=0)
    menu.add_command(label="Restart", command=restart)
    menu.add_command(label="Quit", command=exit)
    menubar.add_cascade(label="Menu", menu=menu)
    window.config(menu=menubar)

# puzzle 모양 넣을 프레임 및 N값 입력창 생성
def make_frame1(path):
    global table, frame1

    frame1 = tkinter.Frame(window, width=340, height=300, relief="solid", bd=2)
    frame1.grid(row=0, column=0, pady=40, padx=50, rowspan=2)

    frame1_label = Label(window, text="N * N의 N값 : ", font=('Arial', 12))
    frame1_label.place(x=50, y=10)

    frame1_input = Entry(window, font=('Arial', 12), width=6)
    frame1_input.place(x=155, y=10)

    frame1_input_button = Button(window, text="입력", width=4, command=lambda: input_reset(frame1_input.get()))
    frame1_input_button.place(x=220, y=7)

    # 위에서 생성한 프레임에 라벨을 넣어서 퍼즐 테이블로 만듦
    for i in path:
        for j in i:
            table.append(tkinter.Label(frame1, text=j, font=('Arial', 30), relief="solid", borderwidth=2, width=4, height=2, background="white"))

    # 위에서 생성한 라벨을 grid 형태로 삽입
    for i in range(n):
        for j in range(n):
            table[n*i+j].grid(row=i, column=j)

# puzzle의 전체 경로를 문자로 보여줄 내용들을 넣을 프레임 생성(리스트박스)
def make_frame2(path):
    global frame2

    frame2 = tkinter.Frame(window, width=200, height=290, relief="solid", bd=2, bg="white")
    frame2.grid(row=0, column=1)
    
    frame2_content = tkinter.Frame(frame2, bg="white")
    frame2_content.pack(side="left", fill="y")

    listbox = Listbox(frame2_content, height=20, width=31, font=('Arial', 13))
    listbox.pack(side="top", fill="x")

    xscrollbar = Scrollbar(frame2_content, orient="h", command=listbox.xview)
    xscrollbar.pack(side="bottom", fill="x")

    frame2_scrollbar = tkinter.Frame(frame2, bg="white")
    frame2_scrollbar.pack(side="right", fill="y")

    yscrollbar = Scrollbar(frame2_scrollbar, orient="v", command=listbox.yview)
    yscrollbar.pack(side="top", expand=True, fill="y")

    label = Label(frame2_scrollbar, bitmap="gray12")
    label.pack(side="bottom")

    listbox.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

    index = 0
    for i in path[::-1]:
        str_i = "".join([str(k) for j in i for k in j])
        if index == 0:
            listbox.insert(END, "  초기값 : " + str_i)
        else:
            listbox.insert(END, "  " + str(index) + "회 : " + str_i)
        if index != len(path):
            listbox.insert(END, " ")
        index += 1
    listbox.insert(END, " ")
    listbox.insert(END, "  총 이동 횟수 : " + str(index-1))



# main 함수
def main():
    global n
    
    al = Algorithm()
    goal = al.init_table(n)
    puz = Problem(goal, 0, 0)
    start_time = time.time()

    # 생성된 초기 퍼즐을 랜덤하게 섞는 반복문
    for i in range(50):
        temp = puz.expand_node()
        puz = temp[random.randint(0, len(temp) - 1)]

    # A* 알고리즘 실행
    result = al.tree_search(puz, goal)
    if result[0] == False: restart()
    else:
        marked = result[0]
        node = result[1]

    # 기록중에서 실제로 올바른 경로를 가져옴
    path = al.search_path(tuple(tuple(i) for i in puz.puzzle), tuple(tuple(i) for i in node.puzzle), marked)
    print(f'\n총 이동 횟수 : {len(path)-1}')

    make_menubar()
    make_frame1(path)
    make_frame2(path)
    
    global path_one
    for i in range(len(path)-1, -1, -1):
        path_one = path[i]
        update_puzzle()
        time.sleep(1)  # 업데이트 간격 시간 때문에

    end_time = time.time()
    print(f'{end_time - start_time : .3f} sec')
    window.mainloop()


n = 3  # 한 변의 사이즈 (N * N)
path = []  
path_one = ""
table = []
frame1 = Frame(window)
frame2 = Frame(window)

main()