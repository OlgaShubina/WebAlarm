from req import Req
import numpy as np
import matplotlib.pyplot as plt
from status_page_config import StatusConfig
import datetime
import matplotlib as mpl
from yattag import Doc
from scipy import signal
import locale

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

borderColor = [
    '#CD6600',
    '#2B2E57',
    '#000000',
    '#00BFFF',
    '#DC143C',
    '#00BFFF',
    '#DC143C',
    '#530006',
    '#808000',
    '#8B4513',
    '#5D478B']


class StatusPage(object):
    def __init__(self):
        self.config = StatusConfig('status_page_config.yaml')
        self.channel = []
        for i in self.config.graphic_list:
            self.channel += self.config.graphics[i]["name_channel"]
            self.channel += self.config.graphics[i]["add_inform"]
        self.channel += self.config.head["name_channel"]

    def select_data(self):
        req = Req("172.16.1.117", 80, "/api/v2")
        array = []
        t1 = datetime.datetime.strftime((datetime.datetime.now() - datetime.timedelta(hours=3)),
                                        '%Y-%m-%d %H:%M:%S.%f')
        t2 = datetime.datetime.strftime((datetime.datetime.now() + datetime.timedelta(hours=3)),
                                        '%Y-%m-%d %H:%M:%S.%f')
        for i in req.CursorCompress(t1, t2, self.channel, "raw"):
            try:
                array.append(i)
            except(KeyError):
                pass
        #print(len(array), array)
        for ch in self.channel:
            if ch not in array[0]:
                array[0][ch] = [{'1970-01-01 00:00:00.00000': 0.0}]
        return array

    def draw_image(self, array):
        # mpl.style.use('dark_background')
        fig, axs = plt.subplots(2, 1, figsize=(8, 5))
        plt.subplots_adjust(left=0.2, right=0.97, top=0.9, bottom=0.1)
        iter = 0
        for graph in self.config.graphic_list:
            color = []
            cell_text = []
            rows = []
            colors = []
            for k, ch in enumerate(self.config.graphics[graph]["name_channel"]):
                x = []
                y = []
                for i in array[0][ch]:
                    x.append(float(i["value"]))
                    y.append(datetime.datetime.strptime(i["time"], '%Y-%m-%d %H:%M:%S.%f'))
                label = self.config.graphics[graph]["translete_name"][k
                        ] + " " + str(x[-1]) + " " + self.config.graphics[graph]["units1"] + "\n" + \
                        self.config.graphics[graph]["translete_add_inform"] + " " + str(
                    array[0][ch][-1]["value"]) + " " + self.config.graphics[graph]["add_units"]
                axs[iter].plot(y, x, label=label, )
                axs[iter].legend(bbox_to_anchor=(-0.25, 1.), loc=2, borderaxespad=0.)
                cell_text.append([str(x[-1]) + " " + self.config.graphics[graph]["units1"]])
                rows.append(self.config.graphics[graph]["translete_name"][k])
                if (self.config.graphics[graph]["translete_add_inform"] != ''):
                    cell_text.append([str(array[0][ch][-1]["value"]) + " " + self.config.graphics[graph]["add_units"]])
                    rows.append(self.config.graphics[graph]["translete_add_inform"])

            iter += 1
        # pass
        fig = plt.gcf()
        fig.set_size_inches(19.2, 10.8)
        fig.savefig('test2png.png', dpi=100)
        plt.show()

    def draw_image2(self, array):
        num = 0
        index_color = 0
        font = {'size': 15}

        plt.rcParams['axes.facecolor'] = "#F4F4F4"
        mpl.rcParams['xtick.labelsize'] = 15
        for graph in self.config.graphic_list:
            for k, ch in enumerate(self.config.graphics[graph]["name_channel"]):
                x = []
                y = []
                try:
                    for i in array[0][ch]:
                        print(i.keys(), i.values())
                        x.append(float(list(i.values())[0]))
                        y.append(datetime.datetime.strptime(list(i.keys())[0], '%Y-%m-%d %H:%M:%S.%f'))
                except:
                    pass
                print(x, y)
                plt.plot(y, signal.medfilt(x), borderColor[index_color], linewidth=2)
                index_color += 1
            plt.ylabel(self.config.graphics[graph]["head"] + ", " + self.config.graphics[graph]["units1"],
                       fontdict=font)
            plt.grid(color="grey", linestyle='-', linewidth=0.5)
            plt.subplots_adjust(left=0.05, right=0.99, top=0.99, bottom=0.1)
            fig = plt.gcf()
            fig.set_size_inches(19.2, float(self.config.graphics[graph]["size"]))
            fig.savefig(str(graph) + '.png', dpi=100, facecolor="#F4F4F4")
            fig.clear()
            num += 1
            # plt.show()

    def generate_html(self, array):
        index_color = 0
        doc, tag, text = Doc().tagtext()
        doc.asis('<!DOCTYPE html>')
        with tag('html', lang="en"):
            with tag('head'):
                doc.asis('<meta charset="utf-8">')
                doc.asis('<meta name="viewport" content="width=device-width, initial-scale=1">')
                doc.asis('<link rel="stylesheet" type="text/css" href="styles.css">')
            with tag('body'):
                with tag('div', ('class', 'head'), id='head'):
                    doc.stag('img', src='logo2.jpg')
                    with tag("h1"):
                        text("VEPP-2000 Status")
                    with tag("div", ('class', 'datetime')):
                        with tag("h3"):
                            doc.stag('img', src='cal.png', klass="photo")
                            text(datetime.datetime.now().strftime("%d-%m-%Y"))
                        with tag("h3"):
                            doc.stag('img', src='clock.png', klass="photo")
                            text(datetime.datetime.now().strftime("%H:%M"))
                    with tag("h2"):
                        text(self.config.head["translete_name"][0] + " " +
                             str(list(array[0][self.config.head["name_channel"][0]][-1].values())[0]) + " " +
                             self.config.head["units"])

                for graph in self.config.graphic_list:
                    with tag('div', ('class', 'main')):
                        if (self.config.graphics[graph]["head"] != ""):
                            with tag('table', ('class', 'table')):
                                with tag('tr'):
                                    with tag('td'):
                                        text()
                                    with tag('td', ('class', 'head_name')):
                                        text(self.config.graphics[graph]["head"])
                                    with tag('td'):
                                        text()
                                for k, ch in enumerate(self.config.graphics[graph]["name_channel"]):
                                    with tag('tr'):
                                        with tag('td'):
                                            doc.stag("span", klass="color",
                                                     style="background-color:" + borderColor[index_color] + ";")
                                        with tag('td'):
                                            text(self.config.graphics[graph]["translete_name"][k])
                                        with tag('td', ('class', 'name')):
                                            try:
                                                text(str(round(list(array[0][ch][-1].values())[0],
                                                               self.config.graphics[graph]["round"])) + " ")
                                                if (self.config.graphics[graph]["units2"] != ""):
                                                    for ch in self.config.graphics[graph]["units2"]:
                                                        text(ch[:ch.index("^")])
                                                        with tag('sup'):
                                                            text(ch[ch.index("^") + 1:])
                                                else:
                                                    text(self.config.graphics[graph]["units1"])
                                            except:
                                                pass
                                    if (len(self.config.graphics[graph]["add_inform"]) != 0):
                                        with tag('tr'):
                                            with tag('td'):
                                                doc.stag("span")
                                            with tag('td'):
                                                text(self.config.graphics[graph]["translete_add_inform"][k])
                                            with tag('td', ('class', 'name')):
                                                text(str(
                                                    round(list(array[0][self.config.graphics[graph]["add_inform"][k]][-1].values())[0],
                                                          self.config.graphics[graph]["add_round"])) + " " +
                                                     self.config.graphics[graph]["add_units"])
                                    index_color += 1
                        doc.stag('img', src=str(graph) + '.png', klass="graph")

                        # print(doc.getvalue())
        Html_file = open("status_page.html", "w")
        Html_file.write(doc.getvalue())
        Html_file.close()


if __name__ == '__main__':
    page = StatusPage()
    arr = []
    arr = page.select_data()
    print("arr")
    page.draw_image2(arr)
    page.generate_html(arr)
