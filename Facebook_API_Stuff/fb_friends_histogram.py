#===========================================================================
# Title: Plotting Popularity within my Facebook friends network
# Author: Matt Buckley
# Description: How connected are my friends to one another? Here I utilize
# the Facebook Graph API to figure that out, first by querying the Graph
# and then organizing the results of the query into a format that can
# be analyzed visually
# Liscense: MIT license: http://www.opensource.org/licenses/mit-license.php 
#===========================================================================

# STEPS:
# 1. Obtain an access token from http://developers.facebook.com
# 2. Store the access token in the fb_resources directory for later
# use
# 3. Issue an fql query to retrieve info about my friends
# 4. From the results of the fql query, select the info
# about my friends' friendships with one another
# 5. Create a measure of popularity by which to rank
# the friends
# 6. Visualize the results

import os
import sys
import webbrowser
import matts_facebook
import urllib


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


qry='select target_id from connection where source_id = me() and target_type =\'user\''
friends=[str(t['target_id']) for t in graph.fql(qry)]

mutual_friendships=[]
N=50

for i in range(len(friends)/N+1):
    q='select uid1, uid2 from friend where uid1 in (%s) and uid2 in (%s)' %(','.join(friends),
                                                                            ','.join(friends[i*N:(i+1)*N]))
    mutual_friendships += graph.fql(q)

q='select uid, first_name, last_name, sex from user where uid in (%s)' % (','.join(friends), )
results=graph.fql(q)
names=dict([(unicode(u['uid']), u['first_name']+' '+u['last_name'][0]+'.') for u in results])
sexes=dict([(unicode(u['uid']), u['sex']) for u in results])


friendships = {}
for f in mutual_friendships:
    (uid1, uid2) = (unicode(f['uid1']), unicode(f['uid2']))
    try:
        name1 = names[uid1]
    except KeyError, e:
        name1 = 'Unknown'
    try:
        name2 = names[uid2]
    except KeyError, e:
        name2 = 'Unknown'

    if friendships.has_key(uid1):
        if uid2 not in friendships[uid1]['friends']:
            friendships[uid1]['friends'].append(uid2)
    else:
        friendships[uid1] = {'name': name1, 'sex': sexes.get(uid1, ''),
                             'friends': [uid2]}

    if friendships.has_key(uid2):
        if uid1 not in friendships[uid2]['friends']:
            friendships[uid2]['friends'].append(uid1)
    else:
        friendships[uid2] = {'name': name2, 'sex': sexes.get(uid2, ''),
                             'friends': [uid1]}


friend_info = []
for fid in friendships:
    friendship = friendships[fid]
    adjacencies = friendship['friends']
    connections = '<br>'.join([names.get(a, 'Unknown') for a in adjacencies])
    normalized_popularity = float((100*len(friendship['friends']))/100)
    sex = friendship['sex']
    friend_info.append({
        'id': fid,
        'name': friendship['name'],
        'data': {'connections': connections,
                 'normalized_popularity': normalized_popularity, 'sex': sex},
        'adjacencies': adjacencies,
    })

popularity_data=[(friend_info[i]['name'],friend_info[i]['data']['normalized_popularity']) for i in range(len(friend_info))]


popularity_dict={}
for x,y in popularity_data:
    popularity_dict[x]=y

import operator
y=[]
srtd=sorted(popularity_dict.iteritems(), key=operator.itemgetter(1))
for i in range(0,len(srtd)):
    y.append(srtd[i][1])
y.reverse()
y.remove(y[0])

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


rank=range(1,len(y)+1)

plt.bar(rank, y, width=2, color='y',facecolor='#E31230', alpha=0.1)
l = plt.plot(rank, y,'r--', linewidth=2)
plt.title("Sample Distribution of Popularity within my Facebook Friends Network (names omitted)")
plt.xlabel('Popularity Rank')
plt.ylabel('Normalized Popularity')
plt.grid(True)

plt.show()