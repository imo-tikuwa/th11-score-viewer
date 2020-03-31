from flask import Flask, render_template, request, send_from_directory
import logzero
from logzero import logger
import io
from io import StringIO
import csv
import sys
import json
import os

CSV_INDEX_DIFFICULTY = 0
CSV_INDEX_SCORE = 1
CSV_INDEX_REMAIN = 2
CSV_INDEX_GRAZE = 3
CSV_INDEX_CURRET = 7


# ログ出力設定 (application.logを出力、標準出力は行わない)
logzero.logfile('log/application.log', disableStderrLogger = True)

app = Flask(__name__, static_folder = 'assets')
# 10MBまでアップロード可
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'assets'), 'favicon.ico', )


@app.route("/", methods=['GET'])
def index():
    # トップ画面表示
    return render_template("index.html")


@app.route("/", methods=['POST'])
def disp_chart():
    # グラフ表示

    # CSVファイル1は必須
    if 'csv_file1' not in request.files:
        return render_template("index.html", error = 'CSVファイル1は必須です。')

    csv_file1 = request.files.get('csv_file1')
    if csv_file1.mimetype not in ['text/csv', 'application/vnd.ms-excel']:
        return render_template("index.html", error = 'CSVファイル1の形式が正しくありません。')

    # 文字エンコーディングがsjisのストリームを取得（ここでutf8にする方法が不明）
    text_stream = io.TextIOWrapper(csv_file1, encoding = 'sjis')
    text_data = StringIO(text_stream.read())

    index = 0
    score_data = {}
    graze_data = {}
    remain_data = {}
    for row in csv.reader(text_data):

        # csvの1行をsjis → utf-8変換？ググってもよくわからず
        row = [x.encode('utf8').decode('utf8') for x in row]

        if index == 0:
            if row != ['難易度', 'スコア', '残機', 'グレイズ', 'ボス', 'ボス残機', 'スペル', '現在地']:
                # ヘッダ行チェック
                return render_template("index.html", error = 'CSVファイル1のヘッダ行が正しくありません。')
        else:
            # データ行を辞書に追加(Python3.7からは辞書に入れた順番が保持される模様)
            current = row[CSV_INDEX_CURRET]
            if current == '':
                current = str(index)
            score_data[current] = row[CSV_INDEX_SCORE]
            graze_data[current] = row[CSV_INDEX_GRAZE]
            remain_data[current] = row[CSV_INDEX_REMAIN]
        index += 1

    logger.debug(score_data)
#     logger.debug(graze_data)
#     logger.debug(remain_data)
    logger.debug(json.dumps(score_data, ensure_ascii=False))
#     logger.debug(json.dumps(graze_data))
#     logger.debug(json.dumps(remain_data))

    return render_template("charts.html",
                           score = json.dumps(score_data, ensure_ascii=False),
                           graze = json.dumps(graze_data, ensure_ascii=False),
                           remain = json.dumps(remain_data, ensure_ascii=False)
                           )


if __name__ == "__main__":
    app.run(debug=True)
#     app.run()