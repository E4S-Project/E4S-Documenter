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
    return name

repoName=input("Input repo name (as found in repo URL): ")
#repoName=getRepoName(repoURL)
spackName=""
whichSpack = shutil.which('spack')
if whichSpack is not None:
    ret=os.system("spack info "+repoName+" >/dev/null")
    if ret != 0:
        spackName=input("Input the spack package name (or enter for none): ")
docList=input("Input comma separated document list: ")
#website=input("Input website URL (or enter for none): ")
subRepos=input("Input coma separated sub-repo url list (or enter for none): ")

os.mkdir(repoName)
outputFile=repoName+"/e4s.yaml"

with open(outputFile, "a") as mdYaml:
    print("-e4s_product: "+repoName, file=mdYaml)
    print("  version: 0.1.0", file=mdYaml)
    print("  docs: ["+docList+"]", file=mdYaml)
    if spackName:
        print("  spack_name: "+spackName, file=mdYaml)
    #if website:
    #    print("  website: "+website, file=mdYaml)
    if subRepos:
        print("  subrepo_urls: ["+subRepos+"]", file=mdYaml)

print("Wrote: "+outputFile)
