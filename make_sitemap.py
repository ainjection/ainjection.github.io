"""One sitemap for everything under ainjection.github.io (all project sites share the host). Re-run after adding pages."""
import glob, os, datetime
B = 'https://ainjection.github.io/'
urls = ['', 'gentle-bookshop/', 'halloween-books/', 'halloween-books/halloween-coloring-pages-printable.html',
        'christmas-books/', 'christmas-books/christmas-coloring-pages-printable.html', 'gentle-bookshop/practice/', 'ai-video-portfolio/']
urls += ['gentle-bookshop/books/' + os.path.basename(p) for p in sorted(glob.glob('D:/gentle-bookshop-live/books/*.html'))]
today = datetime.date.today().isoformat()
body = ''.join(f'  <url><loc>{B}{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls)
open('sitemap.xml', 'w', encoding='utf-8').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n')
open('robots.txt', 'w', encoding='utf-8').write(
    'User-agent: *\nAllow: /\nDisallow: /gentle-bookshop/v3/\nDisallow: /gentle-bookshop/classic.html\n\n'
    f'Sitemap: {B}sitemap.xml\n')
print(len(urls), 'urls')
