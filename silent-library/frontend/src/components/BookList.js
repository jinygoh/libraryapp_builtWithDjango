// This component renders a list of books.
// It fetches the list of books from the backend and displays them.

import React, { useState, useEffect } from 'react';
// Import the pre-configured axios instance.
import axios from '../axios';

const BookList = () => {
    // Use the useState hook to manage the state of the books list.
    const [books, setBooks] = useState([]);

    // Use the useEffect hook to fetch the list of books when the component mounts.
    useEffect(() => {
        // This function fetches the list of books from the backend.
        const fetchBooks = async () => {
            // Make a GET request to the /books endpoint.
            const response = await axios.get('/books');
            // Set the books state variable with the data from the response.
            setBooks(response.data);
        };
        // Call the fetchBooks function.
        fetchBooks();
    }, []); // The empty array ensures that the effect is only run once, when the component mounts.

    return (
        <div>
            <h2>Books</h2>
            <ul>
                {/* Map over the books array and render a list item for each book. */}
                {books.map(book => (
                    <li key={book.id}>{book.title}</li>
                ))}
            </ul>
        </div>
    );
};

export default BookList;
