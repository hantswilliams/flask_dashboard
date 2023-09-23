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
        <div class="p-2 sm:p-3 md:p-4 border rounded bg-white text-base sm:text-md md:text-md">
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
        <div class="flex justify-center items-center">
            <img class="max-w-full h-auto" src="{{ image }}">
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
                        <table class="min-w-full divide-y divide-gray-200 border-collapse">
                            <thead>
                                <tr>
                                {% for header in data[0].keys() %}
                                    <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ header }}</th>
                                {% endfor %}
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                {% for row in data %}
                                    <tr class="{% if loop.index is odd %}bg-gray-50{% endif %} hover:bg-gray-100">
                                        {% for value in row.values() %}
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ value }}</td>
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
            <div class="markdown-body text-base sm:text-lg md:text-xl px-4 sm:px-6 md:px-8">
                {{ content|safe }}
            </div>
        '''
        
        return render_template_string(template, content=html_content)