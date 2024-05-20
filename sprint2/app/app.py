import logging
import os

from flask import Flask


app = Flask(__name__)
current_directory = os.getcwd()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(current_directory, "logs", "app.log"))
logger.addHandler(file_handler)


@app.route("/")
def hello_world():
    msg = "Hola mundo desde Flask!"
    
    logger.info(msg)

    return msg


@app.route("/error")
def error():
    msg = "Error!"
    
    logger.error(msg)

    return msg


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
