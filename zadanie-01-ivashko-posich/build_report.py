"""Збирає PDF-доповідь за переглядом фільму «Посіч: депортована, але не знищена»."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

HERE = Path(__file__).parent
FONTS = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("DV", FONTS + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("DVB", FONTS + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", FONTS + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVB")

ACCENT = colors.HexColor("#1f3a5f")
MUTED = colors.HexColor("#555555")

body = ParagraphStyle("body", fontName="DV", fontSize=9.5, leading=13.5, spaceAfter=4)
small = ParagraphStyle("small", parent=body, fontSize=8.5, leading=11.5)
cap = ParagraphStyle("cap", parent=small, fontName="DVI", textColor=MUTED, alignment=TA_CENTER)
fname = ParagraphStyle("fname", parent=small, fontName="DVB", alignment=TA_CENTER, textColor=ACCENT)
h1 = ParagraphStyle("h1", parent=body, fontName="DVB", fontSize=16, leading=20, textColor=ACCENT, spaceAfter=2)
sub = ParagraphStyle("sub", parent=body, textColor=MUTED, fontSize=9)
h2 = ParagraphStyle("h2", parent=body, fontName="DVB", fontSize=12, leading=16, textColor=ACCENT,
                    spaceBefore=10, spaceAfter=5)
note = ParagraphStyle("note", parent=body, backColor=colors.HexColor("#f3f0e6"),
                      borderColor=colors.HexColor("#c9b98a"), borderWidth=0.6, borderPadding=6,
                      spaceBefore=6, spaceAfter=10)


def P(text, style=body):
    return Paragraph(text, style)


def table(rows, widths, header=True):
    data = [[P(c, small) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8b8b8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e4e9f0")))
    t.setStyle(TableStyle(st))
    return t


def photo(path, title, desc, max_h=150 * mm):
    img = Image(str(HERE / "foto" / path))
    w = 170 * mm
    ratio = img.imageHeight / img.imageWidth
    h = w * ratio
    if h > max_h:
        h = max_h
        w = h / ratio
    img.drawWidth, img.drawHeight = w, h
    return KeepTogether([
        P(title, h2),
        img,
        Spacer(1, 2),
        P(f"Файл: {path}", fname),
        Spacer(1, 3),
        P(desc, body),
    ])


story = []

story += [
    P("Перегляд фільму «Посіч: депортована, але не знищена»", h1),
    P("Завдання 1 (Airtable): «Івашко: сім'я з Посіча і депортація 1950 року». "
      "Етап 1 — фільм, автори, контакти, документи в кадрі.", sub),
    Spacer(1, 8),
]

story += [
    P("1. Відомості про фільм", h2),
    table([
        ["Поле", "Дані"],
        ["Назва", "«Посіч: депортована, але не знищена»"],
        ["Посилання", "https://www.youtube.com/watch?v=1Bqt7R1jtI4"],
        ["Автор ідеї", "Софія Шепетуха"],
        ["Автори", "Софія Шепетуха, Андрій Яворський. Безпосередніх контактів авторів не знайдено."],
        ["Диктори", "Ольга Котюк, Андрій Таньків, Михайло Качанський"],
        ["Оператор", "Світлана Гаєвська"],
        ["Режисер", "Роман Турелик"],
        ["Підтримка", "Federal Foreign Office (Germany), Robert Bosch Stiftung, MitOst, «Інша Освіта»"],
        ["У рамках", "«Студія живої історії» (до неї належить Софія Шепетуха)"],
        ["Про показ", "https://report.if.ua/lyudy/u-frankivsku-pokazaly-film-pro-deportovane-selo-posich/"],
    ], [32 * mm, 138 * mm]),
]

story += [
    P("2. Контакти", h2),
    P("Контакти зібрано для подальшого зв'язку. За умовами завдання самостійно нікому не пишемо, "
      "листування лише після погодження.", small),
    table([
        ["Особа / організація", "Роль", "Контакти"],
        ["«Студія живої історії» / ГУРТ, «Інша Освіта»",
         "Організація, у рамках якої знято фільм",
         "Сайт: https://www.gurt.org.ua/<br/>E-mail: info@gurt.org.ua<br/>"
         "Facebook: https://www.facebook.com/gurt.org.ua<br/>Telegram: t.me/gurtrc<br/>"
         "Instagram: @gurtrc<br/>Співробітниця: oslavska@insha-osvita.org, тел. 066 77 341 61"],
        ["Тамара В'ячеславівна Галицька (нове прізвище Галицька-Дідух)",
         "Кандидатка історичних наук; викладає в Католицькому ліцеї святого Василія Великого "
         "та в Карпатському національному університеті ім. В. Стефаника",
         "tamara.halytska@cnu.edu.ua<br/>Деканат історичного ф-ту: dekanat_istor@cnu.edu.ua, "
         "+38 (0342) 59-61-07<br/>"
         "<b>Ліцей:</b> info@stbasilschool.org.ua, +380 (67) 377 45 68, +380 (342) 752 439, "
         "м. Івано-Франківськ, вул. Шевченка, 11<br/>"
         "<b>Університет:</b> https://cnu.edu.ua, office@cnu.edu.ua"],
        ["Назар Розлуцький",
         "Історик-дослідник; працює в Музеї української діаспори (Київ)",
         "Facebook (закритий профіль): https://www.facebook.com/nazar.rozlutskiy/<br/>"
         "Вікіпедія: https://uk.wikipedia.org/wiki/Назар_Розлуцький<br/>"
         "Музей: https://diaspora.com.ua/"],
    ], [42 * mm, 50 * mm, 78 * mm]),
]

story += [
    P("3. Таймкоди фільму", h2),
    table([
        ["Таймкод", "Зміст"],
        ["0:00 – 1:42", "Вступ"],
        ["1:42 – 2:35", "Структура УПА"],
        ["2:35 – 4:15", "Співпраця з УПА"],
        ["4:16 – 9:36", "Боротьба з радянською владою"],
        ["9:37 – 13:34", "Створення проєкту виселення"],
        ["13:35 – 15:47", "Процес виселення"],
        ["15:48 – 21:18", "Повернення"],
        ["21:18 – 22:31", "Кінець"],
    ], [35 * mm, 135 * mm]),
]

story += [
    P("4. Що знайдено про сім'ю Івашко", h2),
    table([
        ["Кадр / документ", "Запис", "Дані"],
        ["13:34 — друкований список голів сімей (с. Посіч)", "Івашко Федір Іванович", "1 член сім'ї"],
        ["13:34 — той самий список", "Івашко Іва Федорович", "2 члени сім'ї"],
        ["12:45 — третій список (відомість одноразової допомоги переселенцям Лисецького р-ну)",
         "№ 150 — Івашко Марія Василівна",
         "Переселенський квиток № 39932 (прочитання попереднє), 3 члени сім'ї, 1450 крб; "
         "у графі розписки — «за Дмитрів»"],
    ], [60 * mm, 50 * mm, 60 * mm]),
    P("Отже, на зображенні 13:34 є <b>дві сім'ї Івашко</b>: перша — Івашко Федір Іванович "
      "(1 член сім'ї), друга — Івашко Іва Федорович (2 члени сім'ї). На фото 12:45 у третьому списку "
      "під <b>№ 150</b> записана <b>Івашко Марія Василівна</b>.", note),
    P("У тому ж друкованому списку (13:34) видно ще два записи з прізвищем Івашко: "
      "Івашко Онуфрій Іванович і № 27 Івашко Василь Федорович. Кількість членів цих сімей у кадрі "
      "прочитати однозначно не вдається (цифри зміщені відносно рядків, нижні рядки закриває печатка), "
      "тому їх треба перевірити за оригіналом.", body),
]

story += [
    P("5. Де ще можуть бути імена", h2),
    P("• <b>«Реабілітовані історією. Івано-Франківська область»</b> — багатотомне видання "
      "з поіменними довідками про репресованих, зокрема виселених.", body),
    P("• <b>Група УПА «Говерля». Літопис УПА, том 18.</b> Торонто: Літопис УПА, 1990, с. 119 (PDF).", body),
]

story.append(PageBreak())
story.append(P("6. Документальні матеріали з фільму", h2))
story.append(P("Прочитання імен у рукописних документах попереднє й потребує звірки з оригіналом "
               "або зі сканом у кращій якості. Напис «Активация Windows» на кадрах з'явився під час "
               "запису екрана і до документів не належить.", small))

photos = [
    ("01_posich_oblik_zdachi_zernovyh_0-2ha.jpg",
     "Фото 1. Книга обліку обов'язкових поставок (зернові, картопля)",
     "Розграфлена книга обліку поставок господарств групи «0–2 га»: прізвище, ім'я, по батькові, "
     "площа, норма здачі, нараховано до здачі зернових (пшениця, інші продовольчі, зернові), "
     "картопля. Серед записів: Павлюк Микола Ст., Матієшин Йосип Вас., Лущак Емілія Вас., "
     "Долинський Михайло, Михайлів Юрко Ів., Лущак Анна Вас., Воронич Василь Дм., Анисюк Петро Ст., "
     "Дмитрів Олена Петр., Михайлів Йосип Ів. Прізвища Івашко в цьому кадрі немає."),
    ("02_lysec_spysok_pereselentsiv_dopomoga_ark1.jpg",
     "Фото 2. Список переселенців з Лисецького району на одержання одноразової допомоги (перший аркуш)",
     "Заголовок: «Список переселенців з Лисецького району, які переселяються за межі області, "
     "на одержання одноразової допомоги по пере[селенню]». Графи: прізвище, ім'я та по батькові; "
     "кількість членів сім'ї; № переселенського квитка; сума допомоги; розписка в одержанні. "
     "Серед записів: Фединко Іван, Мартинюк Степан, Мартинів Дмитро, Білоус Параска, Сікора Олекса, "
     "Олійник Олекса, Семанюк Олекса, Вацеба Дмитро, Вацеба Іван, Сікора Катерина, Ломей Олекса, "
     "Кузьмич Марія та ін. Квитки мають номери 158xx, окремі 239xx."),
    ("12-45_lysec_spysok_pereselentsiv_dopomoga_132-154_Ivashko_Mariya.jpg",
     "Фото 3 (кадр 12:45). Третій список — продовження відомості, № 132–154",
     "Записи № 132–154 з номерами переселенських квитків 399xx–402xx, кількістю членів сім'ї та "
     "сумою допомоги. <b>№ 150 — Івашко Марія Василівна</b> (квиток 39932, 3 члени сім'ї, 1450 крб). "
     "Також: Михайлів Іван Васильович, Човган Степан Михайлович, Ломей Микола Олексійович, "
     "Бойко Параска Василівна, Харчій Михайло Васильович, Бойко Онуфрій Федорович, Павлюк Петро "
     "Степанович, Яцків Михайло Антонович, Лущак Явдоха Семенівна, Шаламай Іван Федорович, "
     "Останів Марія Василівна, Семанюк Анна Іванівна, Сікора Василь Дмитрович. Підсумок: «Всього по "
     "відомості руб. 229 350»; підписи голови райвиконкому та бухгалтера."),
    ("13-34_drukovanyi_spysok_sim_Posich_Ivashko.jpg",
     "Фото 4 (кадр 13:34). Друкований список голів сімей із кількістю членів і селом",
     "Машинописний список: прізвище, ім'я та по батькові голови сім'ї; скільки членів сім'ї; село "
     "(Іваниківка, Чукалівка, <b>Посіч</b>). З Посіча: Олексин Федір Дмитрович, Івашко Онуфрій "
     "Іванович, Дякун Юрко Савович, <b>Івашко Федір Іванович (1 член сім'ї)</b>, Гаргат Василь "
     "Григорович, Бойко Явдоха Михайлівна, Гаргат Григорій Осипович, Деренько Семен Федорович, "
     "<b>Івашко Іва Федорович (2 члени сім'ї)</b>, Бойчук Афія Якимівна, Яцків Ксенія Іванівна, "
     "Нагорняк Микола Михайлович, Сулима Марія Семенівна, Дякун Іван Онуфрійович, Човган Анна "
     "Дмитрівна, Ломей Семен Іванович, № 27 Івашко Василь Федорович. Внизу — печатка."),
    ("05_eshelonnyi_spysok_semanyuk_harchii_shalamai_matiyeshyn.jpg",
     "Фото 5. Ешелонний список переселенців (друкований бланк)",
     "Бланк з графами: прізвище, ім'я, по батькові голови сім'ї та членів сім'ї; відношення до голови; "
     "рік народження; № переселенського квитка; місце виїзду (район, село, колгосп); місце "
     "вселення (область, район, колгосп); станція призначення; худоба та майно. Внизу: «Начальник "
     "ешелону», «Уповноважений облвиконкому по відправці переселенців». Видно сім'ї Семанюк, Нижник, "
     "Харчій (Марія, 1909, квиток 39939), Шаламай (Анна, 1922, квиток 39945), Матієшин (Михайло, "
     "1900, квиток 39934). Такий список дає склад сім'ї поіменно з роками народження — для Івашко "
     "потрібно знайти відповідний аркуш."),
]
for p in photos:
    story.append(photo(*p))
    story.append(Spacer(1, 10))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 10 * mm, "Посіч: депортована, але не знищена — доповідь за переглядом фільму")
    canvas.drawRightString(190 * mm, 10 * mm, f"с. {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(str(HERE / "Posich_film_dopovid.pdf"), pagesize=A4,
                        leftMargin=20 * mm, rightMargin=20 * mm, topMargin=16 * mm, bottomMargin=16 * mm,
                        title="Посіч: доповідь за переглядом фільму", author="Geneology")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("ok")
