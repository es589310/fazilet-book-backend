"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"

interface CartItem {
  id: number
  title: string
  author: string
  price: number
  image: string
  quantity: number
  stock?: number
  maxQuantity?: number
}

interface CartContextType {
  items: CartItem[]
  isLoading: boolean
  addItem: (item: Omit<CartItem, "quantity"> & { quantity?: number }) => void
  removeItem: (id: number) => void
  updateQuantity: (id: number, quantity: number) => void
  getTotalPrice: () => number
  getTotalItems: () => number
  clearCart: () => void
  syncWithBackend: () => Promise<void>
  saveToBackend: () => Promise<void>
}

const CartContext = createContext<CartContextType | undefined>(undefined)

// Secure storage utilities
const secureStorage = {
  setItem: (key: string, value: string) => {
    try {
      if (typeof window !== 'undefined') {
        localStorage.setItem(key, value)
      }
    } catch (error) {
      console.error('Cart storage error:', error)
    }
  },
  
  getItem: (key: string): string | null => {
    try {
      if (typeof window !== 'undefined') {
        return localStorage.getItem(key)
      }
      return null
    } catch (error) {
      console.error('Cart storage error:', error)
      return null
    }
  },
  
  removeItem: (key: string) => {
    try {
      if (typeof window !== 'undefined') {
        localStorage.removeItem(key)
      }
    } catch (error) {
      console.error('Cart storage error:', error)
    }
  }
}

// Cart validation utilities
const validateCartItem = (item: Omit<CartItem, "quantity"> & { quantity?: number }): void => {
  if (!item.id || typeof item.id !== 'number') {
    throw new Error('Yanlış məhsul ID-si')
  }
  
  if (!item.title || typeof item.title !== 'string') {
    throw new Error('Məhsul adı tələb olunur')
  }
  
  if (!item.price || typeof item.price !== 'number' || item.price <= 0) {
    throw new Error('Yanlış qiymət')
  }
  
  if (item.quantity && (typeof item.quantity !== 'number' || item.quantity <= 0)) {
    throw new Error('Yanlış miqdar')
  }
  
  if (item.stock !== undefined && item.stock < 0) {
    throw new Error('Yanlış stok məlumatı')
  }
}

const validateQuantity = (quantity: number, stock?: number, maxQuantity?: number): void => {
  if (quantity <= 0) {
    throw new Error('Miqdar 0-dan böyük olmalıdır')
  }
  
  if (quantity > 99) {
    throw new Error('Maksimum miqdar 99 ola bilər')
  }
  
  if (stock !== undefined && quantity > stock) {
    throw new Error(`Stokda yalnız ${stock} ədəd var`)
  }
  
  if (maxQuantity !== undefined && quantity > maxQuantity) {
    throw new Error(`Maksimum miqdar ${maxQuantity} ola bilər`)
  }
}

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>(() => {
    // Load cart data from localStorage on mount
    if (typeof window !== 'undefined') {
      try {
        const saved = secureStorage.getItem('cart')
        return saved ? JSON.parse(saved) : []
      } catch (error) {
        console.error('Failed to load cart from storage:', error)
        return []
      }
    }
    return []
  })
  
  const [isLoading, setIsLoading] = useState(false)

  // Save cart data to localStorage whenever items change
  useEffect(() => {
    if (typeof window !== 'undefined') {
      try {
        secureStorage.setItem('cart', JSON.stringify(items))
      } catch (error) {
        console.error('Failed to save cart to storage:', error)
      }
    }
  }, [items])

  const addItem = (newItem: Omit<CartItem, "quantity"> & { quantity?: number }) => {
    try {
      // Validate input
      validateCartItem(newItem)
      
      const quantity = newItem.quantity || 1
      validateQuantity(quantity, newItem.stock, newItem.maxQuantity)
      
      setItems((prevItems) => {
        const existingItem = prevItems.find((item) => item.id === newItem.id)

        if (existingItem) {
          // Check if adding more would exceed limits
          const newQuantity = existingItem.quantity + quantity
          validateQuantity(newQuantity, newItem.stock, newItem.maxQuantity)
          
          return prevItems.map((item) =>
            item.id === newItem.id ? { ...item, quantity: newQuantity } : item,
          )
        }

        return [...prevItems, { ...newItem, quantity }]
      })
      
    } catch (error) {
      console.error('Cart add item error:', error)
      throw error
    }
  }

  const removeItem = (id: number) => {
    try {
      if (!id || typeof id !== 'number') {
        throw new Error('Yanlış məhsul ID-si')
      }
      
      setItems((prevItems) => prevItems.filter((item) => item.id !== id))
      
    } catch (error) {
      console.error('Cart remove item error:', error)
      throw error
    }
  }

  const updateQuantity = (id: number, quantity: number) => {
    try {
      if (!id || typeof id !== 'number') {
        throw new Error('Yanlış məhsul ID-si')
      }
      
      if (quantity <= 0) {
        removeItem(id)
        return
      }
      
      // Find item to get stock info
      const item = items.find(item => item.id === id)
      if (item) {
        validateQuantity(quantity, item.stock, item.maxQuantity)
      }
      
      setItems((prevItems) => 
        prevItems.map((item) => 
          item.id === id ? { ...item, quantity } : item
        )
      )
      
    } catch (error) {
      console.error('Cart update quantity error:', error)
      throw error
    }
  }

  const getTotalPrice = (): number => {
    try {
      return items.reduce((total, item) => {
        const itemTotal = item.price * item.quantity
        if (isNaN(itemTotal)) {
          console.warn('Invalid item total for item:', item)
          return total
        }
        return total + itemTotal
      }, 0)
    } catch (error) {
      console.error('Cart total price calculation error:', error)
      return 0
    }
  }

  const getTotalItems = (): number => {
    try {
      return items.reduce((total, item) => {
        if (typeof item.quantity === 'number' && !isNaN(item.quantity)) {
          return total + item.quantity
        }
        return total
      }, 0)
    } catch (error) {
      console.error('Cart total items calculation error:', error)
      return 0
    }
  }

  const clearCart = () => {
    try {
      setItems([])
      secureStorage.removeItem('cart')
    } catch (error) {
      console.error('Cart clear error:', error)
    }
  }

  const syncWithBackend = async (): Promise<void> => {
    try {
      setIsLoading(true)
      
      // Get auth token
      const token = secureStorage.getItem('token')
      if (!token) {
        console.warn('No auth token, skipping backend sync')
        return
      }
      
      // Fetch cart from backend
      const response = await fetch('/api/cart/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const backendCart = await response.json()
        
        // Merge with local cart (backend takes precedence for stock/price)
        const mergedItems = items.map(localItem => {
          const backendItem = backendCart.items?.find((item: any) => item.id === localItem.id)
          if (backendItem) {
            return {
              ...localItem,
              price: backendItem.price,
              stock: backendItem.stock,
              maxQuantity: backendItem.max_quantity
            }
          }
          return localItem
        })
        
        setItems(mergedItems)
      }
      
    } catch (error) {
      console.error('Cart backend sync error:', error)
      // Don't throw error, just log it
    } finally {
      setIsLoading(false)
    }
  }

  const saveToBackend = async (): Promise<void> => {
    try {
      setIsLoading(true)
      
      // Get auth token
      const token = secureStorage.getItem('token')
      if (!token) {
        console.warn('No auth token, skipping backend save')
        return
      }
      
      // Save cart to backend
      const response = await fetch('/api/cart/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          items: items.map(item => ({
            id: item.id,
            quantity: item.quantity
          }))
        })
      })
      
      if (!response.ok) {
        throw new Error('Backend cart save failed')
      }
      
    } catch (error) {
      console.error('Cart backend save error:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <CartContext.Provider
      value={{
        items,
        isLoading,
        addItem,
        removeItem,
        updateQuantity,
        getTotalPrice,
        getTotalItems,
        clearCart,
        syncWithBackend,
        saveToBackend,
      }}
    >
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  const context = useContext(CartContext)
  if (context === undefined) {
    throw new Error("useCart must be used within a CartProvider")
  }
  return context
}
