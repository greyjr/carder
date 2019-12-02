from app import app
from workbench.blueprint import workbench
import view

app.register_blueprint(workbench, url_prefix='/workbench')

if __name__ == '__main__':
	app.run(debug=True)