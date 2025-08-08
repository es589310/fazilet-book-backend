const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Check if we're on the client side
const isClient = typeof window !== 'undefined';

// Book types
interface Author {
  id: number;
  name: string;
  biography: string;
  birth_date: string | null;
  death_date: string | null;
  photo: string | null;
  nationality: string;
}

interface Category {
  id: number;
  name: string;
  description: string;
  is_active: boolean;
  books_count: number;
}

interface Book {
  id: number;
  title: string;
  slug: string;
  authors: Author[];
  category: Category;
  price: string;
  original_price: string | null;
  cover_image: string;
  is_featured: boolean;
  is_bestseller: boolean;
  is_new: boolean;
  average_rating: number;
  reviews_count: number;
  discount_percentage: number;
  stock_quantity: number;
}

interface BookListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Book[];
}

// API functions
export async function fetchBooks(params: Record<string, string> = {}): Promise<BookListResponse> {
  const url = new URL(`${BASE_URL}/books/`);
  Object.entries(params).forEach(([key, value]) => {
    url.searchParams.append(key, value);
  });
  
  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch books');
  }
  
  return response.json();
}

export async function fetchFeaturedBooks(): Promise<BookListResponse> {
  const response = await fetch(`${BASE_URL}/books/featured/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch featured books');
  }
  
  return response.json();
}

export async function fetchBestsellerBooks(): Promise<BookListResponse> {
  const response = await fetch(`${BASE_URL}/books/bestsellers/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch bestseller books');
  }
  
  return response.json();
}

export async function fetchNewBooks(): Promise<BookListResponse> {
  const response = await fetch(`${BASE_URL}/books/new/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch new books');
  }
  
  return response.json();
}

export async function fetchCategories(): Promise<Category[]> {
  const response = await fetch(`${BASE_URL}/books/categories/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch categories');
  }
  
  return response.json();
}

export async function fetchBookStats(): Promise<{
  total_books: number;
  featured_books: number;
  bestsellers: number;
  new_books: number;
}> {
  const response = await fetch(`${BASE_URL}/books/stats/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch book stats');
  }
  
  return response.json();
}

// Export types
export type { Book, Author, Category, BookListResponse };
