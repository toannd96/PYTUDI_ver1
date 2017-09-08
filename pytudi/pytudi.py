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

                url_tracau = 'http://api.tracau.vn/WBBcwnwQpV89/s/' + word + '/en'
                r = requests.get(url_tracau)
                data_tracau = r.json()
                items = data_tracau['sentences']
                if len(items) > 0:
                    for item_tracau in items:
                        vi = (
                            (item_tracau['fields']['vi']).replace(
                                '<em>', '')).replace(
                            '</em>', '')
                        en = (
                            (item_tracau['fields']['en']).replace(
                                '<em>', '')).replace(
                            '</em>', '')

                url_glosbe = 'https://glosbe.com/gapi/tm?from=eng&dest=vi&format=json&phrase=' + \
                    word + '&page=1&pretty=true'
                r1 = requests.get(url_glosbe)
                data_glosbe = r1.json()
                value_glosbe = data_glosbe['examples']
                if len(value_glosbe) > 0:
                    for item1 in value_glosbe:
                        if((item1['author'] == 89985) or (item1['author'] == 94259)):
                            eng = item1['first']
                            vie = item1['second']
                else:
                    return render_template('nodata.html')
                return render_template(
                    'results2.html',
                    vi=((item_tracau['fields']['vi']).replace('<em>', '')).replace('</em>', ''),
                    en=((item_tracau['fields']['en']).replace('<em>', '')).replace('</em>', ''),
                    items=items, value_glosbe=value_glosbe,
                    eng=item1['first'], vie=item1['second'], word=request.form['word'])
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

                else:
                    return render_template('nodata.html')

                url_tracau = 'http://api.tracau.vn/WBBcwnwQpV89/s/' + word + '/en'
                r = requests.get(url_tracau)
                data_tracau = r.json()
                items = data_tracau['sentences']
                if len(items) > 0:
                    for item_tracau in items:
                        vi = (
                            (item_tracau['fields']['vi']).replace(
                                '<em>', '')).replace(
                            '</em>', '')
                        en = (
                            (item_tracau['fields']['en']).replace(
                                '<em>', '')).replace(
                            '</em>', '')

                url_glosbe = 'https://glosbe.com/gapi/tm?from=eng&dest=vi&format=json&phrase=' + \
                    word + '&page=1&pretty=true'
                r1 = requests.get(url_glosbe)
                data_glosbe = r1.json()
                value_glosbe = data_glosbe['examples']
                if len(value_glosbe) > 0:
                    for item1 in value_glosbe:
                        if((item1['author'] == 89985) or (item1['author'] == 94259)):
                            eng = item1['first']
                            vie = item1['second']

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
                        word_dict_2=word_dict_2,
                        word=request.form['word'])

                return render_template(
                    'results1.html',
                    data_laban=data_laban,
                    word_laban=word_laban,
                    vi=((item_tracau['fields']['vi']).replace('<em>', '')).replace('</em>', ''),
                    en=((item_tracau['fields']['en']).replace('<em>', '')).replace('</em>', ''),
                    items=items, value_glosbe=value_glosbe,
                    eng=item1['first'], vie=item1['second'], word=request.form['word'])

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
                url_tracau = 'http://api.tracau.vn/WBBcwnwQpV89/s/' + word + '/vi'
                r = requests.get(url_tracau)
                data_tracau = r.json()
                items = data_tracau['sentences']
                if len(items) > 0:
                    for item_tracau in items:
                        vi = (
                            (item_tracau['fields']['vi']).replace(
                                '<em>', '')).replace(
                            '</em>', '')
                        en = (
                            (item_tracau['fields']['en']).replace(
                                '<em>', '')).replace(
                            '</em>', '')

                url_glosbe = 'https://glosbe.com/gapi/tm?from=vi&dest=eng&format=json&phrase=' + \
                    word + '&page=1&pretty=true'
                r1 = requests.get(url_glosbe)
                data_glosbe = r1.json()
                value_glosbe = data_glosbe['examples']
                if len(value_glosbe) > 0:
                    for item1 in value_glosbe:
                        if((item1['author'] == 89985) or (item1['author'] == 94259)):
                            eng = item1['first']
                            vie = item1['second']

                else:
                    return render_template('nodata.html')
                return render_template(
                    'results5.html',
                    vi=((item_tracau['fields']['vi']).replace('<em>', '')).replace('</em>', ''),
                    en=((item_tracau['fields']['en']).replace('<em>', '')).replace('</em>', ''),
                    items=items, value_glosbe=value_glosbe,
                    eng=item1['first'], vie=item1['second'])

            url_tracau = 'http://api.tracau.vn/WBBcwnwQpV89/s/' + word + '/vi'
            r = requests.get(url_tracau)
            data_tracau = r.json()
            items = data_tracau['sentences']
            if len(items) > 0:
                for item_tracau in items:
                    vi = (
                        (item_tracau['fields']['vi']).replace(
                            '<em>', '')).replace(
                        '</em>', '')
                    en = (
                        (item_tracau['fields']['en']).replace(
                            '<em>', '')).replace(
                        '</em>', '')

            url_glosbe = 'https://glosbe.com/gapi/tm?from=vi&dest=eng&format=json&phrase=' + \
                word + '&page=1&pretty=true'
            r1 = requests.get(url_glosbe)
            data_glosbe = r1.json()
            value_glosbe = data_glosbe['examples']
            if len(value_glosbe) > 0:
                for item1 in value_glosbe:
                    if((item1['author'] == 89985) or (item1['author'] == 94259)):
                        eng = item1['first']
                        vie = item1['second']

            else:
                return render_template('nodata.html')

            return render_template(
                'results3.html',
                data_laban=data_laban,
                word_laban=word_laban,
                vi=((item_tracau['fields']['vi']).replace('<em>', '')).replace('</em>', ''),
                en=((item_tracau['fields']['en']).replace('<em>', '')).replace('</em>', ''),
                items=items, value_glosbe=value_glosbe,
                eng=item1['first'], vie=item1['second'])


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
