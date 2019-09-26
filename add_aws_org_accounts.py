#!/usr/local/bin/python

import boto3
import time
import urllib
import urllib2
import json
import ssl
import gzip
from botocore.exceptions import ClientError
from StringIO import StringIO

# API keys for org/master account to read member account list
ACCESS_KEY = 'xxxxxxxxxxxxxxxxxx' 
SECRET_KEY = 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'

client = boto3.client('organizations',aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
# Get a list of accounts to add
nextPage = True
nextToken = ''
awsAccountList = {}
awsAccountLength = len(awsAccountList)
currentDivvyAccounts = {}

# Get a list of all AWS accounts in org
while nextPage:
	if nextToken:
		response = client.list_accounts(NextToken='%s' % (nextToken))
	else:
		response = client.list_accounts()

	accountList = response['Accounts']
	for item in accountList:
		#if "Staging Dummy" in item['Name']:
		if item['Status'] == 'ACTIVE':
			awsAccountList[item['Id']] = item['Name']

	if 'NextToken' in response:
		nextToken = response['NextToken'].encode('utf-8')
	else:
		nextPage = False

# Account variables
# Bypass SSL cert check
context = ssl._create_unverified_context()
divvyHost = 'http://your-divvy-endpoint:8001'
#divvyHost = 'https://your-divvy-endpoint'
divvyLogin = '%s/v2/public/user/login' % (divvyHost)
divvyUser = 'YOUR-USERNAME-HERE'
divvyPass = 'YOUR-PASSWORD-HERE'
loginData = {'username':'%s' % (divvyUser), 'password':'%s' % (divvyPass)}
accountPaginationLimit = 25
accountPaginationOffset = 0
accountListData = {'limit':accountPaginationLimit,'offset':accountPaginationOffset,'order_by':'name','filters':[]}
divvyAddAccount = '%s/v2/prototype/cloud/add' % (divvyHost)
divvyListAccount = '%s/v2/public/clouds/list' % (divvyHost)
accountType = 'AWS'
xAuthToken = ''
accountName = ''
accountNumber = ''
authType = 'assume_role'

# STS keys and role to be assumed
apiKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
apiSecret = 'yyyyyyyyyyyyyyyyyyyyyyyyyyyy'
roleName = 'OrganizationAccountReadRole'

harvestStrategy = 1

# Login to DivvyCloud and get token
try:
	req = urllib2.Request(divvyLogin, json.dumps(loginData), {'Content-Type': 'application/json'})
	f = urllib2.urlopen(req, context=context)
	httpResponse = f.read()
	httpResponse = json.loads(httpResponse)
	xAuthToken = httpResponse['session_id']
	f.close()

except urllib2.URLError as e:
	print "An error %s " %e

# Get a list of all AWS accounts already in DivvyCloud
try:
	nextPage = True
	accountPaginationLimit = 25
	accountPaginationOffset = 0

	while nextPage:
		accountListData = {'limit':accountPaginationLimit,'offset':accountPaginationOffset,'order_by':'name','filters':[]}

		req = urllib2.Request(divvyListAccount, json.dumps(accountListData), {'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/json;charset=UTF-8', \
		'Accept': 'application/json, text/plain, */*', 'X-Auth-Token': '%s' % (xAuthToken)})

		f = urllib2.urlopen(req, context=context)
		buffer = StringIO( f.read() )
		gzipResponse = gzip.GzipFile(fileobj=buffer)
		gzipResponse = gzipResponse.read()
		httpResponse = json.loads(gzipResponse)
		f.close()
		accountTotal = httpResponse['total_count']

		# Add known accounts to dict
		for item in httpResponse['clouds']:
			try:
				currentDivvyAccounts[item['account_id']] = item['name']
			except KeyError:
				continue

		accountPaginationOffset += accountPaginationLimit
		if accountTotal < (accountPaginationLimit + accountPaginationOffset):
			nextPage = False

			accountListData = {'limit':accountPaginationLimit,'offset':accountPaginationOffset,'order_by':'name','filters':[]}

			req = urllib2.Request(divvyListAccount, json.dumps(accountListData), {'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/json;charset=UTF-8', \
			'Accept': 'application/json, text/plain, */*', 'X-Auth-Token': '%s' % (xAuthToken)})

			f = urllib2.urlopen(req, context=context)
			buffer = StringIO( f.read() )
			gzipResponse = gzip.GzipFile(fileobj=buffer)
			gzipResponse = gzipResponse.read()
			httpResponse = json.loads(gzipResponse)
			f.close()

			# Add known accounts to dict
			for item in httpResponse['clouds']:
				try:
					currentDivvyAccounts[item['account_id']] = item['name']
				except KeyError:
					continue

	print '%s accounts listed in DivvyCloud, %i unique' % (accountTotal,len(currentDivvyAccounts))

except urllib2.URLError as e:
	print "An error %s " %e


# Prune accounts already in Divvy
doNotAdd = []
for account in awsAccountList:
	if account in currentDivvyAccounts:
		doNotAdd.append(account)

for account in doNotAdd:
	del awsAccountList[account]

# Accounts that you DO NOT want to add to DivvyCloud
blacklist = ['000000000000']
for account in blacklist:
	if account in awsAccountList:
		del awsAccountList[account]


# Iterate through accounts and create appropriate data payload
for account in awsAccountList:
	httpData = {"creation_params":{"cloud_type":"%s" % (accountType),"name":"%s" % (awsAccountList[account]),"account_number":"%s" % (account),"authentication_type":"%s" % (authType), \
	"api_key":"%s" % (apiKey),"secret_key":"%s" % (apiSecret),"role_arn":"arn:aws:iam::%s:role/%s" % (account,roleName),"duration":3600, \
	"session_name":"%s-divvy-sts" % (account),"strategy_id":harvestStrategy}}

	print "Adding %s" % ('%s - %s' % (awsAccountList[account], account))

	try:
		req = urllib2.Request(divvyAddAccount, json.dumps(httpData), {'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/json;charset=UTF-8', \
		'Accept': 'application/json, text/plain, */*', 'X-Auth-Token': '%s' % (xAuthToken)})

		f = urllib2.urlopen(req, context=context)
		f.close()
		time.sleep(1)
		#x += 1

	except urllib2.URLError as e:
		print "An error %s " %e