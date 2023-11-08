import React, { useState, useEffect } from 'react';
import { buyFood, getInventory } from '../api';
import CustomerForm from './CustomerForm';
import '../styles/FoodPurchaseComponent.css';

function FoodPurchaseComponent() {
  const [inventory, setInventory] = useState({});
  const [customerID, setCustomerID] = useState(1); // Default value is 1
  const [foodType, setFoodType] = useState('');
  const [foodID, setFoodID] = useState(1);
  const [quantity, setQuantity] = useState(2);
  const [foodTypes, setFoodTypes] = useState([]);
  const [purchaseResponse, setPurchaseResponse] = useState(null);

  const handleCustomerCreated = (customerID) => {
    setCustomerID(customerID || 1); // Set to 1 if customerID is falsy
  };

  useEffect(() => {
    getInventory()
      .then((response) => {
        setInventory(response.data);
        if (response.data && response.data.stock) {
          const foodTypes = Object.keys(response.data.stock);
          setFoodTypes(foodTypes);
          if (foodTypes.length > 0) {
            setFoodType(foodTypes[0]);
          }
        }
      })
      .catch((error) => {
        console.error('Inventory fetch error:', error);
      });
  }, []);

  const handlePurchase = () => {
    buyFood(customerID, foodType, foodID, quantity)
      .then((response) => {
        setPurchaseResponse(response.data);
      })
      .catch((error) => {
        console.error('Purchase error:', error);
      });
  };

  return (
    <div className="food-purchase-container">
      <h1>Food Purchase</h1>
      <CustomerForm onCustomerCreated={handleCustomerCreated} />
      {customerID !== null ? (
        <div>
          <div className="purchase-form">
            <label>
              Customer ID:
              <input type="number" value={customerID} disabled />
            </label>
            <label>
              Food Type:
              <select
                value={foodType}
                onChange={(e) => setFoodType(e.target.value)}
              >
                {foodTypes.map((foodType) => (
                  <option key={foodType} value={foodType}>
                    {foodType}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Food ID:
              <input
                type="number"
                value={foodID}
                onChange={(e) => setFoodID(e.target.value)}
              />
            </label>
            <label>
              Quantity:
              <input
                type="number"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
              />
            </label>
            <button onClick={handlePurchase}>Purchase Food</button>
          </div>
          {purchaseResponse && (
            <div className="purchase-response">
              <h3 style={{ color: purchaseResponse.message === 'ENJOY!' ? 'green' : 'red' }}>
                {purchaseResponse.message}
              </h3>
            </div>
          )}
        </div>
      ) : null}
    </div>
  );
}

export default FoodPurchaseComponent;
