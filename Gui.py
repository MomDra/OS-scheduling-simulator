from tkinter import *
import tkinter.messagebox as msgbox
from scheduleInfo import Process
from scheduleInfo import Request
from chartinfo import chartinfo
from HRRN import HRRN
from SPN import SPN
from FCFS import FCFS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

root = Tk()
root.title("OS Scheduling")
root.geometry("960x850")
root.resizable(False, True)

# OS Algorithm에 필요한 변수
request = Request()
psList = []

# 표 프레임
frame_xl = LabelFrame(root, text="Table")

# 표 레이블
label_xl = Label(frame_xl, text="")
label_xl.pack(side="left", padx=5, pady=5)

# 인터페이스 프레임
frame_interface = LabelFrame(root, text="Interface")
frame_interface.pack(side="right", padx=5, pady=5)
frame_xl.pack(side="top", anchor="w" ,padx=5, pady=5) # 인터페이스를 먼저 pack()하기 위함

# 프로세스 입력 프레임
frame_input_process = LabelFrame(frame_interface, text="Input Process")
frame_input_process.pack(padx=5, pady=5)

# 프로세스 입력 레이블
label_id = Label(frame_input_process, text="ID")
label_at = Label(frame_input_process, text="AT")
label_bt = Label(frame_input_process, text="BT")

label_id.grid(row=0, column=0)
label_at.grid(row=0, column=1)
label_bt.grid(row=0, column=2)

# 프로세스 입력 엔트리
entry_id = Entry(frame_input_process, width=5)
entry_at = Entry(frame_input_process, width=5)
entry_bt = Entry(frame_input_process, width=5)

entry_id.insert(0, "P0")

entry_id.grid(row=1, column=0, padx=5, pady=5)
entry_at.grid(row=1, column=1, padx=5, pady=5)
entry_bt.grid(row=1, column=2, padx=5, pady=5)


# 입력 프레임
frame_setting = LabelFrame(frame_interface, text="Setting")
frame_setting.pack()

# 라이오 버튼 and time quantum 엔트리
btn_val = IntVar()
btn_FCFS = Radiobutton(frame_setting, text="FCFS", value=1, variable=btn_val)
btn_RR = Radiobutton(frame_setting, text="RR", value=2, variable=btn_val)
btn_SPN = Radiobutton(frame_setting, text="SPN", value=3, variable=btn_val)
btn_SRTN = Radiobutton(frame_setting, text="SRTN", value=4, variable=btn_val)
btn_HRRN = Radiobutton(frame_setting, text="HRRN", value=5, variable=btn_val)
label_time_quantum = Label(frame_setting, text="Time Quantum")
entry_time_quantum = Entry(frame_setting, width=5)
entry_time_quantum.insert(0, "2")

label_num_of_processors = Label(frame_setting, text="Num Of Processors")
entry_num_of_processors = Entry(frame_setting, width=5)
entry_num_of_processors.insert(0, "1")

btn_FCFS.select()

btn_FCFS.pack()
btn_RR.pack()
btn_SPN.pack()
btn_SRTN.pack()
btn_HRRN.pack()
label_time_quantum.pack()
entry_time_quantum.pack()
label_num_of_processors.pack()
entry_num_of_processors.pack()

# 간트 차트 프레임
frame_chart = LabelFrame(root, text="Chart")
frame_chart.pack(side="bottom", padx=5, pady=5)

# 간트 차트 이미지
# image_default = PhotoImage(file="default.png")
# image_gantt = PhotoImage(file="default.png")
# label_chart = Label(frame_chart, image=image_gantt)
# label_chart.pack()

# Table Setting
def set_table():
    idList = []
    atList = []
    btList = []
    wtList = []
    ttList = []
    nttList = []

    for ps in psList:
        idList.append(ps.get_id())
        atList.append(ps.get_at())
        btList.append(ps.get_bt())
        wtList.append(ps.get_wt())
        ttList.append(ps.get_tt())
        nttList.append(ps.get_ntt())


    dic = {"AT": atList, "BT": btList, "WT": wtList, "TT": ttList, "NTT": nttList}
    frame = pd.DataFrame(dic, index=idList)
    label_xl.config(text=frame)


# Draw Chart
figure1 = plt.Figure(figsize=(6,5), dpi=100)
def set_chart(val_return):
    global frame_chart

    # Test용 chartinfo 배열
    # k = Process(0,0,0)
    # processor1_chart1 = [chartinfo(1, 4, 3, k), chartinfo(8, 21, 13, Process(1,0,0)), chartinfo(22, 23, 1, k)]
    # processor2_chart2 = [chartinfo(0, 7, 7, Process(3,0,0)), chartinfo(7, 10, 3, Process(4,0,0)), chartinfo(10, 13, 3, Process(5,0,0))]
    # list_charts = [processor1_chart1, processor2_chart2]

    list_charts = val_return

    # 차트 상세 설정
    figure1.clear()
    frame_chart.destroy()
    frame_chart = LabelFrame(root, text="Chart")
    frame_chart.pack(side="bottom", padx=5, pady=5)
    gnt = figure1.add_subplot(111)
    bar = FigureCanvasTkAgg(figure1, frame_chart)
    bar.get_tk_widget().pack(padx=5, pady=5)
    NavigationToolbar2Tk(bar, frame_chart)
    gnt.set_xlabel('seconds since start')
    gnt.set_ylabel('Processor')
    gnt.set_ylim(0, 50)
    gnt.set_yticks([10, 20, 30, 40])
    gnt.set_yticklabels(['1', '2', '3', '4'])
    gnt.set_xticks(np.arange(0, chartinfo.max_end_time+1, 5))
    gnt.set_xticks(np.arange(0, chartinfo.max_end_time+1), minor=True)
    gnt.grid(which='major', axis='x', color='blue', alpha=0.8, dashes=(3,3))
    gnt.grid(which='minor', axis='x', color='gray', alpha=0.5, dashes=(3,3))
    
    # Draw
    list_already_draw = []
    for i in range(len(list_charts)):
        for ctinfo in list_charts[i]:
            if ctinfo.get_process() in list_already_draw:
                gnt.broken_barh([(ctinfo.get_start_time(), ctinfo.get_last_time())], ((i*10+7, 6)), facecolors =(ctinfo.get_color()))
            else:
                list_already_draw.append(ctinfo.get_process())
                gnt.broken_barh([(ctinfo.get_start_time(), ctinfo.get_last_time())], ((i*10+7, 6)), facecolors =(ctinfo.get_color()), label=str(ctinfo.get_process().get_id()))

    gnt.legend(loc="best")

count = 1
# 프로세스 입력 버튼
def command_push():
    global count
    process_id = entry_id.get()
    process_at = entry_at.get()
    process_bt = entry_bt.get()

    if process_id == "" or process_at == "" or process_bt == "" or not process_at.isdigit() or not process_bt.isdigit():
        msgbox.showwarning("경고", "입력을 제대로 하시오.\n빈 항목이 있거나\nAT or BT가 정수가 아닙니다.")
        
    elif int(process_at)<0 and int(process_bt)<=0:
        msgbox.showwarning("경고", "입력을 제대로 하시오.\nAT >= 0\nBT > 0")
        
    elif len(psList) >= 15:
        msgbox.showinfo("알림", "프로세스는 최대 15개 입니다.\n더이상 추가할 수 없습니다.")
    
    else:
        psList.append(Process(process_id, int(process_at), int(process_bt)))

        entry_id.delete(0, END)
        entry_at.delete(0, END)
        entry_bt.delete(0, END)

        entry_id.insert(0, "P" + str(count))
        count += 1

        set_table()


btn_push = Button(frame_input_process, text="입력", command=command_push)
btn_push.grid(row=2, column=2, padx=5, pady=5)

# 실행버튼
def command_start():
    time_quantum = entry_time_quantum.get()
    num_of_processors = entry_num_of_processors.get()

    if time_quantum == "" or num_of_processors == "" or not time_quantum.isdigit() or not num_of_processors.isdigit() or len(psList) <=0:
        msgbox.showwarning("경고", "입력을 제대로 하시오.")
    
    elif(int(num_of_processors) > 4):
        msgbox.showinfo("알림", "프로세서는 최대 4개 입니다.")
        entry_num_of_processors.delete(0, END)
        entry_num_of_processors.insert(0, "4")

    else:
        request.set_timeQuantum(int(time_quantum))
        request.set_coreNumber(int(num_of_processors))
        chartinfo.reset()
        for i in psList:
            i.reset()

        # 알고리즘 연동
        if btn_val.get() == 1:
            scheduler = FCFS(psList, request)
        elif btn_val.get() == 2:
            print("RR")
        elif btn_val.get() == 3:
            scheduler = SPN(psList, request)
        elif btn_val.get() == 4:
            print("SRTN")
        elif btn_val.get() == 5:
            scheduler = HRRN(psList, request)

        val_return = scheduler.scheduling()
        set_chart(val_return)
        set_table()

btn_start = Button(frame_interface, text="실행", command=command_start)
btn_start.pack(side="right", padx=5, pady=5)

# 초기화 버튼
def command_reset():
    global count
    # global image_gantt
    count = 1
    psList.clear()
    entry_id.delete(0, END)
    entry_id.insert(0, "P0")
    label_xl.config(text="")
    # label_chart.config(image=image_default)

btn_reset = Button(frame_interface, text="초기화", command=command_reset)
btn_reset.pack(side="left", padx=5, pady=5)


root.mainloop()


# 앞으로 해야할것
# 알고리즘 연동
# 기타 구현할것들
# 삽입한 프로세스 삭제, 그래프 legend on/off