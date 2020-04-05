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
CSV_INDEX_CURRENT = 7


# ログ出力設定 (application.logを出力、標準出力は行わない)
logzero.logfile('log/application.log', disableStderrLogger = True)

app = Flask(__name__, static_folder = 'assets')
# 10MBまでアップロード可
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'assets'), 'favicon.ico')


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

    # CSVファイル2を取得
    csv_file2 = None
    logger.debug(request.files)
    if 'csv_file2' in request.files and request.files['csv_file2'].filename != '':
        csv_file2 = request.files.get('csv_file2')
        if csv_file2.mimetype not in ['text/csv', 'application/vnd.ms-excel']:
            return render_template("index.html", error = 'CSVファイル2の形式が正しくありません。')

    # 文字エンコーディングがsjisのストリームを取得（ここでutf8にする方法が不明）
    csv_stream1 = io.TextIOWrapper(csv_file1, encoding = 'sjis')
    csv_data1 = StringIO(csv_stream1.read())

    score_data = []
    graze_data = []
    remain_data = []
    csv1_index_and_current_map = {}
    data_count = 1
    append_index = 0
    for index, row in enumerate(csv.reader(csv_data1)):

        # csvの1行をsjis → utf-8変換？ググってもよくわからず
        row = [x.encode('utf8').decode('utf8') for x in row]

        if index == 0:
            if row != ['難易度', 'スコア', '残機', 'グレイズ', 'ボス', 'ボス残機', 'スペル', '現在地']:
                # ヘッダ行チェック
                return render_template("index.html", error = 'CSVファイル1のヘッダ行が正しくありません。')
        else:
            # データ行を辞書に追加(Python3.7からは辞書に入れた順番が保持される模様)
            current = row[CSV_INDEX_CURRENT]
            if current == '':
                current = str(append_index)
            score_data.append({"current": current, "value0": row[CSV_INDEX_SCORE]})
            graze_data.append({"current": current, "value0": row[CSV_INDEX_GRAZE]})
            remain_data.append({"current": current, "value0": row[CSV_INDEX_REMAIN]})
            csv1_index_and_current_map[current] = append_index
            append_index += 1


    # CSVファイル2が存在するとき1と2が同じ難易度か判定する。違ったら比較は不可とする
    if csv_file2 is not None:
        data_count = 2
        csv_stream2 = io.TextIOWrapper(csv_file2, encoding = 'sjis')
        csv_data2 = StringIO(csv_stream2.read())

        for index, row in enumerate(csv.reader(csv_data2)):
            row = [x.encode('utf8').decode('utf8') for x in row]
            if index == 0:
                if row != ['難易度', 'スコア', '残機', 'グレイズ', 'ボス', 'ボス残機', 'スペル', '現在地']:
                    return render_template("index.html", error = 'CSVファイル2のヘッダ行が正しくありません。')
            else:
                # 比較対象データ(CSVファイル2)の現在地を元にCSVファイル1の現在地のインデックスを取得、空でないときだけセット
                try:
                    map_index = csv1_index_and_current_map[row[CSV_INDEX_CURRENT]]
                    score_data[map_index]["value1"] = row[CSV_INDEX_SCORE]
                    graze_data[map_index]["value1"] = row[CSV_INDEX_GRAZE]
                    remain_data[map_index]["value1"] = row[CSV_INDEX_REMAIN]
                except KeyError:
                    logger.debug("次の現在地はCSVファイル1側に存在しないためスキップ：" + row[CSV_INDEX_CURRENT])


    logger.debug(score_data)
#     logger.debug(graze_data)
#     logger.debug(remain_data)
    logger.debug(json.dumps(score_data, ensure_ascii=False))
#     logger.debug(json.dumps(graze_data, ensure_ascii=False))
#     logger.debug(json.dumps(remain_data, ensure_ascii=False))

    return render_template("charts.html",
                           score = json.dumps(score_data, ensure_ascii=False),
                           graze = json.dumps(graze_data, ensure_ascii=False),
                           remain = json.dumps(remain_data, ensure_ascii=False),
                           data_count = data_count
                           )


if __name__ == "__main__":
    app.run(debug=True)
#     app.run()