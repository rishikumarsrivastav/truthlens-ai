from flask import Flask, send_from_directory
from App.routes import api

app = Flask(
    __name__,
    static_folder="Static",
    static_url_path=""
)

# Register API under /api
app.register_blueprint(api, url_prefix="/api")


@app.route("/")
def home():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(debug=True)