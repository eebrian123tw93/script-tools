import os
import glob
import re
from shutil import copy
import yaml
from datetime import datetime, timedelta
import requests


class IndentDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


class Convert:
    def __init__(self, obsiden_path, hexo_path, note_name):
        self.obsiden_path = obsiden_path
        self.hexo_path = hexo_path
        self.note_name = note_name

    def find_path(self, target: str):
        all_files = glob.glob(f'{self.obsiden_path}/**', recursive=True)
        for file in all_files:
            full_name = os.path.basename(file)
            if target == full_name:
                return file
        return None

    def convert_image_format(self, match_obj):
        content = match_obj.group(1)
        image_path = self.find_path(target=content)
        image_name = os.path.basename(image_path)
        splitext_image_name = os.path.splitext(image_name)
        digit_str = ''.join(list(filter(lambda x: x.isdigit(), splitext_image_name[0])))

        new_name = f'{digit_str}{splitext_image_name[1]}'
        return f'![](/images/{new_name})'

    def convert_remote_image_format(self, match_obj):
        image_url = match_obj.group(1)

        image_name = os.path.basename(image_url)
        splitext_image_name = os.path.splitext(image_name)
        digit_str = ''.join(list(filter(lambda x: x.isdigit() or x.isalpha(), splitext_image_name[0])))

        new_name = f'{digit_str}{splitext_image_name[1]}'
        return f'![](/images/{new_name})'

    def convert_internal_link(self, match_obj):
        content = match_obj.group(1)
        result = '{%' + f' post_link  \"{content}\" ' + '%}'
        return result

    def format_time(self, input_date_string):
        # 將中文星期轉換為英文
        week_translation = {"星期一": "Monday", "星期二": "Tuesday", "星期三": "Wednesday", "星期四": "Thursday",
                            "星期五": "Friday", "星期六": "Saturday", "星期日": "Sunday"}
        for chinese_weekday, english_weekday in week_translation.items():
            input_date_string = input_date_string.replace(chinese_weekday, english_weekday)

        month_translation = {"一月": "January", "二月": "February", "三月": "March", "四月": "April", "五月": "May",
                             "六月": "June", "七月": "July", "八月": "August", "九月": "September", "十月": "October",
                             "十一月": "November", "十二月": "December"}
        for chinese_month, english_month in reversed(month_translation.items()):
            input_date_string = input_date_string.replace(chinese_month, english_month)

        # 解析日期時間字符串
        date_format = "%A %d日 %B %Y %H:%M"
        parsed_date = datetime.strptime(input_date_string, date_format)

        # 添加差異的時間（以分鐘為單位）
        parsed_date_with_difference = parsed_date + timedelta(minutes=70)

        # 將日期時間對象轉換為所需的日期時間字符串格式
        output_date_string = parsed_date_with_difference.strftime("%Y-%m-%d %H:%M:%S")
        return output_date_string

    def split_meta_and_content(self, content):
        parts = content.split('---', 2)
        if len(parts) == 3:
            metadata = yaml.safe_load(parts[1])
            markdown_content = parts[2]
        else:
            metadata = {}
            markdown_content = parts[0]
        return metadata, markdown_content

    def handle_meta(self,  metadata, old_metadata):

        if 'categories' in metadata.keys() and not isinstance(metadata['categories'], list):
            del metadata['categories']

        old_metadata.update(metadata)
        metadata = old_metadata
        created = metadata['created']
        unused_metas = ['aliases', 'Last modified', 'created']
        for unused_meta in unused_metas:
            if unused_meta in metadata:
                del metadata[unused_meta]

        metadata['date'] = self.format_time(input_date_string=created)
        metadata['updated'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if 'categories' not in metadata.keys():
            metadata['categories'] = []
        metadata['description'] = ""

        metadata_str = yaml.dump(metadata, Dumper=IndentDumper, default_style=None, default_flow_style=False,
                                 sort_keys=False,
                                 allow_unicode=True, indent=2, )
        return metadata_str
    

    def metadata_change(self, metadata, old_metadata):
        tags = [] if 'tags' not in metadata.keys() or not isinstance(metadata['tags'], list) else metadata['tags']
        old_tags = [] if 'tags' not in old_metadata.keys() or not isinstance(old_metadata['tags'], list) else old_metadata['tags']
        tags.sort()
        old_tags.sort()
        return tags != old_tags

    def start(self):
        note_path = f"{self.hexo_path}/_posts/{self.note_name}.md"
        note_name_path = self.find_path(target=f'{self.note_name}.md')

        if not os.path.exists('images'):
            os.mkdir('images')

        if note_name_path is None:
            exit(0)

        f = open(note_name_path, 'r')
        content = f.read()
        f.close()

        internal_link_pattern = r'\[\[(.*)\]\]'
        obsiden_image_pattern = r'!\[\[([^|\]]+)(?:\|\d+)?\]\]'
        remote_image_pattern = r'\!\[.*\]\((https://.*?)\)'
        results = re.findall(obsiden_image_pattern, content)
        for result in results:
            image_path = self.find_path(target=result)
            image_name = os.path.basename(image_path)
            splitext_image_name = os.path.splitext(image_name)
            digit_str = ''.join(list(filter(lambda x: x.isdigit(), splitext_image_name[0])))
            new_name = f'{digit_str}{splitext_image_name[1]}'
            copy(src=image_path, dst=f'{self.hexo_path}/images/{new_name}')

        matches = re.findall(remote_image_pattern, content)
        for match in matches:
            image_name = os.path.basename(match)
            splitext_image_name = os.path.splitext(image_name)
            digit_str = ''.join(list(filter(lambda x: x.isdigit() or x.isalpha(), splitext_image_name[0])))
            new_name = f'{digit_str}{splitext_image_name[1]}'
            image_path = f'{self.hexo_path}/images/{new_name}'
            if not os.path.exists(image_path):
                img_data = requests.get(match).content

                with open(image_path, 'wb') as handler:
                    handler.write(img_data)

        old_metadata = {}
        old_markdown_content = ''
        note_path_exist = os.path.exists(note_path)
        if note_path_exist:
            with open(note_path, 'r') as f:
                old_markdown = f.read()
                old_metadata, old_markdown_content = self.split_meta_and_content(content=old_markdown)

        new_content = re.sub(obsiden_image_pattern, self.convert_image_format, content)
        new_content = re.sub(remote_image_pattern, self.convert_remote_image_format, new_content)

        new_content = re.sub(internal_link_pattern, self.convert_internal_link, new_content)

        metadata, markdown_content = self.split_meta_and_content(content=new_content)

        pattern = re.compile(r'---sensitive---.*?---end_sensitive---', re.DOTALL)

        markdown_content = re.sub(pattern, '', markdown_content)

        if len(markdown_content) > 200 :
            new_line_index = markdown_content.find("\n", 200, len(markdown_content) -1)
            if new_line_index >= 0:
                more_index = new_line_index + 1
                markdown_content = f"{markdown_content[:more_index]} <!-- more -->\n {markdown_content[more_index:]}"

        difference = ""
        for char1, char2 in zip(old_markdown_content, markdown_content):
            if char1 != char2:
                difference += char1

        if len(difference) != 0:
            print("差異的部分:", difference)
        metadata_change = self.metadata_change(metadata=metadata , old_metadata=old_metadata)
        if old_markdown_content != markdown_content or metadata_change:

            metadata_str = self.handle_meta(metadata=metadata, old_metadata=old_metadata)
            new_content = f'---\n{metadata_str}---{markdown_content}'

            
            fo = open(note_path, "w")
            fo.write(new_content)
            fo.close()



