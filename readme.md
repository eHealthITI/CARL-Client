# CARL RPi Client
Client application consuming data from local FIBARO Smart Home Home Center Lite (HCL) and devices/sensors and proxies them to the main CARL Server application.

# Tech Stack

![techstack](https://github.com/eHealthITI/ypostirizoclient/blob/master_test/img/tech_stack.png)


## Installation:
CARL Rpi Client's is supposed to be run on a **Raspberry Pi**. For production purposes you can deploy it  on your local machine with **docker**. 

###  Docker Deployment:   
 Clone the master branch. Copy .env.example as .env and fill the necessary information
 Once done, run the following commands.

    $ docker-compose up -d --build

This command creates **5** docker services that are defined in `docker-compose.yml`
* **db**: a dedicated service for our postgres database
* **web**: mandatory service to initiate the django server, apply migration, and initial data.
* **celery**: Handles all async tasks and messages received from redis
* **beat**: handles the scheduling of the async tasks
* **redis**: message broker for celery. 


In order to ensure that all services are up and running, run the following command:

    docker-compose ps 

## Apps:
![workflow](https://github.com/eHealthITI/ypostirizoclient/blob/master_test/img/workflow.png)
### Fibaro: 

Fibaro is responsible to get the data from HCL's API and store it on a local DB (`db_service`).
This app is consists of the following files: 
* [adapter.py](https://github.com/eHealthITI/ypostirizoclient/blob/master/fibaro/adapter.py): Adapter that handles the data that are generated by the Fibaro sensors
* [ypostirizo.py](https://github.com/eHealthITI/ypostirizoclient/blob/master/fibaro/ypostirizo.py): Adapter that is used to send data to CARL Cloud:
* [models.py](https://github.com/eHealthITI/ypostirizoclient/blob/master/fibaro/models.py): Has all the models that we use to store data.
    - Section: represents the section data that are fetched from the HCL API
    - Room: represents the room data that are fetched from the HCL API
    - Device: represents the device data that are fetched from the HCL API
    - Event: represents the event data that are fetched from the HCL API
* [exceptions.py](https://github.com/eHealthITI/ypostirizoclient/blob/master/fibaro/exceptions.py): Some custom exceptions 
* [validators.py](https://github.com/eHealthITI/ypostirizoclient/blob/master/fibaro/validators.py): Validators that are currently not used.

### Scheduler:
Scheduler is responsible for scheduling and executing the get and post requests between HCL and Cloud APIs respectively. It is consisted of 3 modules one for each platform. Each module has tasks.py file that has all the necessary tasks. 


* [Fibaro](https://github.com/eHealthITI/ypostirizoclient/tree/master/scheduler/Fibaro): Fetches the data from HCL via its API.
    - [tasks.py](https://github.com/eHealthITI/ypostirizoclient/blob/master/scheduler/Fibaro/tasks.py)
* [celery.py](https://github.com/eHealthITI/ypostirizoclient/blob/master/scheduler/celery.py): Scheduling configuration where we determine the frequency with which each task is run.
* [celeryconfig.py](https://github.com/eHealthITI/ypostirizoclient/blob/master/scheduler/celeryconfig.py): This is used as a configuration file for celery. 
