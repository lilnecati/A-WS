import sys
import random
import time
import requests  # type: ignore
from PyQt5.QtCore import QThread, pyqtSignal  # type: ignore
from PyQt5.QtWidgets import QAction, QMenuBar, QMessageBox,QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QWidget, QMessageBox, QTabWidget, QListWidget, QTableWidget, QTableWidgetItem  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import os

def get_resource_path(resource_name):
    """PyInstaller ile paketlenmişse doğru dizini döndür."""
    if getattr(sys, 'frozen', False):
        
        resource_path = os.path.join(sys._MEIPASS, resource_name)
    else:
        
        resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), resource_name)
    return resource_path


url_file = get_resource_path("urls.txt")
data_file = get_resource_path("scraped_data.txt")

print(f"urls.txt dosyasının yolu: {url_file}")
print(f"scraped_data.txt dosyasının yolu: {data_file}")

def url_dosya_ile_yükle(dosya_adı="/Users/necati/Desktop/pyqt5/urls.txt"):
    try:
        with open(dosya_adı, 'r') as file:
            urls = [line.strip() for line in file.readlines()]
        return urls
    except FileNotFoundError:
        print(f"Dosya {dosya_adı} bulunamadı!")
        return []


def url_kaydet(url, dosya_adı="/Users/necati/Desktop/pyqt5/urls.txt"):
    urls = url_dosya_ile_yükle(dosya_adı)
    if url not in urls:
        with open(dosya_adı, 'a') as file:
            file.write(url + "\n")
        return True  
    else:
        return False  

def url_dosyadan_kaldır(url, dosya_adı="/Users/necati/Desktop/pyqt5/urls.txt"):
    try:
        urls = url_dosya_ile_yükle(dosya_adı)
        if url in urls:
            with open(dosya_adı, 'w') as file:
                for line in urls:
                    if line.strip() != url:
                        file.write(line + "\n")
            return True  
        else:
            return False  
    except FileNotFoundError:
        print(f"Dosya {dosya_adı} bulunamadı!")
        return False


agentler = [
    "Chrome/68.0.3440.106", "Chrome/69.0.3497.92", "Chrome/72.0.3626.121",
    "Chrome/73.0.3683.103", "Chrome/74.0.3729.169", "Chrome/75.0.3770.142",
    "Chrome/76.0.3809.100", "Chrome/77.0.3865.120", "Chrome/78.0.3904.97",
    "Chrome/78.0.3904.108", "Chrome/79.0.3945.88", "Chrome/80.0.3987.149",
    "Chrome/83.0.4103.61", "Chrome/83.0.4103.97", "Chrome/85.0.4183.121",
    "Chrome/87.0.4280.141", "Chrome/88.0.4324.150", "Chrome/90.0.4430.212",
    "Chrome/90.0.4430.212", "Chrome/91.0.4472.124", "Chrome/92.0.4515.159",
    "Chrome/93.0.4577.82", "Chrome/94.0.4606.81", "Chrome/95.0.4638.54",
    "Chrome/96.0.4664.45", "Chrome/96.0.4664.110", "Chrome/97.0.4692.99",
    "Chrome/98.0.4758.102", "Chrome/98.0.4758.122", "Chrome/99.0.4844.84",
    "Chrome/100.0.4896.60", "Chrome/100.0.4896.127", "Chrome/101.0.4951.64",
    "Chrome/102.0.5005.63", "Chrome/103.0.5060.114", "Chrome/104.0.5112.102",
    "Chrome/105.0.5195.102", "Chrome/106.0.5249.103", "Chrome/107.0.5304.91",
    "Chrome/108.0.5359.95", "Chrome/109.0.5414.87", "Chrome/110.0.5481.77",
    "Chrome/111.0.5563.64", "Chrome/112.0.5615.49", "Chrome/113.0.5679.132",
    "Chrome/114.0.5735.90", "Chrome/115.0.5792.113", "Chrome/116.0.5845.75",
    "Chrome/117.0.5903.98", "Chrome/118.0.5954.115", "Chrome/119.0.6011.42",
    "Chrome/120.0.6055.38", "Chrome/121.0.6093.65", "Chrome/122.0.6137.50",
    "Chrome/123.0.6178.12", "Chrome/124.0.6219.17", "Chrome/125.0.6259.25",
    "Chrome/126.0.6300.30", "Chrome/127.0.6340.48", "Chrome/128.0.6389.76",
    "Chrome/129.0.6420.59", "Chrome/130.0.6469.80", "Chrome/131.0.6518.92",
    "Chrome/132.0.6567.118", "Chrome/133.0.6616.132", "Chrome/134.0.6654.145",
    "Chrome/135.0.6693.163", "Chrome/136.0.6732.171", "Chrome/137.0.6771.183",
    "Chrome/138.0.6810.195", "Chrome/139.0.6850.212", "Chrome/140.0.6889.224",
    "Chrome/141.0.6928.237", "Chrome/142.0.6967.249", "Chrome/143.0.7006.263",
    "Chrome/144.0.7045.276", "Chrome/145.0.7084.288", "Chrome/146.0.7123.300",
    "Chrome/147.0.7162.312", "Chrome/148.0.7201.324", "Chrome/149.0.7240.336",
    "Chrome/150.0.7279.348", "Chrome/151.0.7318.360", "Chrome/152.0.7357.372",
    "Chrome/153.0.7396.384", "Chrome/154.0.7435.396", "Chrome/155.0.7474.408",
    "Chrome/156.0.7513.420", "Chrome/157.0.7552.432", "Chrome/158.0.7591.444",
    "Chrome/159.0.7630.456", "Chrome/160.0.7669.468", "Chrome/161.0.7708.480",
    "Chrome/162.0.7747.492", "Chrome/163.0.7786.504", "Chrome/164.0.7825.516",
    "Chrome/165.0.7864.528", "Chrome/166.0.7903.540", "Chrome/167.0.7942.552",
    "Chrome/168.0.7981.564", "Chrome/169.0.8020.576", "Chrome/170.0.8059.588",
    "Chrome/171.0.8098.600", "Chrome/172.0.8137.612", "Chrome/173.0.8176.624",
    "Chrome/174.0.8215.636", "Chrome/175.0.8254.648", "Chrome/176.0.8293.660",
    "Chrome/177.0.8332.672", "Chrome/178.0.8371.684", "Chrome/179.0.8410.696",
    "Chrome/180.0.8449.708", "Chrome/181.0.8488.720", "Chrome/182.0.8527.732",
    "Chrome/183.0.8566.744", "Chrome/184.0.8605.756", "Chrome/185.0.8644.768",
    "Chrome/186.0.8683.780", "Chrome/187.0.8722.792", "Chrome/188.0.8761.804",
    "Chrome/189.0.8800.816", "Chrome/190.0.8839.828", "Chrome/191.0.8878.840",
    "Chrome/192.0.8917.852", "Chrome/193.0.8956.864", "Chrome/194.0.8995.876",
    "Chrome/195.0.9034.888", "Chrome/196.0.9073.900", "Chrome/197.0.9112.912",
    "Chrome/198.0.9151.924", "Chrome/199.0.9190.936", "Chrome/200.0.9229.948",
    "Chrome/201.0.9268.960", "Chrome/202.0.9307.972", "Chrome/203.0.9346.984",
    "Chrome/204.0.9385.996", "Chrome/205.0.9425.008", "Chrome/206.0.9464.020",
    "Chrome/207.0.9503.032", "Chrome/208.0.9542.044", "Chrome/209.0.9581.056",
    "Chrome/210.0.9620.068", "Chrome/211.0.9659.080", "Chrome/212.0.9698.092",
    "Chrome/213.0.9737.104", "Chrome/214.0.9776.116", "Chrome/215.0.9815.128",
    "Chrome/216.0.9854.140", "Chrome/217.0.9893.152", "Chrome/218.0.9932.164",
    "Chrome/219.0.9971.176", "Chrome/220.0.10010.188", "Chrome/221.0.10049.200",
    "Chrome/222.0.10088.212", "Chrome/223.0.10127.224", "Chrome/224.0.10166.236",
    "Chrome/225.0.10205.248", "Chrome/226.0.10244.260", "Chrome/227.0.10283.272",
    "Chrome/228.0.10322.284", "Chrome/229.0.10361.296", "Chrome/230.0.10399.308",
    "Chrome/231.0.10438.320", "Chrome/232.0.10477.332", "Chrome/233.0.10516.344",
    "Chrome/234.0.10555.356", "Chrome/235.0.10594.368", "Chrome/236.0.10633.380",
    "Chrome/237.0.10672.392", "Chrome/238.0.10711.404", "Chrome/239.0.10750.416",
    "Chrome/240.0.10789.428", "Chrome/241.0.10828.440", "Chrome/242.0.10867.452",
    "Chrome/243.0.10906.464", "Chrome/244.0.10945.476", "Chrome/245.0.10984.488",
    "Chrome/246.0.11023.500", "Chrome/247.0.11062.512", "Chrome/248.0.11101.524",
    "Chrome/249.0.11140.536", "Chrome/250.0.11179.548", "Chrome/251.0.11218.560",
    "Chrome/252.0.11257.572", "Chrome/253.0.11296.584", "Chrome/254.0.11335.596",
    "Chrome/255.0.11374.608", "Chrome/256.0.11413.620", "Chrome/257.0.11452.632",
    "Chrome/258.0.11491.644", "Chrome/259.0.11530.656", "Chrome/260.0.11569.668",
    "Chrome/261.0.11608.680", "Chrome/262.0.11647.692", "Chrome/263.0.11686.704",
    "Chrome/264.0.11725.716", "Chrome/265.0.11764.728", "Chrome/266.0.11803.740",
    "Chrome/267.0.11842.752", "Chrome/268.0.11881.764", "Chrome/269.0.11920.776",
    "Chrome/270.0.11959.788", "Chrome/271.0.11998.800", "Chrome/272.0.12037.812",
    "Chrome/273.0.12076.824", "Chrome/274.0.12115.836", "Chrome/275.0.12154.848",
    "Chrome/276.0.12193.860", "Chrome/277.0.12232.872", "Chrome/278.0.12271.884",
    "Chrome/279.0.12310.896", "Chrome/280.0.12349.908", "Chrome/281.0.12388.920",
    "Chrome/282.0.12427.932", "Chrome/283.0.12466.944", "Chrome/284.0.12505.956",
    "Chrome/285.0.12544.968", "Chrome/286.0.12583.980", "Chrome/287.0.12622.992",
    "Chrome/288.0.12662.004", "Chrome/289.0.12701.016", "Chrome/290.0.12740.028",
    "Chrome/291.0.12779.040", "Chrome/292.0.12818.052", "Chrome/293.0.12857.064",
    "Chrome/294.0.12896.076", "Chrome/295.0.12935.088", "Chrome/296.0.12974.100",
    "Chrome/297.0.13013.112", "Chrome/298.0.13052.124", "Chrome/299.0.13091.136",
    "Chrome/300.0.13130.148", "Chrome/301.0.13169.160", "Chrome/302.0.13208.172",
    "Chrome/303.0.13247.184", "Chrome/304.0.13286.196", "Chrome/305.0.13325.208",
    "Chrome/306.0.13364.220", "Chrome/307.0.13403.232", "Chrome/308.0.13442.244",
    "Chrome/309.0.13481.256", "Chrome/310.0.13520.268", "Chrome/311.0.13559.280",
    "Chrome/312.0.13598.292", "Chrome/313.0.13637.304", "Chrome/314.0.13676.316",
    "Chrome/315.0.13715.328", "Chrome/316.0.13754.340", "Chrome/317.0.13793.352",
    "Chrome/318.0.13832.364", "Chrome/319.0.13871.376", "Chrome/320.0.13910.388",
    "Chrome/321.0.13949.400", "Chrome/322.0.13988.412", "Chrome/323.0.14027.424",
    "Chrome/324.0.14066.436", "Chrome/325.0.14105.448", "Chrome/326.0.14144.460",
    "Chrome/327.0.14183.472", "Chrome/328.0.14222.484", "Chrome/329.0.14261.496",
    "Chrome/330.0.14300.508", "Chrome/331.0.14339.520", "Chrome/332.0.14378.532",
    "Chrome/333.0.14417.544", "Chrome/334.0.14456.556", "Chrome/335.0.14495.568",
    "Chrome/336.0.14534.580", "Chrome/337.0.14573.592", "Chrome/338.0.14612.604",
    "Chrome/339.0.14651.616", "Chrome/340.0.14690.628", "Chrome/341.0.14729.640",
    "Chrome/342.0.14768.652", "Chrome/343.0.14807.664", "Chrome/344.0.14846.676",
    "Chrome/345.0.14885.688", "Chrome/346.0.14924.700", "Chrome/347.0.14963.712",
    "Chrome/348.0.15002.724", "Chrome/349.0.15041.736", "Chrome/350.0.15080.748",
    "Chrome/351.0.15119.760", "Chrome/352.0.15158.772", "Chrome/353.0.15197.784",
    "Chrome/354.0.15236.796", "Chrome/355.0.15275.808", "Chrome/356.0.15314.820",
    "Chrome/357.0.15353.832", "Chrome/358.0.15392.844", "Chrome/359.0.15431.856",
    "Chrome/360.0.15470.868", "Chrome/361.0.15509.880", "Chrome/362.0.15548.892",
    "Chrome/363.0.15587.904", "Chrome/364.0.15626.916", "Chrome/365.0.15665.928",
    "Chrome/366.0.15704.940", "Chrome/367.0.15743.952", "Chrome/368.0.15782.964",
    "Chrome/369.0.15821.976", "Chrome/370.0.15860.988", "Chrome/371.0.15899.1000",
    "Chrome/372.0.15938.1012", "Chrome/373.0.15977.1024", "Chrome/374.0.16016.1036",
    "Chrome/375.0.16055.1048", "Chrome/376.0.16094.1060", "Chrome/377.0.16133.1072",
    "Chrome/378.0.16172.1084", "Chrome/379.0.16211.1096", "Chrome/380.0.16250.1108",
    "Chrome/381.0.16289.1120", "Chrome/382.0.16328.1132", "Chrome/383.0.16367.1144",
    "Chrome/384.0.16406.1156", "Chrome/385.0.16445.1168", "Chrome/386.0.16484.1180",
    "Chrome/387.0.16523.1192", "Chrome/388.0.16562.1204", "Chrome/389.0.16601.1216",
    "Chrome/390.0.16640.1228", "Chrome/391.0.16679.1240", "Chrome/392.0.16718.1252",
    "Chrome/393.0.16757.1264", "Chrome/394.0.16796.1276", "Chrome/395.0.16835.1288",
    "Chrome/396.0.16874.1300", "Chrome/397.0.16913.1312", "Chrome/398.0.16952.1324",
    "Chrome/399.0.16991.1336", "Chrome/400.0.17030.1348", "Chrome/401.0.17069.1360",
    "Chrome/402.0.17108.1372", "Chrome/403.0.17147.1384", "Chrome/404.0.17186.1396",
    "Chrome/405.0.17225.1408", "Chrome/406.0.17264.1420", "Chrome/407.0.17303.1432",
    "Chrome/408.0.17342.1444", "Chrome/409.0.17381.1456", "Chrome/410.0.17420.1468",
    "Chrome/411.0.17459.1480", "Chrome/412.0.17498.1492", "Chrome/413.0.17537.1504",
    "Chrome/414.0.17576.1516", "Chrome/415.0.17615.1528", "Chrome/416.0.17654.1540",
    "Chrome/417.0.17693.1552", "Chrome/418.0.17732.1564", "Chrome/419.0.17771.1576",
    "Chrome/420.0.17810.1588", "Chrome/421.0.17849.1600", "Chrome/422.0.17888.1612",
    "Chrome/423.0.17927.1624", "Chrome/424.0.17966.1636", "Chrome/425.0.18005.1648",
    "Chrome/426.0.18044.1660", "Chrome/427.0.18083.1672", "Chrome/428.0.18122.1684",
    "Chrome/429.0.18161.1696", "Chrome/430.0.18200.1708", "Chrome/431.0.18239.1720",
    "Chrome/432.0.18278.1732", "Chrome/433.0.18317.1744", "Chrome/434.0.18356.1756",
    "Chrome/435.0.18395.1768", "Chrome/436.0.18434.1780", "Chrome/437.0.18473.1792",
    "Chrome/438.0.18512.1804", "Chrome/439.0.18551.1816", "Chrome/440.0.18590.1828",
    "Chrome/441.0.18629.1840", "Chrome/442.0.18668.1852", "Chrome/443.0.18707.1864",
    "Chrome/444.0.18746.1876", "Chrome/445.0.18785.1888", "Chrome/446.0.18824.1900",
    "Chrome/447.0.18863.1912", "Chrome/448.0.18902.1924", "Chrome/449.0.18941.1936",
    "Chrome/450.0.18980.1948", "Chrome/451.0.19019.1960", "Chrome/452.0.19058.1972",
    "Chrome/453.0.19097.1984", "Chrome/454.0.19136.1996", "Chrome/455.0.19175.2008",
    "Chrome/456.0.19214.2020", "Chrome/457.0.19253.2032", "Chrome/458.0.19292.2044",
    "Chrome/459.0.19331.2056", "Chrome/460.0.19370.2068", "Chrome/461.0.19409.2080",
    "Chrome/462.0.19448.2092", "Chrome/463.0.19487.2104", "Chrome/464.0.19526.2116",
    "Chrome/465.0.19565.2128", "Chrome/466.0.19604.2140", "Chrome/467.0.19643.2152",
    "Chrome/468.0.19682.2164", "Chrome/469.0.19721.2176", "Chrome/470.0.19760.2188",
    "Chrome/471.0.19799.2200", "Chrome/472.0.19838.2212", "Chrome/473.0.19877.2224",
    "Chrome/474.0.19916.2236", "Chrome/475.0.19955.2248", "Chrome/476.0.19994.2260",

]


basliklar = {
    "User-Agent": random.choice(agentler),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.amazon.com/",
    "Cache-Control": "max-age=0",
    "TE": "Trailers",
    "DNT": "1",
}


def verileri_dosyaya_kaydet(data):
    with open('/Users/necati/Desktop/pyqt5/scraped_data.txt', 'a') as file:
        for item in data:
            file.write(f"Başlık: {item['title']}\n")
            file.write(f"Fiyat: {item['price']}\n")
            file.write(f"Stok: {item['stock']}\n")
            file.write(f"Çeşitler: {', '.join(item['variations'])}\n")
            file.write("-" * 40 + "\n")

class ScraperThread(QThread):
    update_signal = pyqtSignal(str)
    finish_signal = pyqtSignal()

    def __init__(self, urls, headers):
        super().__init__()
        self.urls = urls
        self.headers = headers

    def run(self):
        index = 0
        while index < len(self.urls):
            url = self.urls[index]
            random_user_agent = random.choice(agentler)
            headers = self.headers.copy()
            print(f"{index+1}. Ürünün user-agenti: {random_user_agent}")
            headers["User-Agent"] = random_user_agent

            ürün_bilgilerini_dosyaya_kaydet = []

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                if "amazon" in url:
                
                    fiyat_tam = soup.find('span', class_='a-price-whole') or soup.find('table', class_='a-lineitem a-align-top')
                    fiyat_yarim = soup.find('span', class_='a-price-fraction') or soup.find('span', {'class': 'aria-hidden="true"'})
                    fiyat_etiketi = soup.find('span', class_='a-price-symbol')

                    if fiyat_tam and fiyat_yarim and fiyat_etiketi:
                        fiyat = f"{fiyat_etiketi.text.strip()}{fiyat_tam.text.strip()}{fiyat_yarim.text.strip()}"
                    else:
                        fiyat = "Fiyat bulunamadı"

                    baslik_tag = soup.find('span', {'id': 'productTitle'})
                    urun_basligi = baslik_tag.get_text(strip=True) if baslik_tag else 'Başlık bulunamadı'
           
                    stok_tag = soup.find('span', {'class': 'a-size-base a-color-price a-text-bold'}) or soup.find('div', {'id': 'availability'})or soup.find('span', {'class': 'a-size-medium a-color-success'})
                    if stok_tag:
                        stok_text = stok_tag.get_text(strip=True)
                        if "out of stock" in stok_text.lower():
                            urun_stok = "Stokta Yok"
                        else:
                            urun_stok = stok_tag.get_text(strip=True)
                    else:
                        urun_stok = "Stok Durumu Bilinmiyor"

                    
                    self.update_signal.emit(f"{index + 1}. Ürün başlığı: {urun_basligi}\n")
                    self.update_signal.emit(f"Fiyat: {fiyat}\n")
                    self.update_signal.emit(f"Stok Durumu: {urun_stok}\n")
                    
                    çeşitler = []
                    variation_section = soup.find_all('button', {'class': 'a-button-text'}) or soup.find('span', class_='a-button-inner')
                    for var in variation_section:
                        çeşitler_text = var.get_text(strip=True)
                        if çeşitler_text and any(char.isdigit() for char in çeşitler_text):  # Varyasyon metninde rakam olmalı
                            çeşitler.append(çeşitler_text)

                    if çeşitler:
                        self.update_signal.emit(f"Çeşitler:\n")
                        for varyasyon in çeşitler:
                            self.update_signal.emit(f"- {varyasyon}\n")
                    else:
                        self.update_signal.emit("Çeşitler bulunamadı\n")

                    
                    ürün_bilgilerini_dosyaya_kaydet.append({
                        'title': urun_basligi,
                        'price': fiyat,
                        'stock': urun_stok,
                        'variations': çeşitler
                    })

                    
                    verileri_dosyaya_kaydet(ürün_bilgilerini_dosyaya_kaydet)

                    self.update_signal.emit("-" * 100 + "\n")

                
                time.sleep(6)

            except requests.exceptions.RequestException as e:
                self.update_signal.emit(f"Hata oluştu: {e}\n")

            index += 1

        self.finish_signal.emit()

class ScraperApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Necati Yıldırım")
        self.setGeometry(300, 100, 1000, 600)

        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        
def show_about(self):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Bu uygulama PyQt5 ile yapılmıştır.")
    msg.setWindowTitle("Hakkında")
    msg.exec_()

    self.create_tabs()

    def create_tabs(self):

        self.web_scraping_tab = QWidget()
        self.web_scraping_layout = QVBoxLayout()

        self.result_text = QTextEdit(self.web_scraping_tab)
        self.result_text.setReadOnly(True)
        self.result_text.setVerticalScrollBarPolicy(1)  
        self.web_scraping_layout.addWidget(self.result_text)

        self.scrape_button = QPushButton("Veri Çek", self.web_scraping_tab)
        self.scrape_button.setStyleSheet("background-color: #007bff; color: white;")
        self.scrape_button.clicked.connect(self.start_scraping)
        self.web_scraping_layout.addWidget(self.scrape_button)

        self.web_scraping_tab.setLayout(self.web_scraping_layout)

        self.url_manage_tab = QWidget()
        self.url_yönetim_düzenleme = QVBoxLayout()

        self.url_list_widget = QListWidget(self.url_manage_tab)
        self.url_yönetim_düzenleme.addWidget(self.url_list_widget)

        self.url_gir = QLineEdit(self.url_manage_tab)
        self.url_gir.setPlaceholderText("Yeni URL ekleyin...")
        self.url_yönetim_düzenleme.addWidget(self.url_gir)

        self.url_ekle_butonu = QPushButton("URL Ekle", self.url_manage_tab)
        self.url_ekle_butonu.setStyleSheet("""
        background-color: green;
        color: white;
        border: 2px solid darkgreen;
        adding: 10px;
        font-size: 14px;
        """)
        self.url_ekle_butonu.clicked.connect(self.add_url)
        self.url_yönetim_düzenleme.addWidget(self.url_ekle_butonu)


        self.url_kaldır_butonu = QPushButton("URL Kaldır", self.url_manage_tab)
        self.url_kaldır_butonu.setStyleSheet("""
        background-color: red;
        color: white;
        border: 2px solid darkred;
        padding: 10px;
        font-size: 14px;
        """)
        self.url_kaldır_butonu.clicked.connect(self.remove_url)
        self.url_yönetim_düzenleme.addWidget(self.url_kaldır_butonu)

        self.update_url_list()

        self.url_manage_tab.setLayout(self.url_yönetim_düzenleme)

        self.tabs.addTab(self.web_scraping_tab, "Web Scraping")
        self.tabs.addTab(self.url_manage_tab, "URL Yönetimi")

    def update_url_list(self):
        """URL listesine numara eklemeden güncelle."""
        self.url_list_widget.clear()
        for url in url_dosya_ile_yükle():
            self.url_list_widget.addItem(url)

    def start_scraping(self):
        """Veri çekme işlemini başlat."""
        self.result_text.clear()  
        self.scraper_thread = ScraperThread(url_dosya_ile_yükle(), basliklar)
        self.scraper_thread.update_signal.connect(self.update_results)
        self.scraper_thread.finish_signal.connect(self.finish_scraping)
        self.scraper_thread.start()

    def update_results(self, result):
        """Sonuçları GUI'ye ekle."""
        self.result_text.insertPlainText(result) 

    def finish_scraping(self):
        """Scraping işlemi tamamlandığında."""
        self.result_text.append("Veri çekme işlemi tamamlandı.")

    def add_url(self):
        """Yeni URL ekle."""
        url = self.url_gir.text()
        if url:
            if url_kaydet(url):
                self.update_url_list()  
                self.url_gir.clear()  
                self.result_text.clear() 
                QMessageBox.information(self, "Başarı", "URL başarıyla eklendi.")
            else:
                QMessageBox.warning(self, "Hata", "URL zaten mevcut.")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir URL girin.")

    def remove_url(self):
        """Seçilen URL'yi kaldır."""
        url_seç = self.url_list_widget.currentItem()
        if url_seç:
            url = url_seç.text()  
            if url_dosyadan_kaldır(url):
                self.update_url_list()  
                self.url_gir.clear()  
                self.result_text.clear() 
                QMessageBox.information(self, "Başarı", "URL başarıyla kaldırıldı.")
            else:
                QMessageBox.warning(self, "Hata", "URL kaldırılmadı.")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir URL seçin.")
     
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScraperApp()
    window.show()
    sys.exit(app.exec_())








