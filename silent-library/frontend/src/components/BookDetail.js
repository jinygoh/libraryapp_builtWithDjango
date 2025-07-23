import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from '../axios';

const BookDetail = () => {
    const { id } = useParams();
    const [book, setBook] = useState(null);

    useEffect(() => {
        const fetchBook = async () => {
            const response = await axios.get(`/books/${id}`);
            setBook(response.data);
        };
        fetchBook();
    }, [id]);

    if (!book) {
        return <div>Loading...</div>;
    }

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
