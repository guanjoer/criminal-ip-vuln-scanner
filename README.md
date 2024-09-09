# Criminal IP API OSINT

This is a Python-based **OSINT** using the [Criminal IP API](https://www.criminalip.io/ko/developer/api/post-user-me) about specified IP address.

## Output Information

- **Location**
- **ISP**
- **VPN(True/False)**
- **Inbound Score**
- **Outbound Score**
- **Open Ports**
- **Services**
- **Vulnerabilities**

## Example Output

**Summary:**

<img src="./images/summary.PNG" width="70%">

**Open Ports:**

<img src="./images/open-ports.PNG" width="70%">

**Vulnerabilites:**

<img src="./images/vulnerabilites.PNG" width="70%">


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/guanjoer/osint-criminalip-api.git
   cd osint-criminalip-api
   ```
2. Install the dependencies:

	`pip install -r requirements.txt`

3. Create a `.env` file in the root directory and add your Criminal IP API key:

	`API_KEY=your_api_key`


## Usage

To run the application, execute the following command:

`streamlit run osint_criminalip_api.py`

This will start a local web server, and you can access the application by navigating to http://localhost:8501 in your web browser.


## Disclaimer

This tool is intended for educational purposes and lawful use only. Use this tool responsibly.

Unauthorized access to systems, data theft, or any form of misuse is strictly prohibited and may result in severe legal consequences. By using this tool, you agree to take full responsibility for your actions and comply with all applicable laws and regulations.

## Acknowledgements

- [Criminal IP](https://www.criminalip.io/) for providing the API used in this project.
- [Streamlit](https://streamlit.io/) for the web application framework.
