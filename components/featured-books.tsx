"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Star, ShoppingCart } from "lucide-react"
import { useCart } from "@/contexts/cart-context"

const featuredBooks = [
  {
    id: 1,
    title: "Kiçik Şahzadə",
    author: "Antoine de Saint-Exupéry",
    price: 15.99,
    originalPrice: 19.99,
    rating: 4.8,
    reviews: 1234,
    image: "/placeholder.svg?height=300&width=200",
    badge: "Bestseller",
  },
  {
    id: 2,
    title: "1984",
    author: "George Orwell",
    price: 12.99,
    originalPrice: 16.99,
    rating: 4.9,
    reviews: 2156,
    image: "/placeholder.svg?height=300&width=200",
    badge: "Klassik",
  },
  {
    id: 3,
    title: "Qaranlıq Meşə",
    author: "Liu Cixin",
    price: 18.99,
    originalPrice: 24.99,
    rating: 4.7,
    reviews: 892,
    image: "/placeholder.svg?height=300&width=200",
    badge: "Yeni",
  },
  {
    id: 4,
    title: "Alxemik",
    author: "Paulo Coelho",
    price: 14.99,
    originalPrice: 18.99,
    rating: 4.6,
    reviews: 3421,
    image: "/placeholder.svg?height=300&width=200",
    badge: "Populyar",
  },
]

export function FeaturedBooks() {
  const { addItem } = useCart()

  const handleAddToCart = (book: (typeof featuredBooks)[0]) => {
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
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Seçilmiş Kitablar</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Ən populyar və yüksək reytinqli kitablarımızı kəşf edin
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {featuredBooks.map((book) => (
            <Card key={book.id} className="group hover:shadow-lg transition-shadow duration-300">
              <CardContent className="p-4">
                <div className="relative mb-4">
                  <img
                    src={book.image || "/placeholder.svg"}
                    alt={book.title}
                    className="w-full h-64 object-cover rounded-lg"
                  />
                  <Badge
                    className="absolute top-2 left-2"
                    variant={book.badge === "Bestseller" ? "destructive" : "secondary"}
                  >
                    {book.badge}
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
                    <span className="text-sm text-gray-500 line-through">${book.originalPrice}</span>
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
      </div>
    </section>
  )
}
