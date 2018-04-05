# Welcome to RestSim
*RestSim* is a Flask application to simulate any REST service

# Assumptions
 1. Linux environment
 2. GET requests

# Getting started
 1. Install python dependencies
    ```bash
    $ pip install -r requirements.txt
    ```
 2. Start RestSim
    ```bash
    $ python restsim.py
    ```
 3. Test your setup
	```bash
	# Default username password admin/secret
	$ curl http://127.0.0.1:4000/acme/profile -u admin:secret
	{
		"name": "Acme Corporation",
		"city": "Tunis"
	}
	$ curl http://127.0.0.1:4000/acme/employee/1 -u admin:secret
	{
		"id": 1,
		"name": "Zied",
		"lastname": "Maktouf",
		"position": "CEO"
	}
	```
 4. Add your own test data by creating the file system hierarchy, matching the URL, inside the folder *data*.

	`GET acme/profile` returns the content of the file `<app-dir>/data/acme/profile.json`
	
	`GET acme/employee/1` returns the content of the file `<app-dir>/data/acme/employee/1.json`
