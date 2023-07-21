import re
import os
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor

def Banner():
    banner = """                                           
	   _      __ _           _          ______          
	  (_)    / _(_)         | |         | ___ \         
	   _ ___| |_ _ _ __   __| | ___ _ __| |_/ / __ ___  
	  | / __|  _| | '_ \ / _` |/ _ \ '__|  __/ '__/ _ \ 
	  | \__ \ | | | | | | (_| |  __/ |  | |  | | | (_) |
	  | |___/_| |_|_| |_|\__,_|\___|_|  \_|  |_|  \___/ 
	 _/ |                                               
	|__/       
                                         
    Usage:python3 jsfinderPro.py -u https://xxx.com/js/app.beeb81af.js -g regex_file\convention.txt
    Usage:python3 jsfinderPro.py -l 测试.js -g regex_file\convention.txt 
    Usage:python3 jsfinderPro.py -l 测试的文件夹 -g regex_file\convention.txt -t 5
    Usage:使用前请提前清空result文件夹，信息提取的结果会保存到result文件中
        """
    print(banner)

def find_matches(content, regex_patterns):
    matches = {}
    for pattern_name, pattern in regex_patterns.items():
        pattern_matches = re.findall(pattern, content)
        if pattern_matches:
            matches[pattern_name] = list(set(pattern_matches))
    print('提示:信息提取中，请稍后........................')
    return matches

def process_file(file_path, regex_patterns):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    return find_matches(content, regex_patterns)

def process_file_with_threading(file_path, regex_patterns):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return file_path, find_matches(content, regex_patterns)

def process_files_in_directory(directory_path, regex_patterns):
    matches = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.js'):
                file_path = os.path.join(root, file)
                file_matches = process_file(file_path, regex_patterns)
                for pattern_name, pattern_matches in file_matches.items():
                    if pattern_name not in matches:
                        matches[pattern_name] = []
                    matches[pattern_name].extend(pattern_matches)
    print('提示:信息提取中，请稍后........................')
    return matches

def process_files_in_directory_with_threading(directory_path, regex_patterns, args):
    matches = {}
    file_paths = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.js'):
                file_path = os.path.join(root, file)
                file_paths.append(file_path)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        for file_path in file_paths:
            future = executor.submit(process_file_with_threading, file_path, regex_patterns)
            futures.append(future)

        for future in futures:
            file_path, file_matches = future.result()
            for pattern_name, pattern_matches in file_matches.items():
                if pattern_name not in matches:
                    matches[pattern_name] = []
                matches[pattern_name].extend(pattern_matches)
    print('提示:信息提取中，请稍后........................')
    return matches

def save_results(matches, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for pattern_name, pattern_matches in matches.items():
        output_file_path = os.path.join(output_directory, f'{pattern_name}.txt')
        pattern_matches = [str(match) for match in pattern_matches]
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(pattern_matches))
            output_file.write('\n')
    print('提示:js信息已提取完毕，结果已保存到result文件夹中')

def process_regex_file(regex_file_path):
    regex_patterns = {}
    with open(regex_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                pattern_name, pattern = line.split(':', 1)
                regex_patterns[pattern_name.strip()] = pattern.strip()
    return regex_patterns

def main():
    parser = argparse.ArgumentParser(description='JS文件信息收集 By 冰糖葫芦')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', help='在线JS文件的URL或文件路径')
    group.add_argument('-l', '--local', help='本地JS文件或目录的路径')
    parser.add_argument('-g', '--regex_file', help='包含正则表达式模式的文件路径')
    parser.add_argument('-t', '--threads', type=int, default=1, help='指定线程数量')
    args = parser.parse_args()

    if args.regex_file:
        regex_patterns = process_regex_file(args.regex_file)
    else:
        regex_patterns = {}

    if args.url:
        url_or_path = args.url

        if url_or_path.startswith('http://') or url_or_path.startswith('https://'):
            # Online URL
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
                'Content-Type': 'application/json'
            }

            response = requests.get(url_or_path, headers=headers)
            content = response.text
            matches = find_matches(content, regex_patterns)
        output_directory = 'result'
        save_results(matches, output_directory)

    elif args.local:
        local_path = args.local

        if os.path.isfile(local_path):
            # Local JS file
            matches = process_file(local_path, regex_patterns)
        elif os.path.isdir(local_path):
            # Local directory
            if args.threads > 1:
                matches = process_files_in_directory_with_threading(local_path, regex_patterns, args)
            else:
                matches = process_files_in_directory(local_path, regex_patterns)

        output_directory = 'result'
        save_results(matches, output_directory)

if __name__ == '__main__':
    Banner()
    main()