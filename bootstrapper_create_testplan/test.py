import testrail,pprint

client=testrail.APIClient('http://openebs.testrail.io/testrail/')
client.user="ashish.ranjan@openebs.io"
client.password="738@Ashish"
result=client.send_post('add_results_for_cases/17',
{
	"results": [
		{
			"case_id": 13,
			"status_id": 5,
			"comment": "This test failed",
			"defects": "TR-7"

		},
		{
			"case_id": 15,
			"status_id": 1,
			"comment": "This test passed",
			"elapsed": "5m",
			"version": "1.0 RC1"
		},
	]
}
)

pprint.pprint(result)