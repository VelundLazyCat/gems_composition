import streamlit as st
# from data_sets import SETS
from gem_sets import gemstone_dict, gem_form, gem_colors, gem_material, gem_cuttin
from data_sets import SETS_DICT
from get_quont_gems import Gemstone


def get_gems_from_item(item):
    """ делает список камней для данного артикула """
    if gemstone_dict.get(item, None):
        gems = [Gemstone(i) for i in gemstone_dict[item].split(",")]
    else:
        return None
    return gems


def get_quontity_gem_items(item_name: str, item_quontity: int) -> list:
    """ Основная функция получения камней из артикула.
    Выдает список камней умноженный на количество изделий одного артикула"""

    gems = get_gems_from_item(item_name)
    if gems:
        gems = [g * item_quontity for g in gems]
    else:
        raise ValueError(f"Item {item_name} not found in DataBase")
    return gems


def get_quontity_set_items(items_set, quontity):
    try:
        items_set = items_set.split(',')
        set_parts = [i.split('_') for i in items_set]
        for i in set_parts:
            i[1] = int(i[1]) * quontity
    except:
        set_parts = []
    return set_parts


def get_gem_composition(articul, quontity):

    gems = get_quontity_gem_items(articul, quontity)
    return gems


def get_set_composition(articul, quontity):
    item_composition = SETS_DICT.get(articul, None)
    if not item_composition:
        raise ValueError(f"Item {articul} not found in DataBase")
    item_composition = get_quontity_set_items(item_composition, quontity)
    return item_composition


def get_text_about_item(item):
    return f"~ {item[0]}: {item[1]} шт"


def get_text_about_gem(gem: Gemstone):
    """Выдает текстовое описание камня для заказа на магазинах """
    obrazec = "~ кабошен квадрат стекло 3х3мм зеленый 10 шт"
    cuttin = gem_cuttin[gem.cutting]
    material = gem_material[gem.material]
    form = gem_form[gem.form]
    size = gem.size.replace('.', ',')
    color = gem_colors[gem.color]
    return f"~ {cuttin} {form} {material} {size}мм {color} {gem.quontity} шт"


predicts = {0: get_gem_composition, 1: get_set_composition}

# Заголовок сторінки
st.title(":blue[Gems and Itemsets Application]")
st.subheader("Enter articul and quontity to determine the composition")

select = st.selectbox('Type of definition', options=[0, 1],
                      format_func=lambda x: "Set compsition" if x == 1 else "Gems composition")
col1, col2 = st.columns(2)

with col1:
    input_articul = st.text_input("Enter articul", value='')

with col2:
    try:
        input_quontity = st.number_input(
            "Enter quontity", value=1, min_value=1, max_value=1000)
    except:
        pass

if st.button(label='Do It ', help='Прожмакай кнопку щоб отримати результат!'):
    try:
        result = predicts[select](input_articul, input_quontity)
        for i in result:
            if not result:
                st.subheader(get_text_about_gem(i))
            else:
                st.subheader(get_text_about_item(i))
    except ValueError as e:
        st.error(str(e))
