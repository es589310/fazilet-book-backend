"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { X, AlertCircle, CheckCircle } from "lucide-react"
import { useAuth } from "@/contexts/auth-context"
import { useErrorHandler } from "./error-boundary"

interface AuthModalProps {
  isOpen: boolean
  onClose: () => void
  mode: "login" | "register"
  onModeChange: (mode: "login" | "register") => void
}

interface FormData {
  email: string
  password: string
  name: string
  confirmPassword: string
}

interface AuthError {
  field?: string
  message: string
}

export function AuthModal({ isOpen, onClose, mode, onModeChange }: AuthModalProps) {
  const [formData, setFormData] = useState<FormData>({
    email: "",
    password: "",
    name: "",
    confirmPassword: "",
  })
  const [isLoading, setIsLoading] = useState(false)
  const [errors, setErrors] = useState<AuthError[]>([])
  const [successMessage, setSuccessMessage] = useState("")
  const { login } = useAuth()
  const { handleError, clearError } = useErrorHandler()

  if (!isOpen) return null

  // Clear errors and success message when mode changes
  const handleModeChange = (newMode: "login" | "register") => {
    setErrors([])
    setSuccessMessage("")
    clearError()
    onModeChange(newMode)
  }

  // Validate form data
  const validateForm = (): boolean => {
    const newErrors: AuthError[] = []

    if (mode === "register") {
      if (!formData.name.trim()) {
        newErrors.push({ field: "name", message: "Ad tələb olunur" })
      }
      
      if (formData.password !== formData.confirmPassword) {
        newErrors.push({ field: "confirmPassword", message: "Şifrələr uyğun gəlmir" })
      }
      
      if (formData.password.length < 6) {
        newErrors.push({ field: "password", message: "Şifrə ən azı 6 simvol olmalıdır" })
      }
    }

    if (!formData.email.trim()) {
      newErrors.push({ field: "email", message: "E-mail tələb olunur" })
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.push({ field: "email", message: "Düzgün e-mail ünvanı daxil edin" })
    }

    if (!formData.password.trim()) {
      newErrors.push({ field: "password", message: "Şifrə tələb olunur" })
    }

    setErrors(newErrors)
    return newErrors.length === 0
  }

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    setIsLoading(true)
    setErrors([])
    setSuccessMessage("")
    clearError()

    try {
      if (mode === "register") {
        // Register API call
        const response = await fetch('/api/auth/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: formData.email,
            email: formData.email,
            password: formData.password,
            first_name: formData.name,
          }),
        })

        const data = await response.json()

        if (!response.ok) {
          if (data.errors) {
            const apiErrors: AuthError[] = Object.entries(data.errors).map(([field, messages]) => ({
              field,
              message: Array.isArray(messages) ? messages[0] : String(messages),
            }))
            setErrors(apiErrors)
          } else {
            setErrors([{ message: data.message || 'Qeydiyyat uğursuz oldu' }])
          }
          return
        }

        setSuccessMessage("Qeydiyyat uğurla tamamlandı! İndi giriş edə bilərsiniz.")
        setTimeout(() => {
          onModeChange("login")
          setFormData({ email: "", password: "", name: "", confirmPassword: "" })
        }, 2000)

      } else {
        // Login API call
        const response = await fetch('/api/auth/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password,
          }),
        })

        const data = await response.json()

        if (!response.ok) {
          if (data.errors) {
            const apiErrors: AuthError[] = Object.entries(data.errors).map(([field, messages]) => ({
              field,
              message: Array.isArray(messages) ? messages[0] : String(messages),
            }))
            setErrors(apiErrors)
          } else {
            setErrors([{ message: data.message || 'Giriş uğursuz oldu' }])
          }
          return
        }

        // Login successful
        login({
          id: data.user.id,
          name: data.user.first_name || data.user.username || 'İstifadəçi',
          email: data.user.email,
          username: data.user.username,
          first_name: data.user.first_name,
          last_name: data.user.last_name,
        })

        setSuccessMessage("Uğurla giriş etdiniz!")
        setTimeout(() => {
          onClose()
          setFormData({ email: "", password: "", name: "", confirmPassword: "" })
        }, 1000)
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Xəta baş verdi'
      handleError(new Error(errorMessage))
      setErrors([{ message: 'Şəbəkə xətası. Zəhmət olmasa yenidən cəhd edin.' }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))

    // Clear field-specific error when user starts typing
    if (errors.some(error => error.field === name)) {
      setErrors(prev => prev.filter(error => error.field !== name))
    }
  }

  // Get error message for specific field
  const getFieldError = (fieldName: string): string | undefined => {
    return errors.find(error => error.field === fieldName)?.message
  }

  // Get general error message
  const getGeneralError = (): string | undefined => {
    return errors.find(error => !error.field)?.message
  }

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      <div className="absolute inset-0 bg-black bg-opacity-50" onClick={onClose} />
      <div className="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full max-w-md bg-white rounded-lg shadow-xl">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold">{mode === "login" ? "Giriş" : "Qeydiyyat"}</h2>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="h-5 w-5" />
            </Button>
          </div>

          {/* Success Message */}
          {successMessage && (
            <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg flex items-center space-x-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <span className="text-sm text-green-800">{successMessage}</span>
            </div>
          )}

          {/* General Error Message */}
          {getGeneralError() && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center space-x-2">
              <AlertCircle className="h-5 w-5 text-red-600" />
              <span className="text-sm text-red-800">{getGeneralError()}</span>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {mode === "register" && (
              <div>
                <Label htmlFor="name">Ad Soyad</Label>
                <Input
                  id="name"
                  name="name"
                  type="text"
                  required
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="Adınızı daxil edin"
                  className={getFieldError("name") ? "border-red-500" : ""}
                />
                {getFieldError("name") && (
                  <p className="text-sm text-red-600 mt-1">{getFieldError("name")}</p>
                )}
              </div>
            )}

            <div>
              <Label htmlFor="email">E-mail</Label>
              <Input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleInputChange}
                placeholder="E-mail ünvanınızı daxil edin"
                className={getFieldError("email") ? "border-red-500" : ""}
              />
              {getFieldError("email") && (
                <p className="text-sm text-red-600 mt-1">{getFieldError("email")}</p>
              )}
            </div>

            <div>
              <Label htmlFor="password">Şifrə</Label>
              <Input
                id="password"
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleInputChange}
                placeholder="Şifrənizi daxil edin"
                className={getFieldError("password") ? "border-red-500" : ""}
              />
              {getFieldError("password") && (
                <p className="text-sm text-red-600 mt-1">{getFieldError("password")}</p>
              )}
            </div>

            {mode === "register" && (
              <div>
                <Label htmlFor="confirmPassword">Şifrəni Təkrarla</Label>
                <Input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  required
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  placeholder="Şifrənizi təkrar daxil edin"
                  className={getFieldError("confirmPassword") ? "border-red-500" : ""}
                />
                {getFieldError("confirmPassword") && (
                  <p className="text-sm text-red-600 mt-1">{getFieldError("confirmPassword")}</p>
                )}
              </div>
            )}

            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? "Gözləyin..." : mode === "login" ? "Giriş Et" : "Qeydiyyatdan Keç"}
            </Button>
          </form>

          {/* Switch Mode */}
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              {mode === "login" ? "Hesabınız yoxdur?" : "Artıq hesabınız var?"}
              <Button
                variant="link"
                className="ml-1 p-0 h-auto"
                onClick={() => handleModeChange(mode === "login" ? "register" : "login")}
              >
                {mode === "login" ? "Qeydiyyatdan keçin" : "Giriş edin"}
              </Button>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
