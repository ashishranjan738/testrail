#This script needs 3 arguments: username, password, Build number 
import os,sys,argparse,datetime,json
from testrail import * 

now=datetime.datetime.now()
date=str(now)[:10]

#Get arguments from command line
parser = argparse.ArgumentParser(description='Bootstrapper create testplan to create Plan containing list of specific suites entered in bootstrapper init')
parser.add_argument('-bn', '--build_number', help='Build number from Jenkins', required=True)
parser.add_argument('-user', '--user_name', help='Username of TestRail', required=True)
parser.add_argument('-pass', '--password',help='Password of Testrail', required=True)
args = vars(parser.parse_args())
build_number=args['build_number']
username=args['user_name']
password=args['password']

path='/tmp/'+date+'_'+build_number+'/testrail/'

access_rights = 0o755

suite_file=open(path+'test.json','r')

suites=json.loads(suite_file.read())
# suite_ids=suites['suite_ids']
# suite_id=suite_ids.split(',')
suite_file.close()


print('Suites to be added in the Plan: ')



client = APIClient('https://openebs.testrail.io')
client.user = username
client.password = password
plan_name=date+'-build-'+build_number
plan = client.send_post('add_plan/1',
  {'name':plan_name ,'description': 'creating from API call'}
)

#Get the Plan ID
plan_id=str(plan['id'])
print('Plan created.\nPlan id:',plan_id)
#Add entries to Plan
for suite in suites['suites']:
  print(suite['suite_id'])

  plan_entry=client.send_post('add_plan_entry/'+plan_id,
  {'suite_id':suite['suite_id'],'description': 'This Test Plan is Created via bootstrap_create_testplan'}
  )

# for suite in suite_id:
#   plan_entry=client.send_post('add_plan_entry/'+plan_id,
#   {'suite_id':suite,'description': 'This Test Plan is Created via bootstrap_create_testplan'}
#   )
# print('------Added Suites to Plan -----')

#Create Directory to Store the result(Test Plan Name and ID)
result_path=path+'plan-'+str(plan_name)
try:
  os.mkdir(result_path,access_rights)
except OSError:
  print("Directory %s creation failed\n" %result_path)
else:
  print("Successfully Created file %s \n" %result_path)

#Store the Plan name and Plan ID to a json file
tp_result=open(result_path+'/tp_create_result.json','w+')
if tp_result.write('{\n  "plan_name" : "' +plan_name+ '",\n  "plan_id" : "' +plan_id+ '"\n}'):
  print ("Success in creating Test Plan result file")
else:
  print("Error while creating Test Plan result file")
tp_result.close()