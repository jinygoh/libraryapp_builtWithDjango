/**
 * This component provides a search bar for users to search for books.
 */
import React, { useState } from 'react';
import BookService from '../services/BookService';
import { Link } from 'react-router-dom';

const Search = () => {
  // State variables for the search query and the list of books
  const [query, setQuery] = useState('');
  const [books, setBooks] = useState([]);

  /**
   * Handles the form submission for book search.
   * @param {object} e - The event object.
   */
  const handleSearch = (e) => {
    e.preventDefault();
    // Call the searchBooks method from the BookService
    BookService.searchBooks(query).then((response) => {
      // Set the state with the data from the API
      setBooks(response.data.books);
    });
  };

  return (
    <div>
      <form onSubmit={handleSearch}>
        <div className="form-group">
          <label htmlFor="query">Search for books</label>
          <input
            type="text"
            className="form-control"
            name="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        <div className="form-group">
          <button className="btn btn-primary btn-block">Search</button>
        </div>
      </form>

      <ul className="list-group">
        {books.map((book) => (
          <li key={book.id} className="list-group-item">
            <Link to={`/book/${book.id}`}>{book.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Search;
