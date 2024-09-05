from app import create_app # The app initialization logic is typically placed in a factory function called create_app, which helps in configuring the app based on different environments.

# Call the 'create_app' function to initialize the Flask app
app = create_app() 

# This ensures the application runs only if the script is executed directly (not imported as a module).
if __name__ == '__main__': 
    # Run app in debug mode to collect logs
    app.run(debug=True) 
