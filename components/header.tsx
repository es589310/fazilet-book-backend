"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Search, ShoppingCart, BookOpen, ChevronDown, Loader2 } from "lucide-react"
import { useCart } from "@/contexts/cart-context"
import { useAuth } from "@/contexts/auth-context"
import { CartSidebar } from "./cart-sidebar"
import { fetchCategories, type Category, searchBooks, type Book } from "@/lib/api"
import { useErrorHandler } from "./error-boundary"

interface HeaderProps {
  onAuthClick: (mode: "login" | "register") => void
}

export function Header({ onAuthClick }: HeaderProps) {
  const [isCartOpen, setIsCartOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [isSearching, setIsSearching] = useState(false)
  const [searchResults, setSearchResults] = useState<Book[]>([])
  const [showSearchResults, setShowSearchResults] = useState(false)
  const [categories, setCategories] = useState<Category[]>([])
  const [isLoadingCategories, setIsLoadingCategories] = useState(true)
  const { items } = useCart()
  const { user, logout } = useAuth()
  const { error, handleError, clearError } = useErrorHandler()

  const totalItems = items.reduce((sum, item) => sum + item.quantity, 0)

  // Load categories on component mount
  useEffect(() => {
    const loadCategories = async () => {
      try {
        setIsLoadingCategories(true)
        const categoriesData = await fetchCategories()
        setCategories(categoriesData.filter(cat => cat.is_active))
      } catch (error) {
        handleError(error instanceof Error ? error : new Error('Kateqoriyalar yüklənə bilmədi'))
      } finally {
        setIsLoadingCategories(false)
      }
    }

    loadCategories()
  }, [handleError])

  // Search functionality with debouncing
  useEffect(() => {
    const searchTimeout = setTimeout(async () => {
      if (searchQuery.trim().length >= 2) {
        try {
          setIsSearching(true)
          const results = await searchBooks(searchQuery.trim())
          setSearchResults(results.results || [])
          setShowSearchResults(true)
        } catch (error) {
          handleError(error instanceof Error ? error : new Error('Axtarış uğursuz oldu'))
          setSearchResults([])
        } finally {
          setIsSearching(false)
        }
      } else {
        setSearchResults([])
        setShowSearchResults(false)
      }
    }, 500) // 500ms debounce

    return () => clearTimeout(searchTimeout)
  }, [searchQuery, handleError])

  // Handle search input change
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value)
    if (e.target.value.trim().length < 2) {
      setShowSearchResults(false)
    }
  }

  // Handle search result click
  const handleSearchResultClick = (book: Book) => {
    setSearchQuery(book.title)
    setShowSearchResults(false)
    // Navigate to book detail page
    window.location.href = `/book/${book.slug}`
  }

  // Handle search submit
  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      // Navigate to search results page
      window.location.href = `/search?q=${encodeURIComponent(searchQuery.trim())}`
    }
  }

  return (
    <>
      <header className="bg-white shadow-sm border-b sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center space-x-2">
              <BookOpen className="h-8 w-8 text-blue-600" />
              <span className="text-2xl font-bold text-gray-900">Dostum Kitab</span>
            </div>

            {/* Search Bar */}
            <div className="flex-1 max-w-lg mx-8">
              <form onSubmit={handleSearchSubmit} className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  type="text"
                  placeholder="Kitab axtarın..."
                  value={searchQuery}
                  onChange={handleSearchChange}
                  className="pl-10 pr-4 w-full"
                  disabled={isSearching}
                />
                {isSearching && (
                  <Loader2 className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4 animate-spin" />
                )}
                
                {/* Search Results Dropdown */}
                {showSearchResults && searchResults.length > 0 && (
                  <div className="absolute top-full left-0 right-0 mt-1 bg-white border rounded-lg shadow-lg max-h-64 overflow-y-auto z-50">
                    {searchResults.map((book) => (
                      <button
                        key={book.id}
                        onClick={() => handleSearchResultClick(book)}
                        className="w-full text-left px-4 py-3 hover:bg-gray-50 border-b last:border-b-0 flex items-center space-x-3"
                      >
                        <div className="w-10 h-14 bg-gray-200 rounded flex-shrink-0">
                          {book.cover_imagekit_url || book.cover_image ? (
                            <img
                              src={book.cover_imagekit_url || book.cover_image}
                              alt={book.title}
                              className="w-full h-full object-cover rounded"
                            />
                          ) : (
                            <div className="w-full h-full bg-gray-300 rounded flex items-center justify-center">
                              <BookOpen className="h-5 w-5 text-gray-500" />
                            </div>
                          )}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="font-medium text-gray-900 truncate">{book.title}</div>
                          <div className="text-sm text-gray-500 truncate">
                            {book.authors.map(author => author.name).join(', ')}
                          </div>
                          <div className="text-sm font-medium text-blue-600">
                            {new Intl.NumberFormat('az-AZ', {
                              style: 'currency',
                              currency: 'AZN',
                            }).format(book.price)}
                          </div>
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </form>
            </div>

            {/* Navigation Menu */}
            <nav className="hidden lg:flex items-center space-x-6">
              <div className="relative group">
                <button className="flex items-center space-x-1 text-gray-700 hover:text-blue-600 transition-colors">
                  <span>Kateqoriyalar</span>
                  <ChevronDown className="h-4 w-4" />
                </button>
                <div className="absolute top-full left-0 mt-2 w-64 bg-white border rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                  <div className="p-2">
                    {isLoadingCategories ? (
                      <div className="flex items-center justify-center py-4">
                        <Loader2 className="h-4 w-4 animate-spin text-gray-400" />
                        <span className="ml-2 text-sm text-gray-500">Yüklənir...</span>
                      </div>
                    ) : error ? (
                      <div className="px-3 py-2 text-sm text-red-600">
                        Kateqoriyalar yüklənə bilmədi
                      </div>
                    ) : categories.length > 0 ? (
                      categories.map((category) => (
                        <a
                          key={category.id}
                          href={`/category/${category.slug}`}
                          className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded"
                        >
                          {category.name}
                        </a>
                      ))
                    ) : (
                      <div className="px-3 py-2 text-sm text-gray-500">
                        Kateqoriya tapılmadı
                      </div>
                    )}
                  </div>
                </div>
              </div>
              <a href="/bestsellers" className="text-gray-700 hover:text-blue-600 transition-colors">
                Bestsellerlər
              </a>
              <a href="/new-books" className="text-gray-700 hover:text-blue-600 transition-colors">
                Yeni Kitablar
              </a>
              <a href="/discounts" className="text-gray-700 hover:text-blue-600 transition-colors">
                Endirimlər
              </a>
            </nav>

            {/* Right Side */}
            <div className="flex items-center space-x-4">
              {/* Cart */}
              <Button variant="ghost" size="sm" className="relative" onClick={() => setIsCartOpen(true)}>
                <ShoppingCart className="h-5 w-5" />
                {totalItems > 0 && (
                  <Badge
                    variant="destructive"
                    className="absolute -top-2 -right-2 h-5 w-5 flex items-center justify-center p-0 text-xs"
                  >
                    {totalItems}
                  </Badge>
                )}
              </Button>

              {/* User Menu */}
              {user ? (
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-700">Salam, {user.name}</span>
                  <Button variant="ghost" size="sm" onClick={logout}>
                    Çıxış
                  </Button>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <Button variant="ghost" size="sm" onClick={() => onAuthClick("login")}>
                    Giriş
                  </Button>
                  <Button size="sm" onClick={() => onAuthClick("register")}>
                    Qeydiyyat
                  </Button>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      <CartSidebar isOpen={isCartOpen} onClose={() => setIsCartOpen(false)} />
    </>
  )
}
