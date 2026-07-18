**Unreleased**
* Remove beautifulsoup4 from requirements.txt
* Prevent transport error messages from exposing the MalShare API key.
* Verify downloaded sample content against the requested hash before writing it to the vault.
* Marked the get file action as mutating because it writes downloaded samples to the SOAR vault.
