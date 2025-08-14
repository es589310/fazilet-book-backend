"use client"

import { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Star, ShoppingCart, AlertCircle, RefreshCw } from "lucide-react"
import { useCart } from "@/contexts/cart-context"
import { fetchFeaturedBooks, type Book, getBookImageUrl, formatPrice, getDiscountPercentage } from "@/lib/api"
import { useErrorHandler } from "./error-boundary"

export function FeaturedBooks() {
  const [books, setBooks] = useState<Book[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [retryCount, setRetryCount] = useState(0)
  const { addItem } = useCart()
  const { handleError, clearError } = useErrorHandler()

  const loadFeaturedBooks = async () => {
    try {
      setLoading(true)
      setError(null)
      clearError()
      
      const booksData = await fetchFeaturedBooks()
      setBooks(booksData)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Seçilmiş kitablar yüklənərkən xəta baş verdi'
      setError(errorMessage)
      handleError(err instanceof Error ? err : new Error(errorMessage))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadFeaturedBooks()
  }, [])

  const handleRetry = () => {
    setRetryCount(prev => prev + 1)
    loadFeaturedBooks()
  }

  const handleAddToCart = (book: Book) => {
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
  }

  const getBadgeText = (book: Book) => {
    if (book.is_bestseller) return 'Bestseller'
    if (book.is_new) return 'Yeni'
    if (book.is_featured) return 'Seçilmiş'
    return 'Kitab'
  }

  const getBadgeVariant = (book: Book) => {
    if (book.is_bestseller) return 'destructive'
    if (book.is_new) return 'default'
    return 'secondary'
  }

  // Loading state with skeleton
  if (loading) {
    return (
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Seçilmiş Kitablar</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Ən populyar və yüksək reytinqli kitablarımızı kəşf edin
            </p>
          </div>
          
          {/* Skeleton loading */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(4)].map((_, index) => (
              <Card key={index} className="animate-pulse">
                <CardContent className="p-4">
                  <div className="relative mb-4">
                    <div className="w-full h-64 bg-gray-200 rounded-lg"></div>
                    <div className="absolute top-2 left-2 w-16 h-6 bg-gray-300 rounded"></div>
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
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Seçilmiş Kitablar</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Ən populyar və yüksək reytinqli kitablarımızı kəşf edin
            </p>
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
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Seçilmiş Kitablar</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Ən populyar və yüksək reytinqli kitablarımızı kəşf edin
          </p>
        </div>

        {books.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {books.map((book) => (
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
                    <Badge
                      className="absolute top-2 left-2"
                      variant={getBadgeVariant(book) as any}
                    >
                      {getBadgeText(book)}
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
                    {book.stock_quantity > 0 ? 'Səbətə At' : 'Stokda yoxdur'}
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
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">Seçilmiş kitab tapılmadı.</p>
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
