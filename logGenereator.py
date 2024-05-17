# pip install streamlit==1.34.0
# pip install numpy==1.26.0


# streamlit run analyseLogs.py

#  RUN With Reload

# streamlit run analyseLogs.py --server.runOnSave=True

import streamlit as st
import pandas as pd
from urllib.parse import urlparse
import json
import base64


def decode_jwt(token):
    try:

        firstPart = token.split(".")[1]
        decoded = base64.urlsafe_b64decode(firstPart).decode("utf-8")
        decoded = json.loads(decoded)
        return decoded
    except Exception as e:
        return None


st.set_page_config(layout="wide")


SUCCESS_RANGE = [200, 299]
BAD_REQUEST_RANGE = [400, 499]
SERVER_ERROR_RANGE = [500, 599]


def main():
    st.title("Logs Analyser")
    # st.write("")

    #  here user can upload file

    #  divide into 2 columns: 1 for file upload and 2nd for direct content input

    col1, col2 = st.columns(2)

    PROCESS = False
    PROCESS_V2 = False

    CONSIDER_UPLOAD = False
    CONSIDER_DIRECT_INPUT = False

    with col1:
        st.write("Upload File")

        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            file_contents = uploaded_file.getvalue()
            # st.write(file_contents)
            file_contents_1 = file_contents.decode("utf-8")
            PROCESS = True
            CONSIDER_UPLOAD = True

    with col2:
        st.write("Direct Text Input")
        file_contents_2 = st.text_area("Enter Text", height=100)
        if file_contents_2:
            PROCESS = True
            CONSIDER_DIRECT_INPUT = True

    if CONSIDER_UPLOAD & CONSIDER_DIRECT_INPUT:
        st.error("Select Only One Option to Proceed, Currently Both are Selected")
    else:
        PROCESS_V2 = True

    if PROCESS & PROCESS_V2:

        if CONSIDER_UPLOAD:
            st.success("Using File Upload")
            file_contents = file_contents_1
        else:
            st.success("Using Direct Text Input")
            file_contents = file_contents_2

        contents = []

        for index, line in enumerate(file_contents.split("\n")):
            try:
                contents.append(json.loads(line))
            except Exception as e:
                pass
                # print(f"Error in line {index}: {e}")
                # st.write(f"Error in line {index}: {e}")

        FILTERED_TOKEN = False

        # if len(contents) == 0:
        #     st.warning("No Data Found")
        #     return

        for c in contents:
            api = c.get("api")
            parsed_url = urlparse(api)
            endpoint = parsed_url.path
            c["endpoint"] = endpoint
            c["headers"] = json.loads(c["headers"])
            # print(c["headers"])
            user_id = None
            if not FILTERED_TOKEN:
                try:
                    token = c["headers"]["AUTHORIZATION"]
                    if token == "***FILTERED***":
                        FILTERED_TOKEN = True
                        continue
                    token = token.split(" ")[1]
                    decoded_token = decode_jwt(token)
                    user_id = decoded_token.get("user_id")
                except Exception as e:
                    # print(e)
                    pass

            c["user_id"] = user_id

        all_keys = list(set(contents[0].keys()))

        # print(all_keys)
        # ['added_on', 'api', 'headers', 'body', 'method', 'client_ip_address', 'response', 'status_code', 'execution_time', 'endpoint']

        #  set checkbox for all keys

        defaukt_keys_selected = ['method', "endpoint", 'body', 'response', 'status_code', 'execution_time']  # ['added_on', 'api', 'headers', 'body', 'method', 'client_ip_address', 'response', 'status_code', 'execution_time']

        selected_keys = st.multiselect("Select Keys", all_keys, defaukt_keys_selected)

        #  Analysis

        #  write excel like table where columsn is selected keys and rows are data

        df = pd.DataFrame(contents)

        if FILTERED_TOKEN:
            st.warning("Token is filtered, can't decode user_id")

        st.write(df[selected_keys])

        #  boolean for additional analysis

        if st.checkbox("Advanced Analysis"):
            st.title("Advanced Analysis")

            # -----------  Total Hits Count -----------

            total_requests = len(df)

            st.write(f"Total Requests: {total_requests}")
            st.write("-----------------------------")

            # -----------  Total Hits Count with status code -----------

            unique_endpoints = df["endpoint"].unique()

            unique_endpoints_df = []

            for endpoint in unique_endpoints:
                total_count_hit = df[df["endpoint"] == endpoint].shape[0]

                all_status_codes = df[df["endpoint"] == endpoint]["status_code"].values

                sucess_count = len([x for x in all_status_codes if x in SUCCESS_RANGE])
                bad_request_count = len([x for x in all_status_codes if x in BAD_REQUEST_RANGE])
                server_error_count = len([x for x in all_status_codes if x in SERVER_ERROR_RANGE])
                avg_execution_time = df[df["endpoint"] == endpoint]["execution_time"].mean()

                unique_endpoints_df.append({"endpoint": endpoint, "Hits": total_count_hit, "Success": sucess_count, "Bad Request": bad_request_count, "Server Error": server_error_count, "Avg Execution Time": avg_execution_time})

            endpoints_df = pd.DataFrame(unique_endpoints_df)

            st.write(f"Total Unique Endpoints: {len(unique_endpoints)}")

            st.write("API Hits by Endpoint with status code range")

            st.write(endpoints_df)
            st.write("-----------------------------")

            # -----------  Analyze header -----------

            #  Unique USER_AGENT for all requests

            user_agents = df["headers"].apply(lambda x: x.get("USER_AGENT", "NA")).unique()
            user_agents_df = []

            for user_agent in user_agents:
                user_agents_df.append({"User Agent": user_agent, "Hits": len(df[df["headers"].apply(lambda x: x.get("USER_AGENT", "NA")) == user_agent])})

            st.write("API Hits by User Agent")
            st.write(pd.DataFrame(user_agents_df))
            st.write("-----------------------------")

            #  Unique User

            users = df["user_id"].unique()

            users_df = []

            for user in users:
                users_df.append({"User Id": user, "Hits": len(df[df["user_id"] == user])})

            st.write("API Hits by User Id")
            st.write(pd.DataFrame(users_df))
            st.write("-----------------------------")

            # Unique IP Address

            ip_addresses = df["client_ip_address"].unique()

            ip_addresses_df = []

            for ip_address in ip_addresses:
                ip_addresses_df.append({"IP Address": ip_address, "Hits": len(df[df["client_ip_address"] == ip_address])})

            st.write("API Hits by IP Address")
            st.write(pd.DataFrame(ip_addresses_df))
            st.write("-----------------------------")


if __name__ == "__main__":
    main()
