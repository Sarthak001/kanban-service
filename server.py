from src import config, service

if __name__ == "__main__":
    service.run(host=config.HOST,
                port=config.PORT,
                debug=config.DEBUG)
