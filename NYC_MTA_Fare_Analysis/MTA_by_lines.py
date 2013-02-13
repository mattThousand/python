#===========================================================================
# Title: Analysis of MTA Fare Data Organized by Individual Subway Line
# Author: Matt Buckley
# Description: Which of the MTA's 16 main subway lines cater to regular
# commuters and which lines cater to tourists and other infrequent riders?
# Here I take data from the New York MTA API and plot total metrocard
# sales against sales of 30-day unlimited passes vizualizing,
# the differences among the individual subway lines
# that make up the New York City subway system
# Liscense: MIT license: http://www.opensource.org/licenses/mit-license.php 
#===========================================================================


# STEPS:
# 1. Generate a list of weeks for which to retrieve MTA fare data
# 2. Download MTA fare data for each week
# 3. Parse MTA fare data into Python dict

import sys
import urllib2
import csv
import pandas as pd
import collections
from pylab import *
from scipy import *

week_temp=sys.argv[1]
week=week_temp.split('/')
week=str(week[2]+week[0]+week[1])

def get_weeks_list(start, end, freq='W-SAT'):
    weeks_list = [d.strftime('%y%m%d') for d in pd.date_range(start,end,freq=freq)]
    return weeks_list

start = '06/12/2010'
end = '12/08/2012'
weeks_list=get_weeks_list(start,end)


def get_week_urls(weeks_list):
    weeks_urls=dict.fromkeys(weeks_list)
    for d in weeks_list:
        weeks_urls[d]='http://www.mta.info/developers/data/nyct/fares/fares_'+d+'.csv'
    return weeks_urls

weeks_urls=get_week_urls(weeks_list)

def clean_lines(lines):
    for i in range(len(lines)):
        lines[i][1]=lines[i][1].strip().replace(' ','_')
    return lines


def parse_urls(weeks_url):
    def bubble_chart(data):
        x=[]
        y=[]
        color=[]
        area=[]
        labels=[data[str(i)]['STATION_NAME'] for i in data]

        for i in data:
            if data[str(i)]['30-DUNL']>1000:
                x.append(data[str(i)]['UNL_PCT'])
                y.append(data[str(i)]['TOT_SALES'])
                color.append(data[str(i)]['TOT_SALES'])
                area.append((sqrt(data[str(i)]['TOT_SALES'])))
            else:
                continue
        sct = scatter(x, y, c=color, s=area, linewidths=2, edgecolor='w')
        sct.set_alpha(0.75)


        for label, x, y in zip(labels, (data[str(i)]['UNL_PCT'] for i in data), (data[str(i)]['TOT_SALES'] for i in data)):
            annotate(
                label,
                xy = (x, y), xytext = (-20, 20),
                textcoords = 'offset points', ha = 'right', va = 'bottom',size=7,
                bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
                arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
        axis([0,70,1000,510000])
        xlabel('30 Day Unlimited Metrocard (Pct of Total Sales)')
        ylabel('Total Metrocard Sales')
        title('MTA Metrocard Sales Analysis: Total Sales vs. % Sales 30-Day Unlimited Metrocard for the Week Ending on: '+week_temp)
        show()

    results=urllib2.urlopen(week_url)
    lines = list(csv.reader(results))
    lines=clean_lines(lines)
    week_dict=collections.OrderedDict.fromkeys(lines[i][0] for i in range(3,len(lines)))
n=3
for station in week_dict:
    station_dict=collections.OrderedDict.fromkeys(['STATION_NAME','FF','SEN/DIS','7-DAFASUNL','30-DAFAS/RMFUNL','JOINTRRTKT','7-DUNL',
                                                   '30-DUNL','14-DRFMUNL','1-DUNL','14-DUNL','7-DUNL','TCMC','LIBSPECSEN',
                                                   'RRUNLNOTRADE','TCMCANNUALMC','MREZPAYEXP','MREZPAYUNL','PATH2-T',
                                                   'AIRTRAINFF','AIRTRAIN30-D','AIRTRAIN10-T','AIRTRAINMTHLY'])
    station_dict['STATION_NAME']=lines[n][1]
    station_dict['FF']=int(lines[n][2])
    station_dict['SEN/DIS']=int(lines[n][3])
    station_dict['7-DAFASUNL']=int(lines[n][4])
    station_dict['30-DAFAS/RMFUNL']=int(lines[n][5])
    station_dict['JOINTRRTKT']=int(lines[n][6])
    station_dict['7-DUNL']=int(lines[n][7])
    station_dict['30-DUNL']=int(lines[n][8])
    station_dict['14-DRFMUNL']=int(lines[n][9])
    station_dict['1-DUNL']=int(lines[n][10])
    station_dict['14-DUNL']=int(lines[n][11])
    station_dict['7-DUNL']=int(lines[n][12])
    station_dict['TCMC']=int(lines[n][13])
    station_dict['LIBSPECSEN']=int(lines[n][14])
    station_dict['RRUNLNOTRADE']=int(lines[n][15])
    station_dict['TCMCANNUALMC']=int(lines[n][16])
    station_dict['MREZPAYEXP']=int(lines[n][17])
    station_dict['MREZPAYUNL']=int(lines[n][18])
    station_dict['PATH2-T']=int(lines[n][19])
    station_dict['AIRTRAINFF']=int(lines[n][20])
    station_dict['AIRTRAIN30-D']=int(lines[n][21])
    station_dict['AIRTRAIN10-T']=int(lines[n][22])
    station_dict['AIRTRAINMTHLY']=int(lines[n][23])
    list_all=[station_dict['FF'],station_dict['SEN/DIS'],
              station_dict['7-DAFASUNL'],station_dict['30-DAFAS/RMFUNL'],
              station_dict['JOINTRRTKT'],station_dict['7-DUNL'],
              station_dict['30-DUNL'],station_dict['14-DRFMUNL'],
              station_dict['1-DUNL'],station_dict['14-DUNL'],
              station_dict['7-DUNL'],station_dict['TCMC'],
              station_dict['LIBSPECSEN'],station_dict['RRUNLNOTRADE'],
              station_dict['TCMCANNUALMC'],station_dict['MREZPAYEXP'],
              station_dict['MREZPAYUNL'],station_dict['PATH2-T'],
              station_dict['AIRTRAINFF'],station_dict['AIRTRAIN30-D'],
              station_dict['AIRTRAIN10-T'],station_dict['AIRTRAINMTHLY']]
    station_dict['TOT_SALES']=sum(list_all)
    station_dict['UNL_PCT']=(100*(station_dict['30-DUNL'])/station_dict['TOT_SALES'])
    n += 1
    week_dict[station]=station_dict
    oneline=['R001','R010','R011','R030','R031','R032','R033','R034','R035',
             'R036','R037','R038','R039','R040','R052','R058','R084','R102','R105',
             'R116','R117','R135','R159','R164','R166','R167','R168','R169',
             'R173','R175','R185','R189','R190','R191','R192','R193','R260',
             'R272','R273','R274','R290','R293','R304','R306','R320','R321',
             'R343','R452',]
    oneline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in oneline_dict:
        oneline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        oneline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    oneline_TOT_SALES=sum(oneline_dict[i]['STATION_SALES'] for i in oneline_dict)
    oneline_UNL_PCT=sum(oneline_dict[i]['STATION_UNL_PCT'] for i in oneline_dict)
    return oneline_TOT_SALES
    return oneline_UNL_PCT


    twoline=['R010','R011','R014','R028','R030','R031','R032','R033','R053','R055','R057','R058',
             'R059','R060','R061','R062','R064','R066','R067','R068','R069','R084','R105','R108',
             'R109','R110','R123','R124','R145','R164','R168','R175','R189','R205',
             'R206','R207','R209','R210','R224','R225','R272','R277','R290','R293','R320',
             'R321','R323','R324','R343','R361','R362','R363','R364','R365','R366','R367',
             'R386','R387','R388','R389','R405','R406','R407','R408','R409','R410','R412',
             'R444','R451','R452','R456',]
    twoline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in twoline_dict:
        twoline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        twoline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    twoline_TOT_SALES=sum(twoline_dict[i]['STATION_SALES'] for i in twoline_dict)
    twoline_UNL_PCT=sum(twoline_dict[i]['STATION_UNL_PCT'] for i in twoline_dict)

    threeline=['R010','R011','R014','R028','R030','R031','R032','R033','R055','R057','R059','R060','R061',
               'R062','R064','R066','R067','R068','R069','R105','R108','R123','R124','R168',
               'R175','R206','R207','R224','R225','R293','R323','R324','R344','R345','R412',
               'R452','R456',]
    threeline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in threeline_dict:
        threeline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        threeline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    threeline_TOT_SALES=sum(threeline_dict[i]['STATION_SALES'] for i in threeline_dict)
    threeline_UNL_PCT=sum(threeline_dict[i]['STATION_UNL_PCT'] for i in threeline_dict)

    fourline=['R014','R016','R027','R028','R041','R042','R043','R044',
              'R045','R046','R047','R048','R050','R051','R052','R055','R057','R058','R059',
              'R060','R061','R062','R064','R066','R067','R068','R069','R108','R118','R119',
              'R123','R124','R131','R132','R133','R143','R144','R160','R161',
              'R170','R176','R177','R178','R179','R180','R181','R182','R183',
              'R194','R195','R205','R243','R244','R275','R307','R308','R309',
              'R322','R412','R461','R462','R463',]
    fourline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in fourline_dict:
        fourline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        fourline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    fourline_TOT_SALES=sum(fourline_dict[i]['STATION_SALES'] for i in fourline_dict)
    fourline_UNL_PCT=sum(fourline_dict[i]['STATION_UNL_PCT'] for i in fourline_dict)

    fiveline=['R014','R027','R028','R041','R042','R043','R044','R045',
              'R046','R047','R048','R050','R051','R052','R053','R055','R057','R062',
              'R064','R066','R067','R068','R069','R108','R109','R110','R123','R132','R135',
              'R170','R179','R205','R209','R210','R226','R277','R292','R307','R329',
              'R361','R362','R363','R364','R365','R366','R367','R386','R387','R388','R389',
              'R405','R406','R407','R408','R409','R410','R412','R430','R431','R451',]
    fiveline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in fiveline_dict:
        fiveline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        fiveline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    fiveline_TOT_SALES=sum(fiveline_dict[i]['STATION_SALES'] for i in fiveline_dict)
    fiveline_UNL_PCT=sum(fiveline_dict[i]['STATION_UNL_PCT'] for i in fiveline_dict)

    sixline=['R016','R044','R045','R046','R047','R050','R051','R106','R107','R118','R120',
             'R121','R131','R132','R143','R144','R146','R160','R162','R170','R176','R177',
             'R178','R179','R180','R181','R182','R194','R222','R245','R322','R325','R326',
             'R427','R428','R429','R445','R446','R447','R448','R449','R450','R461','R462','R463',]
    sixline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in sixline_dict:
        sixline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        sixline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    sixline_TOT_SALES=sum(sixline_dict[i]['STATION_SALES'] for i in sixline_dict)
    sixline_UNL_PCT=sum(sixline_dict[i]['STATION_UNL_PCT'] for i in sixline_dict)

    sevenline=['R008','R010','R011','R032','R033','R045','R046','R047','R054','R055','R096','R097',
               'R122','R134','R147','R208','R223','R261','R276','R291','R310','R327',
               'R328','R346','R347','R359',]
    sevenline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in sevenline_dict:
        sevenline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        sevenline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    sevenline_TOT_SALES=sum(sevenline_dict[i]['STATION_SALES'] for i in sevenline_dict)
    sevenline_UNL_PCT=sum(sevenline_dict[i]['STATION_UNL_PCT'] for i in sevenline_dict)

    aline=['R010','R011','R012','R013','R014','R028','R035','R062','R065','R084','R089','R103',
           'R111','R126','R127','R138','R139','R153','R174','R186','R187','R188','R198',
           'R199','R200','R217','R251','R252','R280','R281','R283','R284','R285','R296',
           'R297','R314','R315','R318','R331','R332','R333','R335','R336','R337','R338',
           'R354','R355','R356','R357','R358','R382','R383','R384','R385','R414','R415',
           'R416','R417','R418','R419','R434','R438','R439','R440','R441','R442',]
    aline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in aline_dict:
        aline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        aline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    aline_TOT_SALES=sum(aline_dict[i]['STATION_SALES'] for i in aline_dict)
    aline_UNL_PCT=sum(aline_dict[i]['STATION_UNL_PCT'] for i in aline_dict)

    bline=['R020','R021','R022','R023','R057','R084','R099','R104','R111','R112','R113','R136',
           'R138','R149','R154','R155','R156','R171','R172','R186','R187','R194',
           'R195','R196','R211','R237','R240','R251','R253','R281','R314','R332','R333',
           'R334','R443','R461',]
    bline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in bline_dict:
        bline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        bline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    bline_TOT_SALES=sum(bline_dict[i]['STATION_SALES'] for i in bline_dict)
    bline_UNL_PCT=sum(bline_dict[i]['STATION_UNL_PCT'] for i in bline_dict)

    cline=['R010','R011','R012','R013','R014','R028','R035','R054','R062','R065',
           'R084','R089','R103','R111','R127','R138','R139','R153','R186','R187',
           'R188','R198','R199','R200','R217','R251','R252','R281','R282','R283',
           'R284','R296','R297','R314','R315','R318','R331','R332','R333','R334',
           'R434','R438','R439','R440','R441','R442',]
    cline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in cline_dict:
        cline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        cline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    cline_TOT_SALES=sum(cline_dict[i]['STATION_SALES'] for i in cline_dict)
    cline_UNL_PCT=sum(cline_dict[i]['STATION_UNL_PCT'] for i in cline_dict)

    dline=['R020','R021','R022','R023','R048','R054','R057','R084','R099','R104','R112',
           'R113','R138','R151','R154','R155','R156','R157','R194','R195','R197','R231',
           'R234','R237','R240','R246','R247','R253','R258','R278','R368','R369',
           'R370','R371','R372','R373','R374','R398','R399','R400','R443','R454','R455',
           'R461',]
    dline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in dline_dict:
        dline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        dline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    dline_TOT_SALES=sum(dline_dict[i]['STATION_SALES'] for i in dline_dict)
    dline_UNL_PCT=sum(dline_dict[i]['STATION_UNL_PCT'] for i in dline_dict)


    eline=['R010','R011','R012','R013','R015','R018','R019','R025','R113','R114','R139','R140',
           'R141','R158','R188','R201','R202','R218','R219','R238','R254','R255',
           'R267','R282','R298','R339','R340','R341','R342','R346','R359',]
    eline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in eline_dict:
        eline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        eline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    eline_TOT_SALES=sum(eline_dict[i]['STATION_SALES'] for i in eline_dict)
    eline_UNL_PCT=sum(eline_dict[i]['STATION_UNL_PCT'] for i in eline_dict)

    fline=['R018','R019','R020','R021','R022','R023','R024''R054','R089','R098','R114',
           'R115','R127','R128','R129','R130','R138','R141','R142','R151','R158','R194',
           'R203','R204','R220','R241','R242','R255','R257','R258','R259','R271','R288',
           'R289','R300','R301','R302','R303','R312','R319','R341','R420','R421','R422',
           'R423','R424','R425','R426','R453','R461',]
    fline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in fline_dict:
        fline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        fline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    fline_TOT_SALES=sum(fline_dict[i]['STATION_SALES'] for i in fline_dict)
    fline_UNL_PCT=sum(fline_dict[i]['STATION_UNL_PCT'] for i in fline_dict)

    gline=['R098','R100','R129','R163','R204','R217','R220','R241','R249','R256',
           'R258','R268','R269','R287','R288','R289','R299','R316','R317','R346',
           'R359','R360',]
    gline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in gline_dict:
        gline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        gline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    gline_TOT_SALES=sum(gline_dict[i]['STATION_SALES'] for i in gline_dict)
    gline_UNL_PCT=sum(gline_dict[i]['STATION_UNL_PCT'] for i in gline_dict)

    jline=['R009','R006','R003','R004','R005','R007','R014',
           'R025','R028','R044','R118','R125','R137','R142','R286','R311','R352',
           'R353','R377','R378','R379','R380','R381','R432','R433','R435','R436','R437',
           'R462','R463',]
    jline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in jline_dict:
        jline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        jline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    jline_TOT_SALES=sum(jline_dict[i]['STATION_SALES'] for i in jline_dict)
    jline_UNL_PCT=sum(jline_dict[i]['STATION_UNL_PCT'] for i in jline_dict)


    lline=['R100','R152','R170','R235','R236','R248','R249','R250','R265','R266',
           'R268','R279','R294','R295','R313','R330','R348','R349','R350','R375',
           'R376','R460',]
    lline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in lline_dict:
        lline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        lline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    lline_TOT_SALES=sum(lline_dict[i]['STATION_SALES'] for i in lline_dict)
    lline_UNL_PCT=sum(lline_dict[i]['STATION_UNL_PCT'] for i in lline_dict)

    nline=['R001','R010','R011','R022','R023','R032','R033','R050','R051','R057',
           'R079','R080','R081','R082','R083','R085','R086','R087','R088','R089',
           'R090','R091','R092','R093','R094','R095','R099','R108','R118','R121',
           'R127','R151','R170','R197','R212','R227','R231','R232','R233','R246',
           'R258','R278','R390','R391','R392','R393','R394','R395','R396','R397',
           'R398','R454','R455','R462','R463',]
    nline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in nline_dict:
        nline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        nline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    nline_TOT_SALES=sum(nline_dict[i]['STATION_SALES'] for i in nline_dict)
    nline_UNL_PCT=sum(nline_dict[i]['STATION_UNL_PCT'] for i in nline_dict)

    qline=['R010','R011','R022','R023','R032','R033','R050','R051','R057',
           'R079','R080','R081','R090','R091','R092','R093','R094','R095','R099',
           'R118','R121','R136','R148','R149','R150','R151','R170','R171',
           'R172','R184','R196','R211','R228','R229','R230','R239','R262','R263',
           'R264','R312','R462','R463',]
    qline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in qline_dict:
        qline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        qline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    qline_TOT_SALES=sum(qline_dict[i]['STATION_SALES'] for i in qline_dict)
    qline_UNL_PCT=sum(qline_dict[i]['STATION_UNL_PCT'] for i in qline_dict)

    rline=['R001','R010','R011','R018','R022','R023','R079','R080','R081','R082',
           'R083','R085','R086','R087','R032','R033','R050','R051','R057','R099',
           'R108','R118','R127','R140','R141','R170','R197','R201','R202','R212',
           'R213','R214','R215','R216','R218','R219','R221','R227','R231','R232',
           'R233','R238','R246','R254','R258','R267','R278','R298','R339','R340',
           'R454','R455','R462','R463',]
    rline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in rline_dict:
        rline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        rline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    rline_TOT_SALES=sum(rline_dict[i]['STATION_SALES'] for i in rline_dict)
    rline_UNL_PCT=sum(rline_dict[i]['STATION_UNL_PCT'] for i in rline_dict)

    sline=['R010','R011','R029','R032','R033','R045','R046','R047',
           'R045','R046','R047','R196','R297','R411','R412','R415','R416','R417',
           'R418','R419',]
    sline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in sline_dict:
        sline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        sline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    sline_TOT_SALES=sum(sline_dict[i]['STATION_SALES'] for i in sline_dict)
    sline_UNL_PCT=sum(sline_dict[i]['STATION_UNL_PCT'] for i in sline_dict)


    zline=['R004','R006','R007','R009','R014','R025','R028','R044','R118','R125',
           'R137','R142','R286','R311','R378','R380','R432','R436','R437','R460','R462']
    zline_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in zline_dict:
        zline_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        zline_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    zline_TOT_SALES=sum(zline_dict[i]['STATION_SALES'] for i in zline_dict)
    zline_UNL_PCT=sum(zline_dict[i]['STATION_UNL_PCT'] for i in zline_dict)

    staten_island=['R070','R165']
    staten_island_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in staten_island_dict:
        staten_island_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        staten_island_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    staten_island_TOT_SALES=sum(staten_island_dict[i]['STATION_SALES'] for i in staten_island_dict)
    staten_island_UNL_PCT=sum(staten_island_dict[i]['STATION_UNL_PCT'] for i in staten_island_dict)

    PA_PATH=['R540','R541','R542','R543','R544','R545','R546','R547','R548','R549','R550',
             'R551','R552']
    PA_PATH_dict=collections.OrderedDict.fromkeys(['TOT_SALES','UNL_PCT'])
    for i in PA_PATH_dict:
        PA_PATH_dict[i]['STATION_SALES']=week_dict[i]['TOT_SALES']
        PA_PATH_dict[i]['STATION_UNL_PCT']=week_dict[i]['UNL_PCT']
    PA_PATH_TOT_SALES=sum(PA_PATH_dict[i]['STATION_SALES'] for i in PA_PATH_dict)
    PA_PATH_UNL_PCT=sum(PA_PATH_dict[i]['STATION_UNL_PCT'] for i in PA_PATH_dict)
    bubble_chart(week_dict)


week_url=weeks_urls[week]

parse_urls(week_url)


