/**
 * Production-ready API integration for Dostum Kitab
 * Handles all API calls with proper error handling and types
 */

// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const API_TIMEOUT = 10000 // 10 seconds

// Types
export interface Book {
  id: number
  title: string
  slug: string
  description: string
  price: number
  original_price?: number
  cover_image?: string
  cover_imagekit_url?: string
  is_featured: boolean
  is_bestseller: boolean
  is_new: boolean
  category: Category
  authors: Author[]
  average_rating: number
  reviews_count: number
  stock_quantity: number
  created_at: string
}

export interface Category {
  id: number
  name: string
  slug: string
  description?: string
  image?: string
  imagekit_url?: string
  is_active: boolean
}

export interface Author {
  id: number
  name: string
  biography?: string
  photo?: string
  photo_imagekit_url?: string
  nationality?: string
}

export interface BookReview {
  id: number
  book: number
  user?: number
  anonymous_user?: number
  rating: number
  comment: string
  created_at: string
}

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  name?: string // Fallback for backward compatibility
}

export interface AuthResponse {
  success: boolean
  access?: string
  refresh?: string
  user?: User
  error?: string
}

// API Error Handler
class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string
  ) {
    super(message)
    this.name = 'APIError'
  }
}

// Fetch wrapper with timeout and error handling
async function apiFetch(endpoint: string, options: RequestInit = {}): Promise<Response> {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT)

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })

    clearTimeout(timeoutId)

    if (!response.ok) {
      throw new APIError(
        `HTTP ${response.status}: ${response.statusText}`,
        response.status
      )
    }

    return response
  } catch (error) {
    clearTimeout(timeoutId)
    
    if (error instanceof APIError) {
      throw error
    }
    
    if (error.name === 'AbortError') {
      throw new APIError('Zaman aşımı', 408, 'TIMEOUT')
    }
    
    throw new APIError('Şəbəkə xətası', 0, 'NETWORK_ERROR')
  }
}

// Books API
export const fetchBooks = async (params?: {
  page?: number
  page_size?: number
  category?: string
  search?: string
  ordering?: string
}): Promise<{ results: Book[]; count: number; next?: string; previous?: string }> => {
  try {
    const searchParams = new URLSearchParams()
    
    if (params?.page) searchParams.append('page', params.page.toString())
    if (params?.page_size) searchParams.append('page_size', params.page_size.toString())
    if (params?.category) searchParams.append('category', params.category)
    if (params?.search) searchParams.append('search', params.search)
    if (params?.ordering) searchParams.append('ordering', params.ordering)
    
    const queryString = searchParams.toString()
    const endpoint = `/api/books/${queryString ? `?${queryString}` : ''}`
    
    const response = await apiFetch(endpoint)
    const data = await response.json()
    
    return data
  } catch (error: unknown) {
    if (error instanceof APIError) {
      throw new APIError('Kitablar yüklənə bilmədi', error.status, error.code)
    }
    throw new APIError('Kitablar yüklənə bilmədi', 500)
  }
}

export const fetchBook = async (slug: string): Promise<Book> => {
  try {
    const response = await apiFetch(`/api/books/${slug}/`)
    const data = await response.json()
    
    return data
  } catch (error: unknown) {
    if (error instanceof APIError) {
      throw new APIError('Kitab məlumatları yüklənə bilmədi', error.status, error.code)
    }
    throw new APIError('Kitab məlumatları yüklənə bilmədi', 500)
  }
}

export const fetchFeaturedBooks = async (): Promise<Book[]> => {
  try {
    const response = await apiFetch('/api/books/featured/')
    const data = await response.json()
    
    return data.results || data
  } catch (error: unknown) {
    if (error instanceof APIError) {
      throw new APIError('Seçilmiş kitablar yüklənə bilmədi', error.status, error.code)
    }
    throw new APIError('Seçilmiş kitablar yüklənə bilmədi', 500)
  }
}

export const fetchBestsellerBooks = async (): Promise<Book[]> => {
  try {
    const response = await apiFetch('/api/books/bestsellers/')
    const data = await response.json()
    
    return data.results || data
  } catch (error: unknown) {
    if (error instanceof APIError) {
      throw new APIError('Bestseller kitablar yüklənə bilmədi', error.status, error.code)
    }
    throw new APIError('Bestseller kitablar yüklənə bilmədi', 500)
  }
}

export const fetchNewBooks = async (): Promise<Book[]> => {
  try {
    const response = await apiFetch('/api/books/new/')
    const data = await response.json()
    
    return data.results || data
  } catch (error: unknown) {
    if (error instanceof APIError) {
      throw new APIError('Yeni kitablar yüklənə bilmədi', error.status, error.code)
    }
    throw new APIError('Yeni kitablar yüklənə bilmədi', 500)
  }
}

// Categories API
export const fetchCategories = async (): Promise<Category[]> => {
  try {
    const response = await apiFetch('/api/categories/')
    const data = await response.json()
    
    return data.results || data
  } catch (error) {
    if (error instanceof APIError) {
      throw new APIError('Kateqoriyalar yüklənə bilmədi', error.status, error.code)
    }
    throw new APIError('Kateqoriyalar yüklənə bilmədi', 500)
  }
}

export const fetchCategory = async (slug: string): Promise<Category> => {
  try {
    const response = await apiFetch(`/api/categories/${slug}/`)
    const data = await response.json()
    
    return data
  } catch (error) {
    if (error instanceof APIError) {
      throw new APIError('Kateqoriya məlumatları yüklənə bilmədi', error.status, error.code)
    }
    throw new APIError('Kateqoriya məlumatları yüklənə bilmədi', 500)
  }
}

// Reviews API
export const fetchBookReviews = async (bookId: number): Promise<BookReview[]> => {
  try {
    const response = await apiFetch(`/api/books/${bookId}/reviews/`)
    const data = await response.json()
    
    return data.results || data
  } catch (error) {
    if (error instanceof APIError) {
      throw new APIError('Rəylər yüklənə bilmədi', error.status, error.code)
    }
    throw new APIError('Rəylər yüklənə bilmədi', 500)
  }
}

export const createBookReview = async (
  bookId: number,
  reviewData: { rating: number; comment: string },
  token?: string
): Promise<BookReview> => {
  try {
    const headers: Record<string, string> = {}
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    const response = await apiFetch(`/api/books/${bookId}/reviews/`, {
      method: 'POST',
      headers,
      body: JSON.stringify(reviewData),
    })
    
    const data = await response.json()
    return data
  } catch (error) {
    if (error instanceof APIError) {
      throw new APIError('Rəy yaradıla bilmədi', error.status, error.code)
    }
    throw new APIError('Rəy yaradıla bilmədi', 500)
  }
}

// Search API
export const searchBooks = async (query: string, params?: {
  page?: number
  page_size?: number
  category?: string
}): Promise<{ results: Book[]; count: number }> => {
  try {
    const searchParams = new URLSearchParams({ search: query })
    
    if (params?.page) searchParams.append('page', params.page.toString())
    if (params?.page_size) searchParams.append('page_size', params.page_size.toString())
    if (params?.category) searchParams.append('category', params.category)
    
    const response = await apiFetch(`/api/books/?${searchParams.toString()}`)
    const data = await response.json()
    
    return data
  } catch (error) {
    if (error instanceof APIError) {
      throw new APIError('Axtarış nəticələri yüklənə bilmədi', error.status, error.code)
    }
    throw new APIError('Axtarış nəticələri yüklənə bilmədi', 500)
  }
}

// Stats API
export const fetchBookStats = async (): Promise<{
  total_books: number
  featured_books: number
  bestsellers: number
  new_books: number
}> => {
  try {
    const response = await apiFetch('/api/books/stats/')
    const data = await response.json()
    
    return data
  } catch (error) {
    if (error instanceof APIError) {
      throw new APIError('Statistika yüklənə bilmədi', error.status, error.code)
    }
    throw new APIError('Statistika yüklənə bilmədi', 500)
  }
}

// Health Check
export const checkAPIHealth = async (): Promise<boolean> => {
  try {
    const response = await apiFetch('/api/books/stats/')
    return response.ok
  } catch (error) {
    return false
  }
}

// Utility functions
export const getBookImageUrl = (book: Book): string => {
  return book.cover_imagekit_url || book.cover_image || '/placeholder.jpg'
}

export const getCategoryImageUrl = (category: Category): string => {
  return category.imagekit_url || category.image || '/placeholder.jpg'
}

export const getAuthorPhotoUrl = (author: Author): string => {
  return author.photo_imagekit_url || author.photo || '/placeholder-user.jpg'
}

export const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('az-AZ', {
    style: 'currency',
    currency: 'AZN',
  }).format(price)
}

export const getDiscountPercentage = (originalPrice: number, currentPrice: number): number => {
  if (originalPrice <= currentPrice) return 0
  return Math.round(((originalPrice - currentPrice) / originalPrice) * 100)
}
