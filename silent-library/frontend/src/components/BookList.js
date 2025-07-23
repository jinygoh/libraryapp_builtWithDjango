import React, { useState, useEffect } from 'react';
import axios from '../axios';

const BookList = () => {
    const [books, setBooks] = useState([]);

    useEffect(() => {
        const fetchBooks = async () => {
            const response = await axios.get('/books');
            setBooks(response.data);
        };
        fetchBooks();
    }, []);

    return (
        <div>
            <h2>Books</h2>
            <ul>
                {books.map(book => (
                    <li key={book.id}>{book.title}</li>
                ))}
            </ul>
        </div>
    );
};

export default BookList;
