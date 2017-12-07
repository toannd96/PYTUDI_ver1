from flask import Flask, render_template, request, url_for
import requests
import json
import re
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def form():
    return render_template('index.html')


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        word = request.form['word']
        if all(ord(char) < 128 for char in word) is True:
            if re.search(r"\s", word):

                url_glosbe = 'https://glosbe.com/gapi/tm?from=eng&dest=vi&format=json&phrase=' + \
                    word + '&page=1&pretty=true'
                r = requests.get(url_glosbe)
                data_glosbe = r.json()
                items = data_glosbe['examples']
                if len(items) > 0:
                    for item_glosbe in items:
                        item1 = item_glosbe['first']
                        item2 = item_glosbe['second']
                else:
                    return render_template('nodata.html')
                return render_template(
                    'results2.html',
                    item1=item_glosbe['first'],
                    item2=item_glosbe['second'],
                    items=items)
            else:
                url_laban = requests.get(
                    'http://dict.laban.vn/find?type=&query=' + word).text
                soup = BeautifulSoup(url_laban, "html.parser")
                word_laban = soup.find("h2", {"class": "fl"}).text
                laban = soup.find("div",
                                  {"class": "green bold margin25 m-top15"})
                if laban is not None:

                    data_laban = soup.find(
                        "div", {"class": "green bold margin25 m-top15"}).text

                    url1_laban = 'http://dict.laban.vn/ajax/getsound?accent=us&word=' + word
                    req1_laban = requests.get(url1_laban)
                    new_text1_laban = json.loads(req1_laban.text)
                    sound1 = new_text1_laban["data"]

                    url2_laban = 'http://dict.laban.vn/ajax/getsound?accent=uk&word=' + word
                    req2_laban = requests.get(url2_laban)
                    new_text2_laban = json.loads(req2_laban.text)
                    sound2 = new_text2_laban["data"]
                else:
                    return render_template('nodata.html')

                url_glosbe = 'https://glosbe.com/gapi/tm?from=eng&dest=vi&format=json&phrase=' + \
                    word + '&page=1&pretty=true'
                r = requests.get(url_glosbe)
                data_glosbe = r.json()
                items = data_glosbe['examples']
                if len(items) > 0:
                    for item_glosbe in items:
                        item1 = item_glosbe['first']
                        item2 = item_glosbe['second']
                else:

                    data_dict = requests.get(
                        "https://www.dict.com/Anh-Viet/" + str(word) + '?').text
                    soup = BeautifulSoup(data_dict, "html.parser")
                    wdict = soup.find("span", {"class": "lex_ful_entr l1"})
                    if wdict is not None:
                        word_dict = soup.find(
                            "span", {"class": "lex_ful_entr l1"}).text
                        word_dict_1 = soup.find(
                            "span", {"class": "lex_ful_pron"}).text
                        word_dict_2 = soup.find(
                            "span", {"class": "lex_ful_tran w l2"}).text
                    else:
                        return render_template('nodata.html')
                    return render_template(
                        'results4.html',
                        word_dict=word_dict,
                        word_dict_1=word_dict_1,
                        word_dict_2=word_dict_2)

                return render_template(
                    'results1.html',
                    data_laban=data_laban,
                    word_laban=word_laban,
                    sound1=sound1,
                    sound2=sound2,
                    item1=item_glosbe['first'],
                    item2=item_glosbe['second'],
                    items=items)

        else:
            url_laban = requests.get(
                'http://dict.laban.vn/find?type=&query=' + word).text
            soup = BeautifulSoup(url_laban, "html.parser")
            word_laban = soup.find("h2", {"class": "fl"}).text
            laban = soup.find("div", {"class": "green bold margin25 m-top15"})
            if laban is not None:
                data_laban = soup.find(
                    "div", {"class": "green bold margin25 m-top15"}).text
            else:
                url_glosbe = 'https://glosbe.com/gapi/tm?from=vi&dest=eng&format=json&phrase=' + \
                    word + '&page=1&pretty=true'
                r = requests.get(url_glosbe)
                data_glosbe = r.json()
                items = data_glosbe['examples']
                if len(items) > 0:
                    for item_glosbe in items:
                        item1 = item_glosbe['first']
                        item2 = item_glosbe['second']
                else:
                    return render_template('nodata.html')
                return render_template(
                    'results2.html',
                    item1=item_glosbe['first'],
                    item2=item_glosbe['second'],
                    items=items)

            url_glosbe = 'https://glosbe.com/gapi/tm?from=vi&dest=eng&format=json&phrase=' + \
                word + '&page=1&pretty=true'
            r = requests.get(url_glosbe)
            data_glosbe = r.json()
            items = data_glosbe['examples']
            if len(items) > 0:
                for item_glosbe in items:
                    item1 = item_glosbe['first']
                    item2 = item_glosbe['second']
            else:
                return render_template('nodata.html')

            return render_template(
                'results3.html',
                data_laban=data_laban,
                word_laban=word_laban,
                item1=item_glosbe['first'],
                item2=item_glosbe['second'],
                items=items)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
