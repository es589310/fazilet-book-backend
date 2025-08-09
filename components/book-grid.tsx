"use client"

import { useState, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Star, ShoppingCart } from "lucide-react"
import { useCart } from "@/contexts/cart-context"
import { fetchBooks, fetchCategories, type Book, type Category } from "@/lib/api"

export function BookGrid() {
  const [books, setBooks] = useState<Book[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string>("")
  const [sortBy, setSortBy] = useState("")
  const [searchTerm, setSearchTerm] = useState("")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const { addItem } = useCart()

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true)
        const [booksResponse, categoriesResponse] = await Promise.all([
          fetchBooks(),
          fetchCategories()
        ])
        setBooks(booksResponse.results)
        setCategories(categoriesResponse)
        setError(null)
      } catch (err) {
        setError('Kitablar yüklənərkən xəta baş verdi')
        console.error('Error fetching data:', err)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [])

  // Filter books based on search and category
  const filteredBooks = books.filter((book) => {
    const matchesCategory = !selectedCategory || book.category.name === selectedCategory
    const matchesSearch =
      book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      book.authors.some(author => author.name.toLowerCase().includes(searchTerm.toLowerCase()))
    return matchesCategory && matchesSearch
  })

  // Sort books
  const sortedBooks = [...filteredBooks].sort((a, b) => {
    switch (sortBy) {
      case "price-low":
        return parseFloat(a.price) - parseFloat(b.price)
      case "price-high":
        return parseFloat(b.price) - parseFloat(a.price)
      case "rating":
        return b.average_rating - a.average_rating
      case "views":
        return b.stock_quantity - a.stock_quantity // Using stock as popularity proxy
      default:
        return b.reviews_count - a.reviews_count
    }
  })

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

  if (loading) {
    return (
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Bütün Kitablar</h2>
            <p className="text-lg text-gray-600">Geniş kitab kolleksiyamızı araşdırın</p>
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
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Bütün Kitablar</h2>
            <p className="text-lg text-gray-600">Geniş kitab kolleksiyamızı araşdırın</p>
          </div>
          <div className="text-center">
            <p className="text-red-500">{error}</p>
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

        {/* Books Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {sortedBooks.map((book) => (
            <Card key={book.id} className="group hover:shadow-lg transition-shadow duration-300">
              <CardContent className="p-4">
                <div className="relative mb-4">
                  <img
                    src={book.cover_image || "/placeholder.svg"}
                    alt={book.title}
                    className="w-full h-64 object-cover rounded-lg"
                  />
                  <Badge className="absolute top-2 left-2" variant="secondary">
                    {book.category.name}
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

                <Button 
                  className="w-full" 
                  onClick={() => handleAddToCart(book)}
                  disabled={book.stock_quantity === 0}
                >
                  <ShoppingCart className="h-4 w-4 mr-2" />
                  {book.stock_quantity === 0 ? 'Stokda Yoxdur' : 'Səbətə At'}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {sortedBooks.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">Heç bir kitab tapılmadı.</p>
          </div>
        )}
      </div>
    </section>
  )
}
