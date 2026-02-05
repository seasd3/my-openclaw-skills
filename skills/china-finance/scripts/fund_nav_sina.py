#!/usr/bin/env python3
"""基金净值查询 - 新浪财经接口（备用方案）

使用新浪财经 API，无需注册，完全免费。
接口地址: http://fundgz.1234567.com.cn/js/{code}.js
"""

import requests
import json
import argparse
import sys

def get_fund_nav_sina(fund_code):
    """获取基金净值（新浪财经）"""
    try:
        url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None
        
        # 解析返回数据 (格式: jsonpgz({...});)
        text = response.text
        if text.startswith('jsonpgz(') and text.endswith(');'):
            data = json.loads(text[8:-2])
            return {
                'code': data.get('fundcode'),
                'name': data.get('name'),
                'nav': float(data.get('gsz', 0)),
                'nav_change': float(data.get('gszzl', 0)),
                'date': data.get('gzrq'),
                'time': data.get('gxrq')
            }
        return None
        
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def get_fund_nav_eastmoney(fund_code):
    """获取基金净值（东方财富接口备用）"""
    try:
        url = f"https://fundgz.1234567.com.cn/js/{fund_code}.js"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None
        
        text = response.text
        if text.startswith('jsonpgz(') and text.endswith(');'):
            data = json.loads(text[8:-2])
            return {
                'code': data.get('fundcode'),
                'name': data.get('name'),
                'nav': float(data.get('gsz', 0)),
                'nav_change': float(data.get('gszzl', 0)),
                'date': data.get('gzrq'),
                'time': data.get('gxrq')
            }
        return None
        
    except Exception as e:
        return None

def main():
    parser = argparse.ArgumentParser(description="查询基金净值 - 新浪财经接口")
    parser.add_argument("--code", required=True, help="基金代码，如: 017193")
    parser.add_argument("--source", default="sina", choices=["sina", "eastmoney"],
                       help="数据源: sina(默认) 或 eastmoney")
    
    args = parser.parse_args()
    
    print(f"查询基金: {args.code}")
    print(f"数据源: {args.source}")
    print("-" * 50)
    
    if args.source == "sina":
        result = get_fund_nav_sina(args.code)
    else:
        result = get_fund_nav_eastmoney(args.code)
    
    if result:
        print(f"基金名称: {result['name']}")
        print(f"基金代码: {result['code']}")
        print(f"单位净值: {result['nav']:.4f}")
        print(f"日增长率: {result['nav_change']:+.2f}%")
        print(f"估算时间: {result['date']} {result['time']}")
    else:
        print("获取数据失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
