import { BookOpen, Mail, Phone } from "lucide-react"

export function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Logo and Description */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <BookOpen className="h-8 w-8 text-blue-400" />
              <span className="text-2xl font-bold">KitabSat</span>
            </div>
            <p className="text-gray-300 mb-4 max-w-md">
              Azərbaycanda ən böyük onlayn kitab mağazası. Minlərlə kitab, ən yaxşı qiymətlər və sürətli çatdırılma
              xidməti.
            </p>
            <div className="flex space-x-4">
              <div className="flex items-center text-sm text-gray-300">
                <Phone className="h-4 w-4 mr-2" />
                +994 12 345 67 89
              </div>
              <div className="flex items-center text-sm text-gray-300">
                <Mail className="h-4 w-4 mr-2" />
                info@kitabsat.az
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Sürətli Keçidlər</h3>
            <ul className="space-y-2 text-gray-300">
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Ana Səhifə
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Kitablar
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Kateqoriyalar
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Bestsellerlər
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Endirimlər
                </a>
              </li>
            </ul>
          </div>

          {/* Customer Service */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Müştəri Xidməti</h3>
            <ul className="space-y-2 text-gray-300">
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Əlaqə
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Çatdırılma
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Qaytarma
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  FAQ
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Dəstək
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2024 KitabSat. Bütün hüquqlar qorunur.</p>
        </div>
      </div>
    </footer>
  )
}
