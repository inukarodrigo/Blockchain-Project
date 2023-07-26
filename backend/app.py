from flask import Flask, request, jsonify
from data_retrieve import get_wallet_details, preprocess_data, predict_with_saved_model

app = Flask(__name__, static_folder="../client/dist", static_url_path="/")


# Add a new API route to call get_wallet_details(wallet_address)
@app.route('/send_transaction', methods=['POST'])
def handle_send_transaction():
    current_account = request.json.get('currentAccount')
    if not current_account:
        return jsonify({'error': 'Invalid currentAccount parameter'}), 400

    wallet_information = get_wallet_details(current_account)
    pre_processed_wallet_information = preprocess_data(wallet_information)
    model_result = predict_with_saved_model(pre_processed_wallet_information)
    print("Model result: ", model_result)
    # You can process the result as needed and return any response to the frontend
    return jsonify(model_result), 200


# Serve the React frontend
@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)
