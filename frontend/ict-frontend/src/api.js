import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/',
});

export const getInventory = () => api.get('/api/get_inventory/');
export const customers = () => api.get('/customer/');
export const createCustomer = (customerData) => {
  return api.post('/customer/', customerData);
};

export const buyFood = (customer_id, food_type, selectedFoodName, quantity, flavor) => {
  return api.post('/api/buy_food/', {
    customer_id,
    food_type,
    name: selectedFoodName,
    quantity,
    flavor,
  });
};