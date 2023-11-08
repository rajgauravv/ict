import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import GetInventory from './components/GetInventory';
import CustomerList from './components/GetCustomerList';
import FoodPurchaseComponent from './components/FoodPurchaseComponent';
import CustomerForm from './components/CustomerForm';

function AppRouter() {
  return (
    <Router>
        <h1>Welcome to Ice Cream Truck App</h1>
      <Routes>
        <Route path="/api/get_inventory" element={<GetInventory />} />
        <Route path="/customer" element={<CustomerList />} />
        <Route path="/api/buy_food" element={<FoodPurchaseComponent />} />
        <Route path="/customer/create" element={<CustomerForm />} /> {/* Add this route */}
      </Routes>
    </Router>
  );
}

export default AppRouter;
