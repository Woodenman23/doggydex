from website import create_app

app = create_app()

if __name__ == "__main__":
    ssl_context = (("certs/cert.pem", "certs/key.pem"),)
    app.run(host="0.0.0.0", port=5001, debug=True)
