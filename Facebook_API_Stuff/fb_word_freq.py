#===========================================================================
# Title: Word Frequency Analysis and Zipf's Law using Facebook Graph API
# Author: Matt Buckley
# Description: Zipf's Law, in the context of natural language, states that
# given some corpus of natural language utterances, the frequency of any
# word is inversely proportional to its rank in the frequency table. Thus
# the most frequent word will occur approximately twice as often as the
# second most frequent word, three times as often as the third most
# frequent word, etc.  Does this hold true with the corpus of words drawn
# from my facebook friends' status updates?
# Liscense: MIT license: http://www.opensource.org/licenses/mit-license.php 
#===========================================================================

# STEPS:
# 1. Obtain an access token from http://developers.facebook.com
# 2. Store the access token in the fb_resources directory for later
# use
# 3. Issue an fql query to retrieve the text of status updates from
# my Facebook friends
# 4. Remove common words and punctuation from the results
# 5. Organize unique words by their frequency within the results
# 6. Plot each word's freqency against its frequency rank within the corpus


import os
import sys
import regex as re
import webbrowser
import matts_facebook
import urllib
import unicodedata
from nltk.corpus import stopwords
import operator



try:
    USER_ID=open('fb_resources/fb.user_id').read()
except IOError, e:
    print 'unable to find user id'

def login():

    permissions = [
        'user_about_me',
        'friends_about_me',
        'user_activities',
        'friends_activities',
        'user_birthday',
        'friends_birthday',
        'user_education_history',
        'friends_education_history',
        'user_events',
        'friends_events',
        'user_groups',
        'friends_groups',
        'user_hometown',
        'friends_hometown',
        'user_interests',
        'friends_interests',
        'user_likes',
        'friends_likes',
        'user_location',
        'friends_location',
        'user_notes',
        'friends_notes',
        'user_online_presence',
        'friends_online_presence',
        'user_photo_video_tags',
        'friends_photo_video_tags',
        'user_photos',
        'friends_photos',
        'user_relationships',
        'friends_relationships',
        'user_religion_politics',
        'friends_religion_politics',
        'user_status',
        'friends_status',
        'user_videos',
        'friends_videos',
        'user_website',
        'friends_website',
        'user_work_history',
        'friends_work_history',
        'email',
        'read_friendlists',
        'read_requests',
        'read_stream',
        'user_checkins',
        'friends_checkins',
        ]

    args = dict(user_id=USER_ID,
        scope=','.join(permissions), type='user_agent', display='popup'
    )

    webbrowser.open('http://developers.facebook.com/tools/explorer/?'
                    + urllib.urlencode(args))
    access_token = raw_input('Enter your access_token: ')

    filename = os.path.join('fb_resources', 'fb.access_token')
    f = open(filename, 'w')
    f.write(access_token)
    f.close()

    print >> sys.stderr, "Access token stored to local file: 'fb_resources/fb.access_token'"

    return access_token

try:
    access_token=open('fb_resources/fb.access_token').read()
except IOError, e:
    print 'unable to retrieve access token from fb_resources'




login()

# Retrieve info fro GraphAPI

graph=matts_facebook.GraphAPI(access_token)
user=graph.get_object('me')


q='select message,place_id from status where uid in (select uid2 from friend where uid1=me())'
results=graph.fql(q)
status_list=[]
for u in range(0,len(results)):
    status_list.append(results[u]['message'])
status_list=' '.join(status_list[:])
status_list=re.sub(ur"\p{P}+", "", status_list)
status_list=re.sub(' +',' ',status_list)
status_list=unicodedata.normalize('NFKD', status_list).encode('ascii','ignore')
status_list=status_list.replace('\n',' ').lower()

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from scipy.optimize import curve_fit
from pylab import *

word_list=status_list.split(' ')
word_list = [w for w in word_list if not w in stopwords.words('english')]

word_dict={}
for i in word_list:
    word_dict[i]=word_list.count(i)

srtd=sorted(word_dict.iteritems(), key=operator.itemgetter(1))

for i in range(0,len(srtd)):
    if ((srtd[i][0]=='')|(srtd[i][0]=='im')):
        srtd.remove(srtd[i])
srtd.reverse()

x=[]
y=[]
for z,w in srtd:
    x.append(z)
    y.append(w)

rank=range(1,len(y)+1)

# Logarithmic best-fit line using curve_fit from scipy.optimize

def func(x, a, b, c):
    return a * np.exp(-b * x) + c

ivar = np.linspace(1,len(y)+1,num=50)
dvar = func(ivar,4, 0.01, 1)
yn = dvar + 0.2*np.random.normal(size=len(ivar))

popt, pcov = curve_fit(func, ivar, yn)

plt.bar(rank, y, width=.05, facecolor='#E31230', alpha=0.5)
plt.plot(ivar, func(ivar, *popt), 'r-', label="Fitted Curve")
plt.title("Word Frequency Analysis of Friends' Facebook Statuses")
plt.xlabel("Frequency 'Rank'")
plt.ylabel('Word Frequency')
plt.grid(True)

plt.show()


labels='Most Frequent Word: ' "'"+x[0]+"'"
x=rank[0]

sct = scatter(rank, y, c=color, s=20, linewidths=2, color='tomato')
sct.set_alpha(0.75)

plt.annotate(
    labels,
    xy = (x, y), xytext = (2, -2),
    textcoords = 'offset points', ha = 'right', va = 'bottom',
    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
    arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
axis([0,1000,0,10])
xlabel('Frequency Rank')
ylabel('Word Frequency')
show()