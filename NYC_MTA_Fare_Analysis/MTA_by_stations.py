#===========================================================================
# Title: Analysis of MTA Fare Data Organized by Individual Subway Station
# Author: Matt Buckley
# Description: Which subway stations cater to regular commuters and
# which stations cater to tourists and other infrequent riders?
# Here I take data from the New York MTA API and plot total
# metrocard sales against sales of 30-day unlimited passes,
# vizualizing the differences among the individual stations
# that make up the New York City subway system
# Liscense: MIT license: http://www.opensource.org/licenses/mit-license.php 
#===========================================================================


# STEPS:
# 1. Generate a list of weeks for which to retrieve MTA fare data
# 2. Download MTA fare data for the chosen week
# 3. Parse MTA fare data into Python dict
# 4. Plot the MTA fare data for each individual subway station in the dict

import sys
import urllib2
import csv
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
                area.append(6*(sqrt(data[str(i)]['TOT_SALES'])))
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
        axis([0,70,1000,450000])
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
    bubble_chart(week_dict)


week_url=weeks_urls[week]

parse_urls(week_url)