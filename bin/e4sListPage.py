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
from distutils.version import LooseVersion

timestamp='{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

introListBlock='''<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8" />
	<!--[if lt IE 9]><script src="https://cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv.min.js"></script><![endif]-->
	<title>E4S Products</title>
	<meta name="keywords" content="" />
	<meta name="description" content="" />

<style>
.product_button {
  background-color: #555;
  color: white;
  cursor: pointer;
  padding: 18px;
  width: 100%;
  border: none;
  text-align: left;
  outline: none;
  font-size: 15px;
}

.active, .product_button:hover {
  background-color: #222;
}

</style>
</head>

<body style="background-color:#777">


<div class="wrapper">

	<header class="header">
		<div class="load-html" id="header" data-source="header.html"></div>
	</header><!-- .header-->

	<div class="middle">

		<div class="container">
			<main class="content">
				<H2>E4S Products</h2>

***TIMESTAMP***<br>
<hr>
<table id="productTable">
<tr>
<th onclick="sortTable(0)">Name</th>
</tr>
'''

introCloseBlock='''			
</table>
<script>
function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("productTable");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
</script>


</main><!-- .content -->
		</div><!-- .container-->

	</div><!-- .middle-->

</div><!-- .wrapper -->
</body>
</html>'''

introHeadingBlock='''<h3>***HEADING***</h3>
'''

introLinkBlock='''<!-- This is a single product entry. To add more copy and edit from here... -->
<tr><td>
<button class="product_button"><b><a href="***LOWNAME***.html">***CAPNAME***</a></b>
</button>
</td></tr>
<!-- ...to here (product entry end) -->'''


introBlock='''<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8" />

	<title>E4S Products: ***CAPNAME***</title>
  </head>
  <body>
		<h1>***CAPNAME***</h1>

        ***TIMESTAMP***
        <br><br>
'''
spackBlock='''<table>
			<tr>
				<td>Description:</td>
				<td>
                    ***DESCRIPTION***
		        <td>
			</tr>
			<tr>
				<td>Website:</td>
				<td><a href="***SITEADDRESS***">***SITEADDRESS***</a><td>
			</tr>
			<tr>
				<td>Version:</td>
				<td>***SPACKVERSION***<td>
			</tr>
			<tr>
				<td>Spack Hash:</td>
				<td>***SPACKHASH***<td>
			</tr>
		</table>
<hr>'''
endBlock='''
  </body>
</html>	'''

docBlock='''<b>***DOCNAME***</b>
	<br>
<pre>
***DOCTEXT***
</pre>

<a href="***DOCURL***">More...</a>
<hr>
<br>
'''

script_path = os.path.dirname(os.path.abspath( __file__))
browserHeaders={'User-Agent' : "Magic Browser"}
rawSegment='/raw/'
blobSegment='/blob/'
e4sDotYaml='/e4s.yaml'
dotE4s='/.e4s/'
bitbucketRaw='?&raw'
currentVersion='0.0.1'

def getSpackInfo(name):
    whichSpack = shutil.which('spack')
    if whichSpack is None:
        return None
    infoBlob = subprocess.run(['spack', 'info', name], stdout=subprocess.PIPE).stdout.decode('utf-8')
    infoBlob
    return infoBlob

def getURLHead(url, numChars=200):
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
    return name

def readRemoteYaml(yaml_url,name):
    req=urllib.request.Request(yaml_url,None,browserHeaders)
    try:
        response=urlopen(req)
    except urllib.error.URLError as e:
        print("Remote metadata for "+name+": "+e.reason+". "+yaml_url)
        return None
    else:
        try:
            yamlMD = yaml.safe_load(response)
        except:
            print("Remote metadata for "+name+": Invalid yaml url. "+yaml_url)
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
        print("Found .e4s directory for "+name+" at "+raw_yaml_url)
        return yamlMD
    
    #print("Raw URL: "+raw_url)
    raw_yaml_url=raw_url+e4sDotYaml
    #print("Raw E4S "+raw_e4s)
    yamlMD=readRemoteYaml(raw_yaml_url,name)
    
    if yamlMD is not None:
        print("Found top-level e4s.yaml for "+name)
        return yamlMD
    else:
        localFile=script_path+'/../data/'+name+e4sDotYaml
        if os.path.isfile(localFile) is True:
            with open(script_path+'/../data/'+name+e4sDotYaml) as MDFile:
                yamlMD = yaml.safe_load(MDFile)
                print("Found local e4s.yaml for "+name)
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
    if 'version' in yamlMD[0]:
                repoVersion=yamlMD[0]['version']
                if LooseVersion(repoVersion) > LooseVersion(currentVersion):
                    print("Warning: using metadata version ("+repoVersion+") newer than supported version ("+currentVersion+").")
    return yamlMD #{'e4s_product':repoName,'docs':docs}

def printProduct(product, sub=False):
    with open(output_prefix+product['e4s_product'].lower()+".html", "a") as ppage:
        capName=product['e4s_product'].upper()
        lowName=capName.lower()

        print(introLinkBlock.replace("***CAPNAME***",capName).replace("***LOWNAME***", lowName), file=listPage)

        introFix=introBlock.replace("***CAPNAME***",capName).replace("***TIMESTAMP***",timestamp)
        print(introFix, file=ppage)

        spackInfo = getSpackInfo(lowName)
        if spackInfo is not None:
            print(spackInfo)

        appendRaw=""
        rawFileURL = product['repo_url']
        #print("RFW "+rawFileURL)
        
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
            docURL=rawFileURL+"/"+doc+appendRaw
            #print(docURL)
            docHead=getURLHead(docURL)
            if docHead is None:
                continue
            docFix = docBlock.replace("***DOCNAME***",doc).replace("***DOCTEXT***",docHead).replace("***DOCURL***",product['repo_url']+"/"+doc)
            print(docFix, file=ppage)
        #.replace('***DESCRIPTION***',"N/A").replace("***SITEADDRESS***","N/A").replace("***SPACKVERSION***","N/A")

        print(endBlock, file=ppage)

output_prefix=""
if(len(sys.argv)>1):
	if(os.path.isdir(sys.argv[1])):
		output_prefix=sys.argv[1]+"/"
	else:
		print("First argument must be a valid output directory")
		sys.exit(-1)


with open(script_path+'/../data/e4s_products.yaml') as MDlist:
    products = yaml.safe_load(MDlist)

with open(output_prefix+'E4S-Products.html', "a") as listPage:
    print(introListBlock.replace("***TIMESTAMP***",timestamp), file=listPage)

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
        
        printProduct(product)
        if 'subrepo_urls' in product:
            for suburl in product['subrepo_urls']:
                print("Generating HTML for SUBURL: "+suburl)
                processedURL=processURL(suburl,True)
                if processedURL is None:
                    continue
                product = processedURL[0]
                #print(product)
                printProduct(product,True)
        
    print(introCloseBlock.replace("***TIMESTAMP***",timestamp), file=listPage)


#print('\n'.join(speclist))
