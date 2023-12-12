import pandas as pd

from PIL import Image
import psycopg2
from config.config import settings
import warnings
from utils import *

warnings.filterwarnings('ignore')


@st.cache_data
def preload_content():
    conn = psycopg2.connect(dbname=settings.db_name, host=settings.db_host, port=settings.db_port,
                            user=settings.db_user, password=settings.db_password)
    banner = Image.open('assets/Bank-Advertising.jpeg')
    df = pd.read_sql_query("SELECT * FROM bank_data;", conn)
    return df, banner


def render_page(df, banner):
    st.title('Повышение эффективности взаимодействия банка с клиентом')
    st.subheader('Исследуем склонность клиента к положительному или отрицательному отклику на предложение банка')
    st.write('Материал - данные банка о клиентах')
    st.image(banner)

    tab1, tab2 = st.tabs([':mag: Исследовать', ':vertical_traffic_light: Значения'])

    with tab1:
        st.write('Exploratory data analysis: исследуем наши данные, предварительно очищенные и обработанные :sparkles:')

        with st.expander("Корреляция признаков"):
            st.write('**Исследуем корреляцию признаков**')
            show_heatmap(df)
            st.write("""Хорошей корреляции признаков с целевой переменной не наблюдаем. 
                     Только очевидные корреляции между некоторыми естественным образом связанными признаками. """)

        with st.expander('Гистограммы признаков'):
            st.write('*Для лучшего понимания датасета, построим гистограммы некоторых признаков.*')
            show_hist(df)

        with st.expander('Числовые характеристики'):
            st.write('**Посмотрим на связь числовых характеристик числовых признаков с целевой переменной**')
            show_avg_min_max(df)
            st.write(
                '*Видим что на предложения от банка откликаются клиенты в среднем более младшего возраста и с меньшим количеством кредитов*')

        with st.expander('Еще'):
            st.write('*В выборке мужчин больше чем женщин, отдают кредиты они примерно одинаково*')
            show_bar_plots(df)
            st.write(
                '*Видим что люди младше по возрасту и с меньшим количеством кредитов более отзывчивы к предложениям банка*')
            show_scatter_3d(df)

    with tab2:
        html_string = """
        <div>
            - AGREEMENT_RK — уникальный идентификатор объекта в выборке; <br>
            - TARGET — целевая переменная: отклик на маркетинговую кампанию (1 — отклик был зарегистрирован, 0 — отклика не было); <br>
            - AGE — возраст клиента; <br>
            - SOCSTATUS_WORK_FL — социальный статус клиента относительно работы (1 — работает, 0 — не работает); <br>
            - SOCSTATUS_PENS_FL — социальный статус клиента относительно пенсии (1 — пенсионер, 0 — не пенсионер); <br>
            - GENDER — пол клиента (1 — мужчина, 0 — женщина); <br>
            - CHILD_TOTAL — количество детей клиента; <br>
            - DEPENDANTS — количество иждивенцев клиента; <br>
            - PERSONAL_INCOME — личный доход клиента (в рублях); <br>
            - LOAN_NUM_TOTAL — количество ссуд клиента; <br>
            - LOAN_NUM_CLOSED — количество погашенных ссуд клиента. <br>
        </div>"""

        st.markdown(html_string, unsafe_allow_html=True)


def load_page():
    df, banner = preload_content()
    render_page(df, banner)


if __name__ == "__main__":
    load_page()
