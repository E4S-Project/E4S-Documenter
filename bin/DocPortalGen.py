#!/usr/bin/env python3

"""e4sListPage.py: Generates web pages listing e4s products from e4s_products.yaml"""
__author__ = "Wyatt Spear"

import urllib.request
from urllib.request import urlopen
import yaml
import subprocess
import datetime
import html
import sys
import os
import shutil
import re
from distutils.version import LooseVersion
import markdown

timestamp='{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

script_path = os.path.dirname(os.path.abspath( __file__))
browserHeaders={'User-Agent' : "Magic Browser"}
rawSegment='/raw/'
blobSegment='/blob/'
e4sDotYaml='/e4s.yaml'
dotE4s='/.e4s/'
bitbucketRaw='?&raw'
currentVersion='0.1.0'

printv=False
htmlBlocks=""

def printV(toPrint):
    if printv is True:
        print(toPrint)

spackInfoTags=['Description','Homepage']
global noSpack
noSpack=False
def getSpackInfo(name):
    global noSpack
    infoMap={}
    if not noSpack:
        whichSpack = shutil.which('spack')
        if whichSpack is None:
            print("Spack not found in path. No Spack info data will be included")
            noSpack=True
            return None
    else:
        return None
    infoBlob = subprocess.run(['spack', 'info', name], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if infoBlob is None:
        return None
    infoList=infoBlob.split("\n\n")
    for item in infoList:
        for tag in spackInfoTags:
            if item.strip().startswith(tag):
                infoEntry=item.strip().split(':',1)
                value=infoEntry[1].strip(' \n')
                if tag == 'Homepage':
                    value="<a href="+value+">"+value+"</a>"
                infoMap[infoEntry[0].strip(' \n')]=value
    return infoMap

def getURLHead(url, numChars=400):
    #masteryaml_url="https://raw.githubusercontent.com/UO-OACISS/e4s/master/docker-recipes/ubi7/x86_64/e4s/spack.yaml"
    #print("Reading URL: "+url)
    #browserHeaders={'User-Agent' : "Magic Browser"}
    req=urllib.request.Request(url,None,browserHeaders)
    #with urlopen(req) as f:
    try:
        f = urlopen(req)
        #Read 2x the target number of characters to look for a good breakpoint in the overflow
        head=html.escape(f.read(numChars*2).decode("utf-8"))
        breakpoint=head.find('\n',numChars)
        if breakpoint < numChars:
            breakpoint=head.find(". ",numChars)
        if breakpoint < numChars:
            breakpoint=head.find(' ',numChars);
        if breakpoint < numChars:
            breakpoint=numChars
        #print("Breakpoint: ",breakpoint)            
        head = head[:breakpoint]
        #print("Resulting Head: "+head)
        return head
    except urllib.error.URLError as e:
        print("ERROR: Document "+url+": "+e.reason)
        return None
    #    yamlMap=yaml.safe_load(url)
    #speclist = yamlMap.get('spack').get('specs')

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
    return name

def readRemoteYaml(yaml_url,name):
    req=urllib.request.Request(yaml_url,None,browserHeaders)
    try:
        response=urlopen(req)
    except urllib.error.URLError as e:
        printV("Remote metadata for "+name+": "+e.reason+". "+yaml_url)
        return None
    else:
        try:
            yamlMD = yaml.safe_load(response)
        except:
            printV("Remote metadata for "+name+": Invalid yaml url. "+yaml_url)
            return None
        else:
            return yamlMD


def getRepoDocs(url,name,sub=False):
    yamlMD=None
    if sub is False:
        #TODO: This should work for github blob urls but may not work for others
        li = url.rsplit(blobSegment, 1)
        raw_url=rawSegment.join(li)
    else:
        raw_url=url
    #Check the hidden .e4s directory for e4s.yaml first
    raw_yaml_url=raw_url+dotE4s+e4sDotYaml
    yamlMD=readRemoteYaml(raw_yaml_url,name)
    if yamlMD is not None:
        printV("Found .e4s directory for "+name+" at "+raw_yaml_url)
        return yamlMD
    
    #print("Raw URL: "+raw_url)
    raw_yaml_url=raw_url+e4sDotYaml
    #print("Raw E4S "+raw_e4s)
    yamlMD=readRemoteYaml(raw_yaml_url,name)
    
    if yamlMD is not None:
        printV("Found top-level e4s.yaml for "+name)
        return yamlMD
    else:
        localFile=script_path+'/../data/'+name+e4sDotYaml
        if os.path.isfile(localFile) is True:
            with open(script_path+'/../data/'+name+e4sDotYaml) as MDFile:
                yamlMD = yaml.safe_load(MDFile)
                printV("Found local e4s.yaml for "+name)
                return yamlMD
    print("No metadata found for "+name)
    return None;
            
       

def processURL(url,sub=False):
    repoName=getRepoName(url,sub)
    if repoName is None:
        return None
    yamlMD=getRepoDocs(url,repoName,sub)
    if yamlMD is not None and 'repo_url' not in yamlMD:
        yamlMD[0]['repo_url']=url
    if yamlMD is not None and 'version' in yamlMD[0]:
                repoVersion=yamlMD[0]['version']
                if LooseVersion(repoVersion) > LooseVersion(currentVersion):
                    print("Warning: using metadata version ("+repoVersion+") newer than supported version ("+currentVersion+").")
    return yamlMD #{'e4s_product':repoName,'docs':docs}

def printProduct(product, ppage, sub=False):
    #with open(output_prefix+product['e4s_product'].lower()+".html", "a") as ppage:
    capName=product['e4s_product'].upper()
    lowName=capName.lower()

    print(htmlBlocks['introLinkBlock'].replace("***CAPNAME***",capName).replace("***LOWNAME***", lowName), file=listPage)

    #introFix=.replace("***CAPNAME***",capName).replace("***TIMESTAMP***",timestamp)
    #print(introFix, file=ppage)

    spackName=lowName
    if 'spack_name' in product:
        spackName=product['spack_name']
    spackInfo = getSpackInfo(spackName)
    if spackInfo is not None:
        #if len(spackInfo)>0:
        #    print("<hr><h3>Spack Info Extract</h3><br>",file=listPage)
        for key,value in spackInfo.items():
            print("<B>"+key+":</B> \n"+value+"<br>\n",file=listPage)
    #if spackInfo is not None:
    #    print(spackInfo)

    appendRaw=""
    rawFileURL = product['repo_url']
    #print("RFW "+rawFileURL)
    print("<hr><h3>Document Summaries</h3><br>",file=listPage)
    if sub is False:
        if 'raw_url' in product:
            rawFileURL = product['raw_url']
        
        if 'bitbucket.' in rawFileURL and '/browse' in rawFileURL:
            appendRaw=bitbucketRaw
            #rawFileURL = product['repo_url']
        else:
            fromRaw="/blob/"
            toRaw="/raw/"
#                if 'raw_replace' in product:
#                    fromRaw=product['raw_replace'][0]
#                    toRaw=product['raw_replace'][1]
            if "bitbucket.org" in rawFileURL:
                fromRaw="/src/"
            rawFileURL = rawFileURL.replace(fromRaw,toRaw)
    #print(rawFileURL)
    for doc in product['docs']:
        docLoc=""
        chars=400;
        if isinstance(doc,str):
            docLoc=doc
        else:
            docLoc=doc["doc"]
            if "chars" in doc:
                chars=doc["chars"]
        docURL=rawFileURL+"/"+docLoc+appendRaw
        #print(docURL)
        docHead=getURLHead(docURL,chars)
        if docHead is None:
            continue
        if docURL.lower().endswith(".md"):
            docHead=markdown.markdown(docHead)
        docFix = htmlBlocks['docBlock'].replace("***DOCNAME***",docLoc).replace("***DOCTEXT***",docHead).replace("***DOCURL***",product['repo_url']+"/"+docLoc)
        print(docFix, file=ppage)
    #.replace('***DESCRIPTION***',"N/A").replace("***SITEADDRESS***","N/A").replace("***SPACKVERSION***","N/A")

    print(htmlBlocks['endBlock'], file=ppage)

def parse_html_blocks(templateLoc):
    with open(templateLoc,"r") as templateFile:
        blockText=templateFile.read()
    items = [item.strip() for item in re.split(r'<!--===|===-->',blockText)]
    return dict(zip(items[1::2], items[2::2]))

output_prefix=""
if(len(sys.argv)>1):
	if(os.path.isdir(sys.argv[1])):
		output_prefix=sys.argv[1]+"/"
	else:
		print("First argument must be a valid output directory")
		sys.exit(-1)

productList=script_path+'/../data/e4s_products.yaml'
if(len(sys.argv)>2):
	if(os.path.isfile(sys.argv[2])):
		productList=sys.argv[2]
	else:
		print("Second argument, if specified, must be a valid yaml product list")
		sys.exit(-1)
		
htmlTemplate=script_path+'/../data/e4s_DocPortal_template.html'
if(len(sys.argv)>3):
	if(os.path.isfile(sys.argv[3])):
		htmlTemplate=sys.argv[3]
	else:
		print("Third argument, if specified, must be a valid html output template")
		sys.exit(-1)

htmlBlocks=parse_html_blocks(htmlTemplate)
#print(htmlBlocks)

with open(productList) as MDlist:
    products = yaml.safe_load(MDlist)

listPageName="DocPortal"
with open(output_prefix+listPageName+'.html', "a") as listPage:
    print(htmlBlocks['introListBlock'].replace("***TIMESTAMP***",timestamp), file=listPage)

    for urls in products:
#        if "github.com" in urls['repo_url']:
#            continue
#        if "heading" in product:
#            print(introHeadingBlock.replace("***HEADING***",product['heading']), file=listPage)
#            continue
        if 'repo_url' not in urls:
            if 'version' in urls:
                repoVersion=urls['version']
                if LooseVersion(repoVersion) > LooseVersion(currentVersion):
                    print("Warning: using repo list version ("+repoVersion+") newer than supported version ("+currentVersion+").")
            continue
        processedURL=processURL(urls['repo_url'])
        if processedURL is None:
            continue
        product = processedURL[0]
        print ('Generating HTML for: '+product['e4s_product'])
        
        printProduct(product, listPage)
        if 'subrepo_urls' in product:
            for suburl in product['subrepo_urls']:
                print("Generating HTML for SUBURL: "+suburl)
                processedURL=processURL(suburl,True)
                if processedURL is None:
                    continue
                product = processedURL[0]
                #print(product)
                printProduct(product, listPage,True)
        
    print(htmlBlocks['introCloseBlock'].replace("***TIMESTAMP***",timestamp), file=listPage)


#print('\n'.join(speclist))
