import React, { useState, useEffect } from 'react';
import { getInventory } from '../api';


function Inventory() {
  const [inventoryData, setInventoryData] = useState({
    ice_creams: [],
    shaved_ice: [],
    snack_bars: [],
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
        <h3>Ice Creams</h3>
        <ul>
          {inventoryData.ice_creams.map((iceCream) => (
            <li key={iceCream.id}>{iceCream.name}</li>
          ))}
        </ul>
      </div>
      <div>
        <h3>Shaved Ice</h3>
        <ul>
          {inventoryData.shaved_ice.map((shavedIce) => (
            <li key={shavedIce.id}>{shavedIce.name}</li>
          ))}
        </ul>
      </div>
      <div>
        <h3>Snack Bars</h3>
        <ul>
          {inventoryData.snack_bars.map((snackBar) => (
            <li key={snackBar.id}>{snackBar.name}</li>
          ))}
        </ul>
      </div>
      <div>
        <h3>Total Revenue</h3>
        <p>{inventoryData.total_revenue}</p>
      </div>
    </div>
  );
}

export default Inventory;
