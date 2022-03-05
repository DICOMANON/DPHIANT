<p align="center">
<!--   <img src="" alt="logo" width="20%"/> -->
</p>
<h1 align="center">
  DPHIANT
</h1>
<h3 align="center"><i>
  "DICOM Personal Health Information Anonymization Tool"
  </i></h3>
<p align="center">
  
</p>

<p align="center">
  DPHIANT is a plugin to anonymize the personal health information contained inside DICOM files.
</p> 
<p align="center">
  🚧 This project (and the readme) is under developement 🚧
</p>

### Table of Contents
- [Getting Started](#getting-started)
  - [Clone](#clone)
  - [Setup](#setup)
    - [Dependencies](#dependencies)
  - [Documentation](#documentation)
- [Install](#install)
- [Usage](#usage)
- [License](#license)
- [Contributors](#contributors)

## Getting Started
### Clone
For prerequisites and detailed build instructions please read the [Installation](#install) instructions. Once the dependencies are installed, run:
```bash
# clone dphiant repo
git clone https://github.com/dicomanon/dphiant.git
cd dphiant
```

### Setup

To start the setup, type: `docker-compose up --build` in your project path.
This will begin to install the various images and dependencies required to run the Orthanc servers through Docker.

Once the three Orthanc servers have started up, use the details below to login.

LOGIN/PASSWORD = demo/demo

Orthanc Modality simulation: [http://localhost:8044](http://localhost:8044)
- Upload a DICOM image
- Open the study and select 'send to modality', select 'middleman'

Orthanc Middleman simulation: [http://localhost:8043](http://localhost:8043)
- Middleman serves as a temporary buffer to modify the images and for de-identification
- Automatically sends image to Orthanc PACS
- No interaction is needed here

Orthanc PACS simulation: [http://localhost:8042](http://localhost:8042)
- View the modified DICOM image sent from Middleman server

Mongo Express: [http://localhost:8081](http://localhost:8081)
- View the MongoDB database via the Mongo Express browser interface

Mongo Database:
- Use this sample to access MongoDB programatically within the container
```
from pymongo import MongoClient

client = MongoClient(
            host = 'mongodb://mongo:27017',
            serverSelectionTimeoutMS = 3000,
            username="root",
            password="example",
)
```

- Use this sample to access MongoDB programatically from outside the container
```
from pymongo import MongoClient

client = MongoClient(
            host = 'mongodb://localhost:27017/',
            serverSelectionTimeoutMS = 3000,
            username="root",
            password="example",
)
```


#### Dependencies
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras rutrum, sapien quis efficitur eleifend, magna velit scelerisque est, ut porttitor augue ante non lectus. Curabitur.

### Documentation
Find our project's documentation files [here](Documentation/).  
You can find the Orthanc project [here](https://www.orthanc-server.com/).

## Install
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras rutrum, sapien quis efficitur eleifend, magna velit scelerisque est, ut porttitor augue ante non lectus. Curabitur.

## Usage
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras rutrum, sapien quis efficitur eleifend, magna velit scelerisque est, ut porttitor augue ante non lectus. Curabitur.

## License
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras rutrum, sapien quis efficitur eleifend, magna velit scelerisque est, ut porttitor augue ante non lectus. Curabitur.

## Contributors
 - [Ben Wilson](https://github.com/benmwilson)
 - [Nigam Lad](https://github.com/NigamLad)
 - [Yidu Guo](https://github.com/yiduguo-hp)
