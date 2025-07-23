// This component renders the details of a single book.
// It fetches the book's details from the backend and displays them.

import React, { useState, useEffect } from 'react';
// Import the useParams hook from react-router-dom to get the book's ID from the URL.
import { useParams } from 'react-router-dom';
// Import the pre-configured axios instance.
import axios from '../axios';

const BookDetail = () => {
    // Get the book's ID from the URL.
    const { id } = useParams();
    // Use the useState hook to manage the state of the book.
    const [book, setBook] = useState(null);

    // Use the useEffect hook to fetch the book's details when the component mounts or the ID changes.
    useEffect(() => {
        // This function fetches the book's details from the backend.
        const fetchBook = async () => {
            // Make a GET request to the /books/{id} endpoint.
            const response = await axios.get(`/books/${id}`);
            // Set the book state variable with the data from the response.
            setBook(response.data);
        };
        // Call the fetchBook function.
        fetchBook();
    }, [id]); // The effect is re-run whenever the ID changes.

    // If the book is not yet loaded, display a loading message.
    if (!book) {
        return <div>Loading...</div>;
    }

    // Render the book's details.
    return (
        <div>
            <h2>{book.title}</h2>
            <p>ISBN: {book.isbn}</p>
            <p>Total Copies: {book.totalCopies}</p>
            <p>Available Copies: {book.availableCopies}</p>
        </div>
    );
};

export default BookDetail;
