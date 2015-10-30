# scale-loadtest
The Grinder based load testing for SCALE.

## Requirements
This load testing is based on The Grinder.  You can get it 
from [http://grinder.sourceforge.net/](http://grinder.sourceforge.net/).

To run the tests, you'll need Apache Ant. You can get it from 
[http://ant.apache.org/](http://ant.apache.org/).  build.xml is configured to run
the agent process with the command 'ant'.

## Setup
- Edit build.xml so that grinder.location points to the installation
of The Grinder.

- Edit grinder.properties with the username, password, and webroot for the test.
The user should be a developer account.
