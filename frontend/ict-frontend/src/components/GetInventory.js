import React, { useState, useEffect } from 'react';
import { getInventory } from '../api';

function Inventory() {
  const [inventoryData, setInventoryData] = useState({
    stock: {},
    total_revenue: 0,
  });

  useEffect(() => {
    getInventory()
      .then((response) => {
        // Log the response data
        console.log('Response Data:', response.data);
        setInventoryData(response.data);
      })
      .catch((error) => console.error(error));
  }, []);

  return (
    <div>
      <h2>Inventory</h2>
      <div>
        {Object.keys(inventoryData.stock).map((foodType) => (
          <div key={foodType}>
            <h3>{foodType}</h3>
            <ul>
              {inventoryData.stock[foodType].map((foodItem) => (
                <li key={foodItem.id}>{foodItem.name}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <div>
        <h3>Total Revenue</h3>
        <p>{inventoryData.total_revenue}</p>
      </div>
    </div>
  );
}

export default Inventory;
