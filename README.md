#DocPortal Toolkit
*Version 0.1.0*

##Purpose
The DocPortal toolkit generates documentation and metadata summaries for software products in online git repositories. It operates on a yaml list of software repositories. For each repository it finds a metadata file either provided in the repository or in a local cache. The metadata file provides information about the software in the repository including pointers to selected documentation files (README, Changelog, License, etc.). The provided metadata and documentation files are used to generate a summary of each product including links to each summarized document. The result is a single menu page providing sortable entries for each product. Each product entry in the list can be expanded to display individual metadata entries and the summary documents. 

##Repo List
The list of repos is provided by a standard .yaml file. It includes one entry for the DocPortal version. All other entries are the base URLs for the software repositories to be summaraized.

[Example](https://github.com/E4S-Project/E4S-Documenter/blob/master/data/e4s_products.yaml)

##Repo Metadata Files
Individual metadata files are constructed as a yaml dictionary. The default file name is e4s.yaml. The file will be searched for in the URL provided by the repo list first in a hidden .e4s directory and then at the top level of the repo. If it is not found in the remote repo it will be searched for in the local cache.

The required elements are e4s_product, for the product name and docs for a list of the documents in the repo to be summarized. The document list can include either strings indicating just the document name/location or dictionaries with entries like: `{doc: README.md, chars: 500, type: readme}` where doc is the document file, chars is the number of characters from the document to be read and type is the type of document (e.g. readme, license, changelog). 

Other valid entries include website, for a link to a primary web resource other than the repository and subrepo_urls which gives a list of urls for other repositories to have their metadata summarized and listed as children of the current repository.

[Example](https://github.com/E4S-Project/E4S-documentation-demo/blob/master/.e4s/e4s.yaml)

##Script Usage
***DocPortalGen.py*** requires a single argument, the path to an existing directory where the summary pages and the top level list page are generated. It reads from a repository list and metadata file cache in its local data directory. Optionally a second argument, a path to an alternate repository list, may be provided.

***metaGen.py*** prompts the user for fields required for a valid metadata yaml file and prints the resulting file to the current directory.
