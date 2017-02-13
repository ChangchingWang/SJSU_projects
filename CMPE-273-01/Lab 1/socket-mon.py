import psutil

############ functions ##############

def transformData(list):
	newList = [];
	for netConnTuple in list:
		if netConnTuple.laddr and netConnTuple.raddr:
			newDic = {};
			newDic["pid"] = str(netConnTuple.pid)
			newDic["laddr"] = netConnTuple.laddr[0] + "@" + str(netConnTuple.laddr[1])
			newDic["raddr"] = netConnTuple.raddr[0] + "@" + str(netConnTuple.raddr[1])
			newDic["status"] = netConnTuple.status
			newList.append(newDic)
		
	return newList

def count(listOfProcess):
	pidCountDic = {}; #ex: pid1:6, pid2:5, pid3:7
	for processDic in listOfProcess:
		thePid = processDic["pid"]
		
		if thePid in pidCountDic:
			pidCountDic[thePid] = pidCountDic[thePid] + 1;
			
		else:
			pidCountDic[thePid] = 1;
	return pidCountDic

def dic2SortedList(dict):
	return sorted(dict, key=dict.__getitem__, reverse=True)
	
def sortProcess(orderList, processDicList):
	newProcessDicList = []
	for nextPid in orderList:
		for processDic in processDicList:
			if(nextPid == processDic["pid"]):
				newProcessDicList.append(processDic)
	return newProcessDicList
	
def formatText(dictList):
	str = "pid,laddr,raddr,status\n"
	
	for dict in dictList:
		str = str + dict["pid"] + "," + dict["laddr"] + "," + dict["raddr"] + "," + dict["status"] + "\n"
	return str

def writeFite(fileName, text):
	target = open(fileName, 'w')
	target.write(text)
	target.close()

############ main process ##############

processTupleList = psutil.net_connections(kind='tcp') #get process source data

processDictList = transformData(processTupleList) #unsorted process info

pidCountDic = count(processDictList) # pid count info

orderList = dic2SortedList(pidCountDic) #sorted pid in descending

newProcessDicList = sortProcess(orderList, processDictList) #sort the process info

text = formatText(newProcessDicList) #format text

writeFite("process-monitor-report.csv", text) #write csv file


