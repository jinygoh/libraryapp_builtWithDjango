import React, { useState } from 'react';
import axios from '../axios';

const Search = () => {
    const [query, setQuery] = useState('');
    const [books, setBooks] = useState([]);

    const handleSearch = async (e) => {
        e.preventDefault();
        const response = await axios.get(`/books/search?q=${query}`);
        setBooks(response.data);
    };

    return (
        <div>
            <form onSubmit={handleSearch}>
                <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} />
                <button type="submit">Search</button>
            </form>
            <ul>
                {books.map(book => (
                    <li key={book.id}>{book.title}</li>
                ))}
            </ul>
        </div>
    );
};

export default Search;
