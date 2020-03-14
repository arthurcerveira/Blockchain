# Blockchain

<a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.6-green.svg"></a>

A simple blockchain implemented in Python with Flask.

## Getting Started

You can either run the application with a docker container or on your machine.

### Running the application with docker

#### Prerequisites

The only tool needed to run this container is Docker.

#### Instructions

To run the image for this docker container, run the following command

```
docker container run -d -p 5000:<port> arthurcerveira/blockchain
```

The port argument represents which port will be exposed to the host.

### Running the application on your machine

#### Prerequisites

For running this project you need a Python 3.6 or higher and pip3.

#### Instructions

For installing you need git to clone the repository and install the requirements

```
git clone https://github.com/arthurcerveira/Blockchain.git
cd Blockchain
pip3 install -r requirements.txt
```

To create a node you can run the following command

```
python3 network.py <port>
```

The port argument represents which port will be accessed, the default value is 5000.

## Built With

The blockchain structure was implemented with built-in Python tools. The network was implemented with the web framework Flask and the requests library.

- [Flask](https://palletsprojects.com/p/flask/) - The Python micro framework for building web applications
- [requests](https://pypi.org/project/requests/) - An elegant and simple HTTP library for Python

## Motivation

This project was created to learn more about the Blockchain architecture and study the use of cryptography in a real application.
