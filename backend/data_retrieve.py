import requests
import pandas as pd
import joblib
import numpy as np
from keras.models import load_model


def get_wallet_details(wallet_address):
    # Rinkeby Etherscan API endpoint for transaction list
    etherscan_api_url = 'https://api-sepolia.etherscan.io/api'

    # Your Etherscan API Key (You can obtain a separate API key for Rinkeby)
    api_key = 'FUZSDV4FWBTUZK3YJUFUH4TF4TDDE61ZDV'

    # API parameters for Rinkeby
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': wallet_address,
        'apikey': api_key
    }

    # Make API call to Rinkeby Etherscan
    response = requests.get(etherscan_api_url, params=params)
    data = response.json()['result']

    # Make API call to Etherscan's ERC20 token transfer API
    params_erc20 = {
        'module': 'account',
        'action': 'tokentx',
        'address': wallet_address,
        'apikey': api_key
    }
    response_erc20 = requests.get(etherscan_api_url, params=params_erc20)
    data_erc20 = response_erc20.json()['result']

    # Convert data to DataFrame
    pd.set_option('display.max_columns', 20)
    df = pd.DataFrame(data)
    df.head(10)
    # Convert 'from' and 'to' columns to lowercase strings
    df['from'] = df['from'].astype(str)
    df['to'] = df['to'].astype(str)

    # Convert column names to lowercase
    df.columns = df.columns.str.lower()

    # Convert 'from' and 'to' columns to lowercase
    df['from'] = df['from'].str.lower()
    df['to'] = df['to'].str.lower()

    # Convert 'timestamp' column to numeric (integer) format
    df['timestamp'] = df['timestamp'].astype(int)

    # Filter out rows with invalid timestamps (e.g., non-numeric values)
    df = df.dropna(subset=['timestamp'])

    # Convert 'timestamp' column to datetime format (assuming it's in seconds since epoch)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')

    # Convert 'value' column to integers
    df['value'] = df['value'].astype('int64')

    # Check the actual column names in the DataFrame
    # print(df.columns)

    # Filter transactions for the target account
    filtered_df = df.loc[(df['from'] == wallet_address.lower()) | (df['to'] == wallet_address.lower())]
    # print(filtered_df)

    # Calculate metrics

    # Convert 'timestamp' column to datetime format (assuming it's in seconds since epoch)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')

    # Filter out rows with invalid timestamps (e.g., non-numeric values)
    df = df.dropna(subset=['timestamp'])

    avg_min_between_sent_txns = (filtered_df[filtered_df['from'] == wallet_address.lower()]['timestamp'].diff() / pd.Timedelta(minutes=1)).mean()
    avg_min_between_received_txns = (filtered_df[filtered_df['to'] == wallet_address.lower()]['timestamp'].diff() / pd.Timedelta(minutes=1)).mean()
    time_diff_first_last = (filtered_df['timestamp'].max() - filtered_df['timestamp'].min()) / pd.Timedelta(minutes=1)
    sent_tnx = filtered_df[filtered_df['from'] == wallet_address.lower()].shape[0]
    received_tnx = filtered_df[filtered_df['to'] == wallet_address.lower()].shape[0]
    num_created_contracts = filtered_df[filtered_df['to'] == wallet_address.lower()]['iserror'].sum()
    max_val_received = filtered_df[filtered_df['to'] == wallet_address.lower()]['value'].max() / 10 ** 18  # Convert from Wei to Ether
    avg_val_received = filtered_df[filtered_df['to'] == wallet_address.lower()]['value'].mean() / 10 ** 18  # Convert from Wei to Ether
    avg_val_sent = filtered_df[filtered_df['from'] == wallet_address.lower()]['value'].mean() / 10 ** 18  # Convert from Wei to Ether
    min_val_sent_to_contract = filtered_df[(filtered_df['from'] == wallet_address.lower()) & (filtered_df['iserror'] == '1')]['value'].min() / 10 ** 18  # Convert from Wei to Ether

    # Calculate total ether received and sent
    total_ether_received = filtered_df[filtered_df['to'] == wallet_address.lower()]['value'].sum() / 10 ** 18  # Convert from Wei to Ether
    total_ether_sent = filtered_df[filtered_df['from'] == wallet_address.lower()]['value'].sum() / 10 ** 18  # Convert from Wei to Ether

    # Calculate ether balance
    ether_balance = total_ether_received - total_ether_sent

    # Calculate total unique addresses from which the account received transactions
    total_unique_received_from_addresses = filtered_df[filtered_df['to'] == wallet_address.lower()]['from'].nunique()

    # Calculate the total number of transactions (including transactions to create contracts)
    total_transactions = filtered_df.shape[0]

    # Process ERC20 token transfer data and calculate additional metrics
    total_ERC20_tnxs = len(data_erc20)
    ERC20_uniq_rec_addr = len(set(entry['from'] for entry in data_erc20))
    ERC20_uniq_rec_contract_addr = len(set(entry['contractAddress'] for entry in data_erc20))
    ERC20_min_val_rec = min(int(entry['value']) for entry in data_erc20) / 10 ** 18
    ERC20_Uniq_Rec_Token_Name = len(set(entry['tokenSymbol'] for entry in data_erc20))

    # Output details using print function
    print(f"Wallet Address: {wallet_address}")
    print(f"Avg min between sent tnx: {avg_min_between_sent_txns:.2f} minutes")
    print(f"Avg min between received tnx: {avg_min_between_received_txns:.2f} minutes")
    print(f"Time Diff between first and last (Mins): {time_diff_first_last:.2f} minutes")
    print(f"Sent tnx: {sent_tnx}")
    print(f"Received Tnx: {received_tnx}")
    print(f"Total Unique Addresses from which account received transactions: {total_unique_received_from_addresses}")
    print(f"Number of Created Contracts: {num_created_contracts}")
    print(f"Max value received: {max_val_received:.6f} Ether")
    print(f"Avg value received: {avg_val_received:.6f} Ether")
    print(f"Total Transactions (including tnx to create contract): {total_transactions}")
    print(f"Avg value sent: {avg_val_sent:.6f} Ether")
    print(f"Min value sent to contract: {min_val_sent_to_contract:.6f} Ether")
    print(f"Total Ether sent: {total_ether_sent:.6f} Ether")
    print(f"Total Ether received: {total_ether_received:.6f} Ether")
    print(f"Total Ether Balance: {ether_balance:.6f} Ether")
    print(f"Total ERC20 Transactions: {total_ERC20_tnxs:.6f}")
    print(f"ERC20 Unique Received Addresses: {ERC20_uniq_rec_addr:.6f}")
    print(f"ERC20 Unique Received Contract Addresses: {ERC20_uniq_rec_contract_addr:.6f}")
    print(f"ERC20 Minimum Value Received: {ERC20_min_val_rec:.6f} Ether")
    print(f"ERC20 Unique Received Token Names: {ERC20_Uniq_Rec_Token_Name:.6f}")

    # Create a dictionary to store the metrics
    metrics_dict = {
        "Avg_min_between_received_tnx": avg_min_between_received_txns,
        "Time_Diff_between_first_and_last(Mins)": time_diff_first_last,
        "Sent_tnx": sent_tnx,
        "Received_tnx": received_tnx,
        "Total_Unique_Addresses_Received_From": total_unique_received_from_addresses,
        "Max_Value_Received": max_val_received,
        "Avg_Value_Received": avg_val_received,
        "Total_Transactions": total_transactions,
        "total_ether_sent": total_ether_sent,
        "total_ether_received": total_ether_received,
        "total_ERC20_tnxs ": total_ERC20_tnxs,
        "ERC20_uniq_rec_addr": ERC20_uniq_rec_addr,
        "ERC20_uniq_rec_contract_addr": ERC20_uniq_rec_contract_addr,
        "ERC20_min_val_rec": ERC20_min_val_rec,
        "ERC20_Uniq_Rec_Token_Name": ERC20_Uniq_Rec_Token_Name
    }

    metrics_list = list(metrics_dict.values())

    return metrics_list

def preprocess_data(new_data):
    # Converting new data into a numpy array
    new_data_array = np.array([new_data])

    # Load the scaler from the file
    loaded_scaler = joblib.load('scaler.pkl')

    # Standardize the new data using the loaded scaler
    new_data_scaled = loaded_scaler.transform(new_data_array)

    # Reshape the new data to match the LSTM input shape
    num_features = 15
    new_data_reshaped = new_data_scaled.reshape(new_data_scaled.shape[0], num_features, 1)
    return new_data_reshaped

def predict_with_saved_model(pre_processed_data):
    # Load the trained model
    loaded_model = load_model('trained_LSTM_model.h5')

    predictions = loaded_model.predict(pre_processed_data)
    binary_predictions = np.round(predictions).astype(int)
    return binary_predictions[0][0]


if __name__ == "__main__":
    wallet_address1 = '0x4886635057704D03ab29541094e99Dca7C6A887C'
    wallet_address2 = '0xCeCDC9F411392133701Ac1e22Bddaa9167f7ca04'
    # get_wallet_details(wallet_address2)

    # Load the scaler from the file
    # loaded_scaler = joblib.load('scaler.pkl')

    # Load the trained model
    # loaded_model = load_model('trained_LSTM_model.h5')

    # Sample data for testing the code
    new_data1 = get_wallet_details(wallet_address1)
    new_data2 = [1093.71, 704785.63, 721, 89, 40, 45.806785, 6.589513, 810, 865.6910932, 586.4666748, 265, 54, 58, 0, 57]
    new_data3 = [18.93, 631.75, 2, 2, 2, 0.511002, 0.505501, 4, 1.010036, 1.011002, 1, 1, 1, 0, 1]

    ## Pre procesing the data

    # Standardize the new data using the loaded scaler
    # new_data_scaled = loaded_scaler.transform(new_data1)

    # Reshape the new data to match the LSTM input shape
    # num_features = 15
    # new_data_reshaped = new_data_scaled.reshape(new_data_scaled.shape[0], num_features, 1)

    # predictions = loaded_model.predict(new_data_reshaped)
    # binary_predictions = np.round(predictions).astype(int)
    # print(binary_predictions)

    clean_data = preprocess_data(new_data3)
    print(predict_with_saved_model(clean_data))
