# components/outputs.py

from flask import render_template_string
import io
import base64
from markdown import markdown

class OutputText:
    def __init__(self, content):
        self.content = content

    def render(self):
        template = '''
        <div class="p-2 border rounded bg-white">
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
            <div class="mt-8 flow-root bg-white">
                <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                    <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
                    <table class="min-w-full divide-y divide-gray-300">
                        <thead>
                            <tr>
                            {% for header in data[0].keys() %}
                                <th class="px-3 py-3.5 text-left text-sm font-semibold text-grey-900">{{ header }}</th>
                            {% endfor %}
                            </tr>
                        </thead>
                        <tbody>
                            {% for row in data %}
                                <tr>
                                    {% for value in row.values() %}
                                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-900">{{ value }}</td>
                                    {% endfor %}
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    </div>
                </div>
                </div>
            </div>
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


class OutputMarkdown:
    def __init__(self, markdown_content):
        self.markdown_content = markdown_content

    def render(self):
        html_content = markdown(self.markdown_content)

        print('Checking for conversion: ', html_content)
        
        template = '''
        <div class="markdown-body">
            {{ content|safe }}
        </div>
        '''
        
        return render_template_string(template, content=html_content)