from src import service,db

service.app_context().push()
db.create_all()

