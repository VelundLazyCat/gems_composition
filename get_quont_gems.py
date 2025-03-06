from gem_sets import gemstone_dict, gem_colors, gem_form
from math import ceil, floor


GEM_TYPE_CODE = "<quontity>_<gem_form>_<gem_material>_<size>_<gem_cuttin>_<gem_colors>"


class Gemstone:
    gem_cuttin = {"cab": "1", "cut": "2",
                  "bead": "3", "glass": "1",
                  "cz": "2",   "ngem": "3ь",
                  "pearl": "4", "coral": "5",
                  "garnet": "5", "kva": "a",
                  "baguet": "b", "octa": "c",
                  "round": "d", "oval": "e",
                  "pear": "f", "trill": "g",
                  "trial": "h", "heart": "i",
                  "cust": "j", "potat": "k",
                  "half": "l", "spher": "m",
                  "drop": "n", "cube": "o"
                  }

    gem_colors = {"white": "a", "red": "b",
                  "garnet": "c", "ruby": "d",
                  "lightblue": "e",
                  "blue": "f", "green": "g",
                  "lightgreen": "h",
                  "purple": "i", "yellow": "j",
                  "black": "k", "quartz": "l",
                  }

    def __init__(self, legend=None):
        self.quontity = 1
        self.form = "round"
        self.material = "glass"
        self.size = "5x5"
        self.cutting = "cab"
        self.color = "red"
        if legend:
            self.legend = legend.split('_')
            self.set_gem_quontity()
            self.set_gem_form()
            self.set_gem_material()
            self.set_gem_size()
            self.set_gem_cutting()
            self.set_gem_color()
        self.hash = self.gem_hash()

    def set_gem_quontity(self, quontity=1):
        try:
            self.quontity = int(self.legend[0]) * quontity
        except:
            self.quontity = 0

    def set_gem_form(self):
        try:
            self.form = self.legend[1]
        except:
            print("Uknown Gemform!")

    def set_gem_material(self):
        try:
            self.material = self.legend[2]
        except:
            print("Uknown Material!")

    def set_gem_size(self):
        try:
            self.size = self.legend[3]
        except:
            print("Size not exists!")

    def set_gem_cutting(self):
        try:
            self.cutting = self.legend[4]
        except:
            print("Unknown cutting!")

    def set_gem_color(self):
        try:
            self.color = self.legend[5]
        except:
            print("Unknown color!")

    def update_gem_color(self, color=None):
        if color:
            self.color = color
            self.hash = self.gem_hash()

    def gem_hash(self):
        try:
            size = float(self.size.split("x")[0]) * \
                10 + float(self.size.split("x")[0])*10
            size = round(size)
        except:
            size = 0
        size = "{:03d}".format(size)
        a = f"{self.gem_cuttin[self.cutting]}{self.gem_cuttin[self.form]}{
            size}{self.gem_colors[self.color]}{self.gem_cuttin[self.material]}"
        return a

    def __lt__(self, b):
        try:
            return self.hash < b.hash
        except:
            return "This gems not summatted"

    def __eq__(self, b):
        try:
            return self.hash == b.hash
        except:
            return "This gems not summatted"

    def __add__(self, b):
        try:
            if self.hash == b.hash:
                self.quontity += b.quontity
        except:
            return "This gems not summatted"
        return self

    def __sub__(self, b):
        try:
            if self.hash == b.hash:
                self.quontity -= b.quontity
        except:
            return "This gems not summatted"
        return self

    def __mul__(self, a):
        self.quontity *= a
        return self

    def __str__(self):
        return f"{self.size} {self.material} {self.form}-{self.cutting} {self.color}: {self.quontity}"


def parse_articul_color(art: str):
    art_parts = art.split('_')
    for part in art_parts[1:]:
        if part in gem_colors:
            return art_parts[0], part
    return art_parts[0], None


def parse_10mounts_set(data):
    """ # articul bag-fix
    Находит сеты по 10 шт и переводит их в поштучно """
    text_search = "10-mounts"
    pos = data[0].find(text_search)
    if pos > 0:
        data[1] = data[1] * 10
        data[0] = data[0][:pos - 1] + data[0][pos + len(text_search):]
    return data


def parse_er24_gem_size(art: str):
    art_parts = art.split('_')
    for part in art_parts[1:]:
        if part.startswith('15') or part.startswith('16') or part.startswith('17'):
            art_parts[0] = 'er24-small'
            break
    return '_'.join(art_parts)


def get_gems_from_item(item):
    """ делает список камней для данного артикула """
    item_name, color = item
    gems = [Gemstone(i) for i in gemstone_dict[item_name].split(",")]
    if color:
        for gem in gems:
            if gem.cutting in ['cab', 'cut']:
                gem.update_gem_color(color)
    return gems


def get_gem_code(gem):
    """ дает код камня по шаблону для записи в БД """
    return f"{gem.quontity}_{gem.form}_{gem.material}_{
        gem.size}_{gem.cutting}_{gem.color}"


def get_gem_items(data):
    """разделяет список арртикулов на 3 части
    1: все что с камнями
    2: сеты с большими буквами
    3: все остальное"""
    result_gems = []
    result_sets = []
    result_other = []
    for d in data:
        name = d[0].split('_')[0]
        if name in gemstone_dict:
            result_gems.append(d)
        elif name.isupper():
            result_sets.append(d)
        else:
            result_other.append(d)
    return result_gems, result_sets, result_other


def razdelenie_smeshannih_articulov(items: list) -> list:
    """разделяет артикулы со смешанными камнями на красный и синий"""
    result = []
    for i in items:
        if i[0] in ['ez35-flower', 'ez-ferr', 'ez-eleon-collar', 'ez-eleon-belt']:
            result.append([i[0], ceil(i[1]/2)])
            result.append([i[0]+'-b', floor(i[1]/2)])
        else:
            result.append(i)
    return result


def get_quontity_gem_items(item: list):
    """ Основная функция получения камней из артикула.
    Выдает список камней умноженный на количество изделий одного
    артикула, получает данные в формате ['Артикул', количество]"""
    item = parse_10mounts_set(item)

    item_name = item[0]
    if item_name.startswith('er24'):
        item_name = parse_er24_gem_size(item_name)
    item_name = parse_articul_color(item_name)
    item_quontity = item[1]
    print(item)
    gems = get_gems_from_item(item_name)
    gems = [g * item_quontity for g in gems]
    return gems


def sort_gems_func(sort_data):
    """Фукция сортировки камней и сложения дублей"""
    temp_data = []
    temp_data_temp = []
    sort_data.sort()

    while len(sort_data) > 0:
        if len(sort_data) == 1:
            temp_data.append(sort_data[0])
            sort_data.pop()
            break

        if sort_data[-2] == sort_data[-1]:
            temp_data_temp = sort_data[-2] + sort_data[-1]
            sort_data.pop()
            sort_data[-1] = temp_data_temp
        else:
            temp_data.append(sort_data[-1])
            sort_data.pop()
    temp_data.sort()
    return temp_data


def sort_gems_form(gem_list: list[Gemstone]):
    """ разделяет общий список на 3 категории, кабошены, граненые камни, жемчуга """
    cab_gems = []
    cut_gems = []
    bead_gems = []
    for gem in gem_list:
        if gem.cutting == 'cab':
            cab_gems.append(gem)
        elif gem.cutting == 'cut':
            cut_gems.append(gem)
        else:
            bead_gems.append(gem)
    return cab_gems, cut_gems, bead_gems


def get_text_about_gem(gem: Gemstone):
    """Выдает текстовое описание камня для заказа на магазинах """
    obrazec = "-квадрат 3х3мм зеленый 10 шт"
    form = gem_form[gem.form]
    size = gem.size.replace('.', ',')
    color = gem_colors[gem.color]
    return f"~{form} {size}мм {color} {gem.quontity} шт"


if __name__ == "__main__":
    print("-----------")
    brooches = [['ea57', 3], ['ea49', 2], ['ea51', 1],
                ['er29', 3], ['ea43', 1], ['er24_17,5_green_g', 2], ["ez-ferr", 1], ['er24_19,5_blue_g', 4]]
    # stones = get_quontity_gem_items(["ea57", 3])
    stones = []
    for i in brooches:
        stones += get_quontity_gem_items(i)
    # stones = sort_gems_func(stones)
    # print(stones)
    for st in stones:
        # print(st)
        # st += st
        # print(st)
        # a = get_gem_code(st)
        # print(a)
        print(get_text_about_gem(st))
        print(st.hash)
        # print("-----------")
    # rrrr = [['ez35-flower', 8], ['ez-ferr', 8],
        # ['ez-eleon-collar', 12], ['ez-eleon-belt', 15]]
    # gems_list = razdelenie_smeshannih_articulov(rrrr)
    # print(gems_list)
    print("-----------")
    er24_small = 'er24_17,5_green_g'
    er24_big = 'er24_green_18,5_g'
    print(parse_er24_gem_size(er24_small))
    print(parse_er24_gem_size(er24_big))
