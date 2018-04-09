def menu(parent_id=0, menutree=None):
    menutree = menutree or []
    cur = g.db.execute('select id, parent, alias, title, ord from static where parent="'+ str(parent_id) +'" and ord>0 order by ord')
    fetch = cur.fetchall()

    if not fetch:
        return None

    return [{'id':raw[0], 'parent':raw[1], 'alias':raw[2], 'title':raw[3], 'sub':menu(raw[0])} for raw in fetch]

create table static (
  id integer primary key autoincrement,
  parent integer,
  alias string not null,
  title string not null,
  text string not null,
  ord integer
);

@app.route('/')
def index():
    menu_list = menu()
    [...]
    return render_template('index.tpl', **locals())


<nav role="navigation">
  {% for menu in menu_list %}
  <li>
    <a{% if page_id == menu.id %} class="active"{% endif %} href="/{{ menu.alias }}">{{ menu.title }}</a>
    {% if menu.sub %}
    <ul>
      {% for sub in menu.sub %}
      <li><a href="/{{ menu.alias }}/{{ sub.alias }}">{{ sub.title }}</a>
        {% if sub.sub %}
        <ul>
          {% for subsub in sub.sub %}
          <li><a href="/{{ menu.alias }}/{{ sub.alias }}/{{ subsub.alias }}">{{ subsub.title }}</a>
          {% endfor %}
        </ul>
        {% endif %}
      </li>
      {% endfor %}
    </ul>
    {% endif %}
  </li>
  {% endfor %}
</nav>



{% block navbar %}
<ul>
    {% for item in nav.top %}
    <li class="{{ 'active' if item.is_active else '' }}">
        {{ item }}
        {% if item.items %}
        <ul>
            {% for child in item.items %}
            <li class="{{ 'active' if child.is_active else '' }}">
            {{ child }}
            </li>
            {% endfor %}
        </ul>
        {% endif %}
    </li>
    {% endfor %}
</ul>
{% endblock %}

nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('Latest News', 'news', {'page': 1}),
    nav.Item('Nestable', 'nestable', items=[
        nav.Item('Nested 1', 'nested-1'),
        nav.Item('Nested 2', 'nested-2'),
    ]),
])


# taken from https://github.com/tonyseek/flask-navigation
# Copyright (c) 2014 Jiangge Zhang
# MIT License
import collections

class Item(object):
    """The navigation item object.
    :param label: the display label of this navigation item.
    :param endpoint: the unique name of this navigation item.
    """
    def __init__(self, label, endpoint, args=None, url=None, html_attrs=None, items=None):
        self.label = label
        self.endpoint = endpoint
        self._args = args
        self._url = url
        self.html_attrs = {} if html_attrs is None else html_attrs
        self.items = ItemCollection(items or None)

    @property
    def args(self):
        """The arguments which will be passed to ``url_for``.
        :type: :class:`dict`
        """
        if self._args is None:
            return {}
        if callable(self._args):
            return dict(self._args())
        return dict(self._args)

    @property
    def ident(self):
        """The identity of this item.
        :type: :class:`~flask.ext.navigation.Navigation.ItemReference`
        """
        return ItemReference(self.endpoint, self.args)


class ItemCollection(collections.MutableSequence, collections.Iterable):
    """The collection of navigation items.
    """
    def __init__(self, iterable=None):
        #: the item collection
        self._items = []
        #: the mapping collection of endpoint -> item
        self._items_mapping = {}
        #: initial extending
        self.extend(iterable or [])

    def __repr__(self):
        return 'ItemCollection(%r)' % self._items

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._items[index]

        if isinstance(index, tuple):
            endpoint, args = index
        else:
            endpoint, args = index, {}
        ident = ItemReference(endpoint, args)
        return self._items_mapping[ident]

    def __setitem__(self, index, item):
        # remove the old reference
        old_item = self._items[index]
        del self._items_mapping[old_item.ident]

        self._items[index] = item
        self._items_mapping[item.ident] = item

    def __delitem__(self, index):
        item = self[index]
        del self._items[index]
        del self._items_mapping[item.ident]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def insert(self, index, item):
        self._items.insert(index, item)
        self._items_mapping[item.ident] = item

class ItemReference(collections.namedtuple('ItemReference', 'endpoint args')):
    """The identity tuple of navigation item.
    :param endpoint: the endpoint of view function.
    :type endpoint: ``str``
    :param args: the arguments of view function.
    :type args: ``dict``
    """
    def __new__(cls, endpoint, args=()):
        if isinstance(args, dict):
            args = freeze_dict(args)
        return super(cls, ItemReference).__new__(cls, endpoint, args)