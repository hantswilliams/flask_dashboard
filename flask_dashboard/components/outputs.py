# components/outputs.py

from flask import render_template_string, send_file
import io
import base64


class OutputText:
    def __init__(self, content):
        self.content = content

    def render(self):
        template = '''
        <div class="p-4 border rounded">
            {{ content }}
        </div>
        '''
        return render_template_string(template, content=self.content)



class OutputChart_Matplotlib:
    def __init__(self, plt_object):
        self.plt_object = plt_object

    def render(self):
        # Create a bytes buffer for the image to save to
        buf = io.BytesIO()

        # Use the provided plt object to save the figure to the buffer
        self.plt_object.savefig(buf, format="png", bbox_inches='tight')
        buf.seek(0)

        # Convert bytes to a data URL (base64 encoding)
        data_url = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode('utf8')

        buf.close()
        
        template = '''
        <div>
            <img class="max-w-full" src="{{ image }}">
        </div>
        '''

        return render_template_string(template, image=data_url)


class OutputTable_HTML:
    def __init__(self, data):
        self.data = data  # Assuming data is a list of dictionaries

    def render(self):
        template = '''
        <table class="min-w-full bg-white border rounded">
            <thead>
                <tr>
                {% for header in data[0].keys() %}
                    <th class="px-4 py-2">{{ header }}</th>
                {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for row in data %}
                    <tr>
                        {% for value in row.values() %}
                            <td class="border px-4 py-2">{{ value }}</td>
                        {% endfor %}
                    </tr>
                {% endfor %}
            </tbody>
        </table>
        '''
        return render_template_string(template, data=self.data)

class OutputImage:
    def __init__(self, src, alt=""):
        self.src = src
        self.alt = alt

    def render(self):
        template = '''
        <div>
            <img class="w-64 h-auto" src="{{ src }}" alt="{{ alt }}">
        </div>
        '''
        return render_template_string(template, src=self.src, alt=self.alt)

