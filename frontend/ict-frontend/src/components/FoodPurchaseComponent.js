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
  const [availableNames, setAvailableNames] = useState([]);


  const handleCustomerCreated = (receivedCustomerID) => {
    if (receivedCustomerID > 0) {
      setCustomerID(receivedCustomerID);
    } else {
      setCustomerID(1);
    }
  };


  useEffect(() => {
    setFoodName('');
    setAvailableNames([]);

    const fetchData = async () => {
      try {
        const response = await getInventory(customerID);

        setInventory(response.data);
        if (response.data && response.data.stock) {
          const foodTypes = Object.keys(response.data.stock);
          setFoodTypes(foodTypes);
          if (foodTypes.length > 0) {
            const selectedFoodType = foodTypes.includes(foodType) ? foodType : foodTypes[0];
            setFoodType(selectedFoodType);
            setAvailableNames(response.data.stock[selectedFoodType]?.map((item) => item.name) || []);
            setFlavors(response.data.flavors || []);
            setSelectedFlavor('');
          }
        }
      } catch (error) {
        console.error('Inventory fetch error:', error);
      }
    };

    fetchData();
  }, [customerID, foodType]);



  const handlePurchase = () => {
    console.log('Purchase button clicked');
    console.log('available names',availableNames);
    console.log('Purchase button clicked',customerID);
    console.log('Purchase button clicked',foodType);
    console.log('Purchase button quantity',quantity);
    console.log('Purchase button foodName',foodName);
    const selectedFoodName = foodName || (availableNames.length > 0 ? availableNames[0] : 'DefaultName');
    console.log(selectedFoodName);
    if (customerID && foodType && quantity && selectedFoodName) {
    console.log('Making API call...');
    buyFood(customerID, foodType, selectedFoodName, quantity, selectedFlavor)
      .then((response) => {
        console.log('API response:', response);
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
            {/*  <select*/}
            {/*  value={foodName}*/}
            {/*  onChange={(e) => setFoodName(e.target.value)}*/}
            {/*>*/}
            {/*  {availableNames.map((name, index) => (*/}
            {/*    <option key={index} value={name}>*/}
            {/*      {name}*/}
            {/*    </option>*/}
            {/*  ))}*/}
            {/*</select>*/}
              <select id={'foodName'}
                value={foodName}
                onChange={(e) => {
                  console.log('Selected value:', e.target.value);
                  console.log('Aavaialble names',availableNames);
                  setFoodName(e.target.value);
                }}
              >
                {Array.from(new Set(availableNames)).map((name) => (
              <option key={name} value={name}>
                {name}
              </option>
                ))}
              </select>
              {/*<select*/}
              {/*  value={foodName}*/}
              {/*  onChange={(e) => {*/}
              {/*    console.log('Selected value:', e.target.value);*/}
              {/*    setFoodName(e.target.value);*/}
              {/*  }}*/}
              {/*>*/}
              {/*  {availableNames.map((name, index) => (*/}
              {/*    <option key={index} value={name}>*/}
              {/*      {name}*/}
              {/*    </option>*/}
              {/*  ))}*/}
              {/*</select>*/}
            </label>
            <label>
              Flavor:
              <select
                value={selectedFlavor}
                onChange={(e) => {
                  console.log(foodName);
                  console.log(typeof(foodName));
                  setSelectedFlavor(e.target.value);}}
                  >
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
