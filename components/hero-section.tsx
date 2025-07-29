"use client"

import { Button } from "@/components/ui/button"
import { ArrowRight, Star } from "lucide-react"
import { useState, useEffect } from "react"
import { ChevronLeft, ChevronRight } from "lucide-react"

export function HeroSection() {
  const [currentSlide, setCurrentSlide] = useState(0)

  const bookAds = [
    {
      id: 1,
      title: "Kiçik Şahzadə",
      author: "Antoine de Saint-Exupéry",
      description: "Dünyada ən çox oxunan kitablardan biri",
      discount: "40% ENDİRİM",
      price: "15.99₼",
      originalPrice: "26.99₼",
      image: "/placeholder.svg?height=400&width=300&text=Kiçik+Şahzadə",
      bgColor: "from-purple-600 to-pink-600",
    },
    {
      id: 2,
      title: "1984",
      author: "George Orwell",
      description: "Distopik ədəbiyyatın şah əsəri",
      discount: "35% ENDİRİM",
      price: "12.99₼",
      originalPrice: "19.99₼",
      image: "/placeholder.svg?height=400&width=300&text=1984",
      bgColor: "from-blue-600 to-indigo-700",
    },
    {
      id: 3,
      title: "Alxemik",
      author: "Paulo Coelho",
      description: "Ruhani səyahət və özünü kəşf etmə",
      discount: "50% ENDİRİM",
      price: "14.99₼",
      originalPrice: "29.99₼",
      image: "/placeholder.svg?height=400&width=300&text=Alxemik",
      bgColor: "from-green-600 to-teal-600",
    },
  ]

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % bookAds.length)
    }, 5000)
    return () => clearInterval(timer)
  }, [bookAds.length])

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % bookAds.length)
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + bookAds.length) % bookAds.length)
  }

  const currentBook = bookAds[currentSlide]

  return (
    <section
      className={`bg-gradient-to-r ${currentBook.bgColor} text-white relative overflow-hidden transition-all duration-1000`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="z-10">
            <div className="inline-block bg-yellow-500 text-black px-4 py-2 rounded-full text-sm font-bold mb-4">
              {currentBook.discount}
            </div>
            <h1 className="text-4xl md:text-6xl font-bold leading-tight mb-6">
              {currentBook.title}
              <span className="block text-yellow-300 text-2xl md:text-3xl mt-2">{currentBook.author}</span>
            </h1>
            <p className="text-xl mb-6 text-blue-100">{currentBook.description}</p>
            <div className="flex items-center space-x-4 mb-8">
              <span className="text-3xl font-bold text-yellow-300">{currentBook.price}</span>
              <span className="text-lg text-gray-300 line-through">{currentBook.originalPrice}</span>
            </div>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button size="lg" className="bg-yellow-500 hover:bg-yellow-600 text-black">
                İndi Al
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="border-white text-white hover:bg-white hover:text-blue-600 bg-transparent"
              >
                Ətraflı Bax
              </Button>
            </div>
            <div className="flex items-center mt-8 space-x-6">
              <div className="flex items-center">
                <div className="flex text-yellow-400">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 fill-current" />
                  ))}
                </div>
                <span className="ml-2 text-sm">4.9/5 reytinq</span>
              </div>
              <div className="text-sm">
                <span className="font-semibold">50,000+</span> məmnun müştəri
              </div>
            </div>
          </div>

          <div className="relative z-10">
            <div className="relative">
              <img
                src={currentBook.image || "/placeholder.svg"}
                alt={currentBook.title}
                className="rounded-lg shadow-2xl mx-auto transform hover:scale-105 transition-transform duration-300"
              />
              <div className="absolute -bottom-6 -left-6 bg-white text-gray-900 p-4 rounded-lg shadow-lg">
                <div className="text-2xl font-bold text-green-600">{currentBook.discount}</div>
                <div className="text-sm">Məhdud müddət</div>
              </div>
            </div>
          </div>
        </div>

        {/* Carousel Controls */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex items-center space-x-4">
          <button onClick={prevSlide} className="p-2 rounded-full bg-white/20 hover:bg-white/30 transition-colors">
            <ChevronLeft className="h-6 w-6" />
          </button>

          <div className="flex space-x-2">
            {bookAds.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentSlide(index)}
                className={`w-3 h-3 rounded-full transition-colors ${
                  index === currentSlide ? "bg-yellow-400" : "bg-white/40"
                }`}
              />
            ))}
          </div>

          <button onClick={nextSlide} className="p-2 rounded-full bg-white/20 hover:bg-white/30 transition-colors">
            <ChevronRight className="h-6 w-6" />
          </button>
        </div>
      </div>

      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-20 w-32 h-32 border-2 border-white rounded-full"></div>
        <div className="absolute bottom-20 right-20 w-24 h-24 border-2 border-white rounded-full"></div>
        <div className="absolute top-1/2 right-10 w-16 h-16 border-2 border-white rounded-full"></div>
      </div>
    </section>
  )
}
