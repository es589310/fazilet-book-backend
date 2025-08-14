"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"

interface User {
  id: number
  name: string
  email: string
  username?: string
  first_name?: string
  last_name?: string
}

interface AuthResponse {
  user: User
  access: string
  refresh?: string
}

interface AuthContextType {
  user: User | null
  token: string | null
  isLoading: boolean
  login: (credentials: { email: string; password: string }) => Promise<void>
  logout: () => Promise<void>
  register: (userData: { name: string; email: string; password: string; confirmPassword: string }) => Promise<void>
  isAuthenticated: boolean
  refreshToken: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

// Secure storage utilities
const secureStorage = {
  setItem: (key: string, value: string) => {
    try {
      if (typeof window !== 'undefined') {
        localStorage.setItem(key, value)
      }
    } catch (error) {
      console.error('Storage error:', error)
    }
  },
  
  getItem: (key: string): string | null => {
    try {
      if (typeof window !== 'undefined') {
        return localStorage.getItem(key)
      }
      return null
    } catch (error) {
      console.error('Storage error:', error)
      return null
    }
  },
  
  removeItem: (key: string) => {
    try {
      if (typeof window !== 'undefined') {
        localStorage.removeItem(key)
      }
    } catch (error) {
      console.error('Storage error:', error)
    }
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Check authentication status on mount
  useEffect(() => {
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    try {
      setIsLoading(true)
      const savedToken = secureStorage.getItem('token')
      const savedUser = secureStorage.getItem('user')
      
      if (savedToken && savedUser) {
        // Verify token with backend
        try {
          const response = await fetch('/api/auth/me/', {
            headers: {
              'Authorization': `Bearer ${savedToken}`,
              'Content-Type': 'application/json'
            }
          })
          
          if (response.ok) {
            const userData = await response.json()
            setUser(userData)
            setToken(savedToken)
          } else {
            // Token invalid, clear storage
            clearAuthData()
          }
        } catch (error) {
          // Network error, clear storage
          clearAuthData()
        }
      }
    } catch (error) {
      console.error('Auth status check error:', error)
      clearAuthData()
    } finally {
      setIsLoading(false)
    }
  }

  const clearAuthData = () => {
    setUser(null)
    setToken(null)
    secureStorage.removeItem('token')
    secureStorage.removeItem('user')
  }

  const login = async (credentials: { email: string; password: string }) => {
    try {
      setIsLoading(true)
      
      const response = await fetch('/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || 'Giriş uğursuz oldu')
      }
      
      const authData: AuthResponse = await response.json()
      
      // Set user and token
      setUser(authData.user)
      setToken(authData.access)
      
      // Store in secure storage
      secureStorage.setItem('token', authData.access)
      secureStorage.setItem('user', JSON.stringify(authData.user))
      
      // Store refresh token if available
      if (authData.refresh) {
        secureStorage.setItem('refresh_token', authData.refresh)
      }
      
    } catch (error) {
      console.error('Login error:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const register = async (userData: { name: string; email: string; password: string; confirmPassword: string }) => {
    try {
      setIsLoading(true)
      
      if (userData.password !== userData.confirmPassword) {
        throw new Error('Şifrələr uyğun gəlmir')
      }
      
      const response = await fetch('/api/auth/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: userData.email,
          email: userData.email,
          password: userData.password,
          first_name: userData.name
        })
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || 'Qeydiyyat uğursuz oldu')
      }
      
      // Registration successful, user can now login
      
    } catch (error) {
      console.error('Register error:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const logout = async () => {
    try {
      // Call backend logout if token exists
      if (token) {
        try {
          await fetch('/api/auth/logout/', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          })
        } catch (error) {
          // Ignore logout errors, still clear local data
          console.warn('Backend logout failed:', error)
        }
      }
      
      // Clear local data
      clearAuthData()
      
    } catch (error) {
      console.error('Logout error:', error)
      // Force clear local data even if error
      clearAuthData()
    }
  }

  const refreshToken = async () => {
    try {
      const refreshToken = secureStorage.getItem('refresh_token')
      
      if (!refreshToken) {
        throw new Error('Refresh token not found')
      }
      
      const response = await fetch('/api/auth/refresh/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          refresh: refreshToken
        })
      })
      
      if (response.ok) {
        const authData: AuthResponse = await response.json()
        setToken(authData.access)
        secureStorage.setItem('token', authData.access)
        
        if (authData.refresh) {
          secureStorage.setItem('refresh_token', authData.refresh)
        }
      } else {
        // Refresh failed, logout user
        logout()
      }
      
    } catch (error) {
      console.error('Token refresh error:', error)
      logout()
    }
  }

  const isAuthenticated = !!user && !!token

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        login,
        logout,
        register,
        isAuthenticated,
        refreshToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
