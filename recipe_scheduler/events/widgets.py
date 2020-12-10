from wtforms.widgets.core import html_params, Markup, escape, text_type
from recipe_scheduler.models import Recipe


class MySelect(object):
    def __init__(self, multiple=False):
        self.multiple = multiple

    def __call__(self, field, select_recipe=None, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        if 'required' not in kwargs and 'required' in getattr(field, 'flags', []):
            kwargs['required'] = True
        html = ['<select %s>' % html_params(name=field.name, **kwargs)]
        # Initial label
        # html.append(self.render_option(value='', label='Select', selected=True, disabled=True, data_category="0"))

        for val, label, selected in field.iter_choices():
            recipe = Recipe.query.filter_by(id=val).first()
            # added custom data attribute to <option></option>
            if not recipe:
                # Initial label
                html.append(self.render_option(
                    0,
                    label='---',
                    selected=False,
                    disabled=True,
                    data_category=0))
            else:
                if val == select_recipe:
                    html.append(self.render_option(
                        val,
                        label,
                        selected=True,
                        disabled=False,
                        data_category=recipe.category_id))
                else:
                    html.append(self.render_option(
                        val,
                        label,
                        selected=False,
                        disabled=False,
                        data_category=recipe.category_id))
        html.append('</select>')
        return Markup(''.join(html))

    @classmethod
    def render_option(cls, value, label, selected, disabled, **kwargs):
        if value is True:
            # Handle the special case of a 'True' value.
            value = text_type(value)
        options = dict(kwargs, value=value)
        if selected:
            options['selected'] = True

        # if disabled:
        #     options['hidden'] = True

        return Markup('<option %s>%s</option>' % (
            html_params(**options), escape(label)))
