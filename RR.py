# 이름 : 김지우
# 학번 : 2017136024
# 2021. 4. 9.

#import scheduleInfo
from collections import deque

class RR:
    # process_list : process 클래스 리스트
    # request : core_number, time_quantum 정보가 담겨있음
    def __init__(self, processList, request):
        self.__process_list = processList
        self.__request = request

    #
    def scheduling(self):
        psList=self.__process_list
        coreNum=self.__request.get_coreNumber()
        readyQueue = deque()#각프로세스 번호저장
        core=[False for i in range(coreNum)]#각 코어가 동작하는지
        core[0]=True#처음 코어는 제일먼저 동작함
        timeQuantum=[0 for i in range(coreNum)]#각 코어의 단위시간 흐름
        timeQuantum[0]=self.__request.get_coreNumber()#처음 코어는 제일 먼저 동작
        remainingTime=[]#각 프로세스별 남은 시간
        for i in psList:
            remainingTime.append(i.get_bt())#각 프로세스별 남은 시간저장
        nowProcess=[]#각 코어의 현재 프로세스
        for i in range(0,coreNum):
            c=-1#idle state일때는 -1로 표기
            if i==0:
                c=0
            nowProcess.append(c)
        ganttList=[deque() for i in range(coreNum)]#간트차트
        endProcessCount=0
        nowTime=0#현재 시간
        while True:
            for i in range (1,len(psList)):#첫번째 프로세스를 제외한 나머지 프로세스를 시간대에 맞게 넣는다
                    if psList[i].get_at()==nowTime and remainingTime[i]>0:
                            readyQueue.append(i)
            for i in range(0,coreNum):
                if core[i]==False:#각 코어가 동작하고 있지 않다면
                    if timeQuantum[i]<=0:#각 코어의 단위시간이 0이하라면 프로세스를 할당함
                        if readyQueue:
                            core[i]=True
                            if remainingTime[nowProcess[i]]>0 and nowProcess[i]!=-1 and coreNum==1:
                                readyQueue.append(nowProcess[i])
                            nowProcess[i]=readyQueue.popleft()
                            timeQuantum[i]=self.__request.get_timeQuantum()
            for i in range(0,coreNum):#간트차트에 작업현황 추가
                ganttList[i].append(nowProcess[i])
            nowTime+=1#
            for i in range(0,coreNum):#각코어의 단위 시간 감소
                timeQuantum[i]-=1
                if coreNum==2:#코어 갯수에 따라 다름
                    if timeQuantum[i]<=0 :#단위 시간이 0이하인 경우에 해당 프로세스의 시간이 남으면 readyqueue에 추가
                        core[i]=False
                        if nowProcess[i]!=-1:
                            if remainingTime[nowProcess[i]]-1>0:
                                readyQueue.append(nowProcess[i])
                elif coreNum>2:
                    if timeQuantum[i]<=0 and core[i]==False:
                        core[i]=False
                        if nowProcess[i]!=-1:
                            if remainingTime[nowProcess[i]]-1>0:
                                readyQueue.append(nowProcess[i])
            for i in range(0,coreNum):
                if nowProcess[i]!=-1:
                    remainingTime[nowProcess[i]]-=1
                    if remainingTime[nowProcess[i]]==0:#해당 프로세스의 남은 시간이 0이면 다른 프로세스로 이동
                        endProcessCount+=remainingTime[nowProcess[i]]==0
                        psList[nowProcess[i]].set_tt(nowTime-psList[nowProcess[i]].get_at())
                        nowProcess[i]=-1
                        core[i]=False
                        timeQuantum[i]=0
                        if readyQueue:
                            nowProcess[i]=readyQueue.popleft()
                            timeQuantum[i]=self.__request.get_timeQuantum()
            if endProcessCount==len(psList):
                break
        for i in psList:#WT,NTT계산
            i.set_wt(i.get_tt()-i.get_bt())
            i.set_wtt(i.get_tt()/i.get_bt())
        return ganttList # 스케줄링 완료된 readyQueue 반환

# psList = []
# psList.append(Process(0, 3))
# psList.append(Process(1, 7))
# psList.append(Process(3, 2))
# psList.append(Process(5, 5))
# psList.append(Process(6, 3))
# request = Request()
# request.set_coreNumber(1)
# request.set_timeQuantum(3)
# scheduler = RR(psList, request)
# q = scheduler.scheduling()
# for i in q:
#     print(i)
# for i in psList:
#     print(i.get_wt()," ",i.get_tt()," ",i.get_wtt())