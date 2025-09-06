import type { Metadata } from 'next'
import { GeistSans } from 'geist/font/sans'
import { GeistMono } from 'geist/font/mono'
import './globals.css'

export const metadata: Metadata = {
  title: 'Fazilet Kitab - Online Kitab Mağazası',
  description: 'Ən yaxşı kitabları online satın alın. Türk və dünya ədəbiyyatı.',
  keywords: 'kitab, online mağaza, türk ədəbiyyatı, dünya ədəbiyyatı, kitab satışı',
  authors: [{ name: 'Dostum Kitab' }],
  creator: 'Dostum Kitab',
  publisher: 'Dostum Kitab',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://dostumkitab.az'),
  alternates: {
    canonical: '/',
  },
      openGraph: {
      title: 'Dostum Kitab - Online Kitab Mağazası',
      description: 'Ən yaxşı kitabları online satın alın. Türk və dünya ədəbiyyatı.',
      url: 'https://dostumkitab.az',
      siteName: 'Dostum Kitab',
      locale: 'az_AZ',
      type: 'website',
    },
  twitter: {
    card: 'summary_large_image',
    title: 'Dostum Kitab - Online Kitab Mağazası',
    description: 'Ən yaxşı kitabları online satın alın.',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="tr">
      <head>
        <style>{`
html {
  font-family: ${GeistSans.style.fontFamily};
  --font-sans: ${GeistSans.variable};
  --font-mono: ${GeistMono.variable};
}
        `}</style>
      </head>
      <body>{children}</body>
    </html>
  )
}
