# Entry point
from thu_messaging.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
