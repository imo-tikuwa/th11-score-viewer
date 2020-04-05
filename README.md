# th11-score-viewer

## このプログラムについて
[th11-score-capture](https://github.com/imo-tikuwa/th11-score-capture)で東方地霊殿から取得したスコア、グレイズ、残機を含むCSVデータをチャート表示するプログラム。  
Flaskを使用しています。

## インストール、起動
初回
```
git clone https://github.com/imo-tikuwa/th11-score-viewer
cd th11-score-viewer
python -m venv venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt
python app.rb
```

---
2回目以降
```
cd th11-score-viewer
.\venv\Scripts\activate.bat
python app.rb
```

---
起動後、ブラウザでhttp://127.0.0.1:5000/ にアクセス
