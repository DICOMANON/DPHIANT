<p align="center">
  <img src="https://i.imgur.com/BuSnzG8.png" alt="logo" width="20%"/>
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
  DPHIANT is a tool to anonymize the personal health information contained inside DICOM files.
</p> 
<p align="center">
  🚧 This project (and the readme) is under developement 🚧
</p>

### Table of Contents
- [Getting Started](#getting-started)
- [Clone](#clone)
- [Setup](#setup)
- [Documentation](#documentation)
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

Dphiant Modality simulation: [http://localhost:8044](http://localhost:8044)
- Upload a DICOM image
- Open the study and select 'send to modality', select 'middleman'

Dphiant Middleman simulation: [http://localhost:8043](http://localhost:8043)
- Middleman serves as a temporary buffer to modify the images and for de-identification
- Automatically sends image to Dphiant PACS
- No interaction is needed here

Dphiant PACS simulation: [http://localhost:8042](http://localhost:8042)
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


### Documentation
Find our project's documentation files [here](https://github.com/DICOMANON/DPHIANT/tree/main/Documentation).  
You can find the Orthanc project [here](https://www.orthanc-server.com/).

## Contributors
 - [Ben Wilson](https://github.com/benmwilson)
 - [Nigam Lad](https://github.com/NigamLad)
 - [Yidu Guo](https://github.com/yiduguo-hp)
