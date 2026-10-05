"""One sitemap for everything under ainjection.github.io (all project sites share the host). Re-run after adding pages."""
import glob, os, datetime
B = 'https://ainjection.github.io/'
urls = ['', 'gentle-bookshop/', 'halloween-books/', 'halloween-books/free-halloween-coloring-book.html', 'halloween-books/halloween-coloring-pages-printable.html',
        'halloween-books/best-pencils-for-grayscale-coloring.html', 'halloween-books/halloween-coloring-pages-for-adults.html', 'gentle-bookshop/about.html',
        'christmas-books/', 'christmas-books/free-christmas-coloring-pages.html', 'christmas-books/christmas-coloring-pages-printable.html', 'gentle-bookshop/practice/', 'curious-kids/', 'janice-kingsley/', 'ai-video-portfolio/']
urls += ['gentle-bookshop/books/' + os.path.basename(p) for p in sorted(glob.glob('D:/gentle-bookshop-live/books/*.html'))]
today = datetime.date.today().isoformat()
REPOS = {'halloween-books/': 'D:/halloween-books', 'gentle-bookshop/': 'D:/gentle-bookshop-live', 'christmas-books/': 'D:/christmas-books',
         'curious-kids/': 'D:/curious-kids', 'janice-kingsley/': 'D:/janice-kingsley', '': 'D:/ainjection-root'}
def lastmod(u):
    """Last commit date of the page's file in its repo (Google ignores a uniform lastmod). Falls back to today."""
    import subprocess
    for prefix, repo in sorted(REPOS.items(), key=lambda kv: -len(kv[0])):
        if u.startswith(prefix):
            rel = u[len(prefix):] or 'index.html'
            if rel.endswith('/'): rel += 'index.html'
            try:
                out = subprocess.run(['git', '-C', repo, 'log', '-1', '--format=%cs', '--', rel], capture_output=True, text=True, timeout=10).stdout.strip()
                if out: return out
            except Exception: pass
            break
    return today
body = ''.join(f'  <url><loc>{B}{u}</loc><lastmod>{lastmod(u)}</lastmod></url>\n' for u in urls)
open('sitemap.xml', 'w', encoding='utf-8').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n')
open('robots.txt', 'w', encoding='utf-8').write(
    'User-agent: *\nAllow: /\nDisallow: /gentle-bookshop/v3/\nDisallow: /gentle-bookshop/classic.html\n\n'
    # AI answer engines are welcome: the crawlers behind ChatGPT, Claude, Perplexity, Gemini, Copilot and Apple
    + ''.join(f'User-agent: {ua}\nAllow: /\n\n' for ua in ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot-Extended', 'CCBot', 'meta-externalagent'])
    + f'Sitemap: {B}sitemap.xml\n# AI-readable site summary: {B}llms.txt\n')
print(len(urls), 'urls')
