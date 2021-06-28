# time-tracking
Automate ServiceNow time tracking

Pre-launch steps:
1. Make sure selenium is installed for Python
2. Update config.ini keys with relevant information (see below)
3. Edit code and uncomment line 78 - submit.click()


Config.ini keys:
1. Username = {Windows username}
2. Browser = {Preferred browser. Can be one of the following: Chrome, Safari, Edge, Firefox}
3. BrowserDriverPath = {Local directory path where you installed your browser's driver}
4. TogglApiToken = {API token for Toggl found in account settings}
5. TogglEmail = {Email address used to sign into Toggl}
6. TogglWorkspaceId = {No longer needed}


External API link: https://github.com/matthewdowney/TogglPy
Toggl API: https://github.com/toggl/toggl_api_docs
