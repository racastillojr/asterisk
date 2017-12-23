#!/usr/bin/env python

#==================================================================================
#Created by Ramon Castillo - rcjr@uic.edu
#Univerisity of Illinois at Chicago
#Academic Computing and Communications Center
#Enterprise Architecture and Development
#==================================================================================

import os
import sys
import subprocess
import time
import MySQLdb
import keyring
import smtplib
#Get ro user password
asteriskpw=keyring.get_password("keyring-system","keyring-user")

#Connect to asterisk database
db=MySQLdb.connect(host="asterisk-mysql-fqdn", passwd=asteriskpw, db="asterisk", user="keyring-user")

c=db.cursor()

#Define max email
numMax=36

#Query that gets netid and voicemail count for users that have over 35 messages
c.execute("""select voicemail_boxes.netid, count(msgnum) from (voicemessages inner join voicemail_boxes on voicemessages.mailboxuser = voicemail_boxes.mailbox) group by voicemail_boxes.netid having count(msgnum) >= %s""",(numMax,))

b=c.fetchall()

#Loop that sends email the netid. Using [1] will give you the mailbox count number
for g in b:
    u = g[0]
    sender = 'do-not-reply@uic.edu'
    receivers = [u+'@uic.edu']
    message = """From: ACCC Voicemail <do-not-reply@uic.edu>
    Subject: Your Email is over the limit
    Body of email here
    
    """

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)
        print "Successfully sent email"
    except smtplib.SMTPException:
        print "Error: unable to send email"  

#Close connection
c.close()
