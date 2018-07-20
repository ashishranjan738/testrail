#This script needs 3 arguments: username, password, Build number 
import os,sys,argparse,datetime,json,pprint,testrail,yaml,requests

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

path='/tmp/'+date+'/'+build_number+'/testrail'

access_rights = 0o755

# suite_file=open(path+'test.json','r')

# suites=json.loads(suite_file.read())
# suite_ids=suites['suite_ids']
# suite_id=suite_ids.split(',')
# suite_file.close()

file=open(path+"/test.yml","r")
suites=yaml.load(file.read())
file.close()

client = testrail.APIClient('https://openebs.testrail.io')
client.user = username
client.password = password

plan_name=date+'-build-'+build_number
plan = client.send_post('add_plan/1',{'name':plan_name ,'description': 'creating from API call'})

#Get the Plan ID
plan_id=str(plan['id'])
# pprint.pprint(plan)
print('Plan created.\nPlan id:',plan_id)

#Add entries to Plan
# for suite in suites['suites']:
#   plan_entry=client.send_post('add_plan_entry/'+plan_id,
#   {'suite_id':suite['suite_id'],'description': 'This Test Plan is Created via bootstrap_create_testplan'}
#   )
#   print("**********************************\n")
#   pprint.pprint(plan_entry)
#   print("\n**********************************")

map_src_id={}
for suite in suites[0]['suites']:
  plan_entry=client.send_post('add_plan_entry/'+plan_id,{'suite_id':suite,'description': 'This Test Plan is Created via bootstrap_create_testplan'})
  map_src_id[plan_entry['suite_id']]={'run_id':plan_entry['runs'][0]['id'],'cases':[]}
  cases=client.send_get('get_cases/1&suite_id='+str(plan_entry['suite_id']))
  for t in cases:
    url,reponame,issue_number=t['refs'].split(',')
    map_src_id[plan_entry['suite_id']]['cases'].append({'case_id':t['id'],'url':url,'reponame':reponame,'issue_number':int(issue_number)})

pprint.pprint(map_src_id)

# for suite in suite_id:
#   plan_entry=client.send_post('add_plan_entry/'+plan_id,
#   {'suite_id':suite,'description': 'This Test Plan is Created via bootstrap_create_testplan'}
#   )
# print('------Added Suites to Plan -----')

#Create Directory to Store the result(Test Plan Name and ID)
# result_path=path+'plan-'+str(plan_name)
# try:
#   os.mkdir(result_path,access_rights)
# except OSError:
#   print("Directory %s creation failed\n" %result_path)
# else:
#   print("Successfully Created file %s \n" %result_path)

# writting map tojson file
file=open(path+"/mapping.json","w+")
file.write(json.dumps(map_src_id))
file.close()

path+="/cases"
try:
  os.mkdir(path,access_rights)
except OSError:
  print("Directory %s creation failed\n" %(path))
else:
  print("Successfully Created file %s \n" %(path))

# downloading ansible playbooks

for k,v in map_src_id.items():
  for t in v['cases']:
    r=requests.get(t['url'])
    try:
      os.mkdir(path+"/"+str(t['case_id']),access_rights)
    except OSError:
      print("Directory %s creation failed\n" %(path+"/"+str(t['case_id'])))
    else:
      print("Successfully Created file %s \n" %(path+"/"+str(t['case_id'])))
    
    file=open(path+"/"+str(t['case_id'])+"/"+"playbook.yml","w+")
    file.write(r.text)
    file.close()

#Store the Plan name and Plan ID to a json file
# tp_result=open(result_path+'/tp_create_result.json','w+')
# if tp_result.write('{\n  "plan_name" : "' +plan_name+ '",\n  "plan_id" : "' +plan_id+ '"\n}'):
#   print ("Success in creating Test Plan result file")
# else:
#   print("Error while creating Test Plan result file")
# tp_result.close()