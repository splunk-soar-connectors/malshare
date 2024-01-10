[comment]: # "Auto-generated SOAR connector documentation"
# MalShare

Publisher: Splunk  
Connector Version: 2.1.8  
Product Vendor: MalShare  
Product Name: MalShare  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 5.1.0  

This app integrates with MalShare to provide several investigative actions

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a MalShare asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**api_key** |  required  | password | MalShare API key

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
**file_type** |  optional  | The file type to retrieve hashes for | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.data.\*.md5 | string |  `md5`  |   64584e3e6a53cf2b078f363575826c8b 
action_result.message | string |  |   Hash count: 485  No hashes processed from hash list. 
action_result.summary.hash_count | numeric |  |   485  0 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.file_type | string |  |   PE32 
action_result.data.\*.md5.md5 | string |  |   8b61ca6d1254da43b8643d478acf485f 
action_result.data.\*.md5.sha1 | string |  |   7d6f0f1f281bbc1446fcb8f42213c0d542557375 
action_result.data.\*.md5.sha256 | string |  |   bdf3eac218cda881ec145d4b3c650fc26b5fe434dcefc971686819f85447f334   

## action: 'list urls'
List the sample sources from the past 24 hours

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.data.\*.source | string |  `url`  `file name`  |   http://trelawnyrose.com/immcld.exe 
action_result.message | string |  |   Source count: 862 
action_result.summary.source_count | numeric |  |   862 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'get file info'
Get the file details associated with a hash

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hash** |  required  | The hash of the file to be queried | string |  `sha256`  `sha1`  `md5` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.message | string |  |   File info found: True 
action_result.parameter.hash | string |  `sha256`  `sha1`  `md5`  |   64584e3e6a53cf2b078f363575826c8b  637015ee34d7a22de65b9eb24ed75105  e35c9d795e7fb1db54465ef46d70efe6  91a61e3be9cc7251972f6ee8d4836cb4 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   0  1 
action_result.data.\*.SHA1 | string |  `sha1`  |   a4a0a781622de17cb20c4982d5e24efd674627d9  2c31bbb3a0fcbfc0052ee75f649be4313480b739  f78c091a623c605e74511dd80d1a48376c2c4145 
action_result.data.\*.SOURCES | string |  `file name`  `url`  |   http://top-rank.eu/dll.exe  http://oyasinsaat.com.tr/86hHYU6  http://shiftspace.ro/87wifhFsdf 
action_result.data.\*.F_TYPE | string |  |   PE32 
action_result.data.\*.SSDEEP | string |  |   768:CnIhn202izqt/rngcsP2u5BFs7PEA+NTIbBdz/7+0g8YaAAaiOIEOf3yb1f:Cni2ezMsums4A+Ns1Fq0a2ywf3c1f  6144:z/wRc2KcrO6z6DuINvYRC+bBRkSDWE0veY6g6FjcvDvOh6Iis2fhBLF3a0tH+R:Em2ZrO6zLVS48WY6g6d6IiLflqI  6144:DyjTcM92KcrO6z6DuINvYRC+bBRkSDWE0veY6g6FjcvDvOh6Iis2fhBLF3a0tH+y:jo2ZrO6zLVS48WY6g6d6IiLflqI 
action_result.data.\*.SHA256 | string |  `sha256`  |   dd598071d081d02bde1aadf7fcadd59c78e30a8307b552da8f6cce6c5c39fa78  6d5d672d9e8402a4e6a2309c71443e93efccccee8f9959afc24ae9a89fe2935c  3d653771933422f9a081ea122865da76edde83cdeb41b8b8e377833e75e21aca 
action_result.data.\*.MD5 | string |  `md5`  |   637015ee34d7a22de65b9eb24ed75105  e35c9d795e7fb1db54465ef46d70efe6  91a61e3be9cc7251972f6ee8d4836cb4 
action_result.summary.file_info_found | boolean |  |   True  False   

## action: 'get file'
Get the file associated with a hash

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**hash** |  required  | The hash of the file to be queried | string |  `sha256`  `sha1`  `md5` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.message | string |  |   Vault id: 51fbcaba1f6832dae1d3b8060a874e71c52e93c8
Name: ec091d840d8e6e179804cf5a2ea81e58
File found: True 
action_result.parameter.hash | string |  `sha256`  `sha1`  `md5`  |   64584e3e6a53cf2b078f363575826c8b  c1736b814389cb6602329186c8181b35  ec091d840d8e6e179804cf5a2ea81e58 
summary.total_objects | numeric |  |   2  1 
summary.total_objects_successful | numeric |  |   0  1 
action_result.data.\*.vault_id | string |  `sha1`  `vault id`  |   db0680862044d6c60a410388c93955c2c757002f  51fbcaba1f6832dae1d3b8060a874e71c52e93c8 
action_result.data.\*.name | string |  `md5`  |   c1736b814389cb6602329186c8181b35  ec091d840d8e6e179804cf5a2ea81e58 
action_result.summary.vault_id | string |  `sha1`  `vault id`  |   db0680862044d6c60a410388c93955c2c757002f  51fbcaba1f6832dae1d3b8060a874e71c52e93c8 
action_result.summary.name | string |  `md5`  |   c1736b814389cb6602329186c8181b35  ec091d840d8e6e179804cf5a2ea81e58 
action_result.summary.file_found | boolean |  |   True  False 