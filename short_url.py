import random
import time

class URLShortener:
    def __init__(self):
        self.s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.url_map = {}  # Maps original URL -> structured data
        self.code_map = {}  # Maps short code -> original URL
        self.base_url = "https://short.ly/"
        self.pre_generated_codes = set(self._generate_pre_generated_codes(10))
        
    def _generate_code(self, length = 7):
        short = [random.choice(self.s) for _ in range(length)]
        return ''.join(short)
        
    def _generate_pre_generated_codes(self, num_codes, length=7):
        codes = []
        for _ in range(num_codes):
            shorten = ''.join(random.choice(self.s) for _ in range(length))
            codes.append(shorten)
        return codes
        
    def shorten_url(self, original_url, expiry_time=None, custom_alias=None):
        # see if original url already in db
        if original_url in self.url_map:
            return self.base_url + self.url_map[original_url]['shorten_code']
        
        # if not present create a short url and return
        if custom_alias:
            short_code = custom_alias
            if short_code in self.code_map:
                return "custom alias taken"
        else:
            # Use pre-generated codes first
            if self.pre_generated_codes:
                short_code = self.pre_generated_codes.pop()
            else:
                short_code = self._generate_code()
                
            # Ensure no collision
            while short_code in self.code_map:
                short_code = self._generate_code()
        #store
        self.url_map[original_url] = {
            'shorten_code': short_code,
            'expiration_time': time.time() + expiry_time if expiry_time else None,
            'clicks': 0,
        }
        self.code_map[short_code] = original_url
        return self.base_url + short_code
        
    def get_original_url(self, short_url):
        shorten_code = short_url.replace(self.base_url, "")
        if shorten_code not in self.code_map:
            return "404: Not Found"
        # Retrieve the original URL
        original_url = self.code_map[shorten_code]
        url_data = self.url_map[original_url]

        # Check for expiration
        if url_data['expiration_time'] and time.time() > url_data['expiration_time']:
            # Remove expired short code
            self._remove_expired_code(shorten_code, original_url)
            return "This short URL has expired."

        # Track clicks
        url_data['clicks'] += 1

        return original_url
    def get_all_urls(self):
        return {
            url: self.base_url + data['shorten_code']
            for url, data in self.url_map.items()
        }
    def get_click_stats(self):
        """
        Retrieve click analytics for all URLs.
        """
        return {
            self.base_url + data['shorten_code']: data['clicks']
            for url, data in self.url_map.items()
        }
    def _remove_expired_code(self, short_code, original_url):
        """
        Remove expired short code and its associated mappings.
        """
        self.code_map.pop(short_code, None)
        self.url_map.pop(original_url, None)
        
shortener = URLShortener()
short1 = shortener.shorten_url("http://www.example.com/my-blog", expiry_time=10)  # Expires in 30 seconds
short2 = shortener.shorten_url("http://www.example.com/awesome-article", custom_alias="custom123")
short3 = shortener.shorten_url("http://www.example.com/short-code")

print("Shortened URLs:")
print(short1)
print(short2)
print(short3)

print("\nOriginal URL for Shortened URL:")
print(shortener.get_original_url(short1))

print("\nAll URLs:")
print(shortener.get_all_urls())
time.sleep(15)
print("\nAfter Expiry:")
print(shortener.get_original_url(short1))  # Should indicate expiry

print(shortener.get_click_stats())