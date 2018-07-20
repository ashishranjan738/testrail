import argparse,github,datetime,json,testrail,pprint

def get_comment(fileName):
    file=open(fileName,"r")
    comment=file.read()
    file.close()
    return comment.strip()

def main():
    parser = argparse.ArgumentParser(description='Issuer cli used to comment on github issues')
    parser.add_argument('-gun', '--gusername', help='username for github', required=True)
    parser.add_argument('-gpass', '--gpassword', help='password for github', required=True)
    parser.add_argument('-tun', '--tusername', help='username for testrail', required=True)
    parser.add_argument('-tpass', '--tpassword', help='password for testrail', required=True)
    parser.add_argument('-bn','--buildnumber',help='buildnumber',required=True)
    args = vars(parser.parse_args())
    gusername,gpassword,tusername,tpassword=args['gusername'],args['gpassword'],args['tusername'],args['tpassword']
    now=datetime.datetime.now()
    date=str(now)[:10]
    path='/tmp/'+date+'/'+args['buildnumber']+'/testrail'
    g=github.Github(gusername,gpassword)
    file=open(path+'/mapping.json','r')
    map_src_id=json.loads(file.read())
    
    client = testrail.APIClient('https://openebs.testrail.io')
    client.user = tusername
    client.password = tpassword
    
    for k,v in map_src_id.items():
        for t in v['cases']:
            # pprint.pprint(t)
            file=open(path+"/cases/"+str(t['case_id'])+"/result.json",'r')
            result_json=json.loads(file.read())
            file.close()
            client.send_post('add_results_for_cases/'+str(v['run_id']),
                    {
                        'results':[
                            {
                            'case_id':t['case_id'],
                            'status_id':str(result_json['status_id'])
                            }
                        ]
                    }
                )
            # pprint.pprint(req)

            # file=open(path+"/cases/"+str(t['case_id'])+"/logs",'r')
            # comment=file.read()
            # file.close()
            # print(comment)
            # print(t['reponame'])
            # print(t['issue_number'])
            print(g.get_user().get_repo(t['reponame']).get_issue(int(t['issue_number'])).create_comment(str(result_json)))


if __name__=="__main__":
    main()