# DocPortal Toolkit
*Version 0.1.0*

## Purpose
The DocPortal toolkit generates documentation and metadata summaries for software products in online git repositories. It operates on a yaml list of software repositories. For each repository it finds a metadata file either provided in the repository or in a local cache. The metadata file provides information about the software in the repository including pointers to selected documentation files (README, Changelog, License, etc.). The provided metadata and documentation files are used to generate a summary of each product including links to each summarized document. The result is a single menu page providing sortable entries for each product. Each product entry in the list can be expanded to display individual metadata entries and the summary documents. 

## Repo List
The list of repos is provided by a standard .yaml file. It includes one entry for the DocPortal version. All other entries are the base URLs for the software repositories to be summaraized.

[Example](https://github.com/E4S-Project/E4S-Documenter/blob/master/data/e4s_products.yaml)

## Repo Metadata Files
Individual metadata files are constructed as a yaml dictionary. The default file name is e4s.yaml. The file will be searched for in the URL provided by the repo list first in a hidden .e4s directory and then at the top level of the repo. If it is not found in the remote repo it will be searched for in the local cache.

The required elements are e4s_product, for the product name and docs for a list of the documents in the repo to be summarized. The document list can include either strings indicating just the document name/location or dictionaries with entries like: `{doc: README.md, chars: 500, type: readme}` where doc is the document file, chars is the number of characters from the document to be read and type is the type of document (e.g. readme, license, changelog). 

Other valid entries include website, for a link to a primary web resource other than the repository and subrepo_urls which gives a list of urls for other repositories to have their metadata summarized and listed as children of the current repository.

[Example](https://github.com/E4S-Project/E4S-documentation-demo/blob/master/.e4s/e4s.yaml)

```yaml
- e4s_product: tau  #The e4s_product entry is the name of the product to display in the table.
  #spack_name: tau #Optional. Define the spack package name if the e4s_product name is different.
  docs:  [README, Changes, LICENSE] #List of documents to be summarized (relative to the root of the repository)
  Area: "Development tools" #The category of product. 
      #Areas include Development Tools, PMR (Programming Models and Runtimes), Math Libraries, Data & Viz, and Software Ecosystem
  Description: "A performance analysis and tuning library." #A very brief description of the application.
  MemberProduct: False #Indicate if the product has adopted E4S community policies.
  Accelerable: True #Indicate if the product is capable of running on accelerator hardware
  ```

## Script Usage
***DocPortalGen.py*** requires a single argument, the path to an existing directory where the summary pages and the top level list page are generated. It reads from a repository list and metadata file cache in its local data directory. Optionally a second argument, a path to an alternate repository list, may be provided.

***metaGen.py*** prompts the user for fields required for a valid metadata yaml file and prints the resulting file to the current directory.

## Adding Your Product to the Docportal
In order for your product summary to appear in the DocPortal two steps are necessary. First a metadata file must be created and added either to the DocPortal repo on your own project in a location where it can be found or to the E4S-Documenter repository. The format of the e4s.yaml file is described above. To administer your own metadata file create `.e4s/e4s.yaml` in the root of your repository. Alternatively you can request creation of a metadata file in the E4S-Documenter repository. Metadata files in the E4S-Documenter repository must be created in a `data/<name>` subdirectory where `name` is the name of product repository.

Second, an entry must be added to the [url_list](https://github.com/E4S-Project/E4S-Documenter/blob/master/data/e4s_products.yaml). This can be done either by submitting a PR or registering an issue with the E4S-Documenter repo. Entries to the list require the URL to the product's repository, on its own line, formatted as in this example: 

`- repo_url: https://github.com/UO-OACISS/tau2`

When these two steps are complete the DocPortal will have the new entry available after its next nightly rebuild. A rebuild can also be launched by request for more immedeate confirmation of a successful update.
