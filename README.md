# Google Sheet to Zalando stock updater

A simple Python script, which pulls the information about your articles and stock from a Google Sheet 
spreadsheet and sends it to Zalando via [Fashion Connector Importer API](https://docs.partner-solutions.zalan.do/en/fci/index.html)
at the beginning of every hour.

## Installation

We assume that you've already passed Zalando KYC process and obtained the client ID, API key and store ID.

1. Enable Google Sheet API
2. Generate a Service Account Key [[example](https://m2msupport.net/m2msupport/generate-service-account-key-in-google-cloud-platform-gcp/)] and save it as `client_secret.json`
3. Create a Google Sheet with the [required](https://docs.partner-solutions.zalan.do/en/fci/getting-started.html#stock-update-columns) structure. Use the headers.
4. Share this Google Sheet with the Service Account as described [here](https://robocorp.com/docs/development-guide/google-sheets/interacting-with-google-sheets#create-a-new-google-sheet-and-add-the-service-account-as-an-editor-to-it)
5. Clone this repository and run `pip install -r requirements.txt`
6. Update `settings.ini` with Zalando credentials and spreadsheet ID
7. (Optional) Update `zalando-updater.service` with the correct installation paths, copy it to `/ets/systemd/system` and run `sudo systemctl enable zalando-updater.service` and then `sudo systemctl start zalando-updater.service`
8. (Alternatively) Run `python3 main.py`

## Author

(C) Constantine Kulak, 2022.