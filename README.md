# E-Commerce Analysis Dashboard ✨
Proyek E-commerce Analysis Dashboard bertujuan untuk memberikan insight mendalam tentang data e-commerce dengan menyajikan visualisasi interaktif melalui dashboard berbasis Streamlit. Analisis di notebook dan dashboard dirancang untuk menjawab pertanyaan bisnis spesifik, seperti pola durasi pengiriman, distribusi lokasi pelanggan dan penjual, serta performa produk. Meskipun analisis di notebook lebih rinci, dashboard memfasilitasi pengguna dalam mengeksplorasi hasil dengan cara yang sederhana dan intuitif.

## Setup Environment - Anaconda
```
conda create --name ecommerce-ds python=3.10
conda activate ecommerce-ds
pip install -r requirements.txt
```

## Setup Environtment - Shell/Terminal
```
mkdir ecommerce-analysis
cd ecommerce-analysis
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Jalankan Streamlit App
Setelah environtment berhasil diatur, jalankan aplikasi Streamlit dengan perintah berikut:
```
streamlit run dashboard/dashboard.py

note: Untuk menjalankan dashboard saat terminal berada di direktori "submission" bukan di direktori "dashboard".
```

## Struktur Proyek
Berikut struktur direktori project ini:
```
ecommerce-analysis/
├── dashboard/
│   ├── all_data.csv 
│   ├── dashboard.py
|
├── data/
│   ├── olist_customer_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_order_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_sellers_dataset.csv
|   ├── product_category_name_translation.csv
│       
├── .gitattributes
├── Analisis_Data_E_Commerce.ipynb
├── README.md
├── requirements.txt                     
├── url.txt              
```