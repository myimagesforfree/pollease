# pollease
**Custom Slack integration for anonymous surveys/polls**

pollease: _What is my purpose?_

slack: _You create polls_

pollease: _Oh my god_

slack: _Yeah, welcome to the club, pal_

## Adding pollease to slack and debugging locally
1. Visit https://ngrok.com/download and download/install ngrok
2. Run `ngrok http 7000` (or whatever port is currently in run.sh) 
    - Note the HTTPS Forwarding URL (HTTPS_FORWARDING_URL)
3. Visit https://api.slack.com/apps?new_app=1
    - Use pollease as the name of the app
    - Select your team. 
    - Leave "I plan to submit this app to the Slack App Directory" unchecked for now.
4. Continue to configure pollease, the new Slack integration:
    - Under "OAuth & Permissions", paste the HTTPS_FORWARDING_URL, and append "/authorize" to the url.
    - Under "Interactive Messages", paste the HTTPS_FORWARDING_URL, and append "/interactive" to the url.
    - Under "Slash Commands", add "/pollease". Use HTTPS_FORWARDING_URL, and append "/pollease" to the url.
5. Configure pollease, the app server
    - Under "Basic Information", copy Client ID and Client Secret to config_local.py
6. Run `sh build.sh`
    - This compiles the docker image
7. Run `sh run.sh`
    - This starts a new container with the pollease server image
8. Add pollease to your Slack team
    - Edit add-to-slack.html and insert your Client ID
    - Open add-to-slack.html in a browser and click the button. 
9. If everything goes correctly, the app should now be added to your team and the /pollease command should be functional. All HTTP requests will now be tunnelled to your localhost.

## Tests
1. To run tests, you must have already built the pollease image via step 6 of the setup process.
2. Run `sh build_test.sh` to build the test image.
3. Run `sh test.sh` to run the test package in a container.