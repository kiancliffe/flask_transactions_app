# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]


# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)
    

# Create operation
@app.route('/add', methods=["GET", "POST"])
def add_transaction():
    if request.method == 'GET':
        return render_template('form.html')
    
    if request.method == 'POST':
        # Create a new transaction object using form field values
        new_transaction = {
            'id': len(transactions)+1,  # Generate a new ID based on the current length of the transactions list
            'date': request.form['date'], # Get the 'date' field value from the form
            'amount': float(request.form['amount']) # Get the 'amount' field value from the form and convert it to a float
        }
        # Append the new transaction to the transactions list
        transactions.append(new_transaction)
        # Redirect to the transactions list page after adding the new transaction
        return redirect(url_for("get_transactions"))
    

# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):

    if request.method == 'GET':

        data_for_form = next((t for t in transactions if t['id'] == transaction_id), None)

        if data_for_form:

            return render_template('edit.html', transaction=data_for_form)

        else: 
            return ({"message": "Transaction not found"}, 404)
    
    
    if request.method == 'POST':

        updated_transaction = {
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }

        for transaction in transactions:
            if transaction_id == transaction['id']:
                transaction.update(updated_transaction)
                break

        return redirect(url_for("get_transactions"))


# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    
    # iterates through transactions to match user passed id to delete entry
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break 

    return redirect(url_for("get_transactions"))
        

@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    
    if request.method == 'POST':
        # Get min and max calues from search form
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])
        # Instantiate a list for filtered content
        filtered_transactions = []
        # Find values withing constraints of min and max values that were entered by user
        for transaction in transactions:
            if transaction['amount'] <= max_amount and transaction['amount'] >= min_amount:
                # If value found add to new filter list
                filtered_transactions.append(transaction)
        # Return user to transaction page with new filtered transactions
        return render_template("transactions.html", transactions=filtered_transactions)

    return render_template('search.html')

@app.route("/balance")
def total_balance():
    
    total : float = 0

    for transaction in transactions:
        total += float(transaction['amount'])

    # Alternate solution found online
    # total = sum(float(transaction['amount']) for transaction in transactions)

    return render_template('transactions.html', transactions=transactions, total=total)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
    