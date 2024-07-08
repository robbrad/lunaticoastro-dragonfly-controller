# Lunaticoastro Dragonfly Controller
Python code serves as a client that controls and queries a dome (DragonFly Dome) controller over a network, allowing it to send commands, and fetch relay and sensor data remotely.

Once the container is running you can open the API at http://<container_ip>:8080/api/ui/

# DragonFly Dome Controller  
This Docker container provides an isolated environment for running a server that interfaces with the DragonFly Dome controller, allowing remote command sending and data retrieval.  

## Getting Started  

These instructions will cover usage information and for the docker container.  

## DockerHub
The image is available on the Docker Hub at [robbrad182/dragonfly-dome-controller:latest](https://hub.docker.com/r/robbrad182/dragonfly-dome-controller)

### Prerequisites  

You need Docker installed on your system. You can download it from [Docker's website](https://www.docker.com/products/docker-desktop).  

### Installing  
Clone the repository to get the required files:  

```bash 
git clone https://github.com/robbrad/lunaticoastro-dragonfly-controller.git 
cd lunaticoastro-dragonfly-controller
```

### Building the Docker Image

Build the Docker image using the following command:

```bash 
docker build -t dragonfly-dome-controller .
```

This command builds the Docker image with the tag `dragonfly-dome-controller`, using the Dockerfile from the current directory.

### Environment Variables

You need to set the following environment variables:

*   `DRAGONFLY_IP`: IP address of the DragonFly Dome controller.
*   `DRAGONFLY_PORT`: Port on which the DragonFly Dome controller is listening.

These can be set directly in the docker run command or through a `.env` file.

### Running the Container

To run the container with the environment variables set, use the following command:

bashCopy code

`docker run -d -p 8080:8080 --env DRAGONFLY_IP=192.168.x.x --env DRAGONFLY_PORT=10000 dragonfly-dome-controller`

Replace `192.168.x.x` with the actual IP address of your DragonFly Dome controller.

### Additional Commands

*   To stop the container, find the container ID with `docker ps` and then stop it with `docker stop <container-id>`.
*   To remove the container once stopped, use `docker rm <container-id>`.
*   To view logs from the running container, use `docker logs <container-id>`.

Built With
----------

*   [Python](https://www.python.org/) - The programming language used.
*   [Docker](https://www.docker.com/) - Containerization platform.

Authors
-------

*   **Robert Bradley** - _Initial work_ - [robbrad](https://github.com/robbrad)

License
-------

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

Acknowledgments
---------------

*   Miguel Angel García Grande
*   Jaime Alemany
*   [lunaticoastro.com](lunaticoastro.com)

