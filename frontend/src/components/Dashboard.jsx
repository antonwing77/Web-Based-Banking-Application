import React, { useEffect, useState } from 'react';

function Dashboard() {
  const [accounts, setAccounts] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('http://localhost:8000/api/accounts/', {
      credentials: 'include'
    })
      .then(res => res.json())
      .then(data => setAccounts(data))
      .catch(() => setError('Could not fetch accounts'));
  }, []);

  return (
    <div className="dashboard-container">
      <h2>Your Accounts</h2>
      {error && <p className="error">{error}</p>}
      <ul>
        {accounts.map(acc => (
          <li key={acc.id}>
            Account #{acc.id} — Balance: ${acc.balance}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
