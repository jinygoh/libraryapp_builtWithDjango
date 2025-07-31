/**
 * This component is the home page of the application.
 * It displays a welcome message and the book search component.
 */
import React from 'react';
import Search from './Search';

const Home = () => {
  return (
    <div>
      <h1>Welcome to the Silent Library</h1>
      <Search />
    </div>
  );
};

export default Home;
