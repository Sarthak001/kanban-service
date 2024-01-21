from src import config, app

if __name__ == "__main__":
    service.run(host= config.HOST,
                port= config.PORT,
                debug= config.DEBUG)