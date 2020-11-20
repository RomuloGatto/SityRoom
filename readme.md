# SityRoom

This project has, as the main objective, the creation of multiple chat rooms. As side features, we have:

- Sign-in/Sign-up of users
- Limitation of the quantity of the messages to be shown
- A bot that expects the command /stock and returns the close price

## Pre Requisites

This project was developed on Windows, so you will need to install the packages below to run everything smooth
- Python 3.8+: `https://www.python.org/downloads/`
- Docker: `https://docs.docker.com/docker-for-windows/install/` 

If you are running it on MacOS/Ubunto, please run command bellow to install the packages needed:
```bash
sudo apt-get install python3.8
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

## Instalation

After cloning the repository, create and use a new environment to keep your personal data apart
```bash
py -m venv env
.\env\Scripts\activate
```

Use the package manager pip to install all required packages.
```bash
pip install -r requirements.txt
```

## Usage

You will need to run: 

- Docker image with RabbitMQ on it, to enable Bot running
```bash
docker run -d --hostname my-rabbit -p 15672:15672 -p 5672:5672 --name rabbit-server -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3-management
```
- Service Bot
```bash
python stooq/app.py
```

- Chat
```bash
python app.py
```

Then, you can simply access `http://127.0.0.1:5000/` on your browser and create your user.

If wanted, you can use our test data, we have 2 users pre-loaded:
| Email           | Username | Password  |
|-----------------|----------|-----------|
| test1@gmail.com | test1    | passTest1 |
| test2@gmail.com | test2    | passTest2 |
<br/>

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

Just remember to update the requirements packages if needed.
```bash
pip3 freeze > requirements.txt
```