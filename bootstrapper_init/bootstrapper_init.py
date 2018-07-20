import os, sys, json, datetime, argparse, requests 

def main(): 
  parser = argparse.ArgumentParser(description='cli to get the required data')
  parser.add_argument('-bn', '--buildnumber', help='It is the build number from jenkins', required=True)
  args = vars(parser.parse_args())
  # print(args)

  buildNumber = args['buildnumber']
  #suitesFileLink = args['testsuites']
  date = datetime.datetime.today().strftime('%Y-%m-%d')
  path = '/tmp/%s/%s' % (date, buildNumber) +'/testrail/'
  
  #define access rights
  access_rights = 0o755

  try:
    os.makedirs(path,access_rights)
  except OSError:
    print("Directory %s creation failed\n" %path)
  else:
    print("Successfully Created directory %s \n" %path)
   
  r=requests.get("https://raw.githubusercontent.com/ashishranjan738/demoe2e/master/test.yml")
  file=open(path+"test.yml","w+")
  file.write(r.text)
  file.close()

if __name__ == '__main__':
  main()