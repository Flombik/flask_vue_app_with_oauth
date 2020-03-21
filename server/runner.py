from server.app import app, db
from flask_cors import CORS
from flask_migrate import MigrateCommand
from flask_script import Manager, Shell

manager = Manager(app)
CORS(app, resources={r'/*': {'origins': '*'}})


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
