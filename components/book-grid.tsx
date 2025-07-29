"use client"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Star, ShoppingCart } from "lucide-react"
import { useCart } from "@/contexts/cart-context"

const allBooks = [
  {
    id: 5,
    title: "Harri Potter və Fəlsəfə Daşı",
    author: "J.K. Rowling",
    price: 16.99,
    originalPrice: 21.99,
    rating: 4.9,
    reviews: 5432,
    category: "Fantastika",
    image: "/placeholder.svg?height=300&width=200",
  },
  {
    id: 6,
    title: "Cinayət və Cəza",
    author: "Fyodor Dostoyevski",
    price: 13.99,
    originalPrice: 17.99,
    rating: 4.7,
    reviews: 2341,
    category: "Klassik",
    image: "/placeholder.svg?height=300&width=200",
  },
  {
    id: 7,
    title: "Dune",
    author: "Frank Herbert",
    price: 19.99,
    originalPrice: 25.99,
    rating: 4.8,
    reviews: 3456,
    category: "Elmi-Fantastik",
    image: "/placeholder.svg?height=300&width=200",
  },
  {
    id: 8,
    title: "Yüz İl Tənhalıq",
    author: "Gabriel García Márquez",
    price: 15.99,
    originalPrice: 19.99,
    rating: 4.6,
    reviews: 1876,
    category: "Ədəbiyyat",
    image: "/placeholder.svg?height=300&width=200",
  },
  {
    id: 9,
    title: "Sapiens",
    author: "Yuval Noah Harari",
    price: 17.99,
    originalPrice: 22.99,
    rating: 4.8,
    reviews: 4321,
    category: "Tarix",
    image: "/placeholder.svg?height=300&width=200",
  },
  {
    id: 10,
    title: "Atomic Habits",
    author: "James Clear",
    price: 14.99,
    originalPrice: 18.99,
    rating: 4.9,
    reviews: 6789,
    category: "Özünü İnkişaf",
    image: "/placeholder.svg?height=300&width=200",
  },
]

const categories = ["Hamısı", "Fantastika", "Klassik", "Elmi-Fantastik", "Ədəbiyyat", "Tarix", "Özünü İnkişaf"]

export function BookGrid() {
  const [selectedCategory, setSelectedCategory] = useState("Hamısı")
  const [sortBy, setSortBy] = useState("popularity")
  const [searchTerm, setSearchTerm] = useState("")
  const { addItem } = useCart()

  const filteredBooks = allBooks.filter((book) => {
    const matchesCategory = selectedCategory === "Hamısı" || book.category === selectedCategory
    const matchesSearch =
      book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      book.author.toLowerCase().includes(searchTerm.toLowerCase())
    return matchesCategory && matchesSearch
  })

  const sortedBooks = [...filteredBooks].sort((a, b) => {
    switch (sortBy) {
      case "price-low":
        return a.price - b.price
      case "price-high":
        return b.price - a.price
      case "rating":
        return b.rating - a.rating
      default:
        return b.reviews - a.reviews
    }
  })

  const handleAddToCart = (book: (typeof allBooks)[0]) => {
    addItem({
      id: book.id,
      title: book.title,
      author: book.author,
      price: book.price,
      image: book.image,
      quantity: 1,
    })
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
              {categories.map((category) => (
                <SelectItem key={category} value={category}>
                  {category}
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
                    src={book.image || "/placeholder.svg"}
                    alt={book.title}
                    className="w-full h-64 object-cover rounded-lg"
                  />
                  <Badge className="absolute top-2 left-2" variant="secondary">
                    {book.category}
                  </Badge>
                </div>

                <h3 className="font-semibold text-lg mb-1 line-clamp-2">{book.title}</h3>
                <p className="text-gray-600 text-sm mb-2">{book.author}</p>

                <div className="flex items-center mb-3">
                  <div className="flex text-yellow-400">
                    {[...Array(5)].map((_, i) => (
                      <Star key={i} className={`h-4 w-4 ${i < Math.floor(book.rating) ? "fill-current" : ""}`} />
                    ))}
                  </div>
                  <span className="ml-2 text-sm text-gray-600">
                    {book.rating} ({book.reviews})
                  </span>
                </div>

                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg font-bold text-green-600">${book.price}</span>
                    {book.originalPrice && (
                      <span className="text-sm text-gray-500 line-through">${book.originalPrice}</span>
                    )}
                  </div>
                </div>

                <Button className="w-full" onClick={() => handleAddToCart(book)}>
                  <ShoppingCart className="h-4 w-4 mr-2" />
                  Səbətə At
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
