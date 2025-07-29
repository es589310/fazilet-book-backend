"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Search, ShoppingCart, BookOpen, ChevronDown } from "lucide-react"
import { useCart } from "@/contexts/cart-context"
import { useAuth } from "@/contexts/auth-context"
import { CartSidebar } from "./cart-sidebar"

interface HeaderProps {
  onAuthClick: (mode: "login" | "register") => void
}

export function Header({ onAuthClick }: HeaderProps) {
  const [isCartOpen, setIsCartOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const { items } = useCart()
  const { user, logout } = useAuth()

  const totalItems = items.reduce((sum, item) => sum + item.quantity, 0)

  return (
    <>
      <header className="bg-white shadow-sm border-b sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center space-x-2">
              <BookOpen className="h-8 w-8 text-blue-600" />
              <span className="text-2xl font-bold text-gray-900">KitabSat</span>
            </div>

            {/* Search Bar */}
            <div className="flex-1 max-w-lg mx-8">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  type="text"
                  placeholder="Kitab axtarın..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 pr-4 w-full"
                />
              </div>
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
                    <a href="#" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">
                      Dini Kitablar
                    </a>
                    <a href="#" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">
                      Uşaqlar üçün Kitablar
                    </a>
                    <a href="#" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">
                      Fəlsəfi Kitablar
                    </a>
                    <a href="#" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">
                      Tarixi Kitablar
                    </a>
                    <a href="#" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">
                      Elmi Kitablar
                    </a>
                    <a href="#" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">
                      Ədəbiyyat
                    </a>
                    <a href="#" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">
                      Biznes Kitabları
                    </a>
                    <a href="#" className="block px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">
                      Psixologiya
                    </a>
                  </div>
                </div>
              </div>
              <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">
                Bestsellerlər
              </a>
              <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">
                Yeni Kitablar
              </a>
              <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">
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
