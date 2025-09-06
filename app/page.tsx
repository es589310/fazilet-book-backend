"use client"

import { useState, useEffect } from "react"
import { Header } from "@/components/header"
import { HeroSection } from "@/components/hero-section"
import { FeaturedBooks } from "@/components/featured-books"
import { BookGrid } from "@/components/book-grid"
import { Footer } from "@/components/footer"
import { AuthModal } from "@/components/auth-modal"
import { CartProvider } from "@/contexts/cart-context"
import { AuthProvider } from "@/contexts/auth-context"

// Production API endpoints
const API_ENDPOINTS = {
  BOOKS_STATS: process.env.NEXT_PUBLIC_API_URL + '/api/books/stats/',
  FEATURED_BOOKS: process.env.NEXT_PUBLIC_API_URL + '/api/books/featured/',
  ALL_BOOKS: process.env.NEXT_PUBLIC_API_URL + '/api/books/',
  CATEGORIES: process.env.NEXT_PUBLIC_API_URL + '/api/categories/',
  SITE_SETTINGS: process.env.NEXT_PUBLIC_API_URL + '/api/site-settings/',
}

// API error types
interface APIError {
  message: string
  status?: number
  code?: string
}

// Production error messages
const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Şəbəkə xətası. İnternet bağlantınızı yoxlayın.',
  API_ERROR: 'Server xətası. Zəhmət olmasa daha sonra yenidən cəhd edin.',
  TIMEOUT_ERROR: 'Zaman aşımı. Zəhmət olmasa yenidən cəhd edin.',
  UNKNOWN_ERROR: 'Naməlum xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.',
}

export default function HomePage() {
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false)
  const [authMode, setAuthMode] = useState<"login" | "register">("login")
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<APIError | null>(null)
  const [retryCount, setRetryCount] = useState(0)
  const [siteSettings, setSiteSettings] = useState<any>(null)

  const openAuthModal = (mode: "login" | "register") => {
    setAuthMode(mode)
    setIsAuthModalOpen(true)
  }

  // Production üçün təkmilləşdirilmiş API health check
  const checkAPIHealth = async (): Promise<boolean> => {
    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 10000) // 10 saniyə timeout

      const response = await fetch(API_ENDPOINTS.BOOKS_STATS, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        signal: controller.signal,
      })

      clearTimeout(timeoutId)

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      console.log('API Health Check Success:', data)
      return true

    } catch (err: any) {
      if (err.name === 'AbortError') {
        throw new Error('TIMEOUT_ERROR')
      }
      throw err
    }
  }

  // Site settings yüklə
  const loadSiteSettings = async () => {
    try {
      const response = await fetch(API_ENDPOINTS.SITE_SETTINGS, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const settings = await response.json()
        setSiteSettings(settings)
      }
    } catch (err) {
      console.warn('Site settings yüklənə bilmədi:', err)
    }
  }

  // Production üçün təkmilləşdirilmiş error handling
  const handleError = (err: any): APIError => {
    console.error('Production Error:', err)

    if (err.message === 'TIMEOUT_ERROR') {
      return { message: ERROR_MESSAGES.TIMEOUT_ERROR, code: 'TIMEOUT' }
    }

    if (err.name === 'TypeError' && err.message.includes('fetch')) {
      return { message: ERROR_MESSAGES.NETWORK_ERROR, code: 'NETWORK' }
    }

    if (err.status >= 500) {
      return { message: ERROR_MESSAGES.API_ERROR, code: 'SERVER_ERROR', status: err.status }
    }

    if (err.status >= 400) {
      return { message: `Client xətası: ${err.status}`, code: 'CLIENT_ERROR', status: err.status }
    }

    return { message: ERROR_MESSAGES.UNKNOWN_ERROR, code: 'UNKNOWN' }
  }

  // Production üçün retry mechanism
  const retryConnection = async () => {
    setRetryCount(prev => prev + 1)
    setError(null)
    setIsLoading(true)
    
    try {
      const isHealthy = await checkAPIHealth()
      if (isHealthy) {
        await loadSiteSettings()
        setError(null)
      }
    } catch (err) {
      const apiError = handleError(err)
      setError(apiError)
    } finally {
      setIsLoading(false)
    }
  }

  // Production üçün təkmilləşdirilmiş useEffect
  useEffect(() => {
    const initializeApp = async () => {
      try {
        const isHealthy = await checkAPIHealth()
        if (isHealthy) {
          await loadSiteSettings()
          setError(null)
        }
      } catch (err) {
        const apiError = handleError(err)
        setError(apiError)
      } finally {
        setIsLoading(false)
      }
    }

    initializeApp()
  }, [])

  // Production üçün təkmilləşdirilmiş loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Yüklənir...</p>
          <p className="text-sm text-gray-500 mt-2">Backend API yoxlanılır...</p>
        </div>
      </div>
    )
  }

  // Production üçün təkmilləşdirilmiş error state
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-4">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Xəta Baş Verdi</h1>
          <p className="text-gray-600 mb-4">{error.message}</p>
          
          {error.code === 'NETWORK' && (
            <p className="text-sm text-gray-500 mb-4">
              İnternet bağlantınızı yoxlayın və yenidən cəhd edin.
            </p>
          )}
          
          {error.code === 'SERVER_ERROR' && (
            <p className="text-sm text-gray-500 mb-4">
              Server problemi var. Texniki komandamız problemi həll etməyə çalışır.
            </p>
          )}

          <div className="space-y-3">
            <button 
              onClick={retryConnection}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors w-full"
            >
              Yenidən Cəhd Et ({retryCount + 1})
            </button>
            
            <button 
              onClick={() => window.location.reload()} 
              className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 transition-colors w-full"
            >
              Səhifəni Yenilə
            </button>
          </div>

          {retryCount > 2 && (
            <p className="text-xs text-gray-500 mt-4">
              Əgər problem davam edərsə, texniki dəstək ilə əlaqə saxlayın.
            </p>
          )}
        </div>
      </div>
    )
  }

  return (
    <AuthProvider>
      <CartProvider>
        <div className="min-h-screen bg-gray-50">
          <Header onAuthClick={openAuthModal} />
          <main>
            <HeroSection />
            <FeaturedBooks />
            <BookGrid />
          </main>
          <Footer />
          <AuthModal
            isOpen={isAuthModalOpen}
            onClose={() => setIsAuthModalOpen(false)}
            mode={authMode}
            onModeChange={setAuthMode}
          />
        </div>
      </CartProvider>
    </AuthProvider>
  )
}
