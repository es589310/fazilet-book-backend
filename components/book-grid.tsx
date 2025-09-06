"use client"

import { useState, useEffect, useMemo, useCallback } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Star, ShoppingCart, AlertCircle, RefreshCw, Loader2 } from "lucide-react"
import { useCart } from "@/contexts/cart-context"
import { fetchBooks, fetchCategories, type Book, type Category, getBookImageUrl, formatPrice, getDiscountPercentage } from "@/lib/api"
import { useErrorHandler } from "./error-boundary"

export function BookGrid() {
  const [books, setBooks] = useState<Book[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string>("")
  const [sortBy, setSortBy] = useState("")
  const [searchTerm, setSearchTerm] = useState("")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [retryCount, setRetryCount] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [hasMore, setHasMore] = useState(true)
  const [isLoadingMore, setIsLoadingMore] = useState(false)
  const { addItem } = useCart()
  const { handleError, clearError } = useErrorHandler()

  const ITEMS_PER_PAGE = 12

  const loadData = useCallback(async (isInitial = true) => {
    try {
      if (isInitial) {
        setLoading(true)
        setError(null)
        clearError()
      } else {
        setIsLoadingMore(true)
      }

      const [booksResponse, categoriesResponse] = await Promise.all([
        fetchBooks({ 
          page: isInitial ? 1 : currentPage + 1,
          page_size: ITEMS_PER_PAGE,
          category: selectedCategory || undefined,
          search: searchTerm || undefined,
          ordering: sortBy || undefined
        }),
        fetchCategories()
      ])

      if (isInitial) {
        setBooks(booksResponse.results)
        setCurrentPage(1)
      } else {
        setBooks(prev => [...prev, ...booksResponse.results])
        setCurrentPage(prev => prev + 1)
      }

      setCategories(categoriesResponse)
      setHasMore(!!booksResponse.next)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Kitablar yüklənərkən xəta baş verdi'
      setError(errorMessage)
      handleError(err instanceof Error ? err : new Error(errorMessage))
    } finally {
      setLoading(false)
      setIsLoadingMore(false)
    }
  }, [selectedCategory, searchTerm, sortBy, currentPage, handleError, clearError])

  // Initial load
  useEffect(() => {
    loadData(true)
  }, [])

  // Reload when filters change
  useEffect(() => {
    setCurrentPage(1)
    setBooks([])
    loadData(true)
  }, [selectedCategory, searchTerm, sortBy])

  const handleRetry = () => {
    setRetryCount(prev => prev + 1)
    loadData(true)
  }

  const handleLoadMore = () => {
    if (!isLoadingMore && hasMore) {
      loadData(false)
    }
  }

  // Filter books based on search and category (client-side filtering for loaded books)
  const filteredBooks = useMemo(() => {
    return books.filter((book) => {
      const matchesCategory = !selectedCategory || book.category.name === selectedCategory
      const matchesSearch =
        book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        book.authors.some(author => author.name.toLowerCase().includes(searchTerm.toLowerCase()))
      return matchesCategory && matchesSearch
    })
  }, [books, selectedCategory, searchTerm])

  // Sort books
  const sortedBooks = useMemo(() => {
    return [...filteredBooks].sort((a, b) => {
      switch (sortBy) {
        case "price-low":
          return a.price - b.price
        case "price-high":
          return b.price - a.price
        case "rating":
          return b.average_rating - a.average_rating
        case "popularity":
          return b.reviews_count - a.reviews_count
        default:
          return b.reviews_count - a.reviews_count
      }
    })
  }, [filteredBooks, sortBy])

  const handleAddToCart = useCallback((book: Book) => {
    try {
      addItem({
        id: book.id,
        title: book.title,
        author: book.authors[0]?.name || 'Naməlum müəllif',
        price: book.price,
        image: getBookImageUrl(book),
        quantity: 1,
      })
    } catch (error) {
      handleError(error instanceof Error ? error : new Error('Səbətə əlavə edilərkən xəta baş verdi'))
    }
  }, [addItem, handleError])

  // Loading state with skeleton
  if (loading) {
    return (
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Bütün Kitablar</h2>
            <p className="text-lg text-gray-600">Geniş kitab kolleksiyamızı araşdırın</p>
          </div>
          
          {/* Skeleton loading */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[...Array(8)].map((_, index) => (
              <Card key={index} className="animate-pulse">
                <CardContent className="p-4">
                  <div className="relative mb-4">
                    <div className="w-full h-64 bg-gray-200 rounded-lg"></div>
                    <div className="absolute top-2 left-2 w-20 h-6 bg-gray-300 rounded"></div>
                  </div>
                  <div className="h-6 bg-gray-200 rounded mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded mb-3 w-3/4"></div>
                  <div className="flex items-center mb-3">
                    <div className="flex space-x-1">
                      {[...Array(5)].map((_, i) => (
                        <div key={i} className="w-4 h-4 bg-gray-200 rounded"></div>
                      ))}
                    </div>
                    <div className="ml-2 w-16 h-4 bg-gray-200 rounded"></div>
                  </div>
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-20 h-6 bg-gray-200 rounded"></div>
                    <div className="w-16 h-6 bg-gray-200 rounded"></div>
                  </div>
                  <div className="w-full h-10 bg-gray-200 rounded"></div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    )
  }

  // Error state with retry option
  if (error) {
    return (
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Bütün Kitablar</h2>
            <p className="text-lg text-gray-600">Geniş kitab kolleksiyamızı araşdırın</p>
          </div>
          
          <div className="text-center py-12">
            <AlertCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
            <p className="text-red-500 text-lg mb-4">{error}</p>
            <Button 
              onClick={handleRetry} 
              variant="outline"
              className="flex items-center space-x-2 mx-auto"
            >
              <RefreshCw className="h-4 w-4" />
              <span>Yenidən cəhd edin</span>
            </Button>
            {retryCount > 0 && (
              <p className="text-sm text-gray-500 mt-2">
                Cəhd sayı: {retryCount}
              </p>
            )}
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Bütün Kitablar</h2>
          <p className="text-lg text-gray-600">Geniş kitab kolleksiyamızı araşdırın</p>
        </div>

        {/* Filters */}
        <div className="flex flex-col md:flex-row gap-4 mb-8">
          <div className="flex-1">
            <Input
              placeholder="Kitab və ya müəllif axtarın..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full"
            />
          </div>
          <Select value={selectedCategory} onValueChange={setSelectedCategory}>
            <SelectTrigger className="w-full md:w-48">
              <SelectValue placeholder="Kateqoriya" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">Hamısı</SelectItem>
              {categories.map((category) => (
                <SelectItem key={category.id} value={category.name}>
                  {category.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={sortBy} onValueChange={setSortBy}>
            <SelectTrigger className="w-full md:w-48">
              <SelectValue placeholder="Sırala" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="popularity">Populyarlıq</SelectItem>
              <SelectItem value="rating">Reytinq</SelectItem>
              <SelectItem value="price-low">Qiymət (Aşağı)</SelectItem>
              <SelectItem value="price-high">Qiymət (Yüksək)</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Results count */}
        <div className="mb-6 text-sm text-gray-600">
          {sortedBooks.length > 0 ? (
            <span>{sortedBooks.length} kitab tapıldı</span>
          ) : (
            <span>Heç bir kitab tapılmadı</span>
          )}
        </div>

        {/* Books Grid */}
        {sortedBooks.length > 0 ? (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {sortedBooks.map((book) => (
                <Card key={book.id} className="group hover:shadow-lg transition-shadow duration-300">
                  <CardContent className="p-4">
                    <div className="relative mb-4">
                      <img
                        src={getBookImageUrl(book)}
                        alt={book.title}
                        className="w-full h-64 object-cover rounded-lg"
                        loading="lazy"
                        onError={(e) => {
                          const target = e.target as HTMLImageElement
                          target.src = "/placeholder.svg"
                        }}
                      />
                      <Badge className="absolute top-2 left-2" variant="secondary">
                        {book.category.name}
                      </Badge>
                      
                      {/* Discount badge */}
                      {book.original_price && book.original_price > book.price && (
                        <Badge 
                          variant="destructive" 
                          className="absolute top-2 right-2"
                        >
                          -{getDiscountPercentage(book.original_price, book.price)}%
                        </Badge>
                      )}
                    </div>

                    <h3 className="font-semibold text-lg mb-1 line-clamp-2">{book.title}</h3>
                    <p className="text-gray-600 text-sm mb-2">
                      {book.authors.map(author => author.name).join(', ')}
                    </p>

                    <div className="flex items-center mb-3">
                      <div className="flex text-yellow-400">
                        {[...Array(5)].map((_, i) => (
                          <Star 
                            key={i} 
                            className={`h-4 w-4 ${i < Math.floor(book.average_rating) ? "fill-current" : ""}`} 
                          />
                        ))}
                      </div>
                      <span className="ml-2 text-sm text-gray-600">
                        {book.average_rating.toFixed(1)} ({book.reviews_count})
                      </span>
                    </div>

                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-2">
                        <span className="text-lg font-bold text-green-600">
                          {formatPrice(book.price)}
                        </span>
                        {book.original_price && book.original_price > book.price && (
                          <span className="text-sm text-gray-500 line-through">
                            {formatPrice(book.original_price)}
                          </span>
                        )}
                      </div>
                    </div>

                    <Button 
                      className="w-full" 
                      onClick={() => handleAddToCart(book)}
                      disabled={book.stock_quantity <= 0}
                    >
                      <ShoppingCart className="h-4 w-4 mr-2" />
                      {book.stock_quantity > 0 ? 'Səbətə At' : 'Stokda Yoxdur'}
                    </Button>
                    
                    {book.stock_quantity <= 5 && book.stock_quantity > 0 && (
                      <p className="text-xs text-orange-600 text-center mt-2">
                        Son {book.stock_quantity} ədəd!
                      </p>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Load More Button */}
            {hasMore && (
              <div className="text-center mt-8">
                <Button 
                  onClick={handleLoadMore} 
                  variant="outline" 
                  disabled={isLoadingMore}
                  className="px-8"
                >
                  {isLoadingMore ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Yüklənir...
                    </>
                  ) : (
                    'Daha çox yüklə'
                  )}
                </Button>
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">Heç bir kitab tapılmadı.</p>
            <Button 
              onClick={handleRetry} 
              variant="outline" 
              className="mt-4"
            >
              Yenidən yüklə
            </Button>
          </div>
        )}
      </div>
    </section>
  )
}
