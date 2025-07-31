/**
 * This component displays the details of a single book, including its reviews.
 */
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import BookService from '../services/BookService';

const Book = () => {
  // Get the book ID from the URL params
  const { id } = useParams();
  // State variables for the book and its reviews
  const [book, setBook] = useState(null);
  const [reviews, setReviews] = useState([]);

  // useEffect hook to fetch the book data when the component mounts or the ID changes
  useEffect(() => {
    // Call the getBook method from the BookService
    BookService.getBook(id).then((response) => {
      // Set the state with the data from the API
      setBook(response.data.book);
      setReviews(response.data.reviews);
    });
  }, [id]);

  // If the book is not yet loaded, display a loading message
  if (!book) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>{book.title}</h2>
      <p>
        <strong>Authors:</strong>{' '}
        {book.authors.map((author) => `${author.first_name} ${author.last_name}`).join(', ')}
      </p>
      <p>
        <strong>Genres:</strong> {book.genres.map((genre) => genre.genre).join(', ')}
      </p>
      <p>
        <strong>ISBN:</strong> {book.isbn}
      </p>
      <p>
        <strong>Available Copies:</strong> {book.available_copies}
      </p>

      <hr />

      <h3>Reviews</h3>
      <ul className="list-group">
        {reviews.map((review) => (
          <li key={review.id} className="list-group-item">
            <p>
              <strong>{review.user.username}</strong> (Rating: {review.rating})
            </p>
            <p>{review.review_text}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Book;
