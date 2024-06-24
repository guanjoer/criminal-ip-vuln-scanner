import os
from dotenv import load_dotenv
import requests
import streamlit as st
import pandas as pd

# Load envirement variables in .env file
load_dotenv()

# Use env varable
api_key = os.getenv('API_KEY')


# Check connection to Criminal IP API Server
def is_connection(api_key):
    url = "https://api.criminalip.io/v1/user/me"
      
    payload={}
    headers = {
        "x-api-key": api_key
    }

    res = requests.request("POST", url, headers=headers, data=payload)
    res_data = res.json() # Get JSON Format

    if res_data['status'] == 200:
        return True
    else:
        return res_data['status']
    

# Fetch Summary Info    
def get_summary_data(ip, api_key):
    url = f"https://api.criminalip.io/v1/asset/ip/summary?ip={ip}"

    payload={}
    headers = {
        "x-api-key": api_key
    }

    res = requests.request("GET", url, headers=headers, data=payload)
    res_data = res.json()

    return res_data

# Fetch Malicious Data
def get_malicious_data(ip, api_key):
    url = f"https://api.criminalip.io/v1/feature/ip/malicious-info?ip={ip}"

    payload={}
    headers = {
        "x-api-key": api_key
    }

    res = requests.request("GET", url, headers=headers, data=payload)
    res_data = res.json()
    
    return res_data

# Fetch Open Ports Info
def get_ports_info(data):
    ports = []
    open_ports = data['current_opened_port']['data']
    for port_info in open_ports:
        port = port_info['port']
        protocol = port_info.get('protocol', 'N/A')
        product_name = port_info.get('product_name', 'N/A')
        product_version = port_info.get('product_version', 'N/A')
        confirmed_time = str(port_info.get('confirmed_time', 'N/A'))
        has_vuln = str(port_info.get('has_vulnerability', 'N/A'))

        ports.append((port, protocol, product_name, product_version, confirmed_time, has_vuln))

    table_data = pd.DataFrame(ports, columns=['Open Port', 'Protocol', 'Product', 'Version', 'Confirmed', 'Vulnerability'], index=range(1, len(ports) + 1))

    return table_data


# Fetch Vuln Info
def get_vuln_info(data):
    vulns = []

    vulns_info = data['vulnerability']['data']

    for vuln_info in vulns_info:
        tcp_port = vuln_info['ports']['tcp']
        cve_id = vuln_info.get('cve_id', 'N/A')
        cvssv3_score = vuln_info.get('cvssv3_score', 'N/A')
        product_name = vuln_info.get('product_name', 'N/A')
        product_version = vuln_info.get('product_version', 'N/A')

        vulns.append((tcp_port, cve_id, cvssv3_score, product_name, product_version))

    df = pd.DataFrame(vulns, columns=['Port', 'CVE ID', 'CVSSV3 Score', 'Product', 'Version'],  index=range(1, len(vulns) + 1))
    return df


# Fetch IP Adress 
def get_ip_address(data):
    return data['ip']


# Fetch Location
def get_location(data):
    locator = 'City, Region, Country, PostalCode, Latitude, Longitude'
    return f"{data['city']}, {data['region']}, {data['country']}, {data['postal_code']}, {data['latitude']}, {data['longitude']} | {locator}" 


# main
def main():
    st.title("Criminal IP Vulnerablity Scanner")

    ip_addr = st.text_input("Enter a Target IP Address: ")
    search_btn = st.button("Search")

    if search_btn:
        if not ip_addr:
            st.error("Please enter a valid IP address.")
        else:
            with st.spinner('Fetching data...'):
                connection = is_connection(api_key) # True or False
                if connection: # True
                    data_summary = get_summary_data(ip_addr, api_key) # Summary Data
                    data_malicious = get_malicious_data(ip_addr, api_key) # Malicious Data

                    st.header("Results")

                    st.subheader("Summary") # Summary Section

                    st.markdown(f"<span style='font-size:17px; font-weight:bold;'>IP Address: </span>{get_ip_address(data_summary)}", unsafe_allow_html=True)

                    st.markdown(f"<span style='font-size:17px; font-weight:bold;'>Location: </span>{get_location(data_summary)}", unsafe_allow_html=True)

                    st.markdown(f"<span style='font-size:17px; font-weight:bold;'>ISP: </span>{data_summary['isp']}", unsafe_allow_html=True)

                    st.markdown(f"<span style='font-size:17px; font-weight:bold;'>VPN: </span>{data_malicious['is_vpn']}", unsafe_allow_html=True)

                    st.markdown(f"<span style='font-size:17px; font-weight:bold;'>Malicious: </span>{data_malicious['is_malicious']}", unsafe_allow_html=True)

                    st.markdown(f"<span style='font-size:17px; font-weight:bold;'>Inbound Score: </span>{data_summary['score']['inbound']}", unsafe_allow_html=True)

                    st.markdown(f"<span style='font-size:17px; font-weight:bold;'>Outbound Score: </span>{data_summary['score']['outbound']}", unsafe_allow_html=True)

                    st.subheader("Open Ports") # Open Ports Section
                    st.markdown(f"**Total:** {data_malicious['current_opened_port']['count']}", unsafe_allow_html=True)
                    
                    st.table(get_ports_info(data_malicious))

                    st.subheader("Vulnerabilities") # Vulnerablilities Section
                    st.markdown(f"**Total:** {data_malicious['vulnerability']['count']}", unsafe_allow_html=True)

                    st.dataframe(get_vuln_info(data_malicious))
                else:
                    st.error(f"Error: Status - {connection}")


# Run streamlit App
if __name__ == '__main__':
    main()     