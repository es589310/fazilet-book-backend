import * as React from "react"

const MOBILE_BREAKPOINT = 768

interface UseMobileReturn {
  isMobile: boolean
  error: string | null
  isLoading: boolean
}

export function useIsMobile(): UseMobileReturn {
  const [isMobile, setIsMobile] = React.useState<boolean>(false)
  const [error, setError] = React.useState<string | null>(null)
  const [isLoading, setIsLoading] = React.useState(true)

  React.useEffect(() => {
    try {
      // SSR compatibility check
      if (typeof window === 'undefined') {
        setIsLoading(false)
        return
      }

      const updateMobileState = () => {
        try {
          const newIsMobile = window.innerWidth < MOBILE_BREAKPOINT
          setIsMobile(newIsMobile)
          setError(null)
        } catch (err) {
          const errorMessage = 'Screen size detection failed'
          setError(errorMessage)
          console.error('Mobile detection error:', err)
        }
      }

      // Initial state
      updateMobileState()

      // Media query listener for responsive updates
      const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`)
      
      const handleMediaChange = (event: MediaQueryListEvent) => {
        try {
          setIsMobile(event.matches)
          setError(null)
        } catch (err) {
          const errorMessage = 'Media query change detection failed'
          setError(errorMessage)
          console.error('Media query change error:', err)
        }
      }

      // Add event listener
      if (mql.addEventListener) {
        mql.addEventListener("change", handleMediaChange)
      } else {
        // Fallback for older browsers
        mql.addListener(handleMediaChange)
      }

      // Cleanup function
      return () => {
        try {
          if (mql.removeEventListener) {
            mql.removeEventListener("change", handleMediaChange)
          } else {
            // Fallback for older browsers
            mql.removeListener(handleMediaChange)
          }
        } catch (err) {
          console.error('Media query cleanup error:', err)
        }
      }

    } catch (err) {
      const errorMessage = 'Mobile detection initialization failed'
      setError(errorMessage)
      console.error('Mobile hook initialization error:', err)
    } finally {
      setIsLoading(false)
    }
  }, [])

  // Reset error when mobile state changes successfully
  React.useEffect(() => {
    if (isMobile !== undefined && !error) {
      setError(null)
    }
  }, [isMobile, error])

  return { 
    isMobile, 
    error, 
    isLoading 
  }
}

// Convenience hook for boolean-only return (backward compatibility)
export function useIsMobileSimple(): boolean {
  const { isMobile, error } = useIsMobile()
  
  // Return false if there's an error (fallback to desktop behavior)
  if (error) {
    console.warn('Mobile detection error, falling back to desktop:', error)
    return false
  }
  
  return isMobile
}
