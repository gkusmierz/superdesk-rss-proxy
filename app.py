from flask import Flask, Response, request, make_response
import cloudscraper

app = Flask(__name__)

@app.route('/feed')
def proxy_feed():
    rss_url = request.args.get('url', 'https://www.lublin112.pl/feed/')

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
        'Accept': 'application/rss+xml, application/xml;q=0.9, */*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        # Use cloudscraper to bypass Cloudflare
        scraper = cloudscraper.create_scraper()
        response = scraper.get(rss_url, headers=headers)
        response.raise_for_status()

        # Create a Flask Response object with the content
        flask_response = make_response(response.content)

        # Copy relevant headers from the original response
        for header_name, header_value in response.headers.items():
            if header_name.lower() not in ['content-encoding', 'content-length', 'transfer-encoding', 'content-disposition']:
                flask_response.headers[header_name] = header_value

        # Set the Content-Type header to display content in browser
        flask_response.headers['Content-Type'] = 'application/rss+xml; charset=utf-8'

        # Remove Content-Disposition header to prevent download
        flask_response.headers.pop('Content-Disposition', None)

        return flask_response

    except Exception as e:
        return f"Error fetching RSS feed: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
