#!/usr/bin/env python3
import os
import shutil
def getRepoName(url, sub=False):
    if sub is True:
        name = os.path.basename(os.path.normpath(url))
        #print (name)
        return name
    #print(url)
    lastblobdex=url.rfind('/blob/')
    if lastblobdex == -1:
        lastblobdex=url.rfind('/src/')
    if lastblobdex == -1:
        lastblobdex=url.rfind('/browse')  #Used in some bitbucket urls
    if lastblobdex == -1:
        print("ERROR PARSING REPO NAME FROM URL: "+url)
        return None
#    print("Name ends at: "+str(lastblobdex))
    firstnamedex=url.rfind('/',0,lastblobdex)
#    print("Name starts at: "+str(firstnamedex))
    name = url[firstnamedex+1:lastblobdex]
    #Some repos (gitlab) include an extra /-/ segment
    if name is "-":
        lastblobdex=url.rfind('/-/')
        firstnamedex=url.rfind('/',0,lastblobdex)
        name = url[firstnamedex+1:lastblobdex]
    print ("Repo Name: "+name)
    return name

repoURL=input("Input URL of example file from repo (e.g. https://github.com/E4S-Project/E4S-documentation-demo/blob/master/README.md): ")
#repoName=input("Input repo name (as found in repo URL): ")
repoName=getRepoName(repoURL)
spackName=""
whichSpack = shutil.which('spack')
if whichSpack is not None:
    ret=os.system("spack info "+repoName+" >/dev/null")
    if ret != 0:
        ret=os.system("spack info "+repoName.lower()+" >/dev/null")
        if ret == 0:
            spackName=repoName.lower()
        else:
            spackName=input("Input the spack package name (or enter for none): ")
else:
    print("Spack executable not found. Not checking package name.")
    spackName=input("Input the spack package name (or enter for none (defaults to repo name)): ")
docList=input("Input comma separated document list: ").strip()
#website=input("Input website URL (or enter for none): ")
subRepos=input("Input coma separated sub-repo url list (or enter for none): ").strip()

os.mkdir(repoName)
outputFile=repoName+"/e4s.yaml"

with open(outputFile, "a") as mdYaml:
    print("- e4s_product: "+repoName, file=mdYaml)
    print("  version: 0.1.0", file=mdYaml)
    print("  docs: ["+docList+"]", file=mdYaml)
    if spackName:
        print("  spack_name: "+spackName, file=mdYaml)
    #if website:
    #    print("  website: "+website, file=mdYaml)
    if subRepos:
        print("  subrepo_urls: ["+subRepos+"]", file=mdYaml)

print("Wrote: "+outputFile)
print("Add this to your repo list:")
print("-  repo_url: "+repoURL.strip().rsplit('/',1)[0])
