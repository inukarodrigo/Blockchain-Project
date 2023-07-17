import requests
import pandas as pd


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

    avg_min_between_sent_txns = (
            filtered_df[filtered_df['from'] == wallet_address.lower()]['timestamp'].diff() / pd.Timedelta(
        minutes=1)).mean()
    avg_min_between_received_txns = (
            filtered_df[filtered_df['to'] == wallet_address.lower()]['timestamp'].diff() / pd.Timedelta(
        minutes=1)).mean()
    time_diff_first_last = (filtered_df['timestamp'].max() - filtered_df['timestamp'].min()) / pd.Timedelta(minutes=1)
    sent_tnx = filtered_df[filtered_df['from'] == wallet_address.lower()].shape[0]
    received_tnx = filtered_df[filtered_df['to'] == wallet_address.lower()].shape[0]
    num_created_contracts = filtered_df[filtered_df['to'] == wallet_address.lower()]['iserror'].sum()
    max_val_received = filtered_df[filtered_df['to'] == wallet_address.lower()][
                           'value'].max() / 10 ** 18  # Convert from Wei to Ether
    avg_val_received = filtered_df[filtered_df['to'] == wallet_address.lower()][
                           'value'].mean() / 10 ** 18  # Convert from Wei to Ether
    avg_val_sent = filtered_df[filtered_df['from'] == wallet_address.lower()][
                       'value'].mean() / 10 ** 18  # Convert from Wei to Ether
    min_val_sent_to_contract = \
    filtered_df[(filtered_df['from'] == wallet_address.lower()) & (filtered_df['iserror'] == '1')][
        'value'].min() / 10 ** 18  # Convert from Wei to Ether

    # Calculate total ether received and sent
    total_ether_received = filtered_df[filtered_df['to'] == wallet_address.lower()]['value'].sum() / 10**18  # Convert from Wei to Ether
    total_ether_sent = filtered_df[filtered_df['from'] == wallet_address.lower()]['value'].sum() / 10**18  # Convert from Wei to Ether

    # Calculate ether balance
    ether_balance = total_ether_received - total_ether_sent

    # Output details using print function
    print(f"Wallet Address: {wallet_address}")
    print(f"Avg min between sent tnx: {avg_min_between_sent_txns:.2f} minutes")
    print(f"Avg min between received tnx: {avg_min_between_received_txns:.2f} minutes")
    print(f"Time Diff between first and last (Mins): {time_diff_first_last:.2f} minutes")
    print(f"Sent tnx: {sent_tnx}")
    print(f"Received Tnx: {received_tnx}")
    print(f"Number of Created Contracts: {num_created_contracts}")
    print(f"Max value received: {max_val_received:.6f} Ether")
    print(f"Avg value received: {avg_val_received:.6f} Ether")
    print(f"Avg value sent: {avg_val_sent:.6f} Ether")
    print(f"Min value sent to contract: {min_val_sent_to_contract:.6f} Ether")
    print(f"Total Ether sent: {total_ether_sent:.6f} Ether")
    print(f"Total Ether received: {total_ether_received:.6f} Ether")
    print(f"Total Ether Balance: {ether_balance:.6f} Ether")

    # Create a dictionary to store the metrics
    metrics_dict = {
        "wallet_address": wallet_address,
        "Avg_min_between_sent_tnx": avg_min_between_sent_txns,
        "Avg_min_between_received_tnx": avg_min_between_received_txns,
        "Time_Diff_between_first_and_last(Mins)": time_diff_first_last,
        "Sent_tnx": sent_tnx,
        "Received_tnx": received_tnx,
        "Number_of_Created_Contracts": num_created_contracts,
        "Max_Value_Received": max_val_received,
        "Avg_Value_Received": avg_val_received,
        "avg_val_sent": avg_val_sent,
        "total_ether_sent": total_ether_sent,
        "total_ether_received": total_ether_received,
        "Total_Ether_Balance": ether_balance,
        "ERC20_Total_Ether_Received": 0,
        "ERC20_Total_Ether_Sent": 0,
        "ERC20_Total_Ether_Sent_Contract": 0,
        "ERC20_Uniq_Sent_Addr": 0,
        "ERC20_Uniq_Rec_Token_Name": 0
    }

    return metrics_dict


if __name__ == "__main__":
    wallet_address = '0x4886635057704D03ab29541094e99Dca7C6A887C'
    get_wallet_details(wallet_address)
