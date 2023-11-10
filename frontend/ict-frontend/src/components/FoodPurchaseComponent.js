import React, { useState, useEffect } from 'react';
import { buyFood, getInventory } from '../api';
import CustomerForm from './CustomerForm';
import '../styles/FoodPurchaseComponent.css';

function FoodPurchaseComponent() {
  const [inventory, setInventory] = useState({});
  const [customerID, setCustomerID] = useState();
  const [foodType, setFoodType] = useState('');
  const [quantity, setQuantity] = useState(2);
  const [foodTypes, setFoodTypes] = useState([]);
  const [purchaseResponse, setPurchaseResponse] = useState(null);
  const [foodName, setFoodName] = useState('');
  const [flavors, setFlavors] = useState([]);
  const [selectedFlavor, setSelectedFlavor] = useState('');

  const handleCustomerCreated = (receivedCustomerID) => {
    if (receivedCustomerID > 0) {
      setCustomerID(receivedCustomerID);
    } else {
      setCustomerID(1);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getInventory(customerID);
        setInventory(response.data);
        if (response.data && response.data.stock) {
          const foodTypes = Object.keys(response.data.stock);
          setFoodTypes(foodTypes);
          if (foodTypes.length > 0) {
            setFoodType((prevFoodType) => {
              const selectedFoodType = foodTypes.includes(prevFoodType) ? prevFoodType : foodTypes[0];
              setFoodName(response.data.stock[selectedFoodType]?.[0]?.name || '');
              setFlavors(response.data.flavors || []);
              return selectedFoodType;
            });
          }
        }
      } catch (error) {
        console.error('Inventory fetch error:', error);
      }
    };

    fetchData();
  }, [customerID]);

  const handlePurchase = () => {
    if (customerID && foodType && quantity && foodName) {
      buyFood(customerID, foodType, foodName, quantity, selectedFlavor)
        .then((response) => {
          setPurchaseResponse(response.data);
        })
        .catch((error) => {
          console.error('Purchase error:', error);
        });
    }
  };


  return (
    <div className="food-purchase-container">
      <h1>Food Purchase</h1>
      {customerID === undefined || customerID === null ? (
        <CustomerForm onCustomerCreated={handleCustomerCreated} />
      ) : (
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
                onChange={(e) => setFoodType(e.target.value)}>
                {foodTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Name:
              <select
                value={foodName}
                onChange={(e) => setFoodName(e.target.value)}>
                {inventory.stock[foodType]?.map((item) => (
                  <option key={item.name} value={item.name}>
                    {item.name}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Flavor:
              <select
                value={selectedFlavor}
                onChange={(e) => setSelectedFlavor(e.target.value)}>
                {flavors.map((flavor) => (
                  <option key={flavor} value={flavor}>
                    {flavor}
                  </option>
                ))}
              </select>
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
      )}
    </div>
  );
}

export default FoodPurchaseComponent;
