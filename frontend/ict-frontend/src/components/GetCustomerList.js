// frontend/src/components/CustomerList.js

import React, { useState, useEffect } from 'react';
import { customers } from '../api';

function CustomerList() {
  const [customerData, setCustomerData] = useState([]);

  useEffect(() => {
    customers()
      .then((response) => setCustomerData(response.data))
      .catch((error) => console.error(error));
  }, []);

  return (
    <div>
      <h2>Customers</h2>
      <ul>
        {customerData.map((customer) => (
          <li key={customer.id}>
            {customer.first_name} {customer.last_name} - {customer.email}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CustomerList;
