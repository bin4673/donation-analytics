# Find Political Donors by individuals
#
# Define function 'median' to calculate the median.
#
def median(lst):
    if not lst:
        return
    lst=sorted(lst)
    if len(lst)%2==1:
        return lst[len(lst)//2]
    else:
        return  (lst[len(lst)//2-1]+lst[len(lst)//2])/2.0

#
# Define function 'zipfun' to return a list that contains CMTE_ID, ZIP_CODE, median, total number and total amount of the transaction.
# The data is treated as that has streamed so far.
#
def zipfun(mylist, llist):
        i=0
        count=1
        mylistout=[[mylist[i][0],mylist[i][1],str(int(round(mylist[i][2]))),str(1),str(int(round(mylist[i][2])))]]
        i=1
        while i<llist:
                j=0
                lll=[mylist[i][2]]
                for j in range(0,i):
                        if mylist[j][0]==mylist[i][0] and mylist[j][1]==mylist[i][1]:
                                count=count+1
                                lll.append(mylist[j][2])
                mylistout.append([mylist[i][0],mylist[i][1],str(int(round(median(lll)))),str(count),str(int(round(sum(lll))))])
                i=i+1
                count = 1
        return mylistout

#
# Define function 'datefun' to return a list that contains CMTE_ID, date, median, total number and total amount of the transaction.
# The data is sorted alphabetical by recipient and then chronologically by date.
#
def datefun(mylist, llist):
        i=0
        count=1
        mylistout = []
        while i<llist:
                if mylist[i][0]!='':
                        j=i+1
                        lll=[mylist[i][2]]
                        for j in range(i+1,llist):
                                if mylist[j][0]==mylist[i][0] and mylist[j][1]==mylist[i][1]:
                                        count=count+1
                                        lll.append(mylist[j][2])
                                        mylist[j][0]=''
                        mylistout.append([mylist[i][0],mylist[i][1],str(int(round(median(lll)))),str(count),str(int(round(sum(lll))))])
                        i=i+1
                        count = 1
                else:
                        i=i+1
	mylistout.sort(key=lambda x: (x[0],x[1][4:8],x[1][0:4]))
        return mylistout

#
# Define function 'wout' to export the corresponding output file.
#
def wout(outtype,mylist):
        outf = open('./output/medianvals_by_'+ outtype +'.txt','w')
        i=0
        for i in range(0,len(mylist)):
                outstr=mylist[i][0]+'|'+mylist[i][1]+'|'+mylist[i][2]+'|'+mylist[i][3]+'|'+mylist[i][4]+'\n'
                outf.write(outstr)
        outf.close()

#
# Read data from itcont.txt. Assign the data to corresponding list 'ziplist' and 'datelist' by getting rid of the data with (1) empty CMTE_ID, 
# (2) empty TRANSACTION_AMT, (3) non-empty OTHER_ID, (4) empty ZIP_CODE for 'ziplist', (5) empty TRANSACTION_DT for 'datelist'
#
f = open('./input/itcont.txt','r')
ziplist = []
datelist = []
lzip = 0
ldate = 0
while 1:
	aline=f.readline()
	if not aline:
		break
	if aline.split('|')[15]=='' and aline.split('|')[0]!=''and aline.split('|')[14]!='':
		if aline.split('|')[10]!='':
			ziplist.append([aline.split('|')[0],aline.split('|')[10][0:5],float(aline.split('|')[14])])
			lzip=lzip+1
		if aline.split('|')[13]!='':
			datelist.append([aline.split('|')[0],aline.split('|')[13],float(aline.split('|')[14])])
			ldate=ldate+1
f.close()

#
# Do the statistical calculation and export corresponding output.
#
wout('zip',zipfun(ziplist,lzip))
wout('date',datefun(datelist,ldate))

