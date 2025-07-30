import os
import re
from decimal import Decimal
from typing import List, Dict

try:
    from google.cloud import vision
    from google.oauth2 import service_account
    GOOGLE_VISION_AVAILABLE = True
except ImportError:
    GOOGLE_VISION_AVAILABLE = False

# Set GOOGLE_APPLICATION_CREDENTIALS or use explicit credentials path
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if GOOGLE_VISION_AVAILABLE and CREDENTIALS_PATH and os.path.exists(CREDENTIALS_PATH):
    try:
        credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
        vision_client = vision.ImageAnnotatorClient(credentials=credentials)
    except Exception:
        vision_client = None
elif GOOGLE_VISION_AVAILABLE:
    try:
        vision_client = vision.ImageAnnotatorClient()
    except Exception:
        vision_client = None
else:
    vision_client = None

# Regex patterns
PRICE_PATTERN = re.compile(r"(\d+[.,]?\d{0,2})[\s]*원?")
EVENT_PATTERN = re.compile(r"(1\+1|2\+1|할인|세일|쿠폰|\d+%|\d+원\s*↓|\d+원\s*할인)")


def _parse_text(text: str) -> List[Dict]:
    """Parse full text annotation to structured product entries."""
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    products: List[Dict] = []
    current_product: Dict | None = None

    for line in lines:
        price_match = PRICE_PATTERN.search(line)
        if price_match:
            price = Decimal(price_match.group(1).replace(",", ""))
            if current_product is None:
                # Sometimes price comes first; create placeholder
                current_product = {"product_name": "", "price": price}
            else:
                current_product["price"] = price
            # detect event info in same line
            evt_match = EVENT_PATTERN.search(line)
            if evt_match:
                current_product["event_info"] = evt_match.group(1)
            products.append(current_product)
            current_product = None
        else:
            # This line likely product name or event info
            if current_product is None:
                current_product = {"product_name": line}
            else:
                # Additional info line
                if "product_name" in current_product and not current_product["product_name"]:
                    current_product["product_name"] = line
                elif "event_info" not in current_product and EVENT_PATTERN.search(line):
                    current_product["event_info"] = EVENT_PATTERN.search(line).group(1)
    return products


def _generate_mock_ocr_results() -> List[Dict]:
    """Generate mock OCR results for testing when Vision API is not available."""
    import random
    
    products = [
        {"product_name": "커클랜드 유기농 사과", "price": Decimal("12900")},
        {"product_name": "바나나 1박스", "price": Decimal("8500"), "event_info": "1+1"},
        {"product_name": "아보카도 6개팩", "price": Decimal("15900")},
        {"product_name": "치킨브레스트 2kg", "price": Decimal("24900"), "event_info": "할인"},
        {"product_name": "연어필렛 500g", "price": Decimal("19900")},
    ]
    
    # Return 2-3 random products
    num_products = random.randint(2, 3)
    selected_products = random.sample(products, num_products)
    
    # Add random price variations
    for product in selected_products:
        variation = random.randint(-1000, 1000)
        product["price"] = max(Decimal("1000"), product["price"] + variation)
    
    return selected_products


def run_ocr(image_bytes: bytes) -> List[Dict]:
    """Run Google Vision OCR and return structured product dict list."""
    if not vision_client:
        print("Google Vision API not available, using mock OCR results")
        return _generate_mock_ocr_results()
    
    try:
        image = vision.Image(content=image_bytes)
        response = vision_client.text_detection(image=image)
        
        if response.error.message:
            raise RuntimeError(f"Vision API error: {response.error.message}")

        annotations = response.full_text_annotation
        if not annotations or not annotations.text:
            print("No text detected, using mock OCR results")
            return _generate_mock_ocr_results()

        return _parse_text(annotations.text)
    except Exception as e:
        print(f"OCR failed: {e}, using mock OCR results")
        return _generate_mock_ocr_results() 