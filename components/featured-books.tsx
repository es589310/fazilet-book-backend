"use client"

import { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Star, ShoppingCart } from "lucide-react"
import { useCart } from "@/contexts/cart-context"
import { fetchFeaturedBooks, type Book } from "@/lib/api"

export function FeaturedBooks() {
  const [books, setBooks] = useState<Book[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const { addItem } = useCart()

  useEffect(() => {
    async function loadFeaturedBooks() {
      try {
        setLoading(true)
        const response = await fetchFeaturedBooks()
        setBooks(response.results)
        setError(null)
      } catch (err) {
        setError('Seçilmiş kitablar yüklənərkən xəta baş verdi')
        console.error('Error fetching featured books:', err)
      } finally {
        setLoading(false)
      }
    }

    loadFeaturedBooks()
  }, [])

  const handleAddToCart = (book: Book) => {
    addItem({
      id: book.id,
      title: book.title,
      author: book.authors[0]?.name || 'Naməlum müəllif',
      price: parseFloat(book.price),
      image: book.cover_image,
      quantity: 1,
    })
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
          <div className="text-center">
            <p className="text-gray-500">Yüklənir...</p>
          </div>
        </div>
      </section>
    )
  }

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
          <div className="text-center">
            <p className="text-red-500">{error}</p>
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

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {books.map((book) => (
            <Card key={book.id} className="group hover:shadow-lg transition-shadow duration-300">
              <CardContent className="p-4">
                <div className="relative mb-4">
                  <img
                    src={book.cover_image || "/placeholder.svg"}
                    alt={book.title}
                    className="w-full h-64 object-cover rounded-lg"
                  />
                  <Badge
                    className="absolute top-2 left-2"
                    variant={getBadgeVariant(book) as any}
                  >
                    {getBadgeText(book)}
                  </Badge>
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
                    <span className="text-lg font-bold text-green-600">₼{book.price}</span>
                    {book.original_price && (
                      <span className="text-sm text-gray-500 line-through">₼{book.original_price}</span>
                    )}
                  </div>
                  {book.discount_percentage > 0 && (
                    <Badge variant="destructive">-{book.discount_percentage}%</Badge>
                  )}
                </div>

                <Button className="w-full" onClick={() => handleAddToCart(book)}>
                  <ShoppingCart className="h-4 w-4 mr-2" />
                  Səbətə At
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {books.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">Seçilmiş kitab tapılmadı.</p>
          </div>
        )}
      </div>
    </section>
  )
}
