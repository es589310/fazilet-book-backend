/** @type {import('next-sitemap').IConfig} */
module.exports = {
  siteUrl: process.env.NEXT_PUBLIC_SITE_URL || 'https://dostumkitab.az',
  generateRobotsTxt: true,
  generateIndexSitemap: false,
  exclude: ['/admin/*', '/api/*', '/_next/*', '/404', '/500'],
  robotsTxtOptions: {
    policies: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin/', '/api/', '/_next/', '/private/'],
      },
      {
        userAgent: 'Googlebot',
        allow: '/',
        disallow: ['/admin/', '/api/', '/_next/'],
      },
    ],
    additionalSitemaps: [
      'https://dostumkitab.az/sitemap.xml',
      'https://dostumkitab.az/books-sitemap.xml',
      'https://dostumkitab.az/categories-sitemap.xml',
    ],
  },
  changefreq: 'daily',
  priority: 0.7,
  sitemapSize: 5000,
  transform: async (config, path) => {
    // Custom priority for different page types
    let priority = config.priority;
    let changefreq = config.changefreq;

    if (path === '/') {
      priority = 1.0;
      changefreq = 'daily';
    } else if (path.startsWith('/book/')) {
      priority = 0.8;
      changefreq = 'weekly';
    } else if (path.startsWith('/category/')) {
      priority = 0.9;
      changefreq = 'weekly';
    } else if (path.startsWith('/search')) {
      priority = 0.6;
      changefreq = 'monthly';
    }

    return {
      loc: path,
      changefreq,
      priority,
      lastmod: new Date().toISOString(),
    };
  },
  additionalPaths: async (config) => {
    // Add dynamic paths for books and categories
    const result = [];

    // Books sitemap
    try {
      const booksResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/books/`);
      if (booksResponse.ok) {
        const books = await booksResponse.json();
        books.results?.forEach((book) => {
          result.push({
            loc: `/book/${book.slug}`,
            changefreq: 'weekly',
            priority: 0.8,
            lastmod: new Date().toISOString(),
          });
        });
      }
    } catch (error) {
      console.warn('Books sitemap generation failed:', error);
    }

    // Categories sitemap
    try {
      const categoriesResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/categories/`);
      if (categoriesResponse.ok) {
        const categories = await categoriesResponse.json();
        categories.results?.forEach((category) => {
          result.push({
            loc: `/category/${category.id}`,
            changefreq: 'weekly',
            priority: 0.9,
            lastmod: new Date().toISOString(),
          });
        });
      }
    } catch (error) {
      console.warn('Categories sitemap generation failed:', error);
    }

    return result;
  },
}; 