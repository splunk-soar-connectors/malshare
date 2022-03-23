[comment]: # "Auto-generated SOAR connector documentation"
# MalShare

Publisher: Splunk  
Connector Version: 2\.1\.7  
Product Vendor: MalShare  
Product Name: MalShare  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.1\.0  

This app integrates with MalShare to provide several investigative actions

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a MalShare asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**api\_key** |  required  | password | MalShare API key

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[list hashes](#action-list-hashes) - List the MD5 hashes from the past 24 hours  
[list urls](#action-list-urls) - List the sample sources from the past 24 hours  
[get file info](#action-get-file-info) - Get the file details associated with a hash  
[get file](#action-get-file) - Get the file associated with a hash  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'list hashes'
List the MD5 hashes from the past 24 hours

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**file\_type** |  optional  | The file type to retrieve hashes for | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.md5 | string |  `md5` 
action\_result\.message | string | 
action\_result\.summary\.hash\_count | numeric | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.file\_type | string | 
action\_result\.data\.\*\.md5\.md5 | string | 
action\_result\.data\.\*\.md5\.sha1 | string | 
action\_result\.data\.\*\.md5\.sha256 | string |   

## action: 'list urls'
List the sample sources from the past 24 hours

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.source | string |  `url`  `file name` 
action\_result\.message | string | 
action\_result\.summary\.source\_count | numeric | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get file info'
Get the file details associated with a hash

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hash** |  required  | The hash of the file to be queried | string |  `sha256`  `sha1`  `md5` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.parameter\.hash | string |  `sha256`  `sha1`  `md5` 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.data\.\*\.SHA1 | string |  `sha1` 
action\_result\.data\.\*\.SOURCES | string |  `file name`  `url` 
action\_result\.data\.\*\.F\_TYPE | string | 
action\_result\.data\.\*\.SSDEEP | string | 
action\_result\.data\.\*\.SHA256 | string |  `sha256` 
action\_result\.data\.\*\.MD5 | string |  `md5` 
action\_result\.summary\.file\_info\_found | boolean |   

## action: 'get file'
Get the file associated with a hash

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hash** |  required  | The hash of the file to be queried | string |  `sha256`  `sha1`  `md5` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.parameter\.hash | string |  `sha256`  `sha1`  `md5` 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.data\.\*\.vault\_id | string |  `sha1`  `vault id` 
action\_result\.data\.\*\.name | string |  `md5` 
action\_result\.summary\.vault\_id | string |  `sha1`  `vault id` 
action\_result\.summary\.name | string |  `md5` 
action\_result\.summary\.file\_found | boolean | 