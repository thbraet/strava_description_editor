# strava_description_editor
Automatically update the description of your Strava activiy

# Run the app locally
Run the command `flask run` and an instance of the app will be started on `127.0.0.1:5000`

If you want to use a "public" domain for e.g. the authentication callback, you can use ngrok to create a temporary URL which if forwarded to your localost
`ngrok http 5000`

This will give you a URL (e.g. ` https://2aea-81-164-42-28.ngrok-free.app`) which you will need to enter as the callback URL of your Strava app before further experimentation.