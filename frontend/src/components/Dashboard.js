/**
 * This component displays the user's dashboard, including their borrowed books and reviews.
 */
import React, { useState, useEffect } from 'react';
import UserService from '../services/UserService';

const Dashboard = () => {
  // State variables for the user's loans and reviews
  const [loans, setLoans] = useState([]);
  const [reviews, setReviews] = useState([]);

  // useEffect hook to fetch the dashboard data when the component mounts
  useEffect(() => {
    // Call the getDashboard method from the UserService
    UserService.getDashboard().then(
      (response) => {
        // Set the state with the data from the API
        setLoans(response.data.loans);
        setReviews(response.data.reviews);
      },
      (error) => {
        // Handle errors from the API
        console.log(error);
      }
    );
  }, []);

  return (
    <div className="container">
      <header className="jumbotron">
        <h3>Dashboard</h3>
      </header>
      <div>
        <h4>Your Loans</h4>
        <ul className="list-group">
          {loans.map((loan) => (
            <li key={loan.id} className="list-group-item">
              {loan.book.title} (Due: {loan.due_date})
            </li>
          ))}
        </ul>
      </div>
      <div className="mt-3">
        <h4>Your Reviews</h4>
        <ul className="list-group">
          {reviews.map((review) => (
            <li key={review.id} className="list-group-item">
              {review.book.title}: {review.review_text} (Rating: {review.rating})
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;
