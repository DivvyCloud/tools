# Table of contents  
  
  
## boilerplate/  
Sample scripts that can be used as a starting point if you're building any other scripts using the DivvyCloud API. Currently there are Python and Bash examples.   
  
## auto_exemption.py  
Script to programmatically add an exemption to a resource and clear any pending bot actions that the resource would have ran on it without exemption. Currently made to work with Slack.   
  
Workflow:  
- Issue comes up  
- Bot sends slack notification immediately and schedules another action to happen in an hour  
- The information required to run the script comes through in the slack message  
- Run the script and it adds an exemption via resource group and clears the pending action  
  
## create_data_collection_with_data.py  
Example of how to create a data collection via API. This creates a collection of AMIs.   
  
## create_pack_with_insights.py  
Creates a custom best practices pack with pre-canned insights and some custom ones too  
  
## find_billable_resources.py  
Script to find all resources in an AWS account that DivvyCloud bills for. Currently runs off of the default AWS profile. 

## full_pack_create_bots.py  
Creates a bot for every insight in a pack and sets each bot up for slack notifications  
  
## full_pack_create_bots_splunk.py  
Creates a bot for every insight in a pack and sets each bot up for splunk notifications  
  
## list_accounts.py  
Script to list all accounts linked to DivvyCloud  
  
Sample Output:    
[Alex-MBP scripts]$python list_accounts.py     
Name | Account_ID | Cloud_Type | Resource_Count | Creation_Time    
AWS Sales Account | 014578312761 | AWS | 1157 | 2016-03-29 16:31:48    
DivvyCloud QA RO | 050283019178 | AWS | 3692 | 2016-03-30 17:09:27    
Acme Corp Development | 212860832355 | AWS | 448 | 2016-04-05 14:52:24    
  
## list_dns_records.py  
Script to list all DNS records seen in DivvyCloud and then output to a CSV. 
Sample output:  
domain	account_name	account_id	cloud	is_private	record_name	record_type	record_data  
divvycloud.net.	AWS Sales Account	14578312421	AWS	FALSE		NS	ns-47.awsdns-05.com.  
divvycloud.net.	AWS Sales Account	14578312421	AWS	FALSE		NS	ns-1570.awsdns-04.co.uk.  
divvycloud.net.	AWS Sales Account	14578312421	AWS	FALSE		NS	ns-1004.awsdns-61.net.  
divvycloud.net.	AWS Sales Account	14578312421	AWS	FALSE		NS	ns-1074.awsdns-06.org.  
divvycloud.net.	AWS Sales Account	14578312421	AWS	FALSE		SOA	ns-1570.awsdns-04.co.uk. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400  
testsupport.com.	AWS Sales Account	14578312421	AWS	FALSE		NS	ns-1935.awsdns-49.co.uk.  
testsupport.com.	AWS Sales Account	14578312421	AWS	FALSE		NS	ns-186.awsdns-23.com.  
testsupport.com.	AWS Sales Account	14578312421	AWS	FALSE		NS	ns-1040.awsdns-02.org.  

## list_insights.py  
Script to list all pre-canned insights by cloud.   
Sample output:    
===========================AWS==================================    
Cloud Account Without Global API Accounting Config    
Instance Has Ephemeral Public IP    
Database Instance Retention Policy Too Low    
Load Balancer Cross Zone Balancing Disabled    
Load Balancer Connection Draining Disabled    
  
  
## list_organizations.py  
Boilerplate script - barebones needed for auth and a single sample function. This list the current orgs in an account  
  
## onboard_aws_bulk_roles.py  
Script to onboard multiple AWS accounts via cross account role¨    
Sample onboard_output¨    
¨    
[Alex-MBP scripts]$python onboard_aws_bulk_roles.py ¨    
Onboarding AWS accounts into DivvyCloud¨    
Account Name: POCs| Status: Success | Account Number: 625820357955¨    
Account Name: test| Status: Error | Account Number: 625820357958¨    
  
## onboard_aws_key_secret.py  
Sample AWS account onboarding via API key and secret  
  
## resource_check.py  
Checks if a resource has showed up / been detected in DivvyCloud. If it has, check to see if there are any compliance violations on it.  
  
## show_user_permissions.py  
Script to list all permissions a user has via groups and roles  
  
## test_drive.sh  
DivvyCloud install script for the test-drive installation. See https://s3.amazonaws.com/get.divvycloud.com/index.html for the latest official version  
  
