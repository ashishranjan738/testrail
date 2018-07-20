
import pprint
from testrail import *

#Sending POST request to TestRail API for updating a test case via case id
client = APIClient('https://openebs.testrail.com/')
client.user="ashish.ranjan@openebs.io"
client.password="738@Ashish"


run_id='17'
result=open("newtext.txt","r")
file1=result.read()
file1=str(file1)
req=client.send_post('add_results_for_cases/'+run_id,
		{
			'results':[
				{
				 'case_id':13,
				 'status_id':'1'
				}
				]
		}
)

pprint.pprint(req)
