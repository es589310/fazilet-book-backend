"use client"

// Inspired by react-hot-toast library
import * as React from "react"

import type {
  ToastActionElement,
  ToastProps,
} from "@/components/ui/toast"

// Production-optimized toast configuration
const TOAST_LIMIT = 5  // More reasonable limit
const TOAST_REMOVE_DELAY = 5000  // 5 seconds default
const TOAST_REMOVE_DELAY_FAST = 3000  // Fast removal for errors
const TOAST_REMOVE_DELAY_SLOW = 8000  // Slow removal for success messages

type ToasterToast = ToastProps & {
  id: string
  title?: React.ReactNode
  description?: React.ReactNode
  action?: ToastActionElement
  role?: 'status' | 'alert'  // Accessibility role
  'aria-live'?: 'polite' | 'assertive'  // Screen reader support
  duration?: number  // Configurable duration
}

const actionTypes = {
  ADD_TOAST: "ADD_TOAST",
  UPDATE_TOAST: "UPDATE_TOAST",
  DISMISS_TOAST: "DISMISS_TOAST",
  REMOVE_TOAST: "REMOVE_TOAST",
} as const

let count = 0

function genId() {
  count = (count + 1) % Number.MAX_SAFE_INTEGER
  return count.toString()
}

type ActionType = typeof actionTypes

type Action =
  | {
      type: ActionType["ADD_TOAST"]
      toast: ToasterToast
    }
  | {
      type: ActionType["UPDATE_TOAST"]
      toast: Partial<ToasterToast>
    }
  | {
      type: ActionType["DISMISS_TOAST"]
      toastId?: ToasterToast["id"]
    }
  | {
      type: ActionType["REMOVE_TOAST"]
      toastId?: ToasterToast["id"]
    }

interface State {
  toasts: ToasterToast[]
}

// Global timeout management with cleanup
const toastTimeouts = new Map<string, ReturnType<typeof setTimeout>>()

// Cleanup function for timeouts
const cleanupTimeouts = () => {
  try {
    toastTimeouts.forEach((timeout) => {
      if (timeout) {
        clearTimeout(timeout)
      }
    })
    toastTimeouts.clear()
  } catch (error) {
    console.error('Toast timeout cleanup error:', error)
  }
}

// Cleanup on page unload
if (typeof window !== 'undefined') {
  window.addEventListener('beforeunload', cleanupTimeouts)
}

const addToRemoveQueue = (toastId: string, duration?: number) => {
  try {
    // Clear existing timeout if any
    if (toastTimeouts.has(toastId)) {
      const existingTimeout = toastTimeouts.get(toastId)
      if (existingTimeout) {
        clearTimeout(existingTimeout)
      }
      toastTimeouts.delete(toastId)
    }

    const timeout = setTimeout(() => {
      try {
        toastTimeouts.delete(toastId)
        dispatch({
          type: "REMOVE_TOAST",
          toastId: toastId,
        })
      } catch (error) {
        console.error('Toast removal error:', error)
      }
    }, duration || TOAST_REMOVE_DELAY)

    toastTimeouts.set(toastId, timeout)
  } catch (error) {
    console.error('Toast timeout setup error:', error)
  }
}

export const reducer = (state: State, action: Action): State => {
  try {
    switch (action.type) {
      case "ADD_TOAST":
        return {
          ...state,
          toasts: [action.toast, ...state.toasts].slice(0, TOAST_LIMIT),
        }

      case "UPDATE_TOAST":
        return {
          ...state,
          toasts: state.toasts.map((t) =>
            t.id === action.toast.id ? { ...t, ...action.toast } : t
          ),
        }

      case "DISMISS_TOAST": {
        const { toastId } = action

        // Add to removal queue
        if (toastId) {
          addToRemoveQueue(toastId)
        } else {
          state.toasts.forEach((toast) => {
            addToRemoveQueue(toast.id)
          })
        }

        return {
          ...state,
          toasts: state.toasts.map((t) =>
            toastId === undefined || t.id === toastId
              ? {
                  ...t,
                  open: false,
                }
              : t
          ),
        }
      }
      
      case "REMOVE_TOAST":
        if (action.toastId === undefined) {
          return {
            ...state,
            toasts: [],
          }
        }
        return {
          ...state,
          toasts: state.toasts.filter((t) => t.id !== action.toastId),
        }
        
      default:
        return state
    }
  } catch (error) {
    console.error('Toast reducer error:', error)
    return state
  }
}

const listeners: Array<(state: State) => void> = []

let memoryState: State = { toasts: [] }

function dispatch(action: Action) {
  try {
    memoryState = reducer(memoryState, action)
    
    // Batch updates for better performance
    React.startTransition(() => {
      listeners.forEach((listener, index) => {
        try {
          listener(memoryState)
        } catch (error) {
          console.error('Toast listener error:', error)
          // Remove problematic listener
          if (index > -1) {
            listeners.splice(index, 1)
          }
        }
      })
    })
  } catch (error) {
    console.error('Toast dispatch error:', error)
  }
}

type Toast = Omit<ToasterToast, "id">

function toast({ 
  duration,
  role = 'status',
  'aria-live': ariaLive = 'polite',
  ...props 
}: Toast) {
  try {
    const id = genId()

    const update = (updateProps: ToasterToast) => {
      try {
        dispatch({
          type: "UPDATE_TOAST",
          toast: { ...updateProps, id },
        })
      } catch (error) {
        console.error('Toast update error:', error)
      }
    }
    
    const dismiss = () => {
      try {
        dispatch({ type: "DISMISS_TOAST", toastId: id })
      } catch (error) {
        console.error('Toast dismiss error:', error)
      }
    }

    // Determine duration based on toast type
    let toastDuration = duration
    if (!toastDuration) {
      if (props.variant === 'destructive') {
        toastDuration = TOAST_REMOVE_DELAY_FAST
      } else if (props.variant === 'default') {
        toastDuration = TOAST_REMOVE_DELAY_SLOW
      } else {
        toastDuration = TOAST_REMOVE_DELAY
      }
    }

    dispatch({
      type: "ADD_TOAST",
      toast: {
        ...props,
        id,
        open: true,
        role,
        'aria-live': ariaLive,
        duration: toastDuration,
        onOpenChange: (open) => {
          if (!open) dismiss()
        },
      },
    })

    return {
      id: id,
      dismiss,
      update,
    }
  } catch (error) {
    console.error('Toast creation error:', error)
    // Return a dummy toast object to prevent crashes
    return {
      id: 'error',
      dismiss: () => {},
      update: () => {},
    }
  }
}

function useToast() {
  const [state, setState] = React.useState<State>(memoryState)

  React.useEffect(() => {
    try {
      listeners.push(setState)
      
      return () => {
        try {
          const index = listeners.indexOf(setState)
          if (index > -1) {
            listeners.splice(index, 1)
          }
        } catch (error) {
          console.error('Toast listener cleanup error:', error)
        }
      }
    } catch (error) {
      console.error('Toast hook setup error:', error)
    }
  }, [])

  // Cleanup timeouts on unmount
  React.useEffect(() => {
    return () => {
      // Clean up any timeouts for toasts that are no longer visible
      try {
        const visibleToastIds = new Set(state.toasts.map(t => t.id))
        toastTimeouts.forEach((timeout, toastId) => {
          if (!visibleToastIds.has(toastId)) {
            clearTimeout(timeout)
            toastTimeouts.delete(toastId)
          }
        })
      } catch (error) {
        console.error('Toast cleanup error:', error)
      }
    }
  }, [state.toasts])

  return {
    ...state,
    toast,
    dismiss: (toastId?: string) => {
      try {
        dispatch({ type: "DISMISS_TOAST", toastId })
      } catch (error) {
        console.error('Toast dismiss error:', error)
      }
    },
  }
}

// Utility functions for common toast types
export const toastSuccess = (title: string, description?: string) => {
  return toast({
    title,
    description,
    variant: 'default',
    duration: TOAST_REMOVE_DELAY_SLOW,
    role: 'status',
    'aria-live': 'polite',
  })
}

export const toastError = (title: string, description?: string) => {
  return toast({
    title,
    description,
    variant: 'destructive',
    duration: TOAST_REMOVE_DELAY_FAST,
    role: 'alert',
    'aria-live': 'assertive',
  })
}

export const toastWarning = (title: string, description?: string) => {
  return toast({
    title,
    description,
    variant: 'default',
    duration: TOAST_REMOVE_DELAY,
    role: 'status',
    'aria-live': 'polite',
  })
}

export const toastInfo = (title: string, description?: string) => {
  return toast({
    title,
    description,
    variant: 'default',
    duration: TOAST_REMOVE_DELAY,
    role: 'status',
    'aria-live': 'polite',
  })
}

export { useToast, toast }
