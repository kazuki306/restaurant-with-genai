import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests
# import bs4tabelog
from bs4 import BeautifulSoup
import pandas as pd
import time
import math
import base64

def get_rate(review):
    rate_element = review.find('b', class_='c-rating-v3__val c-rating-v3__val--strong')
    rate = rate_element.text.strip() if rate_element else "N/A"
    return rate

def get_date(review):
    date_element = review.find('div', class_='rvw-item__date')
    if date_element:
        date_span = date_element.find('span')
        if date_span:
            date = date_span.text.strip()
            date = date.replace('訪問', '')  # "訪問"を削除
        else:
            date = "N/A"
    else:
        date = "N/A"
    return date

def get_title(review):
    title_element = review.find('a', class_='rvw-item__title-target')
    title = title_element.text.strip() if title_element else "N/A"
    return title

def get_content(review, customer_list, base_url="https://tabelog.com/"):
    detail_link = review.find('a', class_='c-link-circle js-link-bookmark-detail')
    if detail_link and detail_link.get('data-detail-url'):
        detail_link_url = detail_link.get('data-detail-url')
        if detail_link_url not in customer_list:
            customer_list.append(detail_link_url)
            detail_url = base_url + detail_link_url
            detail_response = requests.get(detail_url)
            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
            # 詳細コンテンツを抽出
            content_element = detail_soup.find('div', class_='rvw-item__rvw-comment rvw-item__rvw-comment--custom')
            content = content_element.text.strip() if content_element else "N/A"
        else:
            return None, customer_list
    else:
        content = "N/A"
    return content, customer_list

def scraping_tabelog(url, customer_list, num_reviews=20):
    # ユーザーエージェントの設定
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    counter = 0
    # データを格納するリスト
    results = []
    # 同じ人が口コミを書いているか判定
    # customer_list = []
    # ページ数を指定（例：最初の5ページ）
    max_pages = math.ceil(num_reviews/20)

    for page in range(1, max_pages + 3):
        if counter >= num_reviews:
            break
        # ページURLの生成
        page_url = f"{url}{page}"

        # ページの取得
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # 口コミ要素の取得
        reviews = soup.find_all('div', class_='rvw-item js-rvw-item-clickable-area')
        if reviews:
            for review in reviews:
                if counter >= num_reviews:
                    break
                content, customer_list = get_content(review, customer_list)
                if content is not None:
                    rate = get_rate(review)
                    date = get_date(review)
                    title = get_title(review)
                    # content, customer_list = get_content(review)
                    
                    results.append({
                        'rate': rate,
                        'date': date,
                        'title': title,
                        'content': content
                    })
                    
                    counter += 1
        else:
            break
            
    # DataFrameを作成
    df = pd.DataFrame(results)
    return df

def generate_tabelog_url(store_url):
    # base_url = "https://tabelog.com/"
    review_url = "dtlrvwlst/COND-0/smp1/?smp=1&lc=0&rvw_part=all&PG="
    return store_url + review_url

st.title("口コミゲットさん")

store_url = st.text_input("口コミを取得したい食べログの店舗URLを入力してください")
num_reviews = st.selectbox("スクレイピングする口コミの数", [20, 40, 60])

if st.button("実行"):
    url = generate_tabelog_url(store_url)
    # df = scrape_tabelog(restaurant_name, num_reviews)
    customer_list = []
    with st.spinner("口コミ取得中..."):
        df = scraping_tabelog(url, customer_list, num_reviews)
    st.dataframe(df,use_container_width=True)
    
    csv = df.to_csv(index=False)

    # utf-8(BOM)
    b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="result_utf-8-sig.csv">Download Link</a>'
    st.markdown(f"CSVファイルのダウンロード(utf-8 BOM):  {href}", unsafe_allow_html=True)

    # utf-8
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="result_utf-8.csv">Download Link</a>'
    st.markdown(f"CSVファイルのダウンロード(utf-8):  {href}", unsafe_allow_html=True)
