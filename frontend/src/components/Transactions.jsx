import React, { useEffect, useState } from 'react';

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('http://localhost:8000/api/transactions/', {
      credentials: 'include'
    })
      .then(res => res.json())
      .then(data => setTransactions(data))
      .catch(() => setError('Could not fetch transactions'));
  }, []);

  return (
    <div className="dashboard-container">
      <h2>Transaction History</h2>
      {error && <p className="error">{error}</p>}
      <ul>
        {transactions.map(tx => (
          <li key={tx.id}>
            {tx.date}: {tx.type} ${tx.amount} — {tx.description}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Transactions;
