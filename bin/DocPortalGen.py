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
<html lang="en">

    <head>

        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>E4S - DocPortal</title>

        <!-- CSS -->
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Josefin+Sans:300,400|Roboto:300,400,500">
        <link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css">
        <link rel="stylesheet" href="assets/font-awesome/css/font-awesome.min.css">
        <link rel="stylesheet" href="assets/css/animate.css">
        <link rel="stylesheet" href="assets/css/style.css">
        <link rel="stylesheet" href="assets/css/style_perso.css">

        <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
            <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
        <![endif]-->

        <!-- Favicon and touch icons -->
        <link rel="shortcut icon" href="assets/ico/favicon.png">
        <link rel="apple-touch-icon-precomposed" sizes="144x144" href="assets/ico/apple-touch-icon-144-precomposed.png">
        <link rel="apple-touch-icon-precomposed" sizes="114x114" href="assets/ico/apple-touch-icon-114-precomposed.png">
        <link rel="apple-touch-icon-precomposed" sizes="72x72" href="assets/ico/apple-touch-icon-72-precomposed.png">
        <link rel="apple-touch-icon-precomposed" href="assets/ico/apple-touch-icon-57-precomposed.png">
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


.cocontent {
  padding: 0 18px;
  display: none;
  overflow: hidden;
  background-color: #f1f1f1;
  text-align: left;
}

</style>


    </head>

    <body>

    	<!-- Top content -->
        <div class="top-content">

        	<!-- Top menu -->
			<nav class="navbar navbar-inverse" role="navigation">
				<div class="container">
					<div class="navbar-header">
						<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#top-navbar-1">
							<span class="sr-only">Toggle navigation</span>
							<span class="icon-bar"></span>
							<span class="icon-bar"></span>
							<span class="icon-bar"></span>
						</button>
						<a class="navbar-brand" href="index.html">E4S</a>
					</div>
					<!-- Collect the nav links, forms, and other content for toggling -->
					<div class="collapse navbar-collapse" id="top-navbar-1">
						<ul class="nav navbar-nav">
              <li><a href="index.html">Home</a></li>
              <li><a href="events.html">Events</a></li>
              <li><a href="about.html">About</a></li>
              <li><a href="DocPortal.html">DocPortal</a></li>
              <li><a href="contact.html">Contact Us</a></li>
              <li><a href="faq.html">FAQ</a></li>
              <li><a class="btn btn-link-3" href="download.html">Download</a></li>
					</ul>
					</div>
				</div>
			</nav>
        </div>

        <!-- Features -->
        <div class="features-container section-container">
	        <div class="container">

	            <div class="row">
	                <div class="col-sm-12 features section-description wow fadeIn">

                    <div class="row">
                        <div class="col-sm-12 section-description">
				<H2>E4S Products</h2>


<hr>
<table style="table-layout: fixed; width: 100%;" id="productTable">
<tr>
<th onclick="sortTable(0)">Name</th>
</tr>
'''

introCloseBlock='''			
</table>
Last Generated: ***TIMESTAMP***<br>
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


                        </div>
                    </div>

	                </div>
	            </div>

	        </div>
        </div>

        <!-- Footer -->
        <footer>
	        <div class="container">
	        	<div class="row">
	        		<div class="col-sm-12 footer-copyright">
                    	Created for <a href="https://e4s-project.github.io">The Extreme-scale Scientific Software Stack (E4S) Project</a> by <a href="https://maherou.github.io/">Michael A. Heroux</a>
                    </div>
                    <div class="col-sm-12 footer-copyright">
                        <a href="credit.html">Attribution</a> - Derived from a design by Quentin Petit
                    </div>
                </div>
	        </div>
        </footer>


        <!-- Javascript -->
        <script src="assets/js/jquery-1.11.1.min.js"></script>
        <script src="assets/bootstrap/js/bootstrap.min.js"></script>
        <script src="assets/js/jquery.backstretch.min.js"></script>
        <script src="assets/js/wow.min.js"></script>
        <script src="assets/js/retina-1.1.0.min.js"></script>
        <script src="assets/js/scripts.js"></script>

        <!--[if lt IE 10]>
            <script src="assets/js/placeholder.js"></script>
        <![endif]-->


    <script>
        var coll = document.getElementsByClassName("product_button");
        var i;

        for (i = 0; i < coll.length; i++) {
            coll[i].addEventListener("click", function() {
                this.classList.toggle("active");
                var content = this.nextElementSibling;
                if (content.style.display === "block") {
                    content.style.display = "none";
                } else {
                    content.style.display = "block";
                }
            });
        }
    </script>

    </body>

</html>
'''

introHeadingBlock='''<h3>***HEADING***</h3>
'''

introLinkBlock='''<!-- This is a single product entry. To add more copy and edit from here... -->
<tr><td>
<button class="product_button"><b>***CAPNAME***</b>
</button>
<div class="cocontent">
'''


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
</div>
</td></tr>
<!-- ...to here (product entry end) -->'''

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
currentVersion='0.1.0'

printv=False

def printV(toPrint):
    if printv is True:
        print(toPrint)

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
    if 'version' in yamlMD[0]:
                repoVersion=yamlMD[0]['version']
                if LooseVersion(repoVersion) > LooseVersion(currentVersion):
                    print("Warning: using metadata version ("+repoVersion+") newer than supported version ("+currentVersion+").")
    return yamlMD #{'e4s_product':repoName,'docs':docs}

def printProduct(product, ppage, sub=False):
    #with open(output_prefix+product['e4s_product'].lower()+".html", "a") as ppage:
    capName=product['e4s_product'].upper()
    lowName=capName.lower()

    print(introLinkBlock.replace("***CAPNAME***",capName).replace("***LOWNAME***", lowName), file=listPage)

    #introFix=introBlock.replace("***CAPNAME***",capName).replace("***TIMESTAMP***",timestamp)
    #print(introFix, file=ppage)

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
        docLoc=""
        chars=200;
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
        docFix = docBlock.replace("***DOCNAME***",docLoc).replace("***DOCTEXT***",docHead).replace("***DOCURL***",product['repo_url']+"/"+docLoc)
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

productList=script_path+'/../data/e4s_products.yaml'
if(len(sys.argv)>2):
	if(os.path.isfile(sys.argv[2])):
		productList=sys.argv[2]
	else:
		print("Second argument, if specified, must be a valid yaml product list")
		sys.exit(-1)

with open(productList) as MDlist:
    products = yaml.safe_load(MDlist)

listPageName="DocPortal"
with open(output_prefix+listPageName+'.html', "a") as listPage:
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
        
    print(introCloseBlock.replace("***TIMESTAMP***",timestamp), file=listPage)


#print('\n'.join(speclist))
