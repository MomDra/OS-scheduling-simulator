# 이름 : 김종현
# 학번 : 2017136023
# 2021. 4. 09.


from scheduleInfo import Process
from scheduleInfo import Request
from collections import deque
from chartinfo import chartinfo

class FCFS:
    # process_list : process 클래스 리스트
    # request : core_number, time_quantum 정보가 담겨있음
    def __init__(self, processList, request):
        self.__processList = processList
        self.__request = request

    def scheduling(self):
        core_num = self.__request.get_coreNumber()
        ps_list = self.__processList

        returnlist=[]

        readyQueue = [deque() for i in range(core_num)]

        at=[]
        wt=[] # waiting time
        bt=[] # burst time
        for i in range(0,len(ps_list)):
            at.append(0)
            wt.append(0)
            bt.append(0)
        


        ongoing=[]
        for i in range(0,core_num):
            ongoing.append(False)  #프로세서가 일을 진행중인지의 여부

        time=0 #시간
        finishcount=0 #while문 종료조건
        while 1:
            for i in range(0,len(ps_list)):  # 모든 프로세스들을 비교
                if ps_list[i].get_at()==time:  #현재 시간과 arrival time이 같으면 arrive time을 true로
                    ps_list[i].set_arrived()
                if (ps_list[i].get_arrived()==True) & (ps_list[i].get_progress()==False): # 현재 도착한 상태이고 일을 진행중이지 않을 때
                    wt[i]=time-ps_list[i].get_at() # waiting time= 현재시간-arrival time
                    at[i]=ps_list[i].get_at()
            

            for c in range(0,core_num):
                if ongoing[c]==False:  #프로세서가 일을 하지 않고 있다면
                    arrivelist=[]
                    for i in range(0,len(ps_list)): 
                        if (ps_list[i].get_arrived()==True) & (ps_list[i].get_progress()==False): # 프로세서에 도착하고 일을 진행중이지 않은 프로세스들 중에서
                            arrivelist.append([at[i],i])
                    if len(arrivelist)>0:
                        minindex=min(arrivelist)[1]    
                        ps_list[minindex].set_progress() # progress를 true로 바꿔 해당 프로세스가 일을 하는 중 이라고 바꾼다
                        ps_list[minindex].set_where(c)
                        ongoing[c]=True # 프로세서가 일을 하는 중으로 바꾼다
                    

            for c in range(0,core_num):
                if ongoing[c]==True:
                    for i in range(0,len(ps_list)):
                        if (ps_list[i].get_progress()==True) & (ps_list[i].get_finished()==False) & (ps_list[i].get_where()==c):                           
                            if bt[i]+1==ps_list[i].get_bt(): # 현재 시간과 arrival time+burst time+ waiting time이 같을 때 일을 그만함. (time이 아닌 time+1을 넣었을때 올바르게 동작하는데 그 이유는 잘 모르겠음)
                                ongoing[c]=False #프로세스가 일을 끝냈으니 프로세서는 현재 쉬는상태
                                finishcount+=1     # 하나의 프로세스가 일을 마치면 finishcount 증가
                                ps_list[i].set_finished() #해당 프로세스의 일이 끝났다고 표시
                                readyQueue[c].append(ps_list[i])


            if finishcount==len(ps_list):    # finishcount가 프로세스 수와 같아지면 while문 탈출
                break

            for i in range(0,len(ps_list)):
                if (ps_list[i].get_progress()==True) & (ps_list[i].get_finished()==False):
                    bt[i]+=1
            time+=1

        for i in range(0,len(ps_list)):
            ps_list[i].set_wt(wt[i])
            ps_list[i].set_tt(ps_list[i].get_bt()+wt[i])
            ps_list[i].set_ntt(ps_list[i].get_tt()/ps_list[i].get_bt())
            print(str(i+1)+" Process: "+str(ps_list[i].get_id())+"     "+str(ps_list[i].get_at())+"     "+str(ps_list[i].get_bt())+"     "+str(ps_list[i].get_wt())+"     "+str(ps_list[i].get_tt())+"     "+str(ps_list[i].get_ntt()))
        
        for i in range(0,core_num):
            returnlist.append([])
            for j in range(0,len(readyQueue[i])):
                returnlist[i].append(chartinfo(readyQueue[i][j].get_at()+readyQueue[i][j].get_wt(),readyQueue[i][j].get_at()+readyQueue[i][j].get_wt()+readyQueue[i][j].get_bt(),readyQueue[i][j].get_bt(),readyQueue[i][j]))
        
        return readyQueue
        #return returnlist # 스케줄링 완료된 readyQueue 반환 (core 개수가 4개면 queue도 4개)




# psList = []
# n_o_processes=eval(input("number of processes: "))
# n_o_processors=eval(input("number of processors: "))
# for i in range(0,n_o_processes):
#     at=eval(input(str(i+1)+'번째 arrival time: '))
#     bt=eval(input(str(i+1)+"번째 burst time: "))
#     psList.append(Process(i+1,at,bt))
 


# request = Request(0,n_o_processors)

# scheduler = FCFS(psList, request)


# q = scheduler.scheduling()
# #print(q[0][4].get_end_time())

# for i in range(len(q)):
#     for j in range(len(q[i])):
#         print('PID%d %ds' % (q[i][j].get_id(), q[i][j].get_bt()), end=' | ')
#     print()