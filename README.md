# canlii_data_miner
Generates a report of all of the decisions cited by a decision hosted on
CanLII. Accepts a valid CanLII URL as input.

## V 0.3.2
* Completed and incorporated the metadata API call
* Added unformatted metadata to the standard report

## TODO
* Format the metadata in the standard report
* Cache results "offline" for faster/future results
* Replace urllib (& json) with requests
  * Depreciate json_tools.generate\_json()
* Design and implement a Decision class
