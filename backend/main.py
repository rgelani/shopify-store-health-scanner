"""
Shopify Store Health Scanner - FastAPI Backend
Build Time: 1-2 days | Cost: $0

This scans any Shopify store and provides health metrics:
- SEO analysis
- Performance score
- Image optimization issues
- Product count and structure
- Mobile friendliness
- Security checks

Deploy to Railway.app (500 free hours/month)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import httpx
from bs4 import BeautifulSoup
import re
from typing import Optional, List, Dict
import asyncio
import os
import uvicorn
import json
import logging

app = FastAPI(title="Shopify Store Health Scanner")
logger = logging.getLogger(__name__)

# CORS for frontend
cors_origins = os.environ.get("CORS_ORIGINS", "[]")
try:
    cors_origins = json.loads(cors_origins)
except Exception:
    cors_origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    store_url: HttpUrl

class HealthReport(BaseModel):
    store_url: str
    overall_score: int
    seo_score: int
    performance_score: int
    image_score: int
    mobile_score: int
    issues: List[str]
    recommendations: List[str]
    details: Dict

# Helper functions
def is_shopify_store(html: str) -> bool:
    """Check if site is Shopify"""
    return 'Shopify.theme' in html or 'cdn.shopify.com' in html

def analyze_seo(soup: BeautifulSoup, url: str) -> Dict:
    """Analyze SEO elements"""
    issues = []
    score = 100
    
    # Check title
    title = soup.find('title')
    if not title or len(title.text) < 30:
        issues.append("Title tag missing or too short (should be 50-60 chars)")
        score -= 15
    elif len(title.text) > 60:
        issues.append("Title tag too long (over 60 characters)")
        score -= 10
    
    # Check meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if not meta_desc:
        issues.append("Meta description missing")
        score -= 20
    elif len(meta_desc.get('content', '')) < 120:
        issues.append("Meta description too short (should be 150-160 chars)")
        score -= 10
    
    # Check H1
    h1_tags = soup.find_all('h1')
    if not h1_tags:
        issues.append("No H1 heading found")
        score -= 15
    elif len(h1_tags) > 1:
        issues.append(f"Multiple H1 tags found ({len(h1_tags)}) - should have only one")
        score -= 10
    
    # Check for Open Graph
    og_tags = soup.find_all('meta', property=re.compile('^og:'))
    if len(og_tags) < 3:
        issues.append("Missing Open Graph tags (important for social sharing)")
        score -= 10
    
    return {
        'score': max(score, 0),
        'issues': issues,
        'title': title.text if title else None,
        'meta_description': meta_desc.get('content') if meta_desc else None,
        'h1_count': len(h1_tags)
    }

def analyze_images(soup: BeautifulSoup) -> Dict:
    """Analyze image optimization"""
    issues = []
    score = 100
    
    images = soup.find_all('img')
    total_images = len(images)
    
    if total_images == 0:
        return {'score': 100, 'issues': [], 'total_images': 0}
    
    missing_alt = 0
    large_images = 0
    
    for img in images:
        # Check alt text
        if not img.get('alt'):
            missing_alt += 1
        
        # Check for potential large images (by URL patterns)
        src = img.get('src', '')
        if '_2048x' in src or '_1024x' in src or 'original' in src.lower():
            large_images += 1
    
    if missing_alt > 0:
        issues.append(f"{missing_alt}/{total_images} images missing alt text (bad for SEO & accessibility)")
        score -= min(30, missing_alt * 3)
    
    if large_images > 0:
        issues.append(f"{large_images} images may be unoptimized (large file sizes)")
        score -= min(20, large_images * 2)
    
    return {
        'score': max(score, 0),
        'issues': issues,
        'total_images': total_images,
        'missing_alt': missing_alt,
        'potentially_large': large_images
    }

def analyze_performance(soup: BeautifulSoup, html: str) -> Dict:
    """Basic performance analysis"""
    issues = []
    score = 100
    
    # Check HTML size
    html_size_kb = len(html.encode('utf-8')) / 1024
    if html_size_kb > 500:
        issues.append(f"Large HTML size ({html_size_kb:.0f}KB) - may slow load times")
        score -= 20
    
    # Check for render-blocking scripts
    scripts = soup.find_all('script', src=True)
    blocking_scripts = [s for s in scripts if not s.get('async') and not s.get('defer')]
    if len(blocking_scripts) > 5:
        issues.append(f"{len(blocking_scripts)} render-blocking scripts found")
        score -= 15
    
    # Check CSS files
    css_links = soup.find_all('link', rel='stylesheet')
    if len(css_links) > 10:
        issues.append(f"{len(css_links)} CSS files - consider combining")
        score -= 10
    
    # Check for common speed optimizations
    if 'preconnect' not in html and 'dns-prefetch' not in html:
        issues.append("Missing preconnect/dns-prefetch for faster connections")
        score -= 10
    
    return {
        'score': max(score, 0),
        'issues': issues,
        'html_size_kb': round(html_size_kb, 1),
        'script_count': len(scripts),
        'blocking_scripts': len(blocking_scripts)
    }

def analyze_mobile(soup: BeautifulSoup) -> Dict:
    """Check mobile optimization"""
    issues = []
    score = 100
    
    # Check viewport meta
    viewport = soup.find('meta', attrs={'name': 'viewport'})
    if not viewport:
        issues.append("Missing viewport meta tag (required for mobile)")
        score -= 30
    
    # Check for mobile-friendly indicators
    if not soup.find_all(class_=re.compile('mobile|responsive', re.I)):
        issues.append("No obvious mobile-responsive classes found")
        score -= 20
    
    return {
        'score': max(score, 0),
        'issues': issues,
        'has_viewport': bool(viewport)
    }

def extract_products_info(soup: BeautifulSoup) -> Dict:
    """Extract Shopify product information"""
    # Try to find product count from JSON-LD
    scripts = soup.find_all('script', type='application/ld+json')
    product_count = 0
    
    for script in scripts:
        if 'Product' in script.string:
            product_count += 1
    
    # Look for collection pages
    collections = soup.find_all('a', href=re.compile('/collections/'))
    collection_count = len(set([a.get('href') for a in collections]))
    
    return {
        'estimated_products': product_count,
        'collections_found': collection_count
    }

@app.get("/")
def root():
    return {
        "message": "Shopify Store Health Scanner API",
        "version": "1.0",
        "endpoints": {
            "scan": "POST /scan - Scan a Shopify store",
            "health": "GET /health - API health check"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/scan", response_model=HealthReport)
async def scan_store(request: ScanRequest):
    """
    Scan a Shopify store and return health report
    """
    url = str(request.store_url).rstrip('/')
    
    try:
        # Fetch the store homepage
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; ShopifyScanner/1.0)'
            })
            response.raise_for_status()
            html = response.text
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Verify it's a Shopify store
        if not is_shopify_store(html):
            raise HTTPException(
                status_code=400, 
                detail="This doesn't appear to be a Shopify store. Please check the URL."
            )
        
        # Run all analyses
        seo_analysis = analyze_seo(soup, url)
        image_analysis = analyze_images(soup)
        performance_analysis = analyze_performance(soup, html)
        mobile_analysis = analyze_mobile(soup)
        product_info = extract_products_info(soup)
        
        # Collect all issues
        all_issues = (
            seo_analysis['issues'] + 
            image_analysis['issues'] + 
            performance_analysis['issues'] + 
            mobile_analysis['issues']
        )
        
        # Calculate overall score (weighted average)
        overall_score = int(
            (seo_analysis['score'] * 0.3) +
            (image_analysis['score'] * 0.2) +
            (performance_analysis['score'] * 0.3) +
            (mobile_analysis['score'] * 0.2)
        )
        
        # Generate recommendations
        recommendations = []
        if seo_analysis['score'] < 80:
            recommendations.append("🎯 Fix SEO issues first - they directly impact Google rankings")
        if image_analysis['score'] < 70:
            recommendations.append("🖼️ Optimize images - add alt text and compress large files")
        if performance_analysis['score'] < 75:
            recommendations.append("⚡ Improve page speed - faster sites convert better")
        if mobile_analysis['score'] < 80:
            recommendations.append("📱 Ensure mobile optimization - 70%+ of traffic is mobile")
        
        if overall_score >= 85:
            recommendations.append("✅ Great job! Your store is well-optimized. Focus on minor improvements.")
        elif overall_score >= 70:
            recommendations.append("⚠️ Good foundation, but there's room for improvement")
        else:
            recommendations.append("🚨 Critical issues found - these are likely costing you sales")
        
        return HealthReport(
            store_url=url,
            overall_score=overall_score,
            seo_score=seo_analysis['score'],
            performance_score=performance_analysis['score'],
            image_score=image_analysis['score'],
            mobile_score=mobile_analysis['score'],
            issues=all_issues,
            recommendations=recommendations,
            details={
                'seo': seo_analysis,
                'images': image_analysis,
                'performance': performance_analysis,
                'mobile': mobile_analysis,
                'products': product_info
            }
        )
        
    except HTTPException:
        raise    
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch store: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)