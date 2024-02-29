from src import service,db

service.app_context().push()
db.drop_all()
db.create_all()

