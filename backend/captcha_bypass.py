"""
Custom Captcha & Cloudflare Bypass Implementation
No 3rd party APIs - Uses browser automation and stealth techniques
"""

import logging
import random
import time
from playwright.sync_api import Page, Browser, BrowserContext

class CustomCaptchaBypass:
    """
    Custom captcha and Cloudflare bypass using browser automation
    No external paid services required
    """
    
    @staticmethod
    def apply_stealth_mode(page: Page):
        """Apply stealth techniques to avoid detection"""
        try:
            # Override navigator properties to appear as real user
            page.add_init_script("""
                // Override navigator.webdriver
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                // Override permissions
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
                
                // Override plugins to appear real
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                
                // Override languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
                
                // Chrome runtime
                window.chrome = {
                    runtime: {}
                };
                
                // Randomize canvas fingerprint
                const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
                HTMLCanvasElement.prototype.toDataURL = function(type) {
                    const shift = {
                        'r': Math.floor(Math.random() * 10) - 5,
                        'g': Math.floor(Math.random() * 10) - 5,
                        'b': Math.floor(Math.random() * 10) - 5,
                        'a': Math.floor(Math.random() * 10) - 5
                    };
                    
                    const ctx = this.getContext('2d');
                    const imageData = ctx.getImageData(0, 0, this.width, this.height);
                    for (let i = 0; i < imageData.data.length; i += 4) {
                        imageData.data[i] = imageData.data[i] + shift.r;
                        imageData.data[i + 1] = imageData.data[i + 1] + shift.g;
                        imageData.data[i + 2] = imageData.data[i + 2] + shift.b;
                        imageData.data[i + 3] = imageData.data[i + 3] + shift.a;
                    }
                    ctx.putImageData(imageData, 0, 0);
                    
                    return originalToDataURL.apply(this, arguments);
                };
            """)
            
            logging.info("Stealth mode applied successfully")
            return True
        except Exception as e:
            logging.error(f"Failed to apply stealth mode: {e}")
            return False
    
    @staticmethod
    def detect_cloudflare(page: Page):
        """Detect if Cloudflare challenge is present"""
        try:
            # Check for common Cloudflare indicators
            cloudflare_indicators = [
                'cloudflare',
                'cf-challenge',
                'Just a moment',
                'Checking your browser',
                'DDoS protection by Cloudflare'
            ]
            
            page_content = page.content().lower()
            
            for indicator in cloudflare_indicators:
                if indicator.lower() in page_content:
                    logging.info(f"Cloudflare detected: {indicator}")
                    return True
            
            # Check for Cloudflare script
            cf_scripts = page.locator('script[src*="cloudflare"]').count()
            if cf_scripts > 0:
                logging.info("Cloudflare script detected")
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Error detecting Cloudflare: {e}")
            return False
    
    @staticmethod
    def bypass_cloudflare(page: Page, timeout=30000):
        """
        Bypass Cloudflare challenge using browser automation
        Waits for the challenge to complete automatically
        """
        try:
            logging.info("Attempting Cloudflare bypass...")
            
            # Apply stealth mode first
            CustomCaptchaBypass.apply_stealth_mode(page)
            
            # Add random mouse movements to appear human
            try:
                viewport_size = page.viewport_size
                if viewport_size:
                    width = viewport_size['width']
                    height = viewport_size['height']
                    
                    # Perform random mouse movements
                    for _ in range(3):
                        x = random.randint(100, width - 100)
                        y = random.randint(100, height - 100)
                        page.mouse.move(x, y)
                        time.sleep(random.uniform(0.1, 0.3))
            except Exception as mouse_error:
                logging.debug(f"Mouse movement skipped: {mouse_error}")
            
            # Wait for Cloudflare challenge to complete
            # Modern Cloudflare challenges auto-complete with proper browser fingerprint
            start_time = time.time()
            max_wait = timeout / 1000  # Convert to seconds
            
            while time.time() - start_time < max_wait:
                # Check if challenge is gone
                if not CustomCaptchaBypass.detect_cloudflare(page):
                    logging.info("Cloudflare bypass successful")
                    return True
                
                # Check for success indicators
                current_url = page.url
                if 'cloudflare' not in current_url.lower():
                    # Check if we're on the actual page
                    try:
                        # Wait for body content
                        page.wait_for_selector('body', timeout=2000)
                        body_text = page.locator('body').inner_text()
                        
                        # If we have substantial content, bypass succeeded
                        if len(body_text) > 500 and 'cloudflare' not in body_text.lower():
                            logging.info("Cloudflare bypass successful - content loaded")
                            return True
                    except:
                        pass
                
                # Wait a bit before checking again
                time.sleep(1)
            
            logging.warning("Cloudflare bypass timeout - may still be in challenge")
            return False
            
        except Exception as e:
            logging.error(f"Cloudflare bypass error: {e}")
            return False
    
    @staticmethod
    def detect_captcha(page: Page):
        """Detect various types of captchas"""
        captcha_info = {
            'detected': False,
            'type': None,
            'site_key': None
        }
        
        try:
            # Detect reCAPTCHA v2
            if page.locator('iframe[src*="recaptcha/api2"]').count() > 0:
                captcha_info['detected'] = True
                captcha_info['type'] = 'recaptcha_v2'
                
                # Try to extract site key
                try:
                    site_key = page.evaluate("""
                        () => {
                            const iframe = document.querySelector('iframe[src*="recaptcha"]');
                            if (iframe) {
                                const match = iframe.src.match(/k=([^&]+)/);
                                return match ? match[1] : null;
                            }
                            return null;
                        }
                    """)
                    captcha_info['site_key'] = site_key
                except:
                    pass
                
                logging.info("reCAPTCHA v2 detected")
            
            # Detect reCAPTCHA v3
            elif page.locator('script[src*="recaptcha/api.js"]').count() > 0:
                captcha_info['detected'] = True
                captcha_info['type'] = 'recaptcha_v3'
                logging.info("reCAPTCHA v3 detected")
            
            # Detect hCaptcha
            elif page.locator('iframe[src*="hcaptcha"]').count() > 0:
                captcha_info['detected'] = True
                captcha_info['type'] = 'hcaptcha'
                
                # Try to extract site key
                try:
                    site_key = page.evaluate("""
                        () => {
                            const iframe = document.querySelector('iframe[src*="hcaptcha"]');
                            if (iframe) {
                                const match = iframe.src.match(/sitekey=([^&]+)/);
                                return match ? match[1] : null;
                            }
                            return null;
                        }
                    """)
                    captcha_info['site_key'] = site_key
                except:
                    pass
                
                logging.info("hCaptcha detected")
            
            # Detect Cloudflare Turnstile
            elif page.locator('iframe[src*="turnstile"]').count() > 0:
                captcha_info['detected'] = True
                captcha_info['type'] = 'turnstile'
                logging.info("Cloudflare Turnstile detected")
            
            return captcha_info
            
        except Exception as e:
            logging.error(f"Error detecting captcha: {e}")
            return captcha_info
    
    @staticmethod
    def auto_solve_captcha(page: Page, captcha_info: dict, timeout=60000):
        """
        Attempt to automatically solve captcha using browser automation
        This works for some simple captchas and invisible captchas
        """
        try:
            captcha_type = captcha_info.get('type')
            
            if not captcha_type:
                return False
            
            logging.info(f"Attempting auto-solve for {captcha_type}")
            
            # For reCAPTCHA v3 and invisible captchas, just wait
            if captcha_type == 'recaptcha_v3':
                # v3 is invisible and processes in background
                logging.info("reCAPTCHA v3 is invisible - waiting for automatic processing")
                time.sleep(3)
                return True
            
            # For visible captchas, perform human-like interactions
            if captcha_type in ['recaptcha_v2', 'hcaptcha', 'turnstile']:
                # Add random delays to appear human
                time.sleep(random.uniform(1, 3))
                
                # Try to find and click the checkbox (for reCAPTCHA v2)
                try:
                    # Switch to captcha iframe
                    frames = page.frames
                    for frame in frames:
                        if 'recaptcha' in frame.url or 'hcaptcha' in frame.url:
                            try:
                                # Look for checkbox
                                checkbox = frame.locator('.recaptcha-checkbox-border, .checkbox')
                                if checkbox.count() > 0:
                                    # Human-like delay before clicking
                                    time.sleep(random.uniform(0.5, 1.5))
                                    checkbox.first.click()
                                    logging.info("Clicked captcha checkbox")
                                    
                                    # Wait to see if it auto-solves
                                    time.sleep(5)
                                    
                                    # Check if solved
                                    if page.locator('.recaptcha-checkbox-checked').count() > 0:
                                        logging.info("Captcha auto-solved successfully")
                                        return True
                            except:
                                continue
                except Exception as e:
                    logging.debug(f"Checkbox interaction failed: {e}")
                
                # Wait and see if captcha disappears (some are automatic)
                start_time = time.time()
                while time.time() - start_time < (timeout / 1000):
                    new_captcha_info = CustomCaptchaBypass.detect_captcha(page)
                    if not new_captcha_info['detected']:
                        logging.info("Captcha bypassed successfully")
                        return True
                    time.sleep(1)
                
                logging.warning("Captcha auto-solve timeout")
                return False
            
            return False
            
        except Exception as e:
            logging.error(f"Auto-solve captcha error: {e}")
            return False
    
    @staticmethod
    def configure_browser_context(context: BrowserContext):
        """Configure browser context with anti-detection settings"""
        try:
            # Set realistic viewport
            viewports = [
                {'width': 1920, 'height': 1080},
                {'width': 1366, 'height': 768},
                {'width': 1536, 'height': 864},
            ]
            
            # Set extra HTTP headers to appear real
            context.set_extra_http_headers({
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
            })
            
            logging.info("Browser context configured with anti-detection settings")
            return True
            
        except Exception as e:
            logging.error(f"Failed to configure browser context: {e}")
            return False
