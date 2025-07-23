// This component renders a search page for books.
// It contains a form for users to enter a search query and a list of search results.

import React, { useState } from 'react';
// Import the pre-configured axios instance.
import axios from '../axios';

const Search = () => {
    // Use the useState hook to manage the state of the search query and the search results.
    const [query, setQuery] = useState('');
    const [books, setBooks] = useState([]);

    // This function is called when the search form is submitted.
    const handleSearch = async (e) => {
        // Prevent the default form submission behavior.
        e.preventDefault();
        // Make a GET request to the /books/search endpoint with the search query.
        const response = await axios.get(`/books/search?q=${query}`);
        // Set the books state variable with the data from the response.
        setBooks(response.data);
    };

    return (
        <div>
            {/* The search form calls the handleSearch function when it is submitted. */}
            <form onSubmit={handleSearch}>
                {/* The input field for the search query is bound to the query state variable. */}
                <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} />
                <button type="submit">Search</button>
            </form>
            <ul>
                {/* Map over the books array and render a list item for each book. */}
                {books.map(book => (
                    <li key={book.id}>{book.title}</li>
                ))}
            </ul>
        </div>
    );
};

export default Search;
