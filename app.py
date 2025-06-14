from website import create_app, logger

app = create_app()

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(host="0.0.0.0", port=5001, debug=True)
    logger.info("Server started")
